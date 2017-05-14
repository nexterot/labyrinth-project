# -*- coding: utf-8 -*-

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

    @property
    def num_players(self):
        return len(self.players)

    async def accept(self, player, turn):
        # если передвижение по карте
        if turn[0] == "go":
            field = self.fields.at((turn[1], turn[2]))
            if field:
                result, was_error = player.go(field)
                if not was_error:
                    self.next_player()
                return was_error, result
            else:
                result = server_tools.create_packet_go()
                result["error"] = 1
                return True, result

        # если удар ножом
        elif turn[0] == "knife":
            was_error, result = player.knife()
            if not was_error:
                self.next_player()
            return was_error, result

        # если выбрана бомба
        elif turn[0] == "bomb":
            field = self.fields.at((turn[1], turn[2]))
            if field:
                result, was_error = player.set_bomb(field)
                if not was_error:
                    self.next_player()
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
                if not was_error:
                    self.next_player()
                return was_error, result
            else:
                result = server_tools.create_packet_concrete()
                result["error"] = 2
                return True, result

        # если использована аптечка
        elif turn[0] == "aid":
            was_error, result = player.use_aid()
            if not was_error:
                self.next_player()
            return was_error, result

        else:
            logging.critical("Игра не может принять такую команду: {}".format(turn[0]))

    def next_player(self):  # todo работает только для двух игроков
        for player in self.players:
            if self.active_player != player:
                self.active_player = player
                break

    async def end(self):
        logging.info("Завершаю игру...")
        for player in self.players:
            try:
                player.websocket.close()
            except websockets.ConnectionClosed:
                logging.error("Игрок {} уже отключен".format(player.name))

    @server_tools.to_json
    def get_init_data(self, player_name):
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        else:
            print("Нет данных об игроке {}!".format(player_name))
        data = {
            "list_of_players": [player.name for player in self.players],
            "size": [levels.SIZE, levels.SIZE],
            "place": player.location.coordinates,
            "equipment": player.inventory
        }
        return data

    def initialize_level(self):
        """ build game level from mask """
        random.shuffle(self.players)
        num_player = 0
        count_id = 0
        self.fields.dim = levels.SIZE
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
                elif value == 11:  # todo 
                    self.fields.add(fields.Wall(self, count_id, coordinates))
                elif value == 2:
                    grass = fields.Grass(self, count_id, coordinates, None)
                    if num_player < self.num_players:
                        player = self.players[num_player]
                        player.visible_fields[count_id] = True
                        player.location = grass
                        num_player += 1
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

    @server_tools.to_json
    def get_statistics(self, player):
        final_packet = {
            "type": "final",
            "statistics": [self.winner.name] + [player.name for player in self.players if player != self.winner],
            "prize": [0] * 3
        }
        if player.name == self.winner.name:
            final_packet["prize"] = [random.randint(1, 6) for _ in range(3)]

        return final_packet


if __name__ == "__main__":
    print("Game module")
