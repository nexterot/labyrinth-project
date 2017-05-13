# -*- coding: utf-8 -*-

import json
import logging
import datetime

from functools import wraps


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
        "exit": [0] * 2
    }


def create_packet_knife():
    return {
        "type": "turn",
        "type_of_turn": "knife",
        "error": 0,
        "coordinates": [0, 0],
        "is_here_enemy": 0,
        "name_of_victim": None
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
        "error": packet["error"],
        "wall": packet["wall"],
        "is_visible_from": False,
        "is_visible_to": False,
        "to_coordinates": None,
        "from_coordinates": None,  # todo coordinates from where player is going
        "mine": packet["mine"],
        "river": packet["river"],
        "aid": packet["aid"],
        "arm": packet["arm"],
        "bear": 0,
        "treasure": packet["treasure"],
        "metro": packet["metro"],
        "exit": packet["exit"]
    }

    row, col = packet["coordinates"]

    if player.visible_fields[row * player.game.fields.dim + col]:
        data["is_visible_to"] = 1
        data["to_coordinates"] = packet["coordinates"]

    return data


@to_json
def analyze_knife_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "error": packet["error"],
        "are_you_injured": 0,
        "is_here_enemy": packet["is_here_enemy"],
        "victim_name": packet["name_of_victim"],
        "is_visible_knife": 0,
    }

    # если виден удар ножом
    row, col = packet["coordinates"]

    if player.visible_fields[row * player.game.fields.dim + col]:
        data["is_visible_knife"] = True

    if packet["name_of_victim"] == player.name:
        data["are_you injured"] = True

    return data


@to_json
def analyze_bomb_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "error": 0,
        "on_wall": 0,
        "on_ground": 0,
        "is_visible_from": False,
        "is_visible_to": False,
        "to_coordinates": None,
        "from_coordinates": None,  # todo coordinates from where player is planting a bomb
    }

    row, col = packet["wall_or_ground"][1:3]

    if packet["wall_or_ground"][0] == 1:  # обычная стена
        data["on_wall"] = 1
    elif packet["wall_or_ground"][0] == 2:  # искусственный бетон
        data["on_wall"] = 2
    elif packet["wall_or_ground"][0] == 3:  # просто установить бомбу
        data["on_ground"] = 1

    if player.visible_fields[row * player.game.fields.dim + col]:
        data["is_visible_to"] = 1
        data["to_coordinates"] = packet["coordinates"]

    return data


@to_json
def analyze_concrete_turn(player, player_acted, packet):
    data = {
        "name": player.name,
        "error": 0,
        "is_visible_from": False,
        "is_visible_to": False,
        "to_coordinates": None,
        "from_coordinates": None,  # todo coordinates from where player is setting a concrete wall
    }

    row, col = packet["coordinates"]

    if player.visible_fields[row * player.game.fields.dim + col]:
        data["is_visible_to"] = 1
        data["to_coordinates"] = packet["coordinates"]

    return data


@to_json
def analyze_aid_turn(player, player_acted, packet):
    data = {
        "name": player_acted.name,
        "error": 0,
        "is_visible_aid": False,
        "coordinates": None
    }

    row, col = packet["coordinates"]

    if player.visible_fields[row * player.game.fields.dim + col]:
        data["is_visible_aid"] = True
        data["coordinates"] = packet["coordinates"]

    return data
