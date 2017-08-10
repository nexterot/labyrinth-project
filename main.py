#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.locals import *


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 2, 5, 255)


class Images:
    """ static class of images for game sprites """
    background = pygame.image.load("sprites/background.png")
    wall = pygame.image.load("sprites/wall.png")
    weapons = pygame.image.load("sprites/weapons.png")
    mine = pygame.image.load("sprites/mine.png")
    teleport = pygame.image.load("sprites/teleport.png")
    teleport_2 = pygame.image.load("sprites/teleport_2.png")
    teleport_3 = pygame.image.load("sprites/teleport_3.png")
    bear = pygame.image.load("sprites/bear.png")
    hospital = pygame.image.load("sprites/aid.png")
    treasure = pygame.image.load("sprites/treasure.png")
    water = pygame.image.load("sprites/water.png")
    grass = pygame.image.load("sprites/grass.png")
    button_menu = pygame.image.load("sprites/button_menu.png")
    button_exit = pygame.image.load("sprites/button_exit.png")
    player_face = pygame.image.load("sprites/player_face.png")
    panel = pygame.image.load("sprites/panel.png")
    weapon_gun = pygame.image.load("sprites/weapon_gun.png")
    weapon_mine = pygame.image.load("sprites/weapon_mine.png")
    player = pygame.image.load("sprites/player.png")
    scale_health = pygame.image.load("sprites/scale_health.png")
    label_nick = pygame.image.load("sprites/label_nick.png")
    fog = pygame.image.load("sprites/fog.png")


class Player(pygame.sprite.Sprite):
    """ player for the game """
    MAX_HEALTH = 3

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images.player
        self.rect = self.image.get_rect(topleft=(x, y))
        self.location = None
        self.vector = (0, 0)
        self.health = Player.MAX_HEALTH

    def __vector_to(self, obj):
        """ calculates vector distance to object """
        shift_x, shift_y = map((lambda x, y: x - y), obj.coordinates, self.location.coordinates)
        return shift_x, shift_y

    def update(self):
        Game.surface.blit(self.image, self.rect)

    def go(self, field):
        """ player movement logic """
        field.visible = True
        if isinstance(field, Wall):
            self.vector = (0, 0)
            return
        if Game.bear.location == field:
            self.vector = self.__vector_to(field)
            Game.bear.attack(self)
            return
        self.move(field)
        if isinstance(field, Grass):
            if field.obj == "hospital":
                self.heal()
            elif field.obj == "mine":
                self.get_damage(3)
                field.delete_object()
            elif field.obj in ("tp1", "tp2", "tp3"):
                field.pair.visible = True
                self.teleport_from(field)
        # flow down (and left) the river
        elif isinstance(field, Water):
            vector = self.vector
            washed_away = False
            while not washed_away:
                next_water_down = Game.fields.at((field.coordinates[0] + 1, field.coordinates[1]))
                next_water_left = Game.fields.at((field.coordinates[0], field.coordinates[1] - 1))
                if isinstance(next_water_down, Water):
                    self.move(next_water_down)
                    next_water_down.visible = True
                    field = next_water_down
                elif isinstance(next_water_left, Water):
                    self.move(next_water_left)
                    next_water_left.visible = True
                    field = next_water_left
                else:
                    washed_away = True
                field.visible = True
            self.vector = vector

    def move(self, field):
        """ make a move """
        self.vector = self.__vector_to(field)
        self.rect = field.rect
        self.location = field

    def teleport_from(self, field):
        self.rect = field.pair.rect
        self.location = field.pair

    def look(self, field):
        if self.can_look(field):
            field.visible = True
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
        """ TODO """
        pass


class Field(pygame.sprite.Sprite):
    def __init__(self, coordinates=None):
        pygame.sprite.Sprite.__init__(self)
        self.obj = None
        self.image = None
        self.rect = None
        self.coordinates = coordinates
        self.visible = False
        self.fog_image = Images.fog

    def update(self):
        if self.visible:
            Game.surface.blit(self.image, self.rect)
        else:
            Game.surface.blit(self.fog_image, self.rect)

    def delete_object(self):
        pass


class FieldGroup(pygame.sprite.Group):
    """ a container derived from pygame.sprite.Group that represents the game field """
    def __init__(self):
        super().__init__(self)

    def at(self, coordinates) -> Field:
        """ find Field object with coords """
        for field in self.sprites():
            if field.coordinates == coordinates:
                return field

    def at_coords(self, x, y) -> Field:
        """ find Field object with coords (x, y) """
        for field in self.sprites():
            if field.rect.collidepoint(x, y):
                return field

    def update(self):
        for field in self.sprites():
            field.update()

    def add_teleport(self, tp_field) -> None:
        """ method that finds pairs to teleports 1-3 while building level """
        for field in self.sprites():
            if isinstance(field, Grass) and field.obj == tp_field.obj:
                field.pair = tp_field
                tp_field.pair = field
                break
                

class Grass(Field):
    """ grass field; it can contain drop objects as well as hospitals etc. """
    # Yes, I know, it's not the best effective and clear implementation :) TODO
    def __init__(self, x, y, obj=None, coordinates=None):
        Field.__init__(self, coordinates)
        self.obj = obj
        self.pair = None  # for teleports
        if obj == "tp1":
            self.obj_image = Images.teleport
        elif obj == "tp2":
            self.obj_image = Images.teleport_2
        elif obj == "tp3":
            self.obj_image = Images.teleport_3
        elif obj == "hospital":
            self.obj_image = Images.hospital
        elif obj == "ammo":
            self.obj_image = Images.weapons
        elif obj == "mine":
            self.obj_image = Images.mine
        elif obj == "treasure":
            self.obj_image = Images.treasure

        self.image = Images.grass
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        Field.update(self)
        if self.obj and self.visible:
            Game.surface.blit(self.obj_image, self.rect)


class Water(Field):
    """ water field """
    def __init__(self, x, y, coordinates=None):
        Field.__init__(self, coordinates)
        self.image = Images.water
        self.rect = self.image.get_rect(topleft=(x, y))


class Wall(Field):
    """ impassable field """
    def __init__(self, x, y, coordinates):
        Field.__init__(self, coordinates)
        self.image = Images.wall
        self.rect = self.image.get_rect(topleft=(x, y))


class Bear(pygame.sprite.Sprite):
    """ powerful but narrow-minded monster """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images.bear
        self.rect = self.image.get_rect(topleft=(x, y))
        self.location = None

    def attack(self, obj):
        obj.get_damage(2)
        obj.get_pushed(self)

    def update(self):
        if self.location.visible:
            Game.surface.blit(self.image, self.rect)

    def go(self):
        """ bear movement logic """
        field = Game.fields.at((self.location.coordinates[0] - Game.player.vector[0],
                                self.location.coordinates[1] - Game.player.vector[1]))
        if not field or isinstance(field, Wall):
            return
        elif isinstance(field, Grass) and field.obj in ("tp1", "tp2", "tp3"):
            self.move(field.pair)
            return
        elif isinstance(field, Grass) and field.obj == "mine":
            field.delete_object()
        if Game.player.location == field:
            self.attack(Game.player)
            return
        self.move(field)
        # flow down (and left) the river
        if isinstance(field, Water):
            washed_away = False
            while not washed_away:
                next_water_down = Game.fields.at((field.coordinates[0] + 1, field.coordinates[1]))
                next_water_left = Game.fields.at((field.coordinates[0], field.coordinates[1] - 1))
                if isinstance(next_water_down, Water):
                    self.move(next_water_down)
                    field = next_water_down
                elif isinstance(next_water_left, Water):
                    self.move(next_water_left)
                    field = next_water_left
                else:
                    washed_away = True

    def move(self, field):
        self.rect = field.rect
        self.location = field


class Game:
    """ static class representing the game """
    surface = None
    player = None
    bear = None
    fields = FieldGroup()
    clock = pygame.time.Clock()
    screen_size = (900, 650)
    sprite_size = 50
    font = None

    @classmethod
    def update(cls):
        """ main update method """
        cls.fields.update()
        cls.player.update()
        cls.bear.update()

        cls.surface.blit(Images.scale_health, (30, 365))
        cls.surface.blit(cls.font.render("{}".format(cls.player.health), 1, Colors.BLACK), (100, 375))

    @classmethod
    def render_interface(cls):
        """ paint interface on the left"""
        cls.surface.blit(Images.background, (0, 0))
        cls.surface.blit(Images.player_face, (25, 25))
        cls.surface.blit(Images.panel, (25, 275))
        cls.surface.blit(Images.label_nick, (30, 320))
        cls.surface.blit(Images.weapon_gun, (30, 410))
        cls.surface.blit(Images.weapon_mine, (145, 410))
        cls.surface.blit(Images.button_menu, (30, 515))
        cls.surface.blit(Images.button_exit, (30, 570))

    @classmethod
    def initialize_level(cls):
        """ build level from mask of ints"""
        for row in range(Level.size):
            for col in range(Level.size):
                coordinates = (row, col)
                x, y = 275 + col * cls.sprite_size, 25 + row * cls.sprite_size
                value = Level.mask[row][col]
                if value == 1:
                    cls.fields.add(Wall(x, y, coordinates))
                elif value == 9:
                    cls.fields.add(Water(x, y, coordinates))
                else:
                    if value == 0:
                        cls.fields.add(Grass(x, y, coordinates=coordinates))
                    elif value == 2:
                        g = Grass(x, y, coordinates=coordinates)
                        g.visible = True
                        cls.fields.add(g)
                        cls.player = Player(x, y)
                        cls.player.location = g
                    elif value == 3:
                        cls.fields.add(Grass(x, y, obj="ammo", coordinates=coordinates))
                    elif value > 40:
                        if value == 41:
                            tp_x = "tp1"
                        elif value == 42:
                            tp_x = "tp2"
                        elif value == 43:
                            tp_x = "tp3"
                        else:
                            raise Exception("Error!")
                        g = Grass(x, y, obj=tp_x, coordinates=coordinates)
                        cls.fields.add_teleport(g)
                        cls.fields.add(g)
                    elif value == 5:
                        g = Grass(x, y, coordinates=coordinates)
                        cls.fields.add(g)
                        cls.bear = Bear(x, y)
                        cls.bear.location = g
                    elif value == 6:
                        cls.fields.add(Grass(x, y, obj="treasure", coordinates=coordinates))
                    elif value == 7:
                        cls.fields.add(Grass(x, y, obj="mine", coordinates=coordinates))
                    elif value == 8:
                        cls.fields.add(Grass(x, y, obj="hospital", coordinates=coordinates))


class Level:
    """ static class representing game level mask"""
    size = 12
    # 0 - empty, 1 - wall, 2 - player, 3 - weapons, 41-43 - tp, 5 - bear, 6 - treasure, 7 - mine, 8 - aid, 9 - water
    mask = [
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 3, 0, 0, 0, 0, 1, 0, 1, 42, 0, 1],
        [1, 0, 0, 0, 0, 0, 7, 0, 1, 7, 41, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 5, 0, 1, 0, 2, 0, 7, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 41, 1, 0, 0, 9, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 9, 1, 42, 0, 0, 1],
        [1, 7, 0, 0, 0, 8, 9, 1, 0, 0, 0, 1],
        [0, 0, 0, 9, 9, 9, 9, 1, 0, 0, 6, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]


def main():
    pygame.init()
    pygame.display.set_caption('python')
    Game.surface = pygame.display.set_mode(Game.screen_size)
    Game.font = pygame.font.SysFont("Arial", size=34)

    Game.render_interface()
    Game.initialize_level()

    player = Game.player
    bear = Game.bear
    while True:  # main game loop
        Game.clock.tick(25)  # 25 Frames per second
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                # move to field by pressing left mouse button
                if event.button == 1:
                    field = Game.fields.at_coords(*event.pos)
                    if field and player.can_go(field):
                        player.go(field)
                        # move bear just after player
                        bear.go()
                # discover field by pressing right mouse button
                elif event.button == 3:
                    field = Game.fields.at_coords(*event.pos)
                    if field and Game.player.can_look(field):
                        player.look(field)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        Game.update()
        pygame.display.flip()


if __name__ == "__main__":
    main()
