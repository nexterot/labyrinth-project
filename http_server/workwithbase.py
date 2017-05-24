import sqlite3

def create_base():
    conn = sqlite3.connect('labyrinthdb.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE users (login text, password text, email text, phone text, age text, gender text, bomb int, concrete int, aid int )''')
    
    conn.commit()
    c.close()
    conn.close()

def show_base():
    conn = sqlite3.connect('labyrinthdb.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM users''')
    tick = c.fetchall()
    
    c.close()
    conn.close()
    return tick
    
def add_user(login, pswd, email, phone, age, gender):
    conn = sqlite3.connect('labyrinthdb.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE login=?', (login,))
    tick = c.fetchone()
    if tick:
        c.close()
        conn.close()
        return 0
    
    c.execute('SELECT * FROM users WHERE email=?', (email,))
    tick = c.fetchone()
    if tick:
        c.close()
        conn.close()
        return 1
    
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (login, pswd, email, phone, age, gender, 0, 0, 0))
    conn.commit()
    
    c.execute('SELECT * FROM users WHERE login=? and password=?', (login, pswd))
    tick = c.fetchone()
    
    c.close()
    conn.close()
    return tick

def auth_user(login, pswd):
    conn = sqlite3.connect('labyrinthdb.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE login=? and password=?', (login, pswd))
    tick = c.fetchone()
    
    if tick:
        c.close()
        conn.close()
        return tick
    
    c.close()
    conn.close()
    return 0

def begin_game(login):
    conn = sqlite3.connect('labyrinthdb.db')
    c = conn.cursor()
    
    c.execute('SELECT bomb, concrete, aid FROM users WHERE login=?', (login,))
    tick = c.fetchone()
    
    c.close()
    conn.close()
    return tick