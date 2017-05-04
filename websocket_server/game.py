# -*- coding: utf-8 -*-

import random
import json
from functools import wraps

import levels


def to_json(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            result = json.dumps(result, indent=4, sort_keys=True)
        return result
    return inner


class Player:
    """ player for the game """
    MAX_HEALTH = 3

    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.location = None
        self.vector = (0, 0)
        self.health = Player.MAX_HEALTH
        self.visible_fields = [False for _ in game.level]
        self.inventory = {}

    def __vector_to(self, obj):
        """ calculates vector distance to object """
        shift_x, shift_y = map((lambda x, y: x - y), obj.coordinates, self.location.coordinates)
        return shift_x, shift_y

    def update(self):
        pass

    def go(self, field):
        """ player movement logic """
        self.visible_fields[field.id] = True
        if isinstance(field, Wall):
            self.vector = (0, 0)
            return
        if self.game.bear.location == field:
            self.vector = self.__vector_to(field)
            self.game.bear.attack(self)
            return
        self.move(field)
        if isinstance(field, Grass):
            if field.obj == "hospital":
                self.heal()
            elif field.obj == "mine":
                self.get_damage(3)
                field.delete_object()
            elif field.obj in ("tp1", "tp2", "tp3"):
                self.visible_fields[field.pair.id] = True
                self.teleport_from(field)
        # flow down (and left) the river
        elif isinstance(field, Water):
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
            self.vector = vector

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
        if self.health < 0:
            self.health = 0

    def get_pushed(self, from_obj):
        pass


class Field:
    def __init__(self, game, identity, coordinates):
        self.game = game
        self.obj = None
        self.id = identity
        self.coordinates = coordinates

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
        self.num_players = len(players_names)
        self.players_names = players_names
        self.players = [Player(self, name) for name in players_names]
        self.active_player = None
        self.bear = Bear(self)
        self.fields = FieldGroup()
        self.level = levels.get_random_level()

    def add_player(self, player_name):
        self.players_names.append(player_name)
        self.num_players += 1
        self.players.append(Player(self, player_name))

    @to_json
    def get_init_data(self, player_name):
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        data = {
            "list_of_players": self.players_names,
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
        random.shuffle(self.players)
        num_player = 0
        count_id = 0
        for row in range(levels.SIZE):
            for col in range(levels.SIZE):
                coordinates = (row, col)
                value = self.level[row][col]
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
                    self.fields.add(Grass(self, count_id, coordinates, "treasure"))
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
