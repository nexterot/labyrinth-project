
var ipAddr = '37.139.2.176';
var portRoomInfo = 5678;

var portWebsockets = 8765;
var portHttp = 80;

// Сокет для общения с сервером.
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

        // Название комнаты.
        var colRoomName = document.createElement("TD");
        colRoomName.innerHTML = room;
        row.appendChild(colRoomName);

        // Список игроков.
        var colListOfPlayers = document.createElement("TD");
        for (var i = 0; i < data[room].length; i++) {
            colListOfPlayers.innerHTML += data[room] + " ";
        }
        row.appendChild(colListOfPlayers);

        // Кнопка "присоединиться".
        var buttonJoin = document.createElement("TD");
        var button = document.createElement("BUTTON");
        button.innerHTML = "Присоединиться";
        button.onclick = function() {
            setCookie("type", "join");
            setCookie("room_name", room);
            setCookie("equipment", "0_0_0");
            if (!webSocketOpen) {
                webSocket = new WebSocket('ws://' + ipAddr + ':' + portWebsockets);
                webSocketOpen = true;
                // Действия, выполняемые в начале общения сервера и клиента.
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

                // Действия, которые выполняет клиент при получении очередного сообщения от сервера.
                webSocket.onmessage = function(event) {
                    console.log("Текущие данные:" + event.data);
                    automate1(JSON.parse(event.data));
                };

                // Действия, выполняемые при завершении общения сервера и клиента.
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

// Создание кнопки.
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
            automate2(JSON.parse(event.data));
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
