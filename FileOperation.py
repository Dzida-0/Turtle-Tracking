import sqlite3



class FileOperation:

    def __init__(self):
        self.path = 'TurtlesDataBase.db'

    def if_exist(self)->bool:
        conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Turtles (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        conn.commit()
        conn.close()
        return True

    def insert(self):
        cursor.execute('''INSERT INTO users (name, age) VALUES (?, ?)''', ('Alice', 30))


