/* ------------------------------------------------------------------ */
/* Функции отрисовки очередного действия данного игрока */

/* Функция отрисовки перехода на новую клетку.
 * Обрабатывает:
 * 1) ...
 */
function draw_go(data) {
    if (data.error == 1) {
        alert("Сюда нельзя идти, повторите попытку!!!");
        // draw
        CURRENT_STATE = STATE_5__send_signal;
    } else {
        var flag = false;
        console.log("Вы перешли на клетку [" + data.coordinates[0] + " ," + data.coordinates[1] + "]");
        if (data.wall[0] == 1) {
            alert("Вы упёрлись в стену!");
            fields[data.wall[1]][data.wall[2]].changeSprite(275 + data.wall[2] * spriteSize, 25 + data.wall[1] * spriteSize, "wall");
            flag = true;
        }
        if ((data.mine == 1) || (data.mine == 2) || (data.mine == 3)) {
            draw_go_helper1(data, data.coordinates[0], data.coordinates[1], "mine", "player");
            switch (data.mine) {
                case 1: {
                    alert("Вы убиты на мине!");
                    break;
                }
                case 2: {
                    alert("Вы ранены на мине! У вас 50 % здоровья");
                    break;
                }
                case 3: {
                    alert("Вы ранены на мине! У вас 25% здоровья");
                    break;
                }
            }
            flag = true;
        }
        if (data.river[0] == 1) {
            alert("Вы поплылил по реке!");
            draw_go_helper1(data, data.coordinates[0], data.coordinates[1], "water", "player");
            for (var i = 0; i < data.river[1].length; i++)
                draw_go_helper1(data, data.river[1][i][0], data.river[1][i][1], "water", "player");
            flag = true;
        }
        if ((data.aid == 1) || (data.aid == 2) || (data.aid == 3)) {
            draw_go_helper1(data, data.coordinates[0], data.coordinates[1], "hospital", "player");
            switch (data.aid) {
                case 1: {
                    console.log("Вы ожили");
                    alert("Вы ожили");
                    // draw
                    break;
                }
                case 2: {
                    alert("У вас теперь 100% здоровья");
                    break;
                }
                case 3: {
                    alert("У вас плюс одна аптечка");
                    break;
                }
            }
            flag = true;
        }
        if ((data.arm == 1) || (data.arm == 2)) {
            draw_go_helper1(data, data.coordinates[0], data.coordinates[1], "weapons", "player");
            switch (data.arm) {
                case 1: {
                    console.log("У вас плюс один цемент");
                    alert("У вас плюс один цемент");
                    break;
                }
                case 2: {
                    console.log("У вас плюс одна бомба");
                    alert("У вас плюс одна бомба");
                    break;
                }
            }
            flag = true;
        }
        if ((data.bear == 1) || (data.bear == 2) || (data.bear == 3)) {
            console.log("На вас напал медведь!");
            switch (data.bear) {
                case 1: {
                    console.log("Вы убиты!");
                    //draw
                    break;
                }
                case 2: {
                    console.log("Вы ранены! 50% здоровья");
                    //draw
                    break;
                }
                case 3: {
                    console.log("Вы ранены! 25% здоровья");
                    // draw 
                    break;
                }
            }
            console.log("Медведь");
            // draw
            flag = true;
        }
        if (data.treasure == 1) {
            console.log("Вы нашли клад");
            alert("Вы нашли клад!");
            draw_go_helper1(data, data.coordinates[0], data.coordinates[1], "treasure", "player");
            // Отрисовать исчезновение сокровища
            flag = true;
        }
        if (data.metro[0] == 1) {
            console.log("Вы воспользовались метро!");
            draw_go_helper1(data, data.coordinates[0], data.coordinates[1], "teleport", "player");
            draw_go_helper1(data, data.metro[1], data.metro[2], "teleport", "player");
            console.log("Вы воспользовались метрополитеном");
            console.log("Вы перешли на клетку [" + data.metro[1] + ", " + data.metro[2] + "]");
            flag = true;
        }
        if (data.exit[0] == 1) {
            if (data.exit[1] == 1) {
                console.log("Вы выиграли");
                // draw
                CURRENT_STATE = FINAL__somebody_win; return;
            } else {
                console.log("У вас нет клада!!! Вам нельзя выходить");
                // draw
            }
            flag = true;
        }
        if (! flag) {
            draw_go_helper1(data, data.coordinates[0], data.coordinates[1], "grass", "player");
        }
        CURRENT_STATE = STATE_4__sleep;
    }
}

/* Вспомогателььная функция для функции отрисовки draw_go
 */
function draw_go_helper1(data, x, y, fieldImage, playerImage) {
    fields[x][y].changeSprite(275 + y * spriteSize, 25 + x * spriteSize, fieldImage);
    player.sprite.kill();
    player.sprite = game.add.sprite(275 + y * spriteSize, 25 + x * spriteSize, playerImage);
}


/* Функция отрисовки удара ножом.
 * Обрабатывает:
 * 1) ...
 */
function draw_knife(data) {
    if (data.error == 1) {
        console.log("Вы мертвы, а значит не можете пользоваться ножом");
        console.log("Повторите попытку");
        CURRENT_STATE = STATE_5__send_signal;
    } else {
        if ((data.is_here_enemy == 1) || (data.is_here_enemy == 2) || (data.is_here_enemy == 3) || (data.is_here_enemy == 4)) {
            console.log("В этой клетке есть враг!!!");
            // draw
            switch (data.is_here_enemy) {
                case 1: {
                    console.log("Вы убили врага");
                    // draw
                    break;
                }
                case 2: {
                    console.log("Вы ранили врага: у него 25% здоровья");
                    // draw
                    break;
                }
                case 3: {
                    console.log("Вы ранили врага: у него 50% здоровья");
                    // draw
                    break;
                }
                case 4: {
                    console.log("Вы ранили врага: у него 75% здоровья");
                    // draw
                    break;
                }
            }
        }
        CURRENT_STATE = STATE_4__sleep;
    }
}

/* Функция отрисовки установки бомбы.
 * Обрабатывает:
 * 1) ...
 */
function draw_bomb(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                console.log("Вы мертвы, а значит не можете установить бомбу");
                console.log("Повторите попытку");
                // draw                                  
                break;                                    
            }
            case 2: {
                console.log("Сюда ставить бомбу нельзя");
                console.log("Повторите попытку");
                // draw                                   
                break; 
            }
            case 3: {
                console.log("У вас нет ни одной бомбы");
                console.log("Повторите попытку");
                // draw
                break; 
            }
        }
        CURRENT_STATE = STATE_5__send_signal; 
    } else {
        if (data.on_wall[0] == 1) {
            console.log("Клетка [" + data.on_wall[1] + ", " + data.on_wall[2] + "] взорвана!!!");
            // draw
        } else if (data.on_ground[0] == 1) {
            console.log("Бомба в клетке [" + data.on_ground[1] + ", " + data.on_ground[2] + "] установлена!!!");
            // draw
        }
        CURRENT_STATE = STATE_4__sleep;
    }   
}


/* Функция отрисовки установки бетонного блока.
 * Обрабатывает:
 * 1) ...
 */
function draw_concrete(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                console.log("Вы мертвы, а значит не можете установить блок цемента");
                console.log("Повторите попытку");
                // draw
                break;                                    
            }
            case 2: {
                console.log("Сюда ставить блок цемента нельзя");
                console.log("Повторите попытку");
                // draw                               
                break; 
            }
            case 3: {
                console.log("У вас нет ни одного блока цемента");
                console.log("Повторите попытку");
                // draw                              
                break; 
            }                                
        }
        CURRENT_STATE = STATE_5__send_signal;
    } else {
        console.log("Цемент в клетке [" + data.on_ground[1] + ", " + data.on_ground[2] + "] установлен!!!");
        // draw
        CURRENT_STATE = STATE_4__sleep;     
    }     
}

/* Функция отрисовки использования аптечки.
 * Обрабатывает:
 * 1) ...
 */
function draw_aid(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                console.log("Вы мертвы, а значит не можете использовать аптечку");
                console.log("Повторите попытку");
                // draw
                break;                                    
            }
            case 2: {
                console.log("У вас нет ни одной аптечки");
                console.log("Повторите попытку");
                // draw                              
                break; 
            }                              
        }
        CURRENT_STATE = STATE_5__send_signal;                                   
    } else {
        if (now_aid == 1) {
            console.log("Вы использовали аптечку. Теперь ваше здоровье - 50%");
            // draw
        }
        if (now_aid == 2) {
            console.log("Вы использовали аптечку. Теперь ваше здоровье - 75%");
            // draw
        }
        if (now_aid == 3) {
            console.log("Вы использовали аптечку. Теперь ваше здоровье - 100%");
            // draw
        }
        CURRENT_STATE = STATE_4__sleep;
    } 
}

/* ------------------------------------------------------------------ */
