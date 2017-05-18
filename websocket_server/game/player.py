# -*- coding: utf-8 -*-

import random

import server_tools
from game import fields
from game.constants import *


class Player:
    """ Класс, реализующий логику игрока """

    MAX_HEALTH = 4

    def __init__(self, game, name, websocket):
        self.game = game
        self.name = name
        self.location = None
        self.prev_location = None
        self.vector = (0, 0)
        self.health = Player.MAX_HEALTH
        self.visible_fields = [False] * (len(game.level) * len(game.level[0]))
        self.inventory = [0, 0, 0]
        self.has_treasure = False
        self.websocket = websocket

    @property
    def alive(self):
        return self.health > 0

    def __vector_to(self, obj):
        """ calculates vector distance to object """
        shift_x, shift_y = map((lambda x, y: x - y), obj.coordinates, self.location.coordinates)
        return shift_x, shift_y

    def go(self, field):
        """ логика передвижения игрока """
        self.prev_location = self.location

        result = server_tools.create_packet_go()           # создаем пустой пакет для отправки клиенту
        result["coordinates"] = self.location.coordinates  # заполняем текущие координаты

        # если клетка не рядом
        if not self.can_go(field):
            result["error"] = 1
            return result, True

        self.visible_fields[field.id] = True

        # если стена
        if isinstance(field, fields.Wall):
            # self.vector = (0, 0)
            result["wall"] = [1, field.coordinates[0], field.coordinates[1]]
            return result, False

        elif isinstance(field, fields.Grass) and field.concrete:
            result["wall"] = [2, field.coordinates[0], field.coordinates[1]]
            return result, False

        for pl in self.game.players:
            if self.location == pl.location and self != pl:
                if not pl.alive:
                    result["is_here_enemy"] = 1
                else:
                    result["is_here_enemy"] = 2
                result["name"] = pl.name
                result["enemy_alive"] = pl.alive

        if isinstance(self.location, fields.Water):
            result["from_sprite"] = "water"
        elif self.location.has_treasure:
            result["from_sprite"] = "treasure"
        elif self.location.obj == "hospital":
            result["from_sprite"] = "aid"
        elif self.location.obj == "ammo":
            result["from_sprite"] = "arm"
        elif self.location.obj == "mine":
            result["from_sprite"] = "bomb"
        elif self.location.obj in {"tp1", "tp2", "tp3"}:
            result["from_sprite"] = "metro"
        else:
            result["from_sprite"] = "sand"

        result["from_coordinates"] = self.location.coordinates

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
        if isinstance(field, fields.Grass):
            # если клетка - выход из лабиринта
            if field.exit:
                result["exit"][0] = 1
                if self.has_treasure:
                    result["exit"][1] = 1  # выиграл
                    self.game.winner = self
                else:
                    result["exit"][1] = 0  # нужно откинуть
                    # передвинуть игрока
                    self.move(self.prev_location)

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
                if not self.alive:
                    result["arm"] = -1
                elif random.randrange(1, 3) == 1:  # +1 цемент
                    self.inventory[CONCRETE] += 1
                    result["arm"] = 1
                else:  # +1 бомба
                    self.inventory[BOMB] += 1
                    result["arm"] = 2

            # если мина
            elif field.obj == "mine":
                if self.alive:
                    self.get_damage(2)
                    if self.health == 0:
                        result["mine"] = 1
                    elif self.health == 2:
                        result["mine"] = 2
                    elif self.health == 1:
                        result["mine"] = 3
                    field.delete_object()
                else:
                    result["mine"] = -1

            # сокровище :)
            if field.has_treasure:
                if self.alive:
                    self.has_treasure = True
                    field.has_treasure = False
                    result["treasure"] = 1
                else:
                    result["treasure"] = 2

            # если телепорт
            if field.obj in {"tp1", "tp2", "tp3"}:
                result["metro"] = [1, *field.pair.coordinates]
                self.visible_fields[field.pair.id] = True
                self.teleport_from(field)

        # плывем вниз и влево по реке
        if isinstance(field, fields.Water):
            river_info = [1, []]
            vector = self.vector
            washed_away = False

            while not washed_away:
                next_water_down = self.game.fields.at((field.coordinates[0] + 1, field.coordinates[1]))
                next_water_left = self.game.fields.at((field.coordinates[0], field.coordinates[1] - 1))
                if isinstance(next_water_down, fields.Water):
                    self.move(next_water_down)
                    self.visible_fields[next_water_down.id] = True
                    field = next_water_down
                elif isinstance(next_water_left, fields.Water):
                    self.move(next_water_left)
                    self.visible_fields[next_water_left.id] = True
                    field = next_water_left
                else:
                    washed_away = True
                    self.visible_fields[field.id] = True
                river_info[1].append(self.location.coordinates)

            result["river"] = river_info
            self.vector = vector

        return result, False

    def move(self, field):
        """ make a move """
        self.vector = self.__vector_to(field)
        self.location = field

    def stab_with_knife(self):
        self.prev_location = self.location

        packet = server_tools.create_packet_knife()

        if not self.alive:
            packet["error"] = 1
            return True, packet

        packet["coordinates"] = self.location.coordinates

        for player in self.game.players:
            if player.location == self.location and player.alive and player != self:
                packet["name_of_victim"] = player.name
                player.get_damage(1)
                if not player.alive:
                    packet["is_here_enemy"] = 1
                else:
                    packet["is_here_enemy"] = 2
                break

        if isinstance(self.location, fields.Water):
            packet["from_sprite"] = "water"
        elif self.location.has_treasure:
            packet["from_sprite"] = "treasure"
        elif self.location.obj == "hospital":
            packet["from_sprite"] = "aid"
        elif self.location.obj == "ammo":
            packet["from_sprite"] = "arm"
        elif self.location.obj == "mine":
            packet["from_sprite"] = "bomb"
        elif self.location.obj in {"tp1", "tp2", "tp3"}:
            packet["from_sprite"] = "metro"
        else:
            packet["from_sprite"] = "sand"

        return False, packet

    def plant_bomb(self, field):
        self.prev_location = self.location

        packet = server_tools.create_packet_bomb()

        # если клетка не рядом
        if not self.can_go(field):
            packet["error"] = 2
            return packet, True

        # если игрок мертв
        if not self.alive:
            packet["error"] = 1
            return packet, True

        # если у игрока нет бомб
        if self.inventory[BOMB] == 0:
            packet["error"] = 3
            return packet, True

        # нельзя ставить на игрока
        for player in self.game.players:
            if player.location == field:
                packet["error"] = 2
                return packet, True

        self.visible_fields[field.id] = True

        # если клетка - трава и на ней ничего нет - просто установить бомбу
        if isinstance(field, fields.Grass) and not field.obj and not field.has_treasure \
                and not field.concrete and not field.exit:
            packet["wall_or_ground"] = [3, field.coordinates[0], field.coordinates[1]]
            field.obj = "mine"

        # если же там обычная стена, то взорвать стену
        elif isinstance(field, fields.Wall) and not field.indestructible:
            packet["wall_or_ground"] = [1, field.coordinates[0], field.coordinates[1]]
            # поменять тип объекта на пустой Grass
            self.game.fields.sprites[field.id] = fields.Grass(self.game, field.id, field.coordinates, None)

        # если клетка, на которую кто-то установил бетон
        elif isinstance(field, fields.Grass) and field.concrete:
            packet["wall_or_ground"] = [2, field.coordinates[0], field.coordinates[1]]
            # удалить бетон
            field.concrete = False

        else:
            packet["error"] = 2
            return packet, True

        self.inventory[BOMB] -= 1


        return packet, False

    def set_concrete(self, field):
        self.prev_location = self.location

        packet = server_tools.create_packet_concrete()

        # если клетка не рядом
        if not self.can_go(field):
            packet["error"] = 2
            return packet, True

        # если игрок мертв
        if not self.alive:
            packet["error"] = 1
            return packet, True

        # если у игрока нет цемента
        if self.inventory[CONCRETE] == 0:
            packet["error"] = 3
            return packet, True

        # нельзя ставить на игрока
        for player in self.game.players:
            if player.location == field:
                packet["error"] = 2
                return packet, True

        self.visible_fields[field.id] = True

        # если пустой Grass
        if isinstance(field, fields.Grass) and not field.exit and not field.obj and not field.has_treasure and not field.concrete:
            for player in self.game.players:
                if player.location == field:
                    packet["error"] = 2
                    return packet, True
            packet["coordinates"] = field.coordinates
            field.concrete = True
            self.inventory[CONCRETE] -= 1
            return packet, False
        else:
            packet["error"] = 2
            return packet, True

    def use_aid(self):
        self.prev_location = self.location
        packet = server_tools.create_packet_aid()

        # если игрок мертв
        if not self.alive:
            packet["error"] = 1
            return True, packet

        # если нет аптечек
        if self.inventory[AID] == 0:
            packet["error"] = 2
            return True, packet

        # если и так уже здоров
        if self.health == Player.MAX_HEALTH:
            packet["error"] = 3
            return True, packet

        packet["now_health"] = self.health
        packet["coordinates"] = self.location.coordinates

        self.health += 1
        self.inventory[AID] -= 1

        return False, packet

    def teleport_from(self, field):
        self.location = field.pair

    def can_go(self, field):
        """ returns True if self.location is adjacent to field (excluding diagonals) """
        shift_x, shift_y = map((lambda x, y: x - y), field.coordinates, self.location.coordinates)
        return abs(shift_x) + abs(shift_y) == 1

    def heal(self):
        self.health = Player.MAX_HEALTH

    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            if self.has_treasure:
                self.has_treasure = False
                self.location.has_treasure = True
                print("Игрок {} потерял сокровище".format(self.name))

    def get_pushed(self, from_obj):
        pass