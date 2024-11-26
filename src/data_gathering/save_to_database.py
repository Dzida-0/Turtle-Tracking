import json
import logging
import sqlite3


def save_new_turtles(db_path: str, json_file_path: str)-> bool:
    try:
        with open(json_file_path, 'r') as f:
            turtles_data = json.load(f)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for turtle in turtles_data:
            cursor.execute("""
                  INSERT OR REPLACE INTO Turtles 
                  (id, name, species, last_move_datetime, distance_from_release, avg_speed_from_release, 
                   time_from_release, time_from_last_move, time_tracked, description, project, biography)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              """, (
                turtle.get("id"),
                turtle.get("name"),
                turtle.get("species"),
                turtle.get("last_move_datetime"),
                turtle.get("distance_from_release"),
                turtle.get("avg_speed_from_release"),
                turtle.get("time_from_release"),
                turtle.get("time_from_last_move"),
                turtle.get("time_tracked"),
                turtle.get("description"),
                turtle.get("project"),
                turtle.get("biography"),
            ))

        conn.commit()
        conn.close()
        return True
    except (sqlite3.Error, json.JSONDecodeError) as e:
        logging.error(f"Error inserting turtles data: {e}")
        return False