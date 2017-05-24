# -*- coding: utf-8 -*-

import json
import random
import logging
import websockets

from game.bear import Bear
from game.player import Player

import server_tools
from game import fields
from game import levels


class Game:
    """ Класс, реализующий логику игры """

    def __init__(self, players_names):
        self.fields = fields.FieldGroup()
        self.level = levels.get_random_level()
        self.players = [Player(self, name, players_names[name][0]) for name in players_names]
        self.active_player = self.players[0]
        self.bear = Bear(self)
        self.winner = None
        self.ended = False

    @property
    def num_players(self):
        return len(self.players)

    async def inform_whose_turn(self):
        """ корутина, рассылающая имя игрока, который сейчас ходит"""
        for player in self.players:
            response = json.dumps({"type": "whose_turn", "name": self.active_player.name})

            logging.info("Уведомляем игрока {}, о том, что ходит игрок {}".format(
                player.name,
                self.active_player.name
            ))

            await player.websocket.send(response)
            # ждать, чтобы клиент успел отрисовать
            message = await player.websocket.recv()
            logging.info("Игрок {} прислал {}".format(player.name, message))

    def accept(self, player, turn):
        """ 
        Функция, которая принимает пакет с данными о ходе от клиента 
        и возвращает кортеж (была_ошибка, изменения_в_отрисовке)
        """

        # если передвижение по карте
        if turn[0] == "go":
            field = self.fields.at((turn[1], turn[2]))
            if field:
                result, was_error = player.go(field)
                return was_error, result
            else:
                result = server_tools.create_packet_go()
                result["error"] = 1
                return True, result

        # если удар ножом
        elif turn[0] == "knife":
            was_error, result = player.stab_with_knife()
            return was_error, result

        # если выбрана бомба
        elif turn[0] == "bomb":
            field = self.fields.at((turn[1], turn[2]))
            if field:
                result, was_error = player.plant_bomb(field)
                return was_error, result
            else:
                result = server_tools.create_packet_bomb()
                result["error"] = 2
                return True, result

        # если цемент
        elif turn[0] == "concrete":
            field = self.fields.at((turn[1], turn[2]))
            if field:
                result, was_error = player.set_concrete(field)
                return was_error, result
            else:
                result = server_tools.create_packet_concrete()
                result["error"] = 2
                return True, result

        # если использована аптечка
        elif turn[0] == "aid":
            was_error, result = player.use_aid()
            return was_error, result

        else:
            logging.critical("Игра не может принять такую команду: {}".format(turn[0]))

    def next_player(self):
        """ переключает активного игрока """
        # todo при отключении игрока обработать исключение
        pos = self.players.index(self.active_player)
        self.active_player = self.players[(pos + 1) % len(self.players)]

    async def end(self):
        """ завершение игры """
        logging.info("Завершаю игру...")
        for player in self.players:
            try:
                player.websocket.close()
            except websockets.ConnectionClosed:
                logging.error("Игрок {} уже отключен".format(player.name))

    @server_tools.to_json
    def get_init_data(self, player_name):
        """ функция, возвращающая начальные игровые данные для игрока с именем player_name """
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        else:
            logging.critical("Нет данных об игроке {}!".format(player_name))

        data = {
            "list_of_players": [player.name for player in self.players],
            "size": [levels.SIZE, levels.SIZE],
            "place": player.location.coordinates,
            "equipment": player.inventory
        }
        return data

    def initialize_level(self):
        """ функция, выполняющая построение игрового уровня из двумерного списка-маски уровня """
        random.shuffle(self.players)
        count_id = 0
        self.fields.dim = levels.SIZE
        player_start_positions = []  # для рандомного расположения игроков

        for row in range(levels.SIZE):
            for col in range(levels.SIZE):
                coordinates = (row, col)
                value = self.level[row][col]
                if value == 10:
                    grass = fields.Grass(self, count_id, coordinates, None)
                    grass.exit = True
                    self.fields.add(grass)
                if value == 0:
                    self.fields.add(fields.Grass(self, count_id, coordinates, None))
                elif value == 1:
                    self.fields.add(fields.Wall(self, count_id, coordinates))
                elif value == 11:
                    wall = fields.Wall(self, count_id, coordinates)
                    wall.indestructible = True
                    self.fields.add(wall)
                elif value == 2:
                    grass = fields.Grass(self, count_id, coordinates, None)
                    player_start_positions.append(count_id)
                    self.fields.add(grass)
                elif value == 3:
                    self.fields.add(fields.Grass(self, count_id, coordinates, "ammo"))
                elif value > 40:
                    grass = fields.Grass(self, count_id, coordinates, "tp{}".format(value % 10))
                    self.fields.add_teleport(grass)
                    self.fields.add(grass)
                elif value == 5:
                    grass = fields.Grass(self, count_id, coordinates, None)
                    self.fields.add(grass)
                    self.bear.location = grass
                elif value == 6:
                    grass = fields.Grass(self, count_id, coordinates, None)
                    grass.has_treasure = True
                    self.fields.add(grass)
                elif value == 7:
                    self.fields.add(fields.Grass(self, count_id, coordinates, "mine"))
                elif value == 8:
                    self.fields.add(fields.Grass(self, count_id, coordinates, "hospital"))
                elif value == 9:
                    self.fields.add(fields.Water(self, count_id, coordinates))
                count_id += 1

        random.shuffle(player_start_positions)
        for i in range(self.num_players):
            pos = player_start_positions[i]
            player = self.players[i]
            player.visible_fields[pos] = True
            player.location = self.fields.by_id(pos)

    @server_tools.to_json
    def get_statistics(self, player):
        """ функция, получающая финальные данные для игрока player"""
        final_packet = {
            "type": "final",
            "statistics": [self.winner.name] + [player.name for player in self.players if player != self.winner],
            "prize": [0] * 3
        }
        if player.name == self.winner.name:
            final_packet["prize"] = [random.randint(1, 5) for _ in range(3)]

        return final_packet


if __name__ == "__main__":
    print("Game module")
