// отредактировал.

// Игра.
var game;

// Переменные, регулирующие
// отображение игры.
var canvasSizeX = 900;
var canvasSizeY = 650;
var spriteSize = 50;

// Переменные, регулирующие 
// игровой мир.
var player;
var playerAnother;

var land;
var levelSizeX;
var levelSizeY;

var fields = [];

var healthScale;

var styleKnife;
var styleOther;

var buttonKnife;
var numberKnife;

var buttonAid;
var numberAid;

var buttonBomb;
var numberBomb;

var buttonConcrete;
var numberConcrete;

var buttonExit;

// Переменные звуков.
var bombBlastedSound;
var bombPlantedSound;
var concreteSound;
var intoWallSound;
var knifeSound;
var metroSound;
var touchSound;
var waterSound;
var treasureSound;

// Функция preload загружает в игру спрайты и звуки.
function preload() {
    var path = "http://37.139.2.176:8000/game/", path;
    
    // Загрузка изображений.
    path1 = path + "sprites/interface/";
    game.load.image("background", path1 + "background.png");
    game.load.image("playerFaceWait", path1 + "player_face_wait.png");
    game.load.image("playerFaceGo", path1 + "player_face_go.png");
    game.load.image("buttonKnife", path1 + "buttons/knifeButton.png");
    game.load.image("buttonBomb", path1 + "buttons/bombButton.png");
    game.load.image("buttonAid", path1 + "buttons/aidButton.png");
    game.load.image("buttonConcrete", path1 + "buttons/concreteButton.png");
    game.load.image("health100", path1 + "health/health100.png");
    game.load.image("health75", path1 + "health/health75.png");
    game.load.image("health50", path1 + "health/health50.png");
    game.load.image("health25", path1 + "health/health25.png");
    game.load.image("health0", path1 + "health/health0.png");
    game.load.image("panel", path1 + "panel.png");
    game.load.image("buttonExit", path1 + "buttons/exitButton.png");
    
    path1 = path + "sprites/world/";
    game.load.image("fog", path1 + "fog.png");
    game.load.image("sand", path1 + "sand.png");
    game.load.image("wall", path1 + "wall.png");
    game.load.image("water", path1 + "water.png");
    
    path1 = path + "sprites/possession/";
    game.load.image("aid", path1 + "aid.png");
    game.load.image("arm", path1 + "arm.png");
    game.load.image("backpack", path1 + "backpack.png");
    game.load.image("bomb", path1 + "bomb.png");
    game.load.image("concrete", path1 + "concrete.png");
    game.load.image("metro", path1 + "metro.png");
    game.load.image("treasure", path1 + "treasure.png");
    
    path1 = path + "sprites/player/";
    game.load.image("player_bang", path1 + "player_bang.png");
    game.load.image("player_died", path1 + "player_died.png");
    game.load.image("player_injured", path1 + "player_injured.png");
    game.load.image("player_stay", path1 + "player_stay.png");
    game.load.image("player_use_aid", path1 + "player_use_aid.png");
    game.load.image("player_use_bomb_concrete", path1 + "player_use_bomb_concrete.png");
    game.load.image("player_use_knife", path1 + "player_use_knife.png");
    game.load.image("player_ghost", path1 + "player_ghost.png");
    
    // Загрузка звуков.
    path1 = path + "sounds/ogg/";
    var type = ".ogg"
    bombBlastedSound = new Audio(path1 + "bomb_blasted" + type);
    bombPlantedSound = new Audio(path1 + "bomb_planted" + type);
    concreteSound = new Audio(path1 + "concrete" + type);
    intoWallSound = new Audio(path1 + "intoTheWall" + type);
    knifeSound = new Audio(path1 + "knife" + type);
    metroSound = new Audio(path1 + "metro" + type);
    touchSound = new Audio(path1 + "touch" + type);
    waterSound = new Audio(path1 + "water" + type);
    treasureSound = new Audio(path1 + "treasure" + type);
}

// Функция create инициализирует игру: отрисовывает интерфейс и карту.
function create(levelSizeX, levelSizeY, playerX, playerY) {
    /* Отрисовка интерфейса */
    land = game.add.sprite(0, 0, "background");
    land.sendToBack();
    
    var panel = game.add.sprite(25, 25, "panel");
    var playerFace = game.add.sprite(37, 62, "playerFaceWait");
    healthScale = new HealthScale(37, 270);
    
    styleKnife = { font: "32px"};
    styleOther = { font: "20px"};
    
    buttonKnife = new buttonKnifeClass(37, 325);
    numberKnife = game.add.text(47, 320, "∞", styleKnife);
    
    buttonBomb = new buttonBombClass(141, 325);
    numberBomb = game.add.text(153, 329, " 0", styleOther);
    
    buttonAid = new buttonAidClass(37, 430);
    numberAid = game.add.text(49, 434, " 0", styleOther);
    
    buttonConcrete = new buttonConcreteClass(141, 430);
    numberConcrete = game.add.text(153, 434, " 0", styleOther);
    buttonExit = new buttonExitClass(37, 534);
    
    /* Отрисовка карты */
    fields = [];
    for (var i = 0; i < levelSizeX; i++)
        fields.push([]);
    for (var row = 0; row < levelSizeX; row++)
        for (var col = 0; col < levelSizeY; col++)
            fields[row].push(new Field(275 + col * spriteSize, 25 + row * spriteSize, [row, col]));
    fields[playerX][playerY].changeSprite(275 + playerY * spriteSize, 25 + playerX * spriteSize, "sand");
    player = new Player(275 + playerY * spriteSize, 25 + playerX * spriteSize);
    playerAnother = new PlayerAnother();
}

// Класс игрока.
function Player(x, y) {
    this.sprite = game.add.sprite(x, y, "player_stay");
    this.haveTreasure = false;
}

// Клвсс другого игрока
function PlayerAnother() {
    this.sprite = null;
}

// Класс полоски здоровья
function HealthScale(x, y) {
    this.sprite = game.add.sprite(x, y, "health100");
    this.isAlive = true;
}

// Класс поле:
// его метод go для перемещений и действий игрока,
// его метод changeSprite для смены спрайта игрока.
function Field(x, y, _id) {
    this._id = _id;
    this.sprite = game.add.sprite(x, y, "fog");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.go.bind(this) ,this);
}

Field.prototype.go = function() {
    touchSound.play();
    switch (CURRENT_STATE) {
        case STATE_5__send_signal: {
            send_coordinates("go", this._id[0], this._id[1]);
            CURRENT_STATE = STATE_3__show_my_turn;
            break;
        }
        case STATE_7_bomb: {
            send_coordinates("bomb", this._id[0], this._id[1]);
            CURRENT_STATE = STATE_3__show_my_turn;
            break;
        }
        case STATE_8_concrete: {
            send_coordinates("concrete", this._id[0], this._id[1]);
            CURRENT_STATE = STATE_3__show_my_turn;
            break;            
        }
    }
}

Field.prototype.changeSprite = function(x, y, spriteName) {
    this.sprite = game.add.sprite(x, y, spriteName);
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.go.bind(this) ,this);
}

// Кнопка бомбы:
// её метод bomb для установки бомбы.
function buttonBombClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonBomb");
    this.counter = 0;
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.bomb.bind(this), this);
}

buttonBombClass.prototype.bomb = function() {
    touchSound.play();
    if (CURRENT_STATE == STATE_5__send_signal) 
        CURRENT_STATE = STATE_7_bomb;
}

// Кнопка стены:
// её метод concrete для установки стены.
function buttonConcreteClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonConcrete");
    this.counter = 0;
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.concrete.bind(this), this);
}

buttonConcreteClass.prototype.concrete = function() {
    touchSound.play();
    if (CURRENT_STATE == STATE_5__send_signal)
        CURRENT_STATE = STATE_8_concrete;
}

// Кнопка удара ножом:
// её метод knife для удара ножом.
function buttonKnifeClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonKnife");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.knife.bind(this), this);
}

buttonKnifeClass.prototype.knife = function() {
    touchSound.play();
    if (CURRENT_STATE == STATE_5__send_signal) {
        send_coordinates("knife", 0, 0);
        CURRENT_STATE = STATE_3__show_my_turn;        
    } 
}

// Кнопка использования аптечки:
// её метод aid для использования аптечки.
function buttonAidClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonAid");
    this.counter = 0;
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.aid.bind(this), this);
}

buttonAidClass.prototype.aid = function() {
    touchSound.play();
    if (CURRENT_STATE == STATE_5__send_signal) {
        send_coordinates("aid", 0, 0);
        CURRENT_STATE = STATE_3__show_my_turn;        
    }
}

// Кнопка выходи из игры:
// её метод exit для выхода из игры
function buttonExitClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonExit");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.exit.bind(this), this);    
}

buttonExitClass.prototype.exit = function() {
    touchSound.play();
    if (confirm("Выходя из игры, вы потеряете весь прогресс!")) {
        alert("ДОСРОЧНЫЙ ВЫХОД!");
        webSocket.send("Выход");
    }
}
