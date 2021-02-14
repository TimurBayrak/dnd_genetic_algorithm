import json


class Weapon:
    """A Weapon represents the weapon and/or the second weapon from a character"""
    name: str
    damage: str
    cost: int
    finesse: bool
    ranged: bool
    two_handed: bool
    light: bool

    def __init__(self):
        """initialize an instance of the class Weapon"""

    def get_weapon_from_file(self, weapon: str):
        """get weapon informations from json file"""
        self.name = weapon
        # load json file
        with open('equipment/weapon/json_files/{}.json'.format(weapon)) as f:
            w = json.load(f)
        # get all properties for the weapon

        self.finesse = False
        self.ranged = False
        self.two_handed = False
        self.light = False
        self.damage = w['damage']['damage_dice']
        self.cost = w['cost']['quantity']
        for i in w['properties']:
            if i['index'] == 'finesse':
                self.finesse = True
            elif i['index'] == 'ammunition':
                self.ranged = True
            elif i['index'] == 'two-handed':
                self.two_handed = True
            elif i['index'] == 'light':
                self.light = True

    def print_weapon(self):
        """print the weapon"""
        print("Weapon: {} - damage: {}".format(self.name, self.damage))
