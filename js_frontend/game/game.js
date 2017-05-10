var ipAddr = '0.0.0.0';
var portRoomInfo = 5678;

var portWebsockets = 8765;
var portHttp = 8080;

// сокет для общения с сервером
var webSocket;
var webSocketOpen = false;

var ws = new WebSocket('ws://' + ipAddr + ':' + portRoomInfo + '/');
ws.onmessage = function(event) {
    data = JSON.parse(event.data);
    var table = document.getElementById("rooms");
    var row;
    table.innerHTML = "<tr><td>Название комнаты</td><td>Список игроков</td><td>Присоединиться</td></tr>";
    for (var room in data) {
        row = document.createElement("TR");

        // название комнаты
        var colRoomName = document.createElement("TD");
        colRoomName.innerHTML = room;
        row.appendChild(colRoomName);

        // список игроков
        var colListOfPlayers = document.createElement("TD");
        for (var i = 0; i < data[room].length; i++) {
            colListOfPlayers.innerHTML += data[room] + " ";
        }
        row.appendChild(colListOfPlayers);

        // кнопка "присоединиться"
        var buttonJoin = document.createElement("TD");
        var button = document.createElement("BUTTON");
        button.innerHTML = "Присоединиться";
        button.onclick = function() {
            setCookie("type", "join");
            setCookie("room_name", room);
            setCookie("equipment", "0_0_0");
            if (!websocketOpen) {
                webSocket = new WebSocket('ws://' + ipAddr + ':' + portWebsockets);
                webSocketOpen = true;
                /* Действия, выполняемые в начале общения сервера и клиента */
                webSocket.onopen = function(event) {
                    webSocket.send(getCookie('nickname') + "=" + getCookie('hash'));
                    var equipment = getCookie("equipment").split('_');
                    for (var i = 0; i < equipment.length; i++) equipment[i] = parseInt(equipment[i]);
                    webSocket.send(JSON.stringify({
                        "type": getCookie("type"),
                        "name": getCookie("room_name"),
                        "equipment": equipment
                    }));
                };

                /* Действия, которые выполняет клиент при получении очередного сообщения от сервера */
                webSocket.onmessage = function(event) {
                    console.log("Текущие данные:" + event.data);
                    switch (CURRENT_STATE) {
                        case STATE_1__waiting_for_connection:
                            {
                                if (event.data == "111")
                                    CURRENT_STATE = STATE_2__waiting_for_game_start;
                                else {
                                    if (event.data[0] == '0')
                                        alert("Превышено количество комнат!\n          Подождите!");
                                    else if (event.data[1] == '0')
                                        alert("Комната с таким именем уже существует!\n     Придумайте другое название!");
                                    else if (event.data[2] == '0')
                                        alert("Что-то пошло не так...\nПопробуйте зайти в другой раз...");
                                    CURRENT_STATE = ERROR_EXIT;
                                }
                                webSocket.send("ready_to_start");
                                break;
                            }
                        case STATE_2__waiting_for_game_start:
                            {
                                ws.close()
                                document.body.innerHTML = '<div align="center" id="canvas"></div>';
                                game = new Phaser.Game(canvasSizeX, canvasSizeY, Phaser.CANVAS, 'canvas', {
                                    preload: preload
                                });
                                var data = JSON.parse(event.data);
                                var str = "Список игроков:\n";
                                for (var i = 0; i < data.list_of_players.length; i++)
                                    str += ((i + 1) + ") " + data.list_of_players[i] + ";\n");
                                levelSizeX = data.size[0];
                                levelSizeY = data.size[1];
                                create(levelSizeX, levelSizeY, data.place[0], data.place[1]);
                                alert(str);
                                CURRENT_STATE = STATE_4__sleep;
                                webSocket.send("map_build");
                                break;
                            }
                        case STATE_3__show_my_turn:
                            {
                                console.log("ВЫ В 3 СОСТОЯНИИ!!!");
                                turn(JSON.parse(event.data));
                                CURRENT_STATE = STATE_4__sleep;
                                console.log("ВЫ ВЫШЛИ ИЗ 3 СОСТОЯНИЯ!!!");
                                webSocket.send("turn_made");
                                break;
                            }
                        case STATE_4__sleep:
                            {
                                console.log("ВЫ В 4 СОСТОЯНИИ!!!");
                                console.log(event.data);
                                var data = JSON.parse(event.data);
                                if (data.type == "whose_turn") {
                                    if (data.name == my_name) {
                                        console.log("Мой ход");
                                        CURRENT_STATE = STATE_5__send_signal;
                                    } else {
                                        console.log("Не мой ход");
                                        CURRENT_STATE = STATE_6_show_another_turn;
                                    }
                                }
                                if (data.type == "final") {
                                    CURRENT_STATE = FINAL__somebody_win;
                                }
                                console.log("ВЫ ВЫШЛИ ИЗ 4 СОСТОЯНИЯ!!!");
                                webSocket.send("Проснулся");
                                break;
                            }
                        case STATE_6_show_another_turn:
                            {
                                console.log("Вы В 6 СОСТОЯНИИ!!!");
                                another_turn(JSON.parse(event.data));
                                console.log("Вы ВЫШЛИ ИЗ 6 СОСТОЯНИЯ!!!");
                                webSocket.send("Обработал чужой ход");
                            }
                        case FINAL__somebody_win:
                            {
                                var data = JSON.parse(event.data);
                                console.log("Победлитель: " + data.statistics[0]);
                                console.log("Приз: " + data.prize[0] + " бомб; " + data.prize[1] + " блоков цемента; " + data.prize[2] + " аптечек.");
                                console.log("Результаты: ");
                                for (var i = 0; i < data.statistics.length; i++) {
                                    console.log((i + 1) + " место: " + data.statistics[i]);
                                }
                                // draw
                                /* Выход из комнаты всех игроков */
                                webSocket.send("Закончил игру");
                                break;
                            }
                    }
                };

                /* Действия, выполняемые при завершении общения сервера и клиента */
                webSocket.onclose = function(event) {
                    console.log("НАЧАЛО ЗАКРЫТИЯ!!!");
                    if (CURRENT_STATE != FINAL__somebody_win) {
                        console.log("ОШИБКА!!!");
                    } else {
                        console.log("Игра успешно завершилась");
                        console.log("КОНЕЦ ЗАКРЫТИЯ!!!");
                        alert("Игра завершена!");
                        delCookie("room_name");
                        delCookie("type");
                        delCookie("equipment");
                        setTimeout('location="http://' + ipAddr + ':' + portHttp + '"', 3000);
                    }
                };
            }
        };
        buttonJoin.appendChild(button);
        row.appendChild(buttonJoin);
        table.appendChild(row);
    }
};

var create_button = document.getElementById("create_room");
create_button.onclick = function() {
    setCookie("type", "create");
    setCookie("room_name", document.getElementById("room_name").value);
    setCookie("equipment", "0_0_0");
    if (!webSocketOpen) {
        webSocket = new WebSocket('ws://' + ipAddr + ':' + portWebsockets);
        webSocketOpen = true;
        /* Действия, выполняемые в начале общения сервера и клиента */
        webSocket.onopen = function(event) {
            webSocket.send(getCookie('nickname') + "=" + getCookie('hash'));
            var equipment = getCookie("equipment").split('_');
            for (var i = 0; i < equipment.length; i++) equipment[i] = parseInt(equipment[i]);
            webSocket.send(JSON.stringify({
                "type": getCookie("type"),
                "name": getCookie("room_name"),
                "equipment": equipment
            }));
        };

        /* Действия, которые выполняет клиент при получении очередного сообщения от сервера */
        webSocket.onmessage = function(event) {
            console.log("Текущие данные:" + event.data);
            switch (CURRENT_STATE) {
                case STATE_1__waiting_for_connection:
                    {
                        if (event.data == "111")
                            CURRENT_STATE = STATE_2__waiting_for_game_start;
                        else {
                            if (event.data[0] == '0')
                                alert("Превышено количество комнат!\n          Подождите!");
                            else if (event.data[1] == '0')
                                alert("Комната с таким именем уже существует!\n     Придумайте другое название!");
                            else if (event.data[2] == '0')
                                alert("Что-то пошло не так...\nПопробуйте зайти в другой раз...");
                            CURRENT_STATE = ERROR_EXIT;
                        }
                        webSocket.send("ready_to_start");
                        break;
                    }
                case STATE_2__waiting_for_game_start:
                    {
                        ws.close();
                        document.body.innerHTML = '<div align="center" id="canvas"></div>';
                        game = new Phaser.Game(canvasSizeX, canvasSizeY, Phaser.CANVAS, 'canvas', {
                            preload: preload,
                            create: function() {
                                create(levelSizeX, levelSizeY, data.place[0], data.place[1]);
                            }
                        });
                        var data = JSON.parse(event.data);
                        var str = "Список игроков:\n";
                        for (var i = 0; i < data.list_of_players.length; i++)
                            str += ((i + 1) + ") " + data.list_of_players[i] + ";\n");
                        levelSizeX = data.size[0];
                        levelSizeY = data.size[1];

                        alert(str);
                        CURRENT_STATE = STATE_4__sleep;
                        webSocket.send("map_build");
                        break;
                    }
                case STATE_3__show_my_turn:
                    {
                        console.log("ВЫ В 3 СОСТОЯНИИ!!!");
                        turn(JSON.parse(event.data));
                        CURRENT_STATE = STATE_4__sleep;
                        console.log("ВЫ ВЫШЛИ ИЗ 3 СОСТОЯНИЯ!!!");
                        webSocket.send("turn_made");
                        break;
                    }
                case STATE_4__sleep:
                    {
                        console.log("ВЫ В 4 СОСТОЯНИИ!!!");
                        console.log(event.data);
                        var data = JSON.parse(event.data);
                        if (data.type == "whose_turn") {
                            if (data.name == my_name) {
                                console.log("Мой ход");
                                CURRENT_STATE = STATE_5__send_signal;
                            } else {
                                console.log("Не мой ход");
                                CURRENT_STATE = STATE_6_show_another_turn;
                            }
                        }
                        if (data.type == "final") {
                            CURRENT_STATE = FINAL__somebody_win;
                        }
                        console.log("ВЫ ВЫШЛИ ИЗ 4 СОСТОЯНИЯ!!!");
                        webSocket.send("Проснулся");
                        break;
                    }
                case STATE_6_show_another_turn:
                    {
                        console.log("Вы В 6 СОСТОЯНИИ!!!");
                        another_turn(JSON.parse(event.data));
                        console.log("Вы ВЫШЛИ ИЗ 6 СОСТОЯНИЯ!!!");
                        webSocket.send("Обработал чужой ход");
                    }

                case FINAL__somebody_win:
                    {
                        var data = JSON.parse(event.data);
                        console.log("Победлитель: " + data.statistics[0]);
                        console.log("Приз: " + data.prize[0] + " бомб; " + data.prize[1] + " блоков цемента; " + data.prize[2] + " аптечек.");
                        console.log("Результаты: ");
                        for (var i = 0; i < data.statistics.length; i++) {
                            console.log((i + 1) + " место: " + data.statistics[i]);
                        }
                        // draw
                        /* Выход из комнаты всех игроков */
                        webSocket.send("Закончил игру");
                        break;
                    }
            }
        };

        /* Действия, выполняемые при завершении общения сервера и клиента */
        webSocket.onclose = function(event) {
            console.log("НАЧАЛО ЗАКРЫТИЯ!!!");
            if (CURRENT_STATE != FINAL__somebody_win) {
                console.log("ОШИБКА!!!");
            } else {
                console.log("Игра успешно завершилась");
                console.log("КОНЕЦ ЗАКРЫТИЯ!!!");
                alert("Игра завершена!");
                delCookie("room_name");
                delCookie("type");
                delCookie("equipment");
                setTimeout('location="http://' + ipAddr + ':' + portHttp + '"', 3000);
            }
        };
    }
};

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}