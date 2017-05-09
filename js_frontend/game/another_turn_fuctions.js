/* ------------------------------------------------------------------ */
/* Функции отрисовки очередного действия другого игрока */

/* Функция отрисовки перехода на новую клетку.
 * Обрабатывает:
 * 1) ...
 */

function draw_another_go(data) {
    if (data.error == 1) {
        alert("Игрок " + data.name + " пошёл не туда. Он переходит.");
        //draw
        CURRENT_STATE = STATE_6_show_another_turn;
    } else {
        if (data.wall[0] == 1) {
            alert("Игрок" + data.name + " упёрся в стену.");
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            }
        }
        if ((data.mine == 1) || (data.mine == 2) || (data.mine == 3)) {
            switch (data.mine) {
                case 1: {
                    alert("Игрок " + data.name + " убит на мине!");
                    break;
                }
                case 2: {
                    alert("Игрок " + data.name + " ранен на мине! У него 50 % здоровья");
                    break;
                }
                case 3: {
                    alert("Игрок " + data.name + " ранен на мине! У него 25 % здоровья");
                    break;
                }
            }
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            }
        }
        if (data.river[0] == 1) {
            alert("Игрок" + data.name + " поплыл по реке!");
            // draw
            CURRENT_STATE = STATE_4__sleep;
        }
        if ((data.aid == 1) || (data.aid == 2) || (data.aid == 3)) {
            switch (data.aid) {
                case 1: {
                    alert("Игрок " + data.name + " ожил");
                    // draw
                    break;
                }
                case 2: {
                    alert("У игрока " + data.name + " теперь 100% здоровья");
                    break;
                }
                case 3: {
                    alert("У игрока " + data.name + " плюс одна аптечка");
                    break;
                }
            }
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            }
        }
        if ((data.arm == 1) || (data.arm == 2)) {
            switch (data.arm) {
                case 1: {
                    console.log("У игрока " + data.name + " плюс один цемент");
                    alert("У игрока " + data.name + " плюс один цемент");
                    break;
                }
                case 2: {
                    console.log("У игрока " + data.name + " плюс одна бомба");
                    alert("У игрока " + data.name + " плюс одна бомба");
                    break;
                }
            }
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            }
        }       
        if ((data.bear == 1) || (data.bear == 2) || (data.bear == 3)) {
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
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            }
            CURRENT_STATE = STATE_4__sleep;
        }
        if (data.treasure == 1) {
            alert("Игрок " + data.name + " нашёл клад!\n       Мочи его!");
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            }            
        }
        if (data.metro[0] == 1) {
            alert("Игрок " + data.name + " воспользовался метро!");
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            } 
        }
        if (data.exit[0] == 1) {
            if (data.exit[1] == 1) {
                alert("Игрок " + data.name + " выиграл!");
                if (data.is_visible_from == 1) {
                    // draw
                }
                if (data.is_visible_to == 1) {
                    // draw
                }                
                CURRENT_STATE = FINAL__somebody_win; return;
            } else {
                alert("Игрок " + data.name + " попробовал уйти с карты! Но не смог...");
                if (data.is_visible_from == 1) {
                    // draw
                }
                if (data.is_visible_to == 1) {
                    // draw
                }  
            }
        }
        CURRENT_STATE = STATE_4__sleep;        
    }
}

/* Функция отрисовки удара ножом.
 * Обрабатывает:
 * 1) ...
 */
function another_draw_knife(data) {
    if (data.error == 1) {
        alert("Игрок " + name.data + " попробовал воспользоваться ножом,\n когда был мёртв. Он переходит.");
        // draw
        CURRENT_STATE = STATE_6_show_another_turn;
    } else {
        if ((data.are_you_injured == 1) || (data.are_you_injured == 2) || (data.are_you_injured == 3) || (data.are_you_injured == 4)) {
            switch (data.are_you_injured) {
                case 1: {
                    alert("Вы убиты игроком " + data.name + ". А жаль...");
                    // draw
                    break;
                }
                case 2: {
                    alert("Вы ранены игроком " + data.name + ". У вас осталось 25% здоровья.");
                    // draw
                    break;
                }
                case 3: {
                    alert("Вы ранены игроком " + data.name + ". У вас осталось 50% здоровья.");
                    // draw
                    break;
                }
                case 4: {
                    alert("Вы ранены игроком " + data.name + ". У вас осталось 75% здоровья.");
                    // draw
                    break;
                }
            }
        } else if ((data.is_here_enemy == 1) || (data.is_here_enemy == 2)) {
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
        } else if (data.is_here_enemy == 0) {
            alert("Игрок " + data.name + " ударил ножом, но никого не задел.");
            if (data.is_visible_knife == 1) {
                // draw
            } 
        }
        CURRENT_STATE = STATE_4__sleep;
    }
}

/* Функция отрисовки установки бомбы.
 * Обрабатывает:
 * 1) ...
 */
function another_draw_bomb(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                alert("Игрок " + data.name + " попробовал установить бомбу, когда был мёртв. Он переходит.");
                // draw
                break;                                    
            }
            case 2: {
                alert("Игрок " + data.name + " попробовал установить бомбу не туда. Он переходит.");
                // draw                                  
                break; 
            }
            case 3: {
                alert("Игрок " + data.name + " попробовал установить бомбу, когда у него её не было. Он переходит.");
                // draw                                   
                break; 
            }
        }
        CURRENT_STATE = STATE_6_show_another_turn; 
    } else {
        if (data.on_wall[0] == 1) {
            alert("Игрок " + data.name + " взовал стену!");
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            }
        } else if (data.on_ground[0] == 1) {
            alert("Игрок " + data.name + " заложил бомбу!");
            if (data.is_visible_from == 1) {
                // draw
            }
            if (data.is_visible_to == 1) {
                // draw
            } 
        }
        CURRENT_STATE = STATE_4__sleep;
    }   
}

/* Функция отрисовки установки бетонного блока.
 * Обрабатывает:
 * 1) ...
 */
function another_draw_concrete(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                alert("Игрок " + data.name + " попробовал установить блок цемента, когда был мёртв. Он переходит.");
                // draw                                 
                break;                                    
            }
            case 2: {
                alert("Игрок " + data.name + " попробовал установить блок цемента не туда. Он переходит.");
                // draw                                
                break; 
            }
            case 3: {
                alert("Игрок " + data.name + " попробовал установить блок цемента, когда у него его не было. Он переходит.");
                // draw
                break; 
            }                                
        }
        CURRENT_STATE = STATE_6_show_another_turn;
    } else {
        alert("Игрок " + data.name + " установил блок цемента!");
        if (data.is_visible_from == 1) {
            // draw
        }
        if (data.is_visible_to == 1) {
            // draw
        }         
        CURRENT_STATE = STATE_4__sleep;     
    }     
}

/* Функция отрисовки использования аптечки.
 * Обрабатывает:
 * 1) ...
 */
function another_draw_aid(data) {
    if (data.error != 0) {
        switch (data.error) {
            case 1: {
                alert("Игрок " + data.name + " попробовал воспользоваться аптечкой, когда был мёртв. Он переходит.");
                // draw
                break;                                    
            }
            case 2: {
                alert("Игрок " + data.name + " попробовал воспользоваться аптечкой, когда у него её не было. Он переходит.");
                // draw                                
                break; 
            }                                
        }
        CURRENT_STATE = STATE_6_show_another_turn; 
    } else {
        alert("Игрок " + data.name + " воспользовался аптечкой.");
        if (data.is_visible_aid == 1) {
            // draw
        }
        CURRENT_STATE = STATE_4__sleep;
    } 
}

/* ------------------------------------------------------------------ */
