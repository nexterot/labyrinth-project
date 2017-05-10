# -*- coding: utf-8 -*-


class Field:
    def __init__(self, game, identity, coordinates):
        self.game = game
        self.obj = None
        self.id = identity
        self.coordinates = coordinates
        self.has_treasure = False

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
        self.concrete = False

    def update(self):
        pass

    def delete_object(self):
        self.obj = None


class Water(Field):
    """ water field """
    def __init__(self, game, identity, coordinates):
        Field.__init__(self, game, identity, coordinates)


class Wall(Field):
    """ impassable field """
    def __init__(self, game, identity, coordinates):
        Field.__init__(self, game, identity, coordinates)


class FieldGroup:
    """ a container that represents the game battlefield """
    def __init__(self):
        self.sprites = []
        self.dim = None

    def add(self, field):
        self.sprites.append(field)

    def at(self, coordinates):
        """ find Field object with such coordinates """
        return self.sprites[coordinates[0] * self.dim + coordinates[1]]

    def by_id(self, identity):
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
