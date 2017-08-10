// Вспомогательные функции отрисовки хода другого игрока.

// Перемещение.
function drawAnotherGo(data) {
    var playeSprite; 
    if (data.is_alive)
        playerSprite = "player_stay";
    else
        playerSprite = "player_ghost"
    var flag = false;
    if (data.wall[0] == 1) {
        if (data.is_visible_from == 1) {
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            }
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
        }    
        flag = true;
    }
    if (((data.mine == 1) || (data.mine == 2)) && (data.is_alive) || (data.mine == -1)) {
        if (data.is_visible_from == 1) {
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            }
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
            else 
                drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
        }
        if ((data.is_visible_to == 1) && (data.mine == -1)) {
            CURRENT_STATE = STATE_4__sleep;
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "bomb", "player_ghost", data.name);
            return;
        }
        if (data.is_visible_to == 1) {
            bombBlastedSound.play();
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "bomb", "player_stay", data.name);
            setTimeout(drawAnotherHelper, 300, data, data.to_coordinates[0], data.to_coordinates[1], "sand", "player_bang", data.name);
            switch (data.mine) {
                case 1: {
                    setTimeout(drawAnotherHelper, 600, data, data.to_coordinates[0], data.to_coordinates[1], "sand", "player_died", data.name);
                    setTimeout(drawAnotherHelper, 900, data, data.to_coordinates[0], data.to_coordinates[1], "sand", "player_ghost", data.name);
                    break;                
                }
                case 2: {
                    setTimeout(drawAnotherHelper, 600, data, data.to_coordinates[0], data.to_coordinates[1], "sand", "player_injured", data.name);
                    setTimeout(drawAnotherHelper, 900, data, data.to_coordinates[0], data.to_coordinates[1], "sand", "player_stay", data.name);
                    break;
                }
            }
        }
        flag = true;
    }
    if (data.river[0] == 1) {
        if (data.is_visible_from == 1) {
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            }
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
            else 
                drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
        }
        if (data.is_visible_to == 1) {
            waterSound.play();
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "water", playerSprite, data.name);
            for (var i = 0; i < data.river[1].length; i++)
                setTimeout(drawAnotherHelper, (1000 / data.river[1].length) * (i + 1), data, data.river[1][i][0], data.river[1][i][1], "water", playerSprite, data.name);
        }
        flag = true;
    }
    if ((data.aid == 1) || (data.aid == 2)) {
        if (data.is_visible_from == 1) {
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            }
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
            else 
                drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
        }
        if (data.is_visible_to == 1) {
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "aid", playerSprite, data.name);
            setTimeout(drawAnotherHelper, 300, data, data.to_coordinates[0], data.to_coordinates[1], "aid", "player_use_aid", data.name);
            setTimeout(drawAnotherHelper, 700, data, data.to_coordinates[0], data.to_coordinates[1], "aid", "player_stay", data.name);
        }
        flag = true;
    }
    if (((data.arm == 1) || (data.arm == 2)) && (data.is_alive == 1) || (data.arm == -1)) {
        if (data.is_visible_from == 1) {
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            }
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
            else 
                drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
        }
        if ((data.is_visible_to == 1) && (data.arm == -1)) {
            CURRENT_STATE = STATE_4__sleep;
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "arm", "player_ghost", data.name);
            return;
        }
        if (data.is_visible_to == 1) {
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "arm", "player_stay", data.name);
            setTimeout(drawAnotherHelper, 300, data, data.to_coordinates[0], data.to_coordinates[1], "arm", "player_use_aid", data.name);
            setTimeout(drawAnotherHelper, 700, data, data.to_coordinates[0], data.to_coordinates[1], "arm", "player_stay", data.name);
        }
        flag = true;
    }       
    if ((data.treasure == 1) && (data.is_alive == 1)) {
        if (data.is_visible_from == 1) {
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            }
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
            else 
                drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
        }
        if (data.is_visible_to == 1) {
            treasureSound.play();
            setTimeout(drawAnotherHelper, 300, data, data.to_coordinates[0], data.to_coordinates[1], "treasure", "player_use_aid", data.name);
            setTimeout(drawAnotherHelper, 700, data, data.to_coordinates[0], data.to_coordinates[1], "sand", "player_stay", data.name);
            setTimeout(alert("Игрок " + data.name + " нашёл клад!\n       Мочи его!"), 1000);
        }
        alert("Игрок " + data.name + " нашёл клад!\n       Мочи его!");
        flag = true;           
    }
    if (data.metro[0] == 1) {
        if (data.is_visible_from == 1) {
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            }
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
            else 
                drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
            /* ----------------------------------------------------------------------------------------------------------------------------------- */
        }
        if (data.is_visible_to == 1) {
            metroSound.play();
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "metro", playerSprite, data.name);
            setTimeout(drawAnotherHelper, 300, data, data.to_coordinates[0], data.to_coordinates[1], "metro", "player_use_aid", data.name);
            setTimeout(drawAnotherHelper, 600, data, data.metro[1], data.metro[2], "metro", "player_use_aid", data.name);
            setTimeout(drawAnotherHelper, 900, data, data.metro[1], data.metro[2], "metro", playerSprite, data.name);
        } 
        flag = true;
    }
    if (data.exit[0] == 1) {
        if (data.exit[1] == 1) {
            alert("Игрок " + data.name + " выиграл!");
            if (data.is_visible_from == 1) {
                /* ----------------------------------------------------------------------------------------------------------------------------------- */
                if (data.me_left == 1) {
                    if (healthScale.isAlive)
                        drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                    else
                        drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
                }
                // KEK
                else if (data.enemy_left == 1) {
                    if (data.enemy_alive == 1)
                        drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                    else 
                        drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
                }
                // KEK
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
                /* ----------------------------------------------------------------------------------------------------------------------------------- */
            }
            if (data.is_visible_to == 1) {
                drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "sand", playerSprite, data.name);
                setTimeout(drawAnotherHelper, 300, data, data.to_coordinates[0], data.to_coordinates[1], "treasure", playerSprite, data.name);
                setTimeout(drawAnotherHelper, 700, data, data.to_coordinates[0], data.to_coordinates[1], "sand", playerSprite, data.name); // СТРАННО
            }                
            CURRENT_STATE = FINAL__somebody_win; return;
        }
        flag = true;
    }
    if (! flag) {
        if (data.is_visible_from == 1) {
            if (data.me_left == 1) {
                if (healthScale.isAlive)
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay");
                else
                    drawHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost");
            } 
            // KEK
            else if (data.enemy_left == 1) {
                if (data.enemy_alive == 1)
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_stay", data.enemy_name);
                else 
                    drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "player_ghost", data.enemy_name);
            }
            // KEK
               else 
            drawAnotherHelper(data, data.from_coordinates[0], data.from_coordinates[1], data.from_sprite, "-", data.name);
        }
        if (data.is_visible_to == 1) {
            drawAnotherHelper(data, data.to_coordinates[0], data.to_coordinates[1], "sand", playerSprite, data.name);
        }
    }
    CURRENT_STATE = STATE_4__sleep;        
}

// Нож.
function drawAnotherKnife(data) {
    if ((data.are_you_injured == 1) || (data.are_you_injured == 2) || (data.are_you_injured == 3) || (data.are_you_injured == 4)) {
        knifeSound.play();
        drawHelper(data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_stay");
        setTimeout(drawHelper, 300, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_injured");
        switch (data.are_you_injured) {
            case 1: {
                healthScale.isAlive = false;
                setTimeout(drawHelper, 600, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_died");
                setTimeout(drawHelper, 900, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_ghost");
                setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health0");}, 1000);
                break;
            }
            case 2: {
                setTimeout(drawHelper, 600, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_injured");
                setTimeout(drawHelper, 900, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_stay");
                setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health25");}, 1000);
                break;
            }
            case 3: {
                setTimeout(drawHelper, 600, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_injured");
                setTimeout(drawHelper, 900, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_stay");
                setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health50");}, 1000);
                break;
            }
            case 4: {
                setTimeout(drawHelper, 600, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_injured");
                setTimeout(drawHelper, 900, data, data.knife_coordinates[0], data.knife_coordinates[1], data.from_sprite, "player_stay");
                setTimeout(function(){healthScale.sprite = game.add.sprite(37, 270, "health75");}, 1000);
                break;
            }
        }
    }
    // Эта ветка сработает лишь при 3 игроках
    else if ((data.is_here_enemy == 1) || (data.is_here_enemy == 2)) {
        switch (data.is_here_enemy) {
            case 1: {
                alert("Игрок " + data.name + " убил игрока " + data.victim_name);
                break;
            }
            case 2: {
                alert("Игрок " + data.name + " ранил игрока " + data.victim_name);
                break;
            }
        }
        if (data.is_visible_knife == 1) {
            // draw
        } 
    } else {
        alert("Игрок " + data.name + " ударил ножом, но никого не задел.");
        if (data.is_visible_knife == 1) {
            // draw
        } 
    }
    CURRENT_STATE = STATE_4__sleep;
}

// Бомба.
function drawAnotherBomb(data) {
    if (data.visible_bomb == 1) {
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
    }
    CURRENT_STATE = STATE_4__sleep;
}   


// Цемент.
function drawAnotherConcrete(data) {
    if (data.visible_concrete == 1) {
        concreteSound.play();
        drawHelper(data, data.coordinates[0], data.coordinates[1], "concrete", "-");
    }
    CURRENT_STATE = STATE_4__sleep;   
}     

// Аптечка.
function drawAnotherAid(data) {
    if (data.visible_aid == 1) {
        drawAnotherHelper(data, data.coordinates[0], data.coordinates[1], data.from_sprite, "player_stay", data.name);
        setTimeout(drawAnotherHelper, 300, data, data.coordinates[0], data.coordinates[1], data.from_sprite, "player_use_aid", data.name);
        setTimeout(drawAnotherHelper, 700, data, data.coordinates[0], data.coordinates[1], data.from_sprite, "player_stay", data.name);
    }
    CURRENT_STATE = STATE_4__sleep;
} 


// Функция отрисовки.
function drawAnotherHelper(data, x, y, fieldImage, playerImage, name) {
    fields[x][y].changeSprite(275 + y * spriteSize, 25 + x * spriteSize, fieldImage);
    if (playerImage != "-") {
        if (playerAnother[name].sprite != null) {
            playerAnother[name].sprite.kill();
        }
        playerAnother[name].sprite = game.add.sprite(275 + y * spriteSize, 25 + x * spriteSize, playerImage);
    } else {
        if (playerAnother[name].sprite != null) {
            playerAnother[name].sprite.kill();
        }
    }
}
