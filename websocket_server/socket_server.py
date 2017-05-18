#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets

from server_tools import *
from game.game import Game


ip_addr = '0.0.0.0'
port_room_info = 5678
port_websockets = 8765


MIN_PLAYERS = 1
MAX_PLAYERS = 5
MAX_ROOMS = 5


waiting_rooms = []
running_rooms = []


class Room:
    """ класс представляющий собой комнату для игроков """
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.game = None
        self.max_players = None
        self.min_players = None

    def __len__(self):
        """ перегрузка метода __len__: получение количества игроков в комнате"""
        return len(self.players)

    def add(self, nickname, websocket):
        """ добавление игрока как словарь {имя_игрока: [веб-сокет, текущее время]} в атрибут self.players"""
        self.players[nickname] = [websocket, datetime.datetime.now()]

    def remove(self, nickname):
        """ удаления игрока из комнаты """
        if self.players.get(nickname):
            del self.players[nickname]
        else:
            logging.critical("Игрок {} не найден в комнате {}".format(nickname, self.name))

    def start_game(self):
        """ начинает игру """
        self.game = Game(self.players)
        self.game.initialize_level()
        running_rooms.append(self)
        waiting_rooms.remove(self)


class Client:
    def __init__(self, websocket):
        self.ws = websocket
        self.player = None

    async def recv(self):
        try:
            data = await self.ws.recv()
            msg = parse_json(data)
            if msg == "exit":
                raise websockets.ConnectionClosed
        except websockets.ConnectionClosed:
            self.disconnect()
            data = None
        return data

    async def send(self, data):
        try:
            await self.ws.send(data)
        except websockets.ConnectionClosed:
            logging.error("")
            self.disconnect()

    def disconnect(self):
        if self.player is not None:
            ...
            # todo delete player form room


async def rooms_info_handler(websocket, path):
    """ handler сервера на отдельном порту, который передает информацию о текущих комнатах """
    global waiting_rooms
    try:
        while True:
            dict_view = {room.name: [room.max_players] + list(room.players.keys()) for room in waiting_rooms}
            result = json.dumps(dict_view)
            await websocket.send(result)
            # logging.info("Информация о комнатах отправлена: {}".format(result))
            await asyncio.sleep(3)
    except websockets.ConnectionClosed:
        pass
        # logging.info("Перестаю посылать информацию о клиенте")


async def remove_hung():
    """ корутина, отключающая игроков по тайм-ауту; так же используется для закрытия "мертвых" сокетов """
    global waiting_rooms
    time_out = 300  # тайм-аут
    while True:
        now = datetime.datetime.now()
        for room in waiting_rooms + running_rooms:
            keys = list(room.players.keys())
            for player_name in keys:
                if not room:
                    break
                websocket, date_time = room.players[player_name]
                if (now - date_time).seconds > time_out:
                    logging.info("Игрок {} был отключен по тайм-ауту: {} секунд".format(player_name, time_out))
                    await websocket.close()
        await asyncio.sleep(20)


async def get_client_info(websocket):
    """ получение имени игрока и его уникального ключа """
    result = await websocket.recv()
    try:
        player_name, key = result.split("=")
    except ValueError:
        logging.critical("Неопознанный игрок (не установлены куки)")
        await websocket.close()
        return False
    return player_name, key


def update_uptime(room, player_name):
    """ обновляет время клиента, чтобы избежать отключения по тайм-ауту"""
    room.players[player_name][1] = datetime.datetime.now()


async def send_turn_to_enemies(player, packet):
    for pl in player.game.players:
        if player != pl:
            if packet["type_of_turn"] == "go":
                result = analyze_go_turn(pl, player, packet)
            elif packet["type_of_turn"] == "knife":
                result = analyze_knife_turn(pl, player, packet)
            elif packet["type_of_turn"] == "bomb":
                result = analyze_bomb_turn(pl, player, packet)
            elif packet["type_of_turn"] == "aid":
                result = analyze_aid_turn(pl, player, packet)
            elif packet["type_of_turn"] == "concrete":
                result = analyze_concrete_turn(pl, player, packet)
            else:
                result = None
                logging.critical("Неизвестный тип хода: {}".format(packet["type_of_turn"]))

            try:
                await pl.websocket.send(result)
                logging.info("Отправили игроку {} ход игрока {}: {}".format(pl.name, player.name, result))
            except websockets.ConnectionClosed:
                logging.error("Игрок {} отвалился при получении информации о ходе {}".format(pl.name, player.name))
                logging.critical("Реализовать удаление игрока из комнаты!")  # todo


async def inform_about_victory(game):
    for player in game.players:
        stats = game.get_statistics(player)
        try:
            await player.websocket.send(stats)
            logging.info("Игроку {} отправлен пакет: {}".format(player.name, stats))
        except websockets.ConnectionClosed:
            logging.error("Игрок {} отвалился при получении информации об итогах игры.".format(player.name))
            logging.critical("Реализовать удаление игрока из комнаты!")  # todo


async def server_handler(websocket, path):
    """ handler основного сервера """

    player_name = "[неизвестный]"
    player_room = None
    game = None
    try:
        """

        Подключение игрока к комнате

        """

        # получить имя игрока и его уникальный ключ
        player_name, key = await get_client_info(websocket)

        logging.info("Подключился игрок {}[{}]".format(player_name, key))

        # получаем сообщение-запрос (создать-присоединиться) от игрока
        request = await websocket.recv()
        request = parse_json(request)
        logging.info("Игрок {}: {}".format(player_name, request))

        # если пришел сигнал создать комнату
        # todo: возвращать ошибку, если игрок уже создал комнату
        if request["type"] == "create":
            if len(waiting_rooms + running_rooms) >= MAX_ROOMS:  # ошибка: слишком много комнат!
                logging.error("Игрок {} не смог создать комнату: их слишком много".format(player_name))
                await close_reason(websocket, TOO_MANY_ROOMS)
            for room in waiting_rooms + running_rooms:
                if room.name == request["name"]:  # ошибка: такая комната уже существует!
                    logging.error(
                        "Игрок {} не смог создать комнату {}: она уже существует".format(player_name, request["name"]))
                    await close_reason(websocket, ROOM_ALREADY_EXISTS)

            if int(request["num_players"]) < MIN_PLAYERS:
                logging.critical("Заданное количество игроков ({}) меньше допустимого: {}".format(request["num_players"],
                                                                                                  MIN_PLAYERS))
                await close_reason(websocket, "too small players number")

            elif int(request["num_players"]) > MAX_PLAYERS:
                logging.critical(
                    "Заданное количество игроков ({}) больше допустимого: {}".format(request["num_players"],
                                                                                     MIN_PLAYERS))
                await close_reason(websocket, "too big players number")

            # иначе все хорошо; создаем комнату
            new_room = Room(request["name"])

            new_room.max_players = int(request["num_players"])

            # добавить в rooms пару {имя_игрока:вебсокет}
            new_room.add(player_name, websocket)
            player_room = new_room
            waiting_rooms.append(player_room)
            logging.info("Игрок {} создал комнату {}".format(player_name, player_room.name))

        # если пришел сигнал присоединиться к существующей комнате
        elif request["type"] == "join":
            for room in waiting_rooms:
                if room.name == request["name"]:  # находим комнату с нужным именем
                    if len(room) == room.max_players:  # упс, она уже заполнена :(
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
            elif len(player_room) == player_room.max_players:  # если количество игроков достигло максимума создаем игру
                player_room.start_game()
                logging.info("Игрок {}({}): создал игру".format(player_name, player_room.name))
                break
            # в будущем - активировать таймер при минимальном количестве игроков
            # todo: timer
            # elif len(my_room) >= room.min_players:
            #     pass
            else:  # иначе ждать начала игры
                logging.info("Игрок {}({}): жду начала игры".format(player_name, player_room.name))
                await asyncio.sleep(1)

        """

        Запуск игры

        """
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

        # отправляем начальные данные:
        # {"list_of_players":[name1, ..., nameN], "size":[x, y], "place":[x, y], "equipment":[3 elements]}
        init_data = game.get_init_data(player_name)
        await websocket.send(init_data)
        logging.info("Игрок {}({}) отправил клиенту данные: {}".format(player_name, player_room.name, init_data))

        # ждать, чтобы клиент успел отрисовать
        response = await websocket.recv()
        logging.info("Игрок {} прислал {}".format(player_name, response))

        update_uptime(player_room, player_name)

        """

        Основной игровой цикл

        """
        while not game.ended:
            # рассылаем имя игрока, который ходит
            response = json.dumps({"type": "whose_turn", "name": game.active_player.name})

            logging.info("Уведомляем игрока {}({}), о том, что ходит игрок {}".format(
                player_name,
                player_room.name,
                game.active_player.name
            ))
            await websocket.send(response)

            # ждать, чтобы клиент успел отрисовать
            message = await websocket.recv()
            logging.info("Игрок {} прислал {}".format(player_name, message))

            # если ходит текущий игрок
            if player == game.active_player:

                # получить данные об очередном ходе
                turn = await websocket.recv()
                turn = parse_json(turn)
                logging.info("Получен пакет от {}({}): {}".format(player_name, player_room.name, turn))
                was_error, result = await game.accept(player, turn)  # передать игре
                json_result = json.dumps(result)

                # если возвращается ошибка, отправить ее, inform players, и ждать новых данных о ходе
                while was_error:
                    logging.info("ошибка; отправляю игроку {}({}): {}".format(player_name, player_room.name, json_result))
                    await websocket.send(json_result)

                    # ждать, чтобы клиент успел отрисовать
                    response = await websocket.recv()
                    logging.info("Игрок {} прислал {}".format(player_name, response))

                    # inform player
                    response = json.dumps({"type": "whose_turn", "name": game.active_player.name})

                    logging.info("Уведомляем игрока {}({}), о том, что ходит игрок {}".format(
                        player_name,
                        player_room.name,
                        game.active_player.name
                    ))
                    await websocket.send(response)

                    # ждать, чтобы клиент успел отрисовать
                    message = await websocket.recv()
                    logging.info("Игрок {} прислал {}".format(player_name, message))

                    # получить данные об очередном ходе
                    turn = await websocket.recv()
                    turn = parse_json(turn)
                    logging.info("Получен пакет от {}({}): {}".format(player_name, player_room.name, turn))
                    was_error, result = await game.accept(player, turn)
                    json_result = json.dumps(result)

                # в случае успеха отправить клиенту пакет
                logging.info("успех; отправляю игроку {}({}): {}".format(player_name, player_room.name, json_result))
                await websocket.send(json_result)

                # ждать, чтобы клиент успел отрисовать
                response = await websocket.recv()
                logging.info("Игрок {} прислал {}".format(player_name, response))

                # разослать врагам то, что они увидят
                if result["type"] == "turn":
                    await send_turn_to_enemies(player, result)

                    # если выиграл
                    if result["type_of_turn"] == "go" and result["exit"][1] == 1:
                        logging.info("Игрок {} выиграл!".format(player_name))
                        game.ended = True
                        await inform_about_victory(game)
                        break

                update_uptime(player_room, player_name)

            # если же ход другого игрока
            else:
                logging.info("Игрок {}({}): сейчас ходит {}, жду своего хода".format(player_name, player_room.name,
                                                                                      game.active_player.name))
                response = await websocket.recv()
                logging.info("Игрок {} отрисовал ход врага: {}".format(player_name, response))
                await asyncio.sleep(0.2)

    except websockets.ConnectionClosed:
        logging.critical("Игрок {} отвалился".format(player_name))
        if player_room:
            player_room.remove(player_name)
            if len(player_room) == 0:
                logging.info("Не осталось игроков. Комната {} была удалена".format(player_room.name))
                running_rooms.remove(player_room)
                if game is not None:
                    game.next_player()
    else:
        player_room.remove(player_name)
        if len(player_room) == 0:
            logging.info("Не осталось игроков. Комната {} была удалена".format(player_room.name))
            running_rooms.remove(player_room)


def main():
    # логирование
    logging.basicConfig(
        format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
        level=logging.INFO,
        filename="server.log"
    )

    # открыть веб-сокет для сервера
    room_info_server = websockets.serve(rooms_info_handler, ip_addr, port_room_info)

    # открыть веб-сокет для выдачи информации о свободных комнатах
    server = websockets.serve(server_handler, ip_addr, port_websockets)

    # добавить handler'ы в основной цикл asyncio
    asyncio.get_event_loop().run_until_complete(room_info_server)
    asyncio.get_event_loop().run_until_complete(server)

    # добавить Task: отключать по тайм-ауту в 5 минут
    task = asyncio.Task(remove_hung())
    asyncio.get_event_loop().run_until_complete(task)

    print("Сервер запущен на {0}:{1} и {0}:{2}".format(ip_addr, port_websockets, port_room_info))

    # запустить цикл
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.info("Выключение сервера")


if __name__ == "__main__":
    main()
