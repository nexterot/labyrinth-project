function preload() {
    var path = "http://0.0.0.0:8000/game/sprites/";
    
    var path1 = path + "interface/";
    game.load.image("background", path1 + "background.png");
    game.load.image("playerFace", path1 + "player_face.png");
    game.load.image("buttonKnife", path1 + "button_knife.png");
    game.load.image("buttonBomb", path1 + "button_bomb.png");
    game.load.image("buttonAid", path1 + "button_aid.png");
    game.load.image("buttonConcrete", path1 + "button_concrete.png");
    game.load.image("scaleHealth", path1 + "scale_health.png");
    
    var path1 = path + "world/";
    game.load.image("fog", path1 + "fog.png");
    game.load.image("sand", path1 + "sand.png");
    game.load.image("wall", path1 + "wall.png");
    game.load.image("water", path1 + "water.png");
    
    var path1 = path + "possession/";
    game.load.image("aid", path1 + "aid.png");
    game.load.image("arm", path1 + "arm.png");
    game.load.image("backpack", path1 + "backpack.png");
    game.load.image("bomb", path1 + "bomb.png");
    game.load.image("concrete", path1 + "concrete.png");
    game.load.image("metro", path1 + "metro.png");
    game.load.image("treasure", path1 + "treasure.png");
    
    var path1 = path + "player/";
    game.load.image("player_bang", path1 + "player_bang.png");
    game.load.image("player_died", path1 + "player_died.png");
    game.load.image("player_injured", path1 + "player_injured.png");
    game.load.image("player_stay", path1 + "player_stay.png");
    game.load.image("player_use_aid", path1 + "player_use_aid.png");
    game.load.image("player_use_bomb_concrete", path1 + "player_use_bomb_concrete.png");
    game.load.image("player_use_knife", path1 + "player_use_knife.png");
}

function renderInterface() {
    land = game.add.sprite(0, 0, "background");
    land.sendToBack();
    var playerFace = game.add.sprite(25, 25, "playerFace");
    //var panel = game.add.sprite(25, 275, "panel");
    var scaleHealth = game.add.sprite(30, 300, "scaleHealth");
    buttonKnife = new buttonKnifeClass(30, 360);
    buttonBomb = new buttonBombClass(145, 360);
    buttonAid = new buttonAidClass(30, 465);
    buttonConcrete = new buttonConcreteClass(145, 465);
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
    fields[playerX][playerY].changeSprite(275 + playerY * spriteSize, 25 + playerX * spriteSize, "sand");
    player = new Player(275 + playerY * spriteSize, 25 + playerX * spriteSize);
}

function Player(x, y) {
    this.sprite = game.add.sprite(x, y, "player_stay");
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
function buttonBombClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonBomb");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.bomb.bind(this), this);
}

buttonBombClass.prototype.bomb = function() {
    if (CURRENT_STATE == STATE_5__send_signal) 
        CURRENT_STATE = STATE_7_bomb;
}

/* Постройка стены */
function buttonConcreteClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonConcrete");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.concrete.bind(this), this);
}

buttonConcreteClass.prototype.concrete = function() {
    if (CURRENT_STATE == STATE_5__send_signal)
        CURRENT_STATE = STATE_8_concrete;
}

/* Удар ножом */
function buttonKnifeClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonKnife");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.knife.bind(this), this);
}

buttonKnifeClass.prototype.knife = function() {
    if (CURRENT_STATE == STATE_5__send_signal) {
        send_coordinates("knife", 0, 0);
        CURRENT_STATE = STATE_3__show_my_turn;        
    } 
}

/* Использование аптечки */
function buttonAidClass(x, y) {
    this.sprite = game.add.sprite(x, y, "buttonAid");
    this.sprite.inputEnabled = true;
    this.sprite.events.onInputDown.add(this.aid.bind(this), this);
}

buttonAidClass.prototype.aid = function() {
    if (CURRENT_STATE == STATE_5__send_signal) {
        send_coordinates("aid", 0, 0);
        CURRENT_STATE = STATE_3__show_my_turn;        
    }
}

/* ------------------------------------------------------------------ */
