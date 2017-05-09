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


async def inform_whose_turn(player_name, room, active_player_name, response):
    for websocket in room.players.values():
        logging.info("Уведомляем игрока {}({}), о том, что ходит игрок {}".format(player_name, room.name, active_player_name))
        await websocket.send(response)

        # ждать, чтобы клиент успел отрисовать
        message = await websocket.recv()
        logging.info("Игрок {} прислал {}".format(player_name, message))


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


def create_packet():
    return {
        "type": "turn", "type_of_turn": "go", "error": 0, "coordinates": [0, 0],
        "wall": 0, "mine": 0, "river": [0] * 3, "aid": 0, "arm": 0, "bear": 0,
        "treasure": 0, "metro": [0] * 3, "exit": [0] * 2
    }