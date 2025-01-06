import json
import logging
import re
from typing import Tuple


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


def parse_turtle_info(database_handler, storage_handler):
    """
    Parse turtle information from a JSON file and update or insert records in the database.

    :param database_handler: Instance of DatabaseHandler to interact with the database.
    :param storage_handler: Instance of StorageHandler to interact with the storage system.
    :return: Dictionary mapping turtle IDs to their picture URLs.
    """
    ret = {}

    try:
        # Load turtle info JSON from storage
        turtles_info_path = "json/turtles_info.json"
        content = storage_handler.load_file(turtles_info_path)
        data = json.loads(content)
        # Ensure the turtles table exists
        database_handler.execute_query("""
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
                        # Parse description for other attributes
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
            existing_turtle = database_handler.fetch_one("SELECT id FROM turtle WHERE id = ?", (turtle_id,))

            if existing_turtle:
                # Update existing turtle
                database_handler.execute_query("""
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
                database_handler.execute_query("""
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

        logging.info("Turtle information parsed and saved successfully.")

    except FileNotFoundError:
        logging.error("Turtles info JSON file not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        database_handler.rollback()
    finally:
        return ret


def parse_turtle_positions(turtle_id: int,database_handler, storage_handler) -> None:

    try:
        # Load turtle info JSON from storage
        turtles_info_path = f"json/turtles{turtle_id}_positions.json"
        content = storage_handler.load_file(turtles_info_path)
        data = json.loads(content)
        # Ensure the turtles table exists
        database_handler.execute_query("""
                    CREATE TABLE IF NOT EXISTS turtle_pos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        turtle_id INTEGER,
                        x REAL,
                        y REAL,
                        date REAL
                    )
                """)

        for position in data.get('results'):
            if "data" in position:
                position_data = position.get("data", {})
                x = position_data.get("Lat")
                y = position_data.get("Lng")
                date = position_data.get("Collected")

                # Insert the position into the database
                database_handler.execute_query("""
                                 INSERT INTO turtle_pos (turtle_id, x, y,date)
                                 VALUES (?, ?, ?,?)
                             """, (turtle_id, x, y, date))


    except FileNotFoundError:
        logging.error("Turtles info JSON file not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        database_handler.rollback()
