
class Turtle:
    def __init__(self,turtle_data):
        self._turtle_movement = turtle_data[1]
        self._turtle_id = turtle_data[0]['id']
        self._turtle_name = turtle_data[0]['name']
        self._turtle_species = turtle_data[0]['species']
        self._turtle_project = turtle_data[0]['project']
        self._turtle_description = turtle_data[0]['description']
        self._parse_description(turtle_data[0]['description'])

    def _parse_description(self,description:str ):
        description = description.split('.')
        for des in description:
            self._adult = False if des.count('sub - adult') else True
            if des.count('cm'): print('cm',des)
            if des.count('inc'): print('inc',des)
            if des.count('kg'): print('kg',des)
            if des.count('pound'): print('pound',des)


"""
    An
    adult
    female
    loggerhead
    sea
    turtle
    to
    be
    released
    with a satellite transmitter on July 30, 2017 from the Archie Carr National Wildlife Refuge, Florida.
    She measured 89.0 cm curved carapace (shell) length and 84.2 cm curved carapace width.
    Caroline is taking part in the 2017 Tour de Turtles and was named by her sponsor

"""