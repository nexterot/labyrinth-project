#!/usr/bin/env python

import asyncio
import websockets
import json

from game import Game

MIN_PLAYERS = 2
MAX_PLAYERS = 10
MAX_ROOMS = 5

rooms = []
games = []


async def rooms_info_request_handler(websocket, path):
    global rooms
    while True:
        dict_view = {room.name : list(room.players.keys()) for room in rooms}
        result = json.dumps(dict_view, indent=4, sort_keys=True)
        await websocket.send(result)
        await asyncio.sleep(2)
        print("Sent room info")


class Room:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.game = None

    def __len__(self):
        return len(self.players)

    def add(self, nickname):
        self.players.append(nickname)

    def start_game(self):
        self.game = Game(self.players)


async def handler(websocket, url):
    result = await websocket.recv() # receive name and hash
    print(result)
    player_name, __hash = result.split("=") # parse name and hash
    command_json = await websocket.recv() # receive command json
    comd = json.loads(command_json) # parse json
    my_room = None
    if comd["type"] == "create":
        if len(rooms) >= MAX_ROOMS:
            await websocket.send("000")
            await websocket.close()
            return
        for room in rooms:
            if room.name == comd["name"]:
                await websocket.send("100")
                await websocket.close()
                return
        new_room = Room(comd["name"])
        new_room.add(player_name)
        my_room = new_room
    elif comd["type"] == "join":
        for room in rooms:
            if room.name == comd["name"]:
                if len(room) == MAX_PLAYERS:
                    await websocket.send("010")
                    await websocket.close()
                    return
                room.add(player_name)
                my_room = room
                break
        else:  # если комнаты не существует
            await websocket.send("000")
            await websocket.close()
            return
    else:
        await websocket.send("Unknown command")
        await websocket.close()
        return
    # если все хорошо, ждем начала игры или начинаем ее сами
    await websocket.send("111")
    while True:
        if my_room.game:  # если игра уже началась
            break
        elif len(my_room) == MAX_PLAYERS:
            my_room.start_game()
            break
        # elif len(my_room) >= MIN_PLAYERS:
        #     pass  # todo: timer
        else:
            await asyncio.sleep(2)
    init_data = my_room.game.get_init_data(player_name)
    await websocket.send(init_data)


room_info_server = websockets.serve(rooms_info_request_handler, '127.0.0.1', 5678)
server = websockets.serve(handler, '127.0.0.1', 8765)


asyncio.get_event_loop().run_until_complete(room_info_server)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()