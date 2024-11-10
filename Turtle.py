import pandas as pd


class Turtle:
    def __init__(self, turtle_data):
        self.turtle_movement = turtle_data[0]
        self.turtle_id = turtle_data[1]['id']
        self.turtle_name = turtle_data[1]['name']
        self.turtle_species = turtle_data[1]['species']
        self.turtle_project = turtle_data[1]['project']
        self.turtle_description = turtle_data[1]['description']

        ###
        self.release_point = (turtle_data[0].iloc[len(turtle_data[0]) - 1]['latitude'],
                              turtle_data[0].iloc[len(turtle_data[0]) - 1]['longitude'])

    def _parse_description(self, description: str):
        description = description.split('.')
        for des in description:
            self._adult = False if des.count('sub - adult') else True
            if des.count('cm'): print('cm', des)
            if des.count('inc'): print('inc', des)
            if des.count('kg'): print('kg', des)
            if des.count('pound'): print('pound', des)
