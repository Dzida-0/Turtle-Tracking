import json
import logging
from typing import Tuple
import re

from turtle_app.models import Turtle, TurtlePosition
from turtle_app.extensions import db


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


def parse_turtle_info() -> None:
    try:
        with open("data/raw/turtles_info.json", "r") as f:
            data = json.load(f)
        for turtle in data:
            turtle_id = turtle.get("id", "")
            name = turtle.get("name", "")
            last_position = turtle.get("point", "").get("coordinates", "")
            last_position = ','.join(map(str, [last_position[0], last_position[1]]))
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
                elif attribute.get("code", "") == "Project":
                    project_name = attribute.get("value", "")
                elif attribute.get("code", "") == "Biography":
                    biography = attribute.get("value", "")

                existing_turtle = Turtle.query.get(turtle_id)
                if existing_turtle:

                    existing_turtle.name = name
                    existing_turtle.last_position = last_position
                    existing_turtle.is_active = is_active
                    existing_turtle.turtle_sex = turtle_sex
                    existing_turtle.turtle_age = turtle_age
                    existing_turtle.length = length
                    existing_turtle.length_type = length_type
                    existing_turtle.width = width
                    existing_turtle.width_type = width_type
                    existing_turtle.project_name = project_name
                    existing_turtle.biography = biography
                    existing_turtle.description = description
                else:

                    new_turtle = Turtle(
                        id=turtle_id,
                        name=name,
                        last_position=last_position,
                        is_active=is_active,
                        turtle_sex=turtle_sex,
                        turtle_age=turtle_age,
                        length=length,
                        length_type=length_type,
                        width=width,
                        width_type=width_type,
                        project_name=project_name,
                        biography=biography,
                        description=description,
                    )
                    db.session.add(new_turtle)

        try:
            db.session.commit()
            logging.info("Turtles data parsed and saved successfully.")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving turtles to database: {e}")

    except FileNotFoundError:
        pass


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


