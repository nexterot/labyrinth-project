# -*- coding: utf-8 -*-

from game import fields


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
        if not field or isinstance(field, fields.Wall):
            return
        elif isinstance(field, fields.Grass) and field.obj in ("tp1", "tp2", "tp3"):
            self.move(field.pair)
            return
        elif isinstance(field, fields.Grass) and field.obj == "mine":
            field.delete_object()
        if self.game.player.location == field:
            self.attack(self.game.player)
            return
        self.move(field)
        # flow down (and left) the river
        if isinstance(field, fields.Water):
            washed_away = False
            while not washed_away:
                next_water_down = self.game.fields.at((field.coordinates[0] + 1, field.coordinates[1]))
                next_water_left = self.game.fields.at((field.coordinates[0], field.coordinates[1] - 1))
                if isinstance(next_water_down, fields.Water):
                    self.move(next_water_down)
                    field = next_water_down
                elif isinstance(next_water_left, fields.Water):
                    self.move(next_water_left)
                    field = next_water_left
                else:
                    washed_away = True

    def move(self, field):
        self.location = field