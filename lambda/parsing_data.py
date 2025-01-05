import os
from typing import Tuple
import re

from download import download_image,download_turtles_positions
from turtle_app.models import Turtle, TurtlePosition
from turtle_app.extensions import db
import json
import logging
import sqlite3






def parse_turtle_info():
    ret = {}
    try:
        with open(os.path.join(f"{config.DevelopmentConfig.STORAGE_PATH}/json", f'turtles_info.json'), "r") as f:
            data = json.load(f)

        # Establish database connection
        db_path = config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Ensure the turtles table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turtle (
                id TEXT PRIMARY KEY,
                name TEXT,
                last_position TEXT,
                is_active TEXT,
                turtle_sex TEXT,
                turtle_age TEXT,
                length REAL,
                length_type TEXT,
                width REAL,
                width_type TEXT,
                project_name TEXT,
                biography TEXT,
                description TEXT
            )
        """)

        for turtle in data:
            turtle_id = turtle.get("id", "")
            name = turtle.get("name", "")

            # Safely extract last_position
            point = turtle.get("point")
            if point and isinstance(point, dict):
                coordinates = point.get("coordinates", [])
                last_position = ','.join(map(str, [coordinates[0], coordinates[1]])) if len(coordinates) == 2 else None
            else:
                last_position = None

            is_active = None
            turtle_sex = None
            turtle_age = None
            length = None
            length_type = None
            width = None
            width_type = None
            project_name = None
            biography = None
            description = None

            for attribute in turtle.get("attributes", []):
                if attribute.get("code", "") == "is_active":
                    is_active = attribute.get("value", "")
                elif attribute.get("code", "") == "Description":
                    description = attribute.get("value", "")
                    if description is not None:
                        turtle_sex, turtle_age, length, length_type, width, width_type = parse_description(description)
                        description = remove_HTML_elements(description)
                elif attribute.get("code", "") == "Project":
                    project_name = attribute.get("value", "")
                elif attribute.get("code", "") == "Biography":
                    biography = attribute.get("value", "")

            # Safely extract image URL
            image = turtle.get("image")
            if image and isinstance(image, dict):
                urls = image.get("urls", {})
                picture_url = urls.get("origin", None)
            else:
                picture_url = None

            ret[turtle_id] = picture_url


            # Check if the turtle already exists
            cursor.execute("SELECT id FROM turtle WHERE id = ?", (turtle_id,))
            existing_turtle = cursor.fetchone()

            if existing_turtle:
                # Update existing turtle
                cursor.execute("""
                    UPDATE turtle
                    SET name = ?, last_position = ?, is_active = ?, turtle_sex = ?,
                        turtle_age = ?, length = ?, length_type = ?, width = ?,
                        width_type = ?, project_name = ?, biography = ?, description = ?
                    WHERE id = ?
                """, (
                    name, last_position, is_active, turtle_sex,
                    turtle_age, length, length_type, width,
                    width_type, project_name, biography, description, turtle_id
                ))
            else:
                # Insert new turtle
                cursor.execute("""
                    INSERT INTO turtle (
                        id, name, last_position, is_active, turtle_sex,
                        turtle_age, length, length_type, width, width_type,
                        project_name, biography, description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    turtle_id, name, last_position, is_active, turtle_sex,
                    turtle_age, length, length_type, width, width_type,
                    project_name, biography, description
                ))

        # Commit changes
        conn.commit()
        logging.info("Turtles lambda parsed and saved successfully.")
        return ret

    except FileNotFoundError:
        logging.error("Turtles info JSON file not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()


def parse_turtle_positions(turtle_id: int,) -> None:
    try:
        # Open the JSON file
        with open(os.path.join(f"{config.DevelopmentConfig.STORAGE_PATH}/json", f'turtles{turtle_id}_positions.json'), "r") as f:
            data = json.load(f)
            if "results" in data:
                # Establish database connection
                db_path = config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Ensure the turtle_positions table exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS turtle_pos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        turtle_id INTEGER,
                        x REAL,
                        y REAL
                    )
                """)

                for position in data.get('results'):
                    if "lambda" in position:
                        position_data = position.get("lambda", {})
                        x = position_data.get("Lat")
                        y = position_data.get("Lng")

                        # Insert the position into the database
                        cursor.execute("""
                            INSERT INTO turtle_pos (turtle_id, x, y)
                            VALUES (?, ?, ?)
                        """, (turtle_id, x, y))

                # Commit the transaction
                conn.commit()
                logging.info(f"Turtle positions for turtle_id={turtle_id} parsed and saved successfully.")
    except FileNotFoundError:
        logging.warning(f"File for turtle_id={turtle_id} not found.")
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()  # Rollback in case of any error
        logging.error(f"Error processing turtle positions for turtle_id={turtle_id}: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
