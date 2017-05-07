#!/usr/bin/env python

import asyncio
import websockets
import json

from websocket_server.game import Game

MIN_PLAYERS = 1
MAX_PLAYERS = 1
MAX_ROOMS = 5

TOO_MANY_ROOMS = "000"
ROOM_ALREADY_EXISTS = "100"
NO_SUCH_ROOM = "000"
ROOM_FILLED = "010"
SUCCESS = "111"

rooms = []
games = []


async def rooms_info_request_handler(websocket, path):
    global rooms
    while True:
        dict_view = {room.name : list(room.players.keys()) for room in rooms}
        result = json.dumps(dict_view)
        await websocket.send(result)
        await asyncio.sleep(2)
        print("Sent rooms info")


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
    # получить имя игрока и его уникальный ключ
    result = await websocket.recv()
    try:
        player_name, key = result.split("=")
    except ValueError:  # не установлены куки!
        print("Неопознанный игрок!")
        await websocket.close()
        return

    print("Подключился игрок {}[{}]".format(player_name, key))

    # получаем сообщение-команду от игрока
    command_json = await websocket.recv()
    comd = json.loads(command_json)  # parse json
    print("Игрок {}:".format(player_name), comd)

    my_room = None

    # если пришел сигнал создать комнату
    if comd["type"] == "create":
        if len(rooms) >= MAX_ROOMS:  # ошибка: слишком много комнат!
            print("Игрок {} не смог создать комнату: их слишком много".format(player_name))
            await websocket.send(TOO_MANY_ROOMS)
            await websocket.close()
            return
        for room in rooms:
            if room.name == comd["name"]:  # ошибка: такая комната уже существует!
                print("Игрок {} не смог создать комнату {}: она уже существует".format(player_name, comd["name"]))
                await websocket.send(ROOM_ALREADY_EXISTS)
                await websocket.close()
                return
        # иначе все хорошо; создаем комнату
        new_room = Room(comd["name"])
        new_room.add(player_name)
        my_room = new_room
        rooms.append(my_room)
        print("Игрок {} создал комнату {}".format(player_name, my_room.name))

    # если пришел сигнал присоединиться к существующей комнате
    elif comd["type"] == "join":
        for room in rooms:
            if room.name == comd["name"]:  # находим комнату с нужным именем
                if len(room) == MAX_PLAYERS:  # упс, она уже заполнена :(
                    print("Игрок {} не смог присоединиться к комнате {}: она уже заполнена")
                    await websocket.send(ROOM_FILLED)
                    await websocket.close()
                    return
                # иначе все ОК, добавляем игрока в комнату
                room.add(player_name)
                my_room = room
                print("Игрок {} присодинился к комнате {}".format(player_name, comd["name"]))
                break
        else:
            # если комнаты не существует
            print("Игрок {} не смог присоединиться к несуществующей комнате {}".format(player_name, comd["name"]))
            await websocket.send(NO_SUCH_ROOM)
            await websocket.close()
            return
    else:  # этого быть не должно
        print("Неизвестная команда {}. Закрываю соединение...".format(comd["type"]))
        await websocket.close()
        return

    # всё идет по плану
    await websocket.send(SUCCESS)
    print("Игрок {}({}): оповещаю клиент об успехе".format(player_name, my_room.name))

    # ждем начала игры или начинаем ее сами
    while True:
        if my_room.game:  # если игра уже началась
            print("Игрок {}({}): игра уже началась, вхожу".format(player_name, my_room.name))
            break
        elif len(my_room) == MAX_PLAYERS:  # если количество игроков достигло максимума, создаем игру
            my_room.start_game()
            print("Игрок {}({}): создал игру".format(player_name, my_room.name))
            break
        # в будущем - активировать таймер при минимальном количестве игроков
        # todo: timer
        # elif len(my_room) >= MIN_PLAYERS:
        #     pass
        else:  # иначе ждать начала игры
            print("Игрок {}({}): жду начала игры".format(player_name, my_room.name))
            await asyncio.sleep(1)

    game = my_room.game

    # находим объект игрока по его нику
    player = None
    for pl in game.players:
        if player_name == pl.name:
            player = pl
            break
    else:  # такого быть не должно
        print("Объект игрока с именем {} не найден!!! PANIC".format(player_name))
        await websocket.close()
        return

    # заполняем инвентарь игрока
    player.inventory = comd["equipment"]

    # отправляем начальные данные: {"list_of_players":[name1, ..., nameN], "place":[x, y], "equipment":[3 elements]}
    init_data = game.get_init_data(player_name)
    await websocket.send(init_data)
    print("Игрок {}({}) отправил клиенту данные: {}".format(player_name, my_room.name, init_data))

    # основной игровой цикл
    while True:
        # рассылаем имя игрока, который ходит todo возможно не все игроки получат эту информацию!
        response = json.dumps({"whose_turn": game.active_player.name})
        print("Уведомляем игрока {}({}), что ходит игрок {}".format(player_name, my_room.name, game.active_player.name))
        await websocket.send(response)

        # переключаем контекст на активного игрока
        while player != game.active_player:
            print("Игрок {}({}): сейчас ходит {}, жду своего хода".format(player_name, my_room.name, game.active_player))
            await asyncio.sleep(0.1)

        turn = await websocket.recv()                  # получить данные об очередном ходе
        turn = json.loads(turn)                        # и распарсить json
        print("Получен пакет от {}({}): {}".format(player_name, my_room.name, turn))
        was_error, result = game.accept(player, turn)  # передать игре

        # если возвращается ошибка, отправить ее и ждать новых данных о ходе
        while was_error:
            print("ошибка; отправляю игроку {}({}): {}".format(player_name, my_room.name, result))
            await websocket.send(result)
            turn = await websocket.recv()
            turn = json.loads(turn)
            print("Получен пакет от {}({}): {}".format(player_name, my_room.name, turn))
            was_error, result = game.accept(player, turn)

        # в случае успеха отправить клиенту пакет
        print("успех; отправляю игроку {}({}): {}".format(player_name, my_room.name, result))
        await websocket.send(result)


# открыть веб-сокет для сервера
room_info_server = websockets.serve(rooms_info_request_handler, '0.0.0.0', 5678)

# открыть веб-сокет для выдачи информации о свободных комнатах
server = websockets.serve(handler, '0.0.0.0', 8765)

# добавить handler'ы в основной цикл asyncio
asyncio.get_event_loop().run_until_complete(room_info_server)
asyncio.get_event_loop().run_until_complete(server)

# запустить цикл
asyncio.get_event_loop().run_forever()