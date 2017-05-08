# -*- coding: utf-8 -*-

import random
import json
from functools import wraps

import levels


BOMB = 0
CONCRETE = 1
AID = 2


def to_json(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            result = json.dumps(result)
        return result
    return inner


def create_packet():
    return {
        "type": "turn", "type_of_turn": "go", "error": 0, "coordinates": [None, None],
        "wall": False, "mine": False, "river": [None, None, None], "aid": None, "arm": False, "bear": False,
        "treasure": False, "metro": [None, None, None], "exit": [None, None]
    }


class Player:
    """ player for the game """
    MAX_HEALTH = 4

    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.location = None
        self.vector = (0, 0)
        self.health = Player.MAX_HEALTH
        self.visible_fields = [False] * (len(game.level) * len(game.level[0]))
        self.inventory = [0, 0, 0]
        self.has_treasure = False

    def __vector_to(self, obj):
        """ calculates vector distance to object """
        shift_x, shift_y = map((lambda x, y: x - y), obj.coordinates, self.location.coordinates)
        return shift_x, shift_y

    def update(self):
        pass

    def go(self, field):
        """ player movement logic """

        # создаем пустой пакет для отправки клиенту
        result = create_packet()

        # текущие координаты
        result["coordinates"] = self.location.coordinates

        # если клетка не рядом
        if not self.can_go(field):
            result["error"] = 1
            return result, True

        self.visible_fields[field.id] = True

        # если стена
        if isinstance(field, Wall):
            self.vector = (0, 0)
            result["wall"] = True
            return result, False

        # помещаем коориданты клетки, на которую перейдем
        result["coordinates"] = field.coordinates

        # передвинуть игрока
        self.move(field)

        # если на клетке стоит медведь
        if self.game.bear.location == field:
            self.vector = self.__vector_to(field)
            self.game.bear.attack(self)
            if self.health == 0:
                result["bear"] = 1
            elif self.health == 2:
                result["bear"] = 2
            elif self.health == 1:
                result["bear"] = 3
            return result, False

        # если обычная клетка
        if isinstance(field, Grass):

            # если клетка - выход из лабиринта
            if field.exit:
                result["exit"][0] = 1
                if self.has_treasure:
                    result["exit"][1] = 1  # выиграл
                    self.game.winner = self
                else:
                    result["exit"][1] = 0  # нужно откинуть

            # если на этой клетке лежит аптечка
            elif field.obj == "hospital":
                if self.health == 0:
                    result["aid"] = 1
                    self.heal()
                elif self.health < Player.MAX_HEALTH:
                    result["aid"] = 2
                    self.heal()
                else:
                    result["aid"] = 3
                    self.inventory[AID] += 1

            # если на этой клетке лежит вооружение
            elif field.obj == "ammo":
                if random.randrange(1, 3) == 1:  # +1 цемент
                    self.inventory[CONCRETE] += 1
                    result["arm"] = 1
                else:  # +1 бомба
                    self.inventory[BOMB] += 1
                    result["arm"] = 2

            # сокровище :)
            elif field.treasure:
                field.treasure = False
                self.has_treasure = True
                result["treasure"] = 1
                # todo уведомить остальных игроков, что клад найден мною
                print("Игрок {} нашел клад!".format(self.name))

            # если мина
            elif field.obj == "mine":
                self.get_damage(2)
                if self.health == 0:
                    result["mine"] = 1
                elif self.health == 2:
                    result["mine"] = 2
                elif self.health == 1:
                    result["mine"] = 3
                field.delete_object()

            # если телепорт
            elif field.obj in {"tp1", "tp2", "tp3"}:
                result["metro"] = [1, *field.pair.coordinates]
                self.visible_fields[field.pair.id] = True
                self.teleport_from(field)

        # flow down (and left) the river
        elif isinstance(field, Water):
            river_info = [1, []]
            vector = self.vector
            washed_away = False

            while not washed_away:
                next_water_down = self.game.fields.at((field.coordinates[0] + 1, field.coordinates[1]))
                next_water_left = self.game.fields.at((field.coordinates[0], field.coordinates[1] - 1))
                if isinstance(next_water_down, Water):
                    self.move(next_water_down)
                    self.visible_fields[next_water_down.id] = True
                    field = next_water_down
                elif isinstance(next_water_left, Water):
                    self.move(next_water_left)
                    self.visible_fields[next_water_left.id] = True
                    field = next_water_left
                else:
                    washed_away = True
                    self.visible_fields[field.id] = True
                river_info[1].append(self.location.coordinates.copy())

            result["river"] = river_info
            self.vector = vector

        return result, False

    def move(self, field):
        """ make a move """
        self.vector = self.__vector_to(field)
        self.location = field

    def teleport_from(self, field):
        self.location = field.pair

    def look(self, field):
        if self.can_look(field):
            self.visible_fields[field.id] = True
            self.vector = (0, 0)

    def can_go(self, field):
        """ returns True if self.location is adjacent to field (excluding diagonals) """
        shift_x, shift_y = map((lambda x, y: x - y), field.coordinates, self.location.coordinates)
        return abs(shift_x) + abs(shift_y) == 1

    def can_look(self, field):
        """ returns True if self.location is adjacent to field (including diagonals) """
        shift_x, shift_y = map((lambda x, y: x - y), field.coordinates, self.location.coordinates)
        return abs(shift_x) | abs(shift_y) == 1

    def heal(self):
        self.health = Player.MAX_HEALTH

    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

            # если убит, то теряет клад
            if self.has_treasure:
                self.has_treasure = False
                self.location.treasure = True
                print("Игрок {} потерял клад!".format(self.name))

    def get_pushed(self, from_obj):
        pass


class Field:
    def __init__(self, game, identity, coordinates):
        self.game = game
        self.obj = None
        self.id = identity
        self.coordinates = coordinates
        self.treasure = False

    def update(self):
        pass

    def delete_object(self):
        pass


class Grass(Field):
    """ grass field; it can contain drop objects as well as hospitals etc. """
    def __init__(self, game, identity, coordinates, obj):
        Field.__init__(self, game, identity, coordinates)
        self.obj = obj
        self.pair = None  # for teleports
        self.exit = False

    def update(self):
        pass


class Water(Field):
    """ water field """
    def __init__(self, game, identity, coordinates):
        Field.__init__(self, game, identity, coordinates)


class Wall(Field):
    """ impassable field """
    def __init__(self, game, identity, coordinates):
        Field.__init__(self, game, identity, coordinates)


class Bear:
    """ powerful but narrow-minded monster """
    def __init__(self, game):
        self.game = game
        self.location = None

    def attack(self, obj):
        obj.get_damage(2)
        obj.get_pushed(self)

    def update(self):
        pass

    def go(self):
        """ bear movement logic """
        field = self.game.fields.at((self.location.coordinates[0] - self.game.player.vector[0],
                                    self.location.coordinates[1] - self.game.player.vector[1]))
        if not field or isinstance(field, Wall):
            return
        elif isinstance(field, Grass) and field.obj in ("tp1", "tp2", "tp3"):
            self.move(field.pair)
            return
        elif isinstance(field, Grass) and field.obj == "mine":
            field.delete_object()
        if self.game.player.location == field:
            self.attack(self.game.player)
            return
        self.move(field)
        # flow down (and left) the river
        if isinstance(field, Water):
            washed_away = False
            while not washed_away:
                next_water_down = self.game.fields.at((field.coordinates[0] + 1, field.coordinates[1]))
                next_water_left = self.game.fields.at((field.coordinates[0], field.coordinates[1] - 1))
                if isinstance(next_water_down, Water):
                    self.move(next_water_down)
                    field = next_water_down
                elif isinstance(next_water_left, Water):
                    self.move(next_water_left)
                    field = next_water_left
                else:
                    washed_away = True

    def move(self, field):
        self.location = field


class Game:
    """ class representing the game """
    def __init__(self, players_names):
        self.fields = FieldGroup()
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
                result = create_packet()
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

    def get_statistics(self):
        print("Игрок {} выиграл!!!".format(self.winner.name))
        final_result = {
            "type": "final",
            "statistics": ['michelin', 'nexterot'],
            "prize": [0, 0, 0]
        }
        return final_result
        # todo закончить игру

    @to_json
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

    def update(self, events: dict) -> dict:
        """ main update method """
        # go on to next player
        if self.active_player is None:
            self.active_player = self.players[0]
        else:
            self.active_player = self.players[(self.players.index(self.active_player) + 1) % len(self.players)]

        self.fields.update()
        self.active_player.update()
        self.bear.update()

        return events

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
                    grass = Grass(self, count_id, coordinates, None)
                    grass.exit = True
                    self.fields.add(grass)
                if value == 0:
                    self.fields.add(Grass(self, count_id, coordinates, None))
                elif value == 1:
                    self.fields.add(Wall(self, count_id, coordinates))
                elif value == 2:
                    grass = Grass(self, count_id, coordinates, None)
                    if num_player < self.num_players:
                        player = self.players[num_player]
                        player.visible_fields[count_id] = True
                        player.location = grass
                        num_player += 1
                    self.fields.add(grass)
                elif value == 3:
                    self.fields.add(Grass(self,  count_id, coordinates, "ammo"))
                elif value > 40:
                    assert 41 <= value <= 43
                    grass = Grass(self, count_id, coordinates, "tp{}".format(value % 10))
                    self.fields.add_teleport(grass)
                    self.fields.add(grass)
                elif value == 5:
                    grass = Grass(self, count_id, coordinates, None)
                    self.fields.add(grass)
                    self.bear.location = grass
                elif value == 6:
                    grass = Grass(self, count_id, coordinates, None)
                    grass.treasure = True
                    self.fields.add(grass)
                elif value == 7:
                    self.fields.add(Grass(self, count_id, coordinates, "mine"))
                elif value == 8:
                    self.fields.add(Grass(self, count_id, coordinates, "hospital"))
                elif value == 9:
                    self.fields.add(Water(self, count_id, coordinates))
                count_id += 1


class FieldGroup:
    """ a container that represents the game battlefield """
    def __init__(self):
        self.sprites = []

    def add(self, field):
        self.sprites.append(field)

    def at(self, coordinates):
        """ find Field object with such coordinates """
        for field in self.sprites:
            if field.coordinates == coordinates:
                return field

    def by_id(self, identity):
        assert identity < len(self.sprites)
        return self.sprites[identity]

    def update(self):
        for field in self.sprites:
            field.update()

    def add_teleport(self, tp_field) -> None:
        """ method that finds pairs to teleports 1-3 while building level """
        for field in self.sprites:
            if isinstance(field, Grass) and field.obj == tp_field.obj:
                field.pair = tp_field
                tp_field.pair = field
                break


if __name__ == "__main__":
    print("Game module")
