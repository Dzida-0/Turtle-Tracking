import os
from typing import Tuple
import re

import config
from download_data import download_image
from turtle_app.models import Turtle, TurtlePosition
from turtle_app.extensions import db
import json
import logging
import sqlite3

def remove_HTML_elements(text: str) -> str:
    """
    Remove unnecessary HTML elements form text.
    :param text: Text
    :return: Text
    """
    text = text.replace("&nbsp;", " ")
    h = True
    while h:
        h = False
        start = text.find('<')
        stop = text.find('>')
        if start >= 0 and stop >= 0:
            new_text = text[:start]
            if text[start - 1] != " ":
                new_text += " "
            new_text += text[stop + 1:]
            text = new_text
            h = True
    return re.sub(r'\s+', ' ', text)


def parse_description(description: str) -> Tuple:
    """

    :param description:
    :return:
    """
    description = description.replace(".", "")
    description = description.replace(",", "")
    description = remove_HTML_elements(description)
    d = description.split(" ")

    she_count = sum(d.count(i) for i in ["she", "She", "female", "Female", "her", "Her"])
    he_count = sum(d.count(i) for i in ["he", "He", "male", "Male", "his", "His"])
    turtle_sex = None
    if she_count > he_count >= 0:
        turtle_sex = "Female"
    elif he_count > she_count >= 0:
        turtle_sex = "Male"

    turtle_age = None
    adult_count = sum(d.count(i) for i in ["adult", "Adult"])
    kid_count = sum(d.count(i) for i in ["immature", "juvenile", "sub-adult"])
    if adult_count > kid_count >= 0:
        turtle_age = "Adult"
    elif kid_count > adult_count >= 0:
        turtle_age = "Sub-adult"

    length = None
    length_type = None
    width = None
    width_type = None
    while "cm" in d:
        e = d.index("cm")
        dd = d[e:]
        if "length" in dd:
            f = dd.index("length")
            if f <= 5:
                length = d[e - 1]
                if "curved" in d[e:e + f]:
                    length_type = "curved"
                elif "straight" in d[e:e + f]:
                    length_type = "straight"
        elif "width" in dd:
            f = dd.index("width")
            if f <= 5:
                width = d[e - 1]
                if any(substr in d[e:e + f] for substr in ["curved", "CCL"]):
                    width_type = "curved"
                elif any(substr in d[e:e + f] for substr in ["straight", "SCL"]):
                    width_type = "straight"
        d.remove(d[e])

    return turtle_sex, turtle_age, length, length_type, width, width_type


def parse_turtle_info():  # Path to your SQLite database file

    try:
        with open(os.path.join(f"{config.DevelopmentConfig.STORAGE_PATH}/json", f'turtles_info.json'), "r") as f:
            data = json.load(f)

        # Establish database connection
        conn = sqlite3.connect(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
        cursor = conn.cursor()

        # Ensure the turtles table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turtles (
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
            last_position = turtle.get("point", {}).get("coordinates", [])
            last_position = ','.join(map(str, [last_position[0], last_position[1]])) if last_position else None

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

            picture_url = turtle.get("image", {}).get("urls", {}).get("origin", None)
            if picture_url:
                download_image(picture_url, turtle_id)

            # Check if the turtle already exists
            cursor.execute("SELECT id FROM turtles WHERE id = ?", (turtle_id,))
            existing_turtle = cursor.fetchone()

            if existing_turtle:
                # Update existing turtle
                cursor.execute("""
                    UPDATE turtles
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
                    INSERT INTO turtles (
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
        logging.info("Turtles data parsed and saved successfully.")

    except FileNotFoundError:
        logging.error("Turtles info JSON file not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

def parse_turtle_positions(turtle_id) -> None:
    try:
        with open(f"data/raw/turtles{turtle_id}_positions.json", "r") as f:
            data = json.load(f)
            if "results" in data:
                for position in data.get('results'):
                    if "data" in position:
                        data = position.get("data", "")

                        new_turtle_position = TurtlePosition(
                            turtle_id=turtle_id,
                            x=data.get("Lat"),
                            y=data.get("Lng")
                        )
                        db.session.add(new_turtle_position)

        try:
            db.session.commit()
            logging.info("Turtles data parsed and saved successfully.")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving turtles to database: {e}")

    except FileNotFoundError:
        pass
