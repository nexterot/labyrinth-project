//var ipAddress = '192.168.43.210';
var ipAddress = '0.0.0.0';
var port = '8765';

//var webSocket;

var my_name = getCookie("nickname");

var land;
var player;

/* ------------------------------------------------------------------ */
/* Кнопки */
var buttonKnife, buttonAid, buttonBomb, buttonConcrete;
/* ------------------------------------------------------------------ */

var canvasSizeX = 900;
var canvasSizeY = 650;
var spriteSize = 50;

var game;

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
/* Глобальная переменная - текущая координата */
var CURRENT_STATE = STATE_1__waiting_for_connection;

var fields = [];

var levelSizeX;
var levelSizeY;

/* ------------------------------------------------------------------ */

/* ------------------------------------------------------------------ */

////////////////////////////////////

/* send_coordinates() - функция, которая отправляет на сервер тип хода и его координаты */
function send_coordinates(type, x, y) {
    console.log(JSON.stringify([type, x, y]));
    webSocket.send(JSON.stringify([type, x, y]));
}

/* turn - функция, определяющая какой ход нужно отрисовать */
function turn(data) {
    switch (data.type_of_turn) {
        case "go": {
            draw_go(data);
            break;
        }
        case "knife": {
            draw_knife(data);
            break;
        }
        case "bomb": {
            draw_bomb(data);
            break;
        }
        case "concrete": {
            draw_concrete(data);
            break;
        }
        case "aid": {
            draw_aid(data);
            break;
        }
    }
}

function another_turn(data) {
    console.log("Ходит игрок с ником " + data.name);

}


function setCookie(cname, cvalue, exdays) {
    console.log(document.cookie);
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    console.log(document.cookie);
}

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

function delCookie(name) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
