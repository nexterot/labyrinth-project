#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets

from server_tools import *
from game.game import Game

MIN_PLAYERS = 1
MAX_PLAYERS = 1
MAX_ROOMS = 5

rooms = []
games = []


class Room:
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.game = None

    def __len__(self):
        return len(self.players)

    def add(self, nickname, websocket):
        self.players[nickname] = websocket

    def remove(self, nickname):
        if self.players.get(nickname):
            del self.players[nickname]
        else:
            logging.error("Игрок {} не найден в комнате {}".format(nickname, self.name))

    def start_game(self):
        self.game = Game(self.players.keys())


async def rooms_info_handler(websocket, path):
    global rooms
    try:
        while True:
            dict_view = {room.name: list(room.players.keys()) for room in rooms}
            result = json.dumps(dict_view)
            await websocket.send(result)
            logging.info("Информация о комнатах отправлена: {}".format(result))
            await asyncio.sleep(5)
    except websockets.ConnectionClosed:
        logging.info("Перестаю посылать информацию о клиенте")


async def get_client_info(websocket):
    # получить имя игрока и его уникальный ключ
    result = await websocket.recv()
    try:
        player_name, key = result.split("=")
    except ValueError:  # не установлены куки!
        logging.critical("Неопознанный игрок (не установлены куки)")
        await websocket.close()
        return False
    return player_name, key


async def server_handler(websocket, path):
    player_name = "[неизвестный]"
    player_room = None
    try:
        # получить имя игрока и его уникальный ключ
        player_name, key = await get_client_info(websocket)

        logging.info("Подключился игрок {}[{}]".format(player_name, key))

        # получаем сообщение-запрос (создать-присоединиться) от игрока
        request = await websocket.recv()
        request = parse_json(request)
        logging.info("Игрок {}: {}".format(player_name, request))

        # если пришел сигнал создать комнату
        if request["type"] == "create":
            if len(rooms) >= MAX_ROOMS:  # ошибка: слишком много комнат!
                logging.error("Игрок {} не смог создать комнату: их слишком много".format(player_name))
                await close_reason(websocket, TOO_MANY_ROOMS)
            for room in rooms:
                if room.name == request["name"]:  # ошибка: такая комната уже существует!
                    logging.error(
                        "Игрок {} не смог создать комнату {}: она уже существует".format(player_name, request["name"]))
                    await close_reason(websocket, ROOM_ALREADY_EXISTS)
            # иначе все хорошо; создаем комнату
            new_room = Room(request["name"])
            # добавить в rooms пару {имя_игрока:вебсокет}
            new_room.add(player_name, websocket)
            player_room = new_room
            rooms.append(player_room)
            logging.info("Игрок {} создал комнату {}".format(player_name, player_room.name))

        # если пришел сигнал присоединиться к существующей комнате
        elif request["type"] == "join":
            for room in rooms:
                if room.name == request["name"]:  # находим комнату с нужным именем
                    if len(room) == MAX_PLAYERS:  # упс, она уже заполнена :(
                        logging.error(
                            "Игрок {} не смог присоединиться к комнате {}: она уже заполнена".format(player_name,
                                                                                                     room.name))
                        await close_reason(websocket, ROOM_FILLED)
                    # иначе все ОК, добавляем игрока в комнату
                    room.add(player_name, websocket)
                    player_room = room
                    logging.info("Игрок {} присодинился к комнате {}".format(player_name, request["name"]))
                    break
            else:
                # если комнаты не существует
                logging.error(
                    "Игрок {} не смог присоединиться к несуществующей комнате {}".format(player_name, request["name"]))
                await close_reason(websocket, NO_SUCH_ROOM)
        else:  # этого быть не должно
            logging.critical("Неизвестная команда {}. Закрываю соединение...".format(request["type"]))
            await websocket.close()

        # всё идет по плану
        await websocket.send(SUCCESS)
        logging.info("Игрок {}({}): оповещаю клиент об успехе".format(player_name, player_room.name))

        # ждем сообщения от клиента
        message = await websocket.recv()
        logging.info("Игрок {} прислал {}".format(player_name, message))

        # ждем начала игры или начинаем ее сами
        while True:
            if player_room.game:  # если игра уже началась
                logging.info("Игрок {}({}): игра уже началась, вхожу".format(player_name, player_room.name))
                break
            elif len(player_room) == MAX_PLAYERS:  # если количество игроков достигло максимума, создаем игру
                player_room.start_game()
                logging.info("Игрок {}({}): создал игру".format(player_name, player_room.name))
                break
            # в будущем - активировать таймер при минимальном количестве игроков
            # todo: timer
            # elif len(my_room) >= MIN_PLAYERS:
            #     pass
            else:  # иначе ждать начала игры
                logging.info("Игрок {}({}): жду начала игры".format(player_name, player_room.name))
                await asyncio.sleep(1)

        game = player_room.game

        # находим объект игрока по его нику
        player = None
        for pl in game.players:
            if player_name == pl.name:
                player = pl
                break
        else:  # такого быть не должно
            logging.error("Объект игрока с именем {} не найден!!! PANIC".format(player_name))
            await websocket.close()


        # заполняем инвентарь игрока
        player.inventory = request["equipment"]

        # await asyncio.sleep(5)

        # отправляем начальные данные:
        # {"list_of_players":[name1, ..., nameN], "size":[x, y], "place":[x, y], "equipment":[3 elements]}
        init_data = game.get_init_data(player_name)
        await websocket.send(init_data)
        logging.info("Игрок {}({}) отправил клиенту данные: {}".format(player_name, player_room.name, init_data))

        # await asyncio.sleep(5)

        # ждать, чтобы клиент успел отрисовать
        response = await websocket.recv()
        logging.info("Игрок {} прислал {}".format(player_name, response))

        # основной игровой цикл
        while True:
            # рассылаем имя игрока, который ходит
            name_active_player = json.dumps({"type": "whose_turn", "name": game.active_player.name})
            await inform_whose_turn(player_name, player_room, game.active_player.name, name_active_player)

            # переключаем контекст на активного игрока
            while player != game.active_player:
                logging.info("Игрок {}({}): сейчас ходит {}, жду своего хода".format(player_name, player_room.name,
                                                                                     game.active_player))
                await asyncio.sleep(0.1)

            # получить данные об очередном ходе
            turn = await websocket.recv()
            turn = parse_json(turn)
            logging.info("Получен пакет от {}({}): {}".format(player_name, player_room.name, turn))
            was_error, result = game.accept(player, turn)  # передать игре

            json_result = json.dumps(result)

            # если возвращается ошибка, отправить ее, inform players, и ждать новых данных о ходе
            while was_error:
                logging.info("ошибка; отправляю игроку {}({}): {}".format(player_name, player_room.name, json_result))
                await websocket.send(json_result)

                # ждать, чтобы клиент успел отрисовать
                response = await websocket.recv()
                logging.info("Игрок {} прислал {}".format(player_name, response))

                # inform player
                await inform_whose_turn(player_name, player_room, game.active_player.name, name_active_player)

                # receive turn info
                turn = await websocket.recv()
                turn = parse_json(turn)
                logging.info("Получен пакет от {}({}): {}".format(player_name, player_room.name, turn))
                was_error, result = game.accept(player, turn)
                json_result = json.dumps(result)

            # в случае успеха отправить клиенту пакет
            logging.info("успех; отправляю игроку {}({}): {}".format(player_name, player_room.name, json_result))
            await websocket.send(json_result)

            # ждать, чтобы клиент успел отрисовать
            response = await websocket.recv()
            logging.info("Игрок {} прислал {}".format(player_name, json.dumps(response)))

            # если выиграл todo разослать всем игрокам, завершить игру
            if result["exit"][1] == 1:
                final_result = game.get_statistics(player_name)
                logging.info("Игрок {} выиграл!".format(player_name))
                logging.info("Посылаем игроку {} {}".format(player_name, final_result))
                await websocket.send(json.dumps(final_result))
                break

    except websockets.ConnectionClosed:
        logging.critical("Игрок {} отвалился".format(player_name))
        if player_room:
            player_room.remove(player_name)
            if len(player_room) == 0:
                logging.info("Не осталось игроков. Комната {} была удалена".format(player_room.name))
                rooms.remove(player_room)
    else:
        player_room.remove(player_name)
        if len(player_room) == 0:
            logging.info("Не осталось игроков. Комната {} была удалена".format(player_room.name))
            rooms.remove(player_room)


def main():
    # логирование
    logging.basicConfig(
        format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
        level=logging.INFO,
        # filename="server.log"
    )

    # открыть веб-сокет для сервера
    room_info_server = websockets.serve(rooms_info_handler, '0.0.0.0', 5678)

    # открыть веб-сокет для выдачи информации о свободных комнатах
    server = websockets.serve(server_handler, '0.0.0.0', 8765)

    # добавить handler'ы в основной цикл asyncio
    asyncio.get_event_loop().run_until_complete(room_info_server)
    asyncio.get_event_loop().run_until_complete(server)

    # запустить цикл
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server on Ctrl+C")


if __name__ == "__main__":
    main()
