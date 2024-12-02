import json
import logging
import os
from typing import Optional, Dict

from time import sleep
# TO DO
# adult kid

def remove_HTML_elements(text:str) -> str:
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
        if start > 0 and stop > 0:
            new_text = text[:start]
            if text[start-1] != " ":
                new_text += " "
            new_text += text[stop+1:]
            text = new_text
            h = True
    return text


def parse_description(description: str) -> None:
    """

    :param description:
    :return:
    """
    description = description.replace(".", "")
    description = description.replace(",", "")
    description = remove_HTML_elements(description)
    d = description.split(" ")

    she_count = sum(d.count(i) for i in["she","She","female","Female","her","Her"])
    he_count = sum(d.count(i) for i in["he","He","male","Male","his","His"])
    turtle_sex = None
    if she_count > he_count >= 0:
        turtle_sex = "Female"
    elif he_count > she_count >= 0:
        turtle_sex = "Male"

    turtle_age = None
    adult_count = sum(d.count(i) for i in["adult","Adult"])
    kid_count = sum(d.count(i) for i in ["immature", "juvenile","sub-adult"])
    if adult_count > kid_count >= 0:
        turtle_age = "Adult"
    elif kid_count > adult_count >= 0:
        turtle_age = "Sub-adult"

    while "cm" in d:
        e = d.index("cm")
        dd = d[e:]
        if "length" in dd:
            f = dd.index("length")
            if f <= 5:
                length = d[e - 1]
                length_type = ""
                if "curved" in d[e:e + f]:
                    length_type = "curved"
                elif "straight" in d[e:e + f]:
                    length_type = "straight"
                print(length, length_type, "length")
        elif "width" in dd:
            f = dd.index("width")
            if f <= 5:
                width = d[e - 1]
                width_type = ""
                if any(substr in d[e:e + f] for substr in ["curved", "CCL"]):
                    width_type = "curved"
                elif any(substr in d[e:e + f] for substr in ["straight", "SCL"]):
                    width_type = "straight"
                print(width, width_type, "width")
        d.remove(d[e])


def parse_turtle_info() -> None:
    try:
        with open("../../data/raw/turtles_info.json", "r") as f:
            data = json.load(f)
        for turtle in data:
            id = turtle.get("id", "")
            name = turtle.get("name", "")
            last_position = turtle.get("point", "").get("coordinates", "")
            for attribute in turtle.get("attributes", []):
                if attribute.get("code", "") == "is_active":
                    active_turtle = attribute.get("value", "")
                elif attribute.get("code", "") == "Description":
                    description = attribute.get("value", "")
                    if description is not None:
                        parse_description(description)
                        print(description)
                        print()
                elif attribute.get("code", "") == "Project":
                    project_name = attribute.get("value", "")
                elif attribute.get("code", "") == "Biography":
                    biography = attribute.get("value", "")

    except FileNotFoundError:
        pass


if __name__ == '__main__':
    parse_turtle_info()

