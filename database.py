import sqlite3

connect = sqlite3.connect('authentication.db')
c = connect.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT, password TEXT)')

def add_user(username, password):
    c.execute('INSERT INTO user VALUES(?,?)', (username,password))
    connect.commit()

def login_user(username, password):
    c.execute('SELECT * FROM user WHERE username=? AND password=?' (username,password))
    data = c.fetchall()
    return data 

def view_all():
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    return data 




