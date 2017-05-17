// Вспомогательные функции отрисовки хода данного игрока.

// Перемещение.
function drawGo(data) {
    if (data.error == 1) {
        alert("Сюда идти нельзя!\n Повторите попытку!");
    } else {
        var playeSprite;
        if (healthScale.isAlive)
            playerSprite = "player_stay";
        else
            playerSprite = "player_ghost";
        var flag = false;
        if (data.is_here_enemy == 1)
            drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
        if (data.is_here_enemy == 2)
            drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
        if ((data.wall[0] == 1) || (data.wall[0] == 2)) {
            intoWallSound.play();
            switch (data.wall[0]) {
                case 1: {
                    fields[data.wall[1]][data.wall[2]].changeSprite(275 + data.wall[2] * spriteSize, 25 + data.wall[1] * spriteSize, "wall");
                    break;
                }
                case 2: {
                    fields[data.wall[1]][data.wall[2]].changeSprite(275 + data.wall[2] * spriteSize, 25 + data.wall[1] * spriteSize, "concrete");
                    break;
                }
            }
            flag = true;    
        }
        if ((data.mine == 1) || (data.mine == 2) || (data.mine == 3)) {
            bombBlastedSound.play()
            drawHelper(data, data.coordinates[0], data.coordinates[1], "bomb", playerSprite);
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "sand", "player_bang");
            switch (data.mine) {
                case 1: {
                    setTimeout(drawHelper, 600, data, data.coordinates[0], data.coordinates[1], "sand", "player_died");
                    setTimeout(drawHelper, 900, data, data.coordinates[0], data.coordinates[1], "sand", "player_ghost");
                    setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health0");}, 1000);
                    healthScale.isAlive = false;
                    break;
                }
                case 2: {
                    setTimeout(drawHelper, 600, data, data.coordinates[0], data.coordinates[1], "sand", "player_injured");
                    setTimeout(drawHelper, 900, data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
                    setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health50");}, 1000);                  
                    break;
                }
                case 3: {
                    setTimeout(drawHelper, 600, data, data.coordinates[0], data.coordinates[1], "sand", "player_injured");
                    setTimeout(drawHelper, 900, data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
                    setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health25");}, 1000); 
                    break;
                }
            }
            flag = true;
        }
        if (data.river[0] == 1) {
            waterSound.play();
            setTimeout(drawHelper, 0, data, data.coordinates[0], data.coordinates[1], "water", playerSprite);
            for (var i = 0; i < data.river[1].length; i++)
                setTimeout(drawHelper, (1000 / data.river[1].length) * (i + 1), data, data.river[1][i][0], data.river[1][i][1], "water", playerSprite);
        }
        if ((data.aid == 1) || (data.aid == 2) || (data.aid == 3)) {
            if (healthScale.isAlive)
                drawHelper(data, data.coordinates[0], data.coordinates[1], "aid", "player_stay")
            else
                drawHelper(data, data.coordinates[0], data.coordinates[1], "aid", "player_ghost");
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "aid", "player_use_aid");
            setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "aid", "player_stay");
            switch (data.aid) {
                case 1: {
                    setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health100");}, 1000);
                    healthScale.isAlive = true;
                    break;
                }
                case 2: {
                    setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health100");}, 1000);             
                    break;
                }
                case 3: {
                    setTimeout(function(){
                        buttonAid.counter++;
                        if (buttonAid.counter < 10) {
                            numberAid.destroy();
                            numberAid = game.add.text(49, 434, " " + buttonAid.counter.toString(), styleOther);
                        } else {
                            numberAid.destroy();
                            numberAid = game.add.text(49, 434, buttonAid.counter.toString(), styleOther);
                        }
                    }, 1000); 
                    break;
                }
            }
            flag = true;
        }
        if ((data.arm == 1) || (data.arm == 2)) {
            drawHelper(data, data.coordinates[0], data.coordinates[1], "arm", playerSprite);
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "arm", "player_use_aid");
            setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "arm", playerSprite);
            switch (data.arm) {
                case 1: {
                    setTimeout(function(){
                        buttonConcrete.counter++
                        if (buttonConcrete.counter < 10) {
                            numberConcrete.destroy();
                            numberConcrete = game.add.text(153, 434, " " + buttonConcrete.counter.toString(), styleOther);
                        } else {
                            numberConcrete.destroy();
                            numberConcrete = game.add.text(153, 434, buttonConcrete.counter.toString(), styleOther);
                        }
                    }, 1000);
                    break;
                }
                case 2: {
                    setTimeout(function(){
                        buttonBomb.counter++;
                        if (buttonBomb.counter < 10) {
                            numberBomb.destroy();
                            numberBomb = game.add.text(153, 329, " " + buttonBomb.counter.toString(), styleOther);
                        } else {
                            numberBomb.destroy();
                            numberBomb = game.add.text(153, 329, buttonBomb.counter.toString(), styleOther);
                        }
                    }, 1000);
                    break;
                }
            }
            flag = true;
        }
        if ((data.treasure == 1) || (data.treasure == 2)) {
            if (data.treasure == 1) {
                treasureSound.play();
                drawHelper(data, data.coordinates[0], data.coordinates[1], "treasure", playerSprite);
                setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "treasure", "player_use_aid");
                setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
                setTimeout(function(){alert("Вы нашли клад!");}, 1000);
            } else if (data.treasure == 2) {
                drawHelper(data, data.coordinates[0], data.coordinates[1], "treasure", playerSprite);
            }

            flag = true;
        }
        if (data.metro[0] == 1) {
            metroSound.play();
            drawHelper(data, data.coordinates[0], data.coordinates[1], "metro", playerSprite);
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "metro", "player_use_aid");
            setTimeout(drawHelper, 600, data, data.metro[1], data.metro[2], "metro", "player_use_aid");
            setTimeout(drawHelper, 900, data, data.metro[1], data.metro[2], "metro", playerSprite);
            flag = true;
        }
        if (data.exit[0] == 1) {
            if (data.exit[1] == 1) {
                drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
                setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "treasure", playerSprite);
                setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
                setTimeout(function(){alert("Вы выиграли!");}, 1000);
                CURRENT_STATE = FINAL__somebody_win; return;
            } else {
                drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", "-");
                alert("У вас нет клада!\n Вам сюда нельзя!")
            }
            flag = true;
        }
        if (! flag) {
            drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
        }
    }
    CURRENT_STATE = STATE_4__sleep;
}

// Нож.
function drawKnife(data) {
    if (data.error == 1) {
        alert("Вы мертвы, а значит не можете пользоваться ножом!\n  Повторите попытку!");
        CURRENT_STATE = STATE_5__send_signal;
    } else {
        knifeSound.play();
        drawHelper(data, data.coordinates[0], data.coordinates[1], data.from_sprite, "player_stay");
        setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], data.from_sprite, "player_use_knife");
        setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], data.from_sprite, "player_stay");
        switch (data.is_here_enemy) {
            case 0: {
                setTimeout(function(){alert("Вы промахнулись!");}, 1000);
                break;
            }
            case 1: {
                setTimeout(function(){alert("Вы убили врага!");}, 1000);
                break;
            }
            case 2: {
                setTimeout(function(){alert("Вы ранили врага!");}, 1000);                    
                break;
            }
        }
    }
    CURRENT_STATE = STATE_4__sleep;
}

// Бомба.
function drawBomb(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                alert("Вы мертвы, а значит не можете установить бомбу!\n      Повторите попытку");                                
                break;                                    
            }
            case 2: {
                alert("Сюда нельзя ставить бомбу!\n     Повторите попытку!");                            
                break; 
            }
            case 3: {
                alert("У вас нет ни одной бомбы!\n   Повторите попытку!");
                break; 
            }
        }
        CURRENT_STATE = STATE_5__send_signal; 
    } else {
        if ((data.wall_or_ground[0] == 1) || (data.wall_or_ground[0] == 2)) {
            bombBlastedSound.play();
            if (data.wall_or_ground[0] == 1) 
                drawHelper(data, data.wall_or_ground[1], data.wall_or_ground[2], "wall", "-");
            else 
                drawHelper(data, data.wall_or_ground[1], data.wall_or_ground[2], "concrete", "-");
            setTimeout(drawHelper, 300, data, data.wall_or_ground[1], data.wall_or_ground[2], "player_bang", "-");
            setTimeout(drawHelper, 700, data, data.wall_or_ground[1], data.wall_or_ground[2], "sand", "-"); 
            setTimeout(function(){
                buttonBomb.counter--;
                if (buttonBomb.counter < 10) {
                    numberBomb.destroy();
                    numberBomb = game.add.text(153, 329, " " + buttonBomb.counter.toString(), styleOther);
                } else {
                    numberBomb.destroy();
                    numberBomb = game.add.text(153, 329, buttonBomb.counter.toString(), styleOther);
                }
            }, 1000); 
        } else if (data.wall_or_ground[0] == 3) {
            bombPlantedSound.play();
            drawHelper(data, data.wall_or_ground[1], data.wall_or_ground[2], "bomb", "-");     
            setTimeout(function(){
                buttonBomb.counter--;
                if (buttonBomb.counter < 10) {
                    numberBomb.destroy();
                    numberBomb = game.add.text(153, 329, " " + buttonBomb.counter.toString(), styleOther);
                } else {
                    numberBomb.destroy();
                    numberBomb = game.add.text(153, 329, buttonBomb.counter.toString(), styleOther);
                }
            }, 1000);        
        }
    }   
    CURRENT_STATE = STATE_4__sleep;
}


// Цемент.
function drawConcrete(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                alert("Вы мертвы, а значит не можете установить блок цемента!\n    Повторите попытку!");
                break;                                    
            }
            case 2: {
                alert("Сюда нельзя ставить блок цемента!\n    Повторите попытку");
                break; 
            }
            case 3: {
                alert("У вас нет ни одного блока цемента!\n      Повторите попытку!");                     
                break; 
            }                                
        }
    } else {
        concreteSound.play();
        drawHelper(data, data.coordinates[0], data.coordinates[1], "concrete", "-");
        setTimeout(function(){
            buttonConcrete.counter--;
            if (buttonConcrete.counter < 10) {
                numberConcrete.destroy();
                numberConcrete = game.add.text(153, 434, " " + buttonConcrete.counter.toString(), styleOther);
            } else {
                numberConcrete.destroy();
                numberConcrete = game.add.text(153, 434, buttonConcrete.counter.toString(), styleOther);
            }
        }, 1000);
    }   
    CURRENT_STATE = STATE_4__sleep;   
}

// Аптечка.
function drawAid(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                alert("Вы мертвы, а значит не можете использовать аптечку!\n     Повторите попытку!");
                break;                                    
            }
            case 2: {
                alert("У вас нет ни одной аптечки!\n     Повторите попытку!");
                break; 
            }      
            case 3: {
                alert("У вас и так 100% здоровье!\n      Повторите поптыку!");
                break;
            }                        
        }                                
    } else {
        drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
        setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "sand", "player_use_aid");
        setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "sand", playerSprite);
        setTimeout(function(){
            buttonAid.counter--;
            if (buttonAid.counter < 10) {
                numberAid.destroy();
                numberAid = game.add.text(49, 434, " " + buttonAid.counter.toString(), styleOther);
            } else {
                numberAid.destroy();
                numberAid = game.add.text(49, 434, buttonAid.counter.toString(), styleOther);
            }
        }, 1000); 
        if (data.now_heatlh == 1) {
            setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health50");}, 1000);
        }
        if (data.now_health == 2) {
            setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health75");}, 1000);
        }
        if (data.now_health == 3) {
            setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health100");}, 1000);
        }
    } 
    CURRENT_STATE = STATE_4__sleep;
}

// Функция отрисовки.
function drawHelper(data, x, y, fieldImage, playerImage) {
    fields[x][y].changeSprite(275 + y * spriteSize, 25 + x * spriteSize, fieldImage);
    if (playerImage != "-") {
        player.sprite.kill();
        player.sprite = game.add.sprite(275 + y * spriteSize, 25 + x * spriteSize, playerImage);
    }
}
