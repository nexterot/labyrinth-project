// отредактировал.

//var ipAddress = '192.168.43.210';
//var webSocket;

// Где стартует игра:
var ipAddress = '0.0.0.0';
var port = '8765';

var my_name = getCookie("nickname");

// JS-фронтэнд представляет из себя конечный автомат
// с 10 состояними. 
var STATE_1__waiting_for_connection = 1;
var STATE_2__waiting_for_game_start = 2;
var STATE_3__show_my_turn = 3;
var STATE_4__sleep = 4;
var STATE_5__send_signal = 5;
var STATE_6_show_another_turn = 6;
var STATE_7_bomb = 7;
var STATE_8_concrete = 8;
var FINAL__somebody_win = 0;
var ERROR_EXIT = -1;

// текущее состояние.
var CURRENT_STATE = STATE_1__waiting_for_connection;

// send_coordinates(type, x, y) - функция, отправляющая информацию
// об очередном ходе игрока.
function send_coordinates(type, x, y) {
    console.log(JSON.stringify([type, x, y]));
    webSocket.send(JSON.stringify([type, x, y]));
}

// turn(data) - функция, отвечающая за отрисовку хода
// текущего игрока.
function turn(data) {
    switch (data.type_of_turn) {
        case "go": {
            drawGo(data);
            break;
        }
        case "knife": {
            drawKnife(data);
            break;
        }
        case "bomb": {
            drawBomb(data);
            break;
        }
        case "concrete": {
            drawConcrete(data);
            break;
        }
        case "aid": {
            drawAid(data);
            break;
        }
    }
}

// another_turn(data) - функция, отвечающая за отрисовку хода
// другого игрока.
function another_turn(data) {
    console.log("Ходит игрок с ником " + data.name);

}

// Установка куки.
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// Получение куки.
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
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

// Удаление куки.
function delCookie(name) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
