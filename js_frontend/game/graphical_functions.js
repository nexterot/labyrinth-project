function preload() { //
    var path = "http://0.0.0.0:8000/game/";
    game.load.image("grass", path+"sprites/grass.png");
    game.load.image("fog", path+"sprites/fog.png");
    game.load.image("background", path+"sprites/background.png");
    game.load.image("wall", path+"sprites/wall.png");
    game.load.image("mine", path+"sprites/mine.png");
    game.load.image("teleport", path+"sprites/teleport.png");
    game.load.image("teleport2", path+"sprites/teleport_2.png");
    game.load.image("teleport3", path+"sprites/teleport_3.png");
    game.load.image("bear", path+"sprites/bear.png");
    game.load.image("panel", path+"sprites/panel.png");
    game.load.image("player", path+"sprites/player.png");
    game.load.image("water", path+"sprites/water.png");
    game.load.image("buttonMenu", path+"sprites/button_menu.png");
    game.load.image("buttonExit", path+"sprites/button_exit.png");
    game.load.image("hospital", path+"sprites/aid.png");
    game.load.image("playerFace", path+"sprites/player_face.png");
    game.load.image("weaponGun", path+"sprites/weapon_gun.png");
    game.load.image("weaponMine", path+"sprites/weapon_mine.png");
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
    var weaponGun = game.add.sprite(30, 360, "weaponGun");
    var weaponMine = game.add.sprite(145, 360, "weaponMine");
    var weaponGun2 = game.add.sprite(30, 465, "weaponGun");
    var weaponMine2 = game.add.sprite(145, 465, "weaponMine");
    var buttonMenu = game.add.sprite(30, 570, "buttonMenu");
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
