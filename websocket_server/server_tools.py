# -*- coding: utf-8 -*-

import json
import logging
import datetime

from functools import wraps

from game import fields


TOO_MANY_ROOMS = "000"
ROOM_ALREADY_EXISTS = "100"
NO_SUCH_ROOM = "000"
ROOM_FILLED = "010"
SUCCESS = "111"


async def close_reason(websocket, reason):
    await websocket.send(reason)
    await websocket.close()


def parse_json(message):
    try:
        py_obj = json.loads(message)
    except (json.decoder.JSONDecodeError, TypeError):
        logging.critical("Невозможно распарспить json! {}".format(message))
        return False
    return py_obj


def to_json(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            result = json.dumps(result)
        return result
    return inner


def create_packet_go():
    return {
        "type": "turn",
        "type_of_turn": "go",
        "error": 0,
        "coordinates": [0, 0],
        "wall": 0,
        "mine": 0,
        "river": [0] * 3,
        "aid": 0,
        "arm": 0,
        "bear": 0,
        "treasure": 0,
        "metro": [0] * 3,
        "exit": [0] * 2,
        "is_here_enemy": 0,
        "name": None,
        "from_sprite": "-",
        "from_coordinates": None,
    }


def create_packet_knife():
    return {
        "type": "turn",
        "type_of_turn": "knife",
        "error": 0,
        "coordinates": [0, 0],
        "is_here_enemy": 0,
        "name_of_victim": None,
        "from_sprite": "-",
    }


def create_packet_bomb():
    return {
        "type": "turn",
        "type_of_turn": "bomb",
        "error": 0,
        "wall_or_ground": [0, 0, 0],
    }


def create_packet_concrete():
    return {
        "type": "turn",
        "type_of_turn": "concrete",
        "error": 0,
        "coordinates": [0, 0]
    }


def create_packet_aid():
    return {
        "type": "turn",
        "type_of_turn": "aid",
        "error": 0,
        "now_health": 0,
        "coordinates": None
    }


@to_json
def analyze_go_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "type_of_turn": "go",
        "wall": [0],
        "is_visible_from": 0,
        "is_visible_to": 0,
        "to_coordinates": None,
        "from_coordinates": None,
        "from_sprite": "-",
        "mine": 0,
        "aid": 0,
        "is_alive": 0,
        "river": 0,
        "arm": 0,
        "bear": 0,
        "treasure": [0],
        "metro": [0],
        "exit": [0],
        "enemy_left": 0,
        "enemy_alive": 0,
        "me_left": 0,
    }

    # если игрок нашел сокровище
    if packet["treasure"] == 1:
        data["treasure"][0] = 1

        row, col = player_acted.location.coordinates
        dim = player.game.fields.dim

        if row < dim / 2:  # север
            data["treasure"].append("north")
        else:               # юг
            data["treasure"].append("south")

        if col < dim / 2:  # запад
            data["treasure"].append("west")
        else:               # восток
            data["treasure"].append("east")

    # если мина
    if packet["mine"] == 1:
        data["mine"] = 1
    elif packet["mine"] in {2, 3}:
        data["mine"] = 2
    elif packet["mine"] == -1:
        data["mine"] = -1

    # если аптечка
    if packet["aid"] == 1:
        data["aid"] = 1
    elif packet["aid"] in {2, 3}:
        data["aid"] = 2

    row, col = packet["coordinates"]

    # если видно куда пошел
    if player.visible_fields[row * player.game.fields.dim + col]:
        data["is_visible_to"] = 1
        data["to_coordinates"] = packet["coordinates"]

        data["wall"] = packet["wall"]
        data["river"] = packet["river"]
        data["arm"] = packet["arm"]
        data["metro"] = packet["metro"]
        data["exit"] = packet["exit"]

        if player_acted.alive:
            data["is_alive"] = 1

    # если видно откуда пошел
    if player.visible_fields[player_acted.prev_location.id]:
        # что останется лежать на этой клетке
        if isinstance(player_acted.prev_location, fields.Water):
            data["from_sprite"] = "water"
        elif player_acted.prev_location.has_treasure:
            data["from_sprite"] = "treasure"
        elif player_acted.prev_location.obj == "hospital":
            data["from_sprite"] = "aid"
        elif player_acted.prev_location.obj == "ammo":
            data["from_sprite"] = "arm"
        elif player_acted.prev_location.obj == "mine":
            data["from_sprite"] = "bomb"
        elif player_acted.prev_location.obj in {"tp1", "tp2", "tp3"}:
            data["from_sprite"] = "metro"
        else:
            data["from_sprite"] = "sand"

        data["is_visible_from"] = 1
        data["from_coordinates"] = player_acted.prev_location.coordinates
        if player_acted.alive:
            data["is_alive"] = 1

        for pl in player.game.players:
            if player_acted.prev_location == pl.location:
                # если игрок - это сам ходивший игрок
                if pl == player_acted:
                    pass
                # если игрок - это наблюдающий
                elif pl == player:
                    data["me_left"] = 1
                # если какой-то другой игрок стоит на этой же клетке
                else:
                    data["enemy_left"] = 1
                    data["enemy_alive"] = int(pl.alive)
                    data["enemy_name"] = pl.name

    return data


@to_json
def analyze_knife_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "type_of_turn": "knife",
        "are_you_injured": 0,
        "is_alive": 0,
        "knife_coordinates": None,
        "is_here_enemy": packet["is_here_enemy"],
        "victim_name": packet["name_of_victim"],
        "is_visible_knife": 0,
    }

    row, col = packet["coordinates"]

    # если виден удар ножом
    if player.visible_fields[row * player.game.fields.dim + col]:
        data["is_visible_knife"] = 1
        data["knife_coordinates"] = packet["coordinates"]
        if player_acted.alive:
            data["is_alive"] = 1

    # если ранен игрок, у которого отображается ход
    if packet["name_of_victim"] == player.name:
        if not player.alive:
            data["are_you_injured"] = 1
        elif player.health == 1:
            data["are_you_injured"] = 2
        elif player.health == 2:
            data["are_you_injured"] = 3
        elif player.health == 3:
            data["are_you_injured"] = 4

    return data


@to_json
def analyze_bomb_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "type_of_turn": "bomb",
        "wall_or_ground": None,
        "is_alive": 0,
        "visible_bomb": 0
    }

    row, col = packet["wall_or_ground"][1:3]

    # если видно куда ставит
    if player.visible_fields[row * player.game.fields.dim + col]:
        data["visible_bomb"] = 1
        data["wall_or_ground"] = packet["wall_or_ground"]
        if player_acted.alive:
            data["is_alive"] = 1

    return data


@to_json
def analyze_concrete_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "type_of_turn": "concrete",
        "visible_concrete": 0,
        "coordinates": None,
        "is_alive": 0,
    }

    row, col = packet["coordinates"]

    # если видно куда он ставит бетон
    if player.visible_fields[row * player.game.fields.dim + col]:
        data["visible_concrete"] = 1
        data["coordinates"] = packet["coordinates"]
        if player_acted.alive:
            data["is_alive"] = 1

    return data


@to_json
def analyze_aid_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "type_of_turn": "aid",
        "visible_aid": 0,
        "coordinates": None,
        "is_alive": 0,
    }

    row, col = packet["coordinates"]

    if player.visible_fields[row * player.game.fields.dim + col]:
        data["visible_aid"] = 1
        data["coordinates"] = packet["coordinates"]
        if player_acted.alive:
            data["is_alive"] = 1

    return data

