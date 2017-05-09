# -*- coding: utf-8 -*-

import random

from game.bear import Bear
from game.player import Player


import server_tools
from game import fields
from game import levels


class Game:
    """ class representing the game """
    def __init__(self, players_names):
        self.fields = fields.FieldGroup()
        self.level = levels.get_random_level()
        self.players_names = list(players_names)
        self.num_players = len(self.players_names)
        self.players = [Player(self, name) for name in players_names]
        self.active_player = self.players[0]
        self.bear = Bear(self)
        self.winner = None
        self.initialize_level()

    def accept(self, player, turn):
        if turn[0] == "go":
            field = self.fields.at((turn[1], turn[2]))
            if field:
                result, was_error = player.go(field)
                return was_error, result
            else:
                result = server_tools.create_packet()
                result["error"] = 1
                return True, result

        elif turn[0] == "knife":
            ...

        elif turn[0] == "concrete":
            ...

        elif turn[0] == "bomb":
            ...

        elif turn[0] == "aid":
            ...

        else:
            print("Unknown command to accept by game: {}".format(turn[0]))

    def end(self, winner):
        print("Игрок {} выиграл!!!".format(winner.name))
        # todo закончить игру

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
            "list_of_players": self.players_names,
            "size": [levels.SIZE, levels.SIZE],
            "place": player.location.coordinates,
            "equipment": player.inventory
        }
        return data

    def initialize_level(self):
        """ build game level from mask """
        # random.shuffle(self.players)
        num_player = 0
        count_id = 0
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

    def get_statistics(self, player_name):
        final_packet = {
            "type": "final",
            "statistics": [self.winner.name] + [player.name for player in self.players if player != self.winner],
            "prize": None
        }
        if player_name == self.winner.name:
            final_packet["prize"] = [random.randint(1, 5+1) for _ in range(3)]
        else:
            final_packet["prize"] = [0] * 3

        return final_packet


if __name__ == "__main__":
    print("Game module")
