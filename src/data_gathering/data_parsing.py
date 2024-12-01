import json
import logging
import os
from typing import Optional, Dict
def parse_description(description:str)-> None:
    d = description.split(" ")
    while "cm" in d:
        e = d.index("cm")
        dd = d[e:]
        if "length" in dd:
            f = dd.index("length")
            if f <= 5:
                length = float(d[e-1])
                print(length)
        print(d[e-1],d[e],d[e+1],d[e+2],d[e+3],d[e+4],d[e+5])
        d.remove(d[e])
def parse_turtle_info()-> None:

    try:
        with open("../../data/raw/turtles_info.json", "r") as f:
            data = json.load(f)
        for turtle in data:
            id = turtle.get("id","")
            name = turtle.get("name","")
            last_position = turtle.get("point","").get("coordinates","")
            for attribute in turtle.get("attributes",[]):
                if attribute.get("code","") == "is_active":
                    active_turtle = attribute.get("value","")
                elif attribute.get("code","") == "Description":
                    description = attribute.get("value","")
                    if len(description) > 1:
                        parse_description(description)
                        #print(description)
                        print()
                elif attribute.get("code", "") == "Project":
                    project_name = attribute.get("value", "")
                elif attribute.get("code", "") == "Biography":
                    biography = attribute.get("value", "")


        print(data[40])


    except FileNotFoundError:
        pass


if __name__ == '__main__':
    parse_turtle_info()