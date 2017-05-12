// Вспомогательные функции отрисовки хода данного игрока.

// Перемещение.
function drawGo(data) {
    if (data.error == 1) {
        alert("Сюда идти нельзя!\n Повторите попытку!");
        CURRENT_STATE = STATE_5__send_signal;
    } else {
        var flag = false;
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
            drawHelper(data, data.coordinates[0], data.coordinates[1], "bomb", "player_stay");
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "sand", "player_bang");
            switch (data.mine) {
                case 1: {
                    setTimeout(drawHelper, 600, data, data.coordinates[0], data.coordinates[1], "sand", "player_died");
                    setTimeout(drawHelper, 900, data, data.coordinates[0], data.coordinates[1], "sand", "player_ghost");
                    setTimeout(function(){alert("Вы убиты на мине!");}, 1000);
                    break;
                }
                case 2: {
                    setTimeout(drawHelper, 600, data, data.coordinates[0], data.coordinates[1], "sand", "player_injured");
                    setTimeout(drawHelper, 900, data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
                    setTimeout(function(){alert("Вы ранены на мине!\n У вас 50 % здоровья!");}, 1000);                   
                    break;
                }
                case 3: {
                    setTimeout(drawHelper, 600, data, data.coordinates[0], data.coordinates[1], "sand", "player_injured");
                    setTimeout(drawHelper, 900, data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
                    setTimeout(function(){alert("Вы ранены на мине!\n У вас 25 % здоровья!");}, 1000);    
                    break;
                }
            }
            flag = true;
        }
        if (data.river[0] == 1) {
            waterSound.play();
            setTimeout(drawHelper, 0, data, data.coordinates[0], data.coordinates[1], "water", "player_stay");
            for (var i = 0; i < data.river[1].length; i++)
                setTimeout(drawHelper, (1000 / data.river[1].length) * (i + 1), data, data.river[1][i][0], data.river[1][i][1], "water", "player_stay");
        }
        if ((data.aid == 1) || (data.aid == 2) || (data.aid == 3)) {
            drawHelper(data, data.coordinates[0], data.coordinates[1], "aid", "player_stay");
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "aid", "player_use_aid");
            setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "aid", "player_stay");
            switch (data.aid) {
                case 1: {
                    setTimeout(function(){alert("Вы попали в госпиталь!\n  Вы ожили!");}, 1000);
                    break;
                }
                case 2: {
                    setTimeout(function(){alert("Вы попали в госпиталь!\n   У вас теперь 100% здоровья!");}, 1000);              
                    break;
                }
                case 3: {
                    setTimeout(function(){alert("Вы попали в госпиталь!\n   У вас плюс одна аптечка!");}, 1000); 
                    break;
                }
            }
            flag = true;
        }
        if ((data.arm == 1) || (data.arm == 2)) {
            drawHelper(data, data.coordinates[0], data.coordinates[1], "arm", "player_stay");
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "arm", "player_use_aid");
            setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "arm", "player_stay");
            switch (data.arm) {
                case 1: {
                    setTimeout(function(){alert("Вы попали в арсенал!\n  У вас плюс один цемент!");}, 1000);  
                    break;
                }
                case 2: {
                    setTimeout(function(){alert("Вы попали в арсенал!\n  У вас плюс одна бомба");}, 1000); 
                    break;
                }
            }
            flag = true;
        }
        if (data.treasure == 1) {
            treasureSound.play();
            drawHelper(data, data.coordinates[0], data.coordinates[1], "treasure", "player_stay");
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "treasure", "player_use_aid");
            setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
            setTimeout(function(){alert("Вы нашли клад!");}, 1000); 
            flag = true;
        }
        if (data.metro[0] == 1) {
            metroSound.play();
            drawHelper(data, data.coordinates[0], data.coordinates[1], "metro", "player_stay");
            setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "metro", "player_use_aid");
            setTimeout(drawHelper, 600, data, data.metro[1], data.metro[2], "metro", "player_use_aid");
            setTimeout(drawHelper, 900, data, data.metro[1], data.metro[2], "metro", "player_stay");
            flag = true;
        }
        if (data.exit[0] == 1) {
            if (data.exit[1] == 1) {
                drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
                setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "treasure", "player_stay");
                setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
                setTimeout(function(){alert("Вы выиграли!");}, 1000);
                CURRENT_STATE = FINAL__somebody_win; return;
            } else {
                drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");                
                alert("У вас нет клада!\n Вам сюда нельзя!")
            }
            flag = true;
        }
        if (! flag) {
            drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
        }
        CURRENT_STATE = STATE_4__sleep;
    }
}

// Нож.
function drawKnife(data) {
    if (data.error == 1) {
        alert("Вы мертвы, а значит не можете пользоваться ножом!\n  Повторите попытку!");
        CURRENT_STATE = STATE_5__send_signal;
    } else {
        knifeSound.play();
        drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
        setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "sand", "player_use_knife");
        setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
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
        CURRENT_STATE = STATE_4__sleep;
    }
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
        } else if (data.wall_or_ground[0] == 3) {
            bombPlantedSound.play();
            drawHelper(data, data.wall_or_ground[1], data.wall_or_ground[2], "bomb", "-");             
        }
        CURRENT_STATE = STATE_4__sleep;
    }   
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
        CURRENT_STATE = STATE_5__send_signal;
    } else {
        concreteSound.play();
        drawHelper(data, data.coordinates[0], data.coordinates[1], "concrete", "-");
        CURRENT_STATE = STATE_4__sleep;     
    }     
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
        CURRENT_STATE = STATE_5__send_signal;                                   
    } else {
        drawHelper(data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
        setTimeout(drawHelper, 300, data, data.coordinates[0], data.coordinates[1], "sand", "player_use_aid");
        setTimeout(drawHelper, 700, data, data.coordinates[0], data.coordinates[1], "sand", "player_stay");
        if (data.now_heatlh == 1) {
            setTimeout(function(){alert("Вы использовали аптечку. Теперь ваше здоровье - 50%");}, 1000); 
        }
        if (data.now_health == 2) {
            setTimeout(function(){alert("Вы использовали аптечку. Теперь ваше здоровье - 75%");}, 1000); 
        }
        if (data.now_health == 3) {
            setTimeout(function(){alert("Вы использовали аптечку. Теперь ваше здоровье - 100%");}, 1000); 
        }
        CURRENT_STATE = STATE_4__sleep;
    } 
}

// Функция отрисовки.
function drawHelper(data, x, y, fieldImage, playerImage) {
    fields[x][y].changeSprite(275 + y * spriteSize, 25 + x * spriteSize, fieldImage);
    if (playerImage != "-") {
        player.sprite.kill();
        player.sprite = game.add.sprite(275 + y * spriteSize, 25 + x * spriteSize, playerImage);
    }
}
