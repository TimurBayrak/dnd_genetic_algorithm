import json


class Armor:
    """An Armor represents the json_files or shield of a character"""
    name: str
    base_armor: int
    category: str
    cost: int
    stealth_disadvantage: bool

    def __init__(self):
        """Initialize an instance of the class Armor"""

    def get_armor_from_file(self, armor: str):
        """get weapon informations from json file"""
        self.name = armor
        with open('equipment/armor/json_files/{}.json'.format(armor)) as f:
            ar = json.load(f)
        self.category = ar['armor_category']
        self.base_armor = ar['armor_class']['base']
        self.cost = ar['cost']['quantity']
        self.stealth_disadvantage = ar['stealth_disadvantage']

    def print_armor(self):
        """print the json_files"""
        print(
            "Armor: {} - base_armor: {} - category: {}".format(self.name, self.base_armor,
                                                               self.category))
