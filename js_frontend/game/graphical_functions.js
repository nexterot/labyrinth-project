function preload() {
    var path = "http://0.0.0.0:8000/game/";
    game.load.image("grass", path+"sprites/sand.png");
    game.load.image("fog", path+"sprites/fog.png");
    game.load.image("background", path+"sprites/background.png");
    game.load.image("wall", path+"sprites/wall.png");
    game.load.image("mine", path+"sprites/mine.png");
    game.load.image("teleport", path+"sprites/metro.png");
    game.load.image("bear", path+"sprites/bear.png");
    game.load.image("panel", path+"sprites/panel.png");
    game.load.image("player", path+"sprites/player.png");
    game.load.image("water", path+"sprites/water.png");
    game.load.image("hospital", path+"sprites/aid.png");
    game.load.image("playerFace", path+"sprites/player_face.png");
    game.load.image("buttonKnife", path+"sprites/button_knife.png");
    game.load.image("buttonBomb", path+"sprites/button_bomb.png");
    game.load.image("buttonAid", path+"sprites/button_aid.png");
    game.load.image("buttonConcrete", path+"sprites/button_concrete.png");
    game.load.image("scaleHealth", path+"sprites/scale_health.png");
    game.load.image("labelNick", path+"sprites/label_nick.png");
    game.load.image("weapons", path+"sprites/weapons.png");
    game.load.image("treasure", path+"sprites/treasure.png");
}

function renderInterface() {
    land = game.add.sprite(0, 0, "background");
    land.sendToBack();
    var playerFace = game.add.sprite(25, 25, "playerFace");
    var panel = game.add.sprite(25, 275, "panel");
    var labelNick = game.add.sprite(30, 205, "labelNick");
    var scaleHealth = game.add.sprite(30, 300, "scaleHealth");
    var buttonKnife = game.add.sprite(30, 360, "buttonKnife");
    var buttonBomb = game.add.sprite(145, 360, "buttonBomb");
    var buttonAid = game.add.sprite(30, 465, "buttonAid");
    var buttonConcrete = game.add.sprite(145, 465, "buttonConcrete");
}

function create(levelSizeX, levelSizeY, playerX, playerY) {
    fields = [];
    for (var i = 0; i < levelSizeX; i++)
        fields.push([]);
    initializeLevel(levelSizeX, levelSizeY, playerX, playerY);
    renderInterface();
}

function initializeLevel(levelSizeX, levelSizeY, playerX, playerY) {
    for (var row = 0; row < levelSizeX; row++)
        for (var col = 0; col < levelSizeY; col++)
            fields[row].push(new Field(275 + col * spriteSize, 25 + row * spriteSize, [row, col]));
    fields[playerX][playerY].changeSprite(275 + playerY * spriteSize, 25 + playerX * spriteSize, "grass");
    player = new Player(275 + playerY * spriteSize, 25 + playerX * spriteSize);
}

function Player(x, y) {
    this.sprite = game.add.sprite(x, y, "player");
}

function Field(x, y, _id) {
    this._id = _id;
    this.sprite = game.add.sprite(x, y, "fog");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.go.bind(this) ,this);
}

Field.prototype.go = function() {
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

function Bear(x, y) {
    this.sprite = game.add.sprite(x, y, "bear");
    this.sprite.visible = false;
    this.location = null;
}

/* ------------------------------------------------------------------ */
/* Кнопки */

/* Взрыв бомбы */
function buttonBomb(x, y) {
    this.sprite = game.add.sprite(x, y, "button_bomb");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.bomb.bind(this), this);
}

buttonBomb.prototype.bomb = function() {
    if (CURRENT_STATE == STATE_5__send_signal)
        CURRENT_STATE = STATE_7_bomb;
}

/* Постройка стены */
function buttonConcrete(x, y) {
    this.sprite = game.add.sprite(x, y, "button_concrete");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.concrete.bind(this), this);
}

buttonBomb.prototype.concrete = function() {
    if (CURRENT_STATE == STATE_5__send_signal)
        CURRENT_STATE = STATE_8_concrete;
}

/* Удар ножом */
function buttonKnife(x, y) {
    this.sprite = game.add.sprite(x, y, "button_knife");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.knife.bind(this), this);
}

buttonKnife.prototype.knife = function() {
    if (CURRENT_STATE == STATE_5__send_signal) {
        send_coordinates("knife", 0, 0);
        CURRENT_STATE = STATE_3_show_my_turn;        
    } 
}

/* Использование аптечки */
function buttonAid(x, y) {
    this.sprite = game.add.sprite(x, y, "button_aid");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.aid.bind(this), this);
}

buttonAid.prototype.aid = function() {
    if (CURRENT_STATE == STATE_5__send_signal) {
        send_coordinates("aid", 0, 0);
        CURRENT_STATE = STATE_3_show_my_turn;        
    }
}

/* ------------------------------------------------------------------ */
