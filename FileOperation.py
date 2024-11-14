import sqlite3
import pandas as pd


class FileOperation:
    """

    """
    def __init__(self):
        self.path = "TurtlesDataBase.db"

    def if_exist(self) -> None:
        """

        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Turtles (
                        id INTEGER PRIMARY KEY, 
                        name TEXT,
                        species TEXT,
                        last_move_datetime TEXT,
                        distance_from_release TEXT,
                        avg_speed_from_release TEXT,
                        time_from_release TEXT,
                        time_from_last_move TEXT,
                        time_tracked TEXT,
                        description TEXT,
                        project TEXT,
                        biography TEXT
                        )"""
        )
        conn.commit()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Positions (
            id INTEGER PRIMARY KEY,
             latitude DOUBLE,
             longitude DOUBLE,
             distance DOUBLE,
             duration DOUBLE,
             direction TEXT,
             time TEXT
             )"""
        )
        conn.commit()
        conn.close()

    def insert_turtle(self,turtle) -> bool:
        """

        :param turtle:
        :return:
        """
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO Turtles (id,name,species,last_move_datetime,distance_from_release,avg_speed_from_release,
                time_from_release,time_from_last_move,time_tracked,description,project,biography) VALUES
                 (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?)""",
                turtle,
            )
            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError as e:
            print(f"Integrity error occurred: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational error occurred: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    def insert_turtle_movement(self, data: pd.DataFrame) -> bool:
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Positions ( id,latitude ,longitude,distance ,duration,direction,time) VALUES (?, ?,?,?,?,?,?)""", data
        )
        conn.commit()
        conn.close()

    def get_turtles(self) -> pd.DataFrame:
        pass
