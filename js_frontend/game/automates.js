
// Функции, реализующие работу конечного автомата.
function automate1(data) {
    switch (CURRENT_STATE) {
        case STATE_1__waiting_for_connection: {
            STATE_1_func(data);
            break;
        }
        case STATE_2__waiting_for_game_start: {
            ws.close()
            document.body.innerHTML = '<div align="center" id="canvas"></div>';
            levelSizeX = data.size[0];
            levelSizeY = data.size[1];
            game = new Phaser.Game(canvasSizeX, canvasSizeY, Phaser.CANVAS, 'canvas', { preload: preload,
                create: function(){ create(levelSizeX, levelSizeY, data.place[0], data.place[1]); }});
            var str = "Список игроков:\n";
            for (var i = 0; i < data.list_of_players.length; i++)
                str += ((i + 1) + ") " + data.list_of_players[i] + ";\n");
            alert(str);
            CURRENT_STATE = STATE_4__sleep;
            webSocket.send("map_build");
            break;
        }
        case STATE_3__show_my_turn: {
            STATE_3_func(data);
            break;
        }
        case STATE_4__sleep: {
            STATE_4_func(data);
            break;
        }
        case STATE_6_show_another_turn: {
            STATE_6_func(data);
            break;
        }
        case FINAL__somebody_win: {
            FINAL_func(data);
            break;
        }
    }
}

function automate2(data) {
    switch (CURRENT_STATE) {
        case STATE_1__waiting_for_connection: {
            STATE_1_func(data);
            break;
        }
        case STATE_2__waiting_for_game_start: {
            ws.close();
            document.body.innerHTML = '<div align="center" id="canvas"></div>';
            game = new Phaser.Game(canvasSizeX, canvasSizeY, Phaser.CANVAS, 'canvas', { preload: preload,
                create: function() { create(levelSizeX, levelSizeY, data.place[0], data.place[1]); }});
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
        case STATE_3__show_my_turn: {
            STATE_3_func(data);
            break;
        }
        case STATE_4__sleep: {
            STATE_4_func(data);
            break;
        }
        case STATE_6_show_another_turn: {
            STATE_6_func(data);
            break;
        }
        case FINAL__somebody_win: {
            FINAL_func(data);
            break;
        }
    }
}

function STATE_1_func(data) {
    if (data == "111")
        CURRENT_STATE = STATE_2__waiting_for_game_start;
    else {
        if (data[0] == '0')
            alert("Превышено количество комнат!\n          Подождите!");
        else if (data[1] == '0')
            alert("Комната с таким именем уже существует!\n     Придумайте другое название!");
        else if (data[2] == '0')
            alert("Что-то пошло не так...\nПопробуйте зайти в другой раз...");
        CURRENT_STATE = ERROR_EXIT;
    }
    webSocket.send("ready_to_start");
}

function STATE_3_func(data) {
    console.log("ВЫ В 3 СОСТОЯНИИ!!!");
    turn(data);
    CURRENT_STATE = STATE_4__sleep;
    console.log("ВЫ ВЫШЛИ ИЗ 3 СОСТОЯНИЯ!!!");
    webSocket.send("turn_made");
}

function STATE_4_func(data) {
    console.log("ВЫ В 4 СОСТОЯНИИ!!!");
    console.log(data);
    if (data.type == "whose_turn") {
        if (data.name == my_name) {
            console.log("Мой ход");
            CURRENT_STATE = STATE_5__send_signal;
            webSocket.send("мой ход!");
        } else {
            console.log("Не мой ход");
            CURRENT_STATE = STATE_6_show_another_turn;
            webSocket.send("не мой ход.");
        }
    }
    if (data.type == "final") {
        CURRENT_STATE = FINAL__somebody_win;
    }
    console.log("ВЫ ВЫШЛИ ИЗ 4 СОСТОЯНИЯ!!!");
}

function STATE_6_func(data) {
    console.log("Вы В 6 СОСТОЯНИИ!!!");
    another_turn(data);
    console.log("Вы ВЫШЛИ ИЗ 6 СОСТОЯНИЯ!!!");
    webSocket.send("Обработал чужой ход");
    CURRENT_STATE = STATE_4__sleep;
}

function FINAL_func(data) {
    alert("Победлитель: " + data.statistics[0]);
    alert("Приз: " + data.prize[0] + " бомб; " + data.prize[1] + " блоков цемента; " + data.prize[2] + " аптечек.");
    console.log("Результаты: ");
    for (var i = 0; i < data.statistics.length; i++) {
        console.log((i + 1) + " место: " + data.statistics[i]);
    }
    // draw
    /* Выход из комнаты всех игроков */
    webSocket.send("Закончил игру");
}
