import sqlite3
import pandas as pd

class FileOperation:

    def __init__(self):
        self.path = 'TurtlesDataBase.db'

    def if_exist(self) -> None:
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Turtles (id INTEGER PRIMARY KEY, name TEXT)''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Positions (id INTEGER PRIMARY KEY, name TEXT)''')
        conn.commit()
        conn.close()

    def insert_turtle(self)->bool:
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Turtles (id,name) VALUES (?, ?)''', ('Alice', 30))
        conn.commit()
        conn.close()

    def insert_turtle_movment(self,data: pd.DataFrame)-> bool:
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Positions (name, age) VALUES (?, ?)''', ('Alice', 30))
        conn.commit()
        conn.close()

    def get_turtles(self)->pd.DataFrame:
        pass