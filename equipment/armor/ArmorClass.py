from character.character_values.AbilityScore import AbilityScore
from equipment.Equipment import Equipment
from classes.fighter.FightingStyle import FightingStyle


def get_dexterity_bonus(equipment: Equipment, dexterity: AbilityScore) -> int:
    """return the dexterity bonus for the given json_files
    light json_files -> full dex
    medium -> max 2 dex
    heavy -> no dex
    """
    if equipment.armor.category == 'Light':
        return dexterity.mod
    elif equipment.armor.category == 'Medium':
        if dexterity.mod <= 2:
            return dexterity.mod
        else:
            return 2
    elif equipment.armor.category == 'Heavy':
        return 0


class ArmorClass:
    """the class ArmorClass is the character calculated AC for the Fitnessfunction"""
    base_armor: int
    dexterity_bonus: int
    shield: int
    other_bonus: int
    ac: int

    def __init__(self):
        """initialize an instance of the class ArmorClass"""

    def set_armor_class(self, equipment: Equipment, fighting_style: FightingStyle, dexterity: AbilityScore):
        self.dexterity_bonus = get_dexterity_bonus(equipment, dexterity)
        self.base_armor = equipment.armor.base_armor
        self.set_shield(equipment)
        self.set_fighting_style(fighting_style)
        self.calc_armor_class()

    def set_shield(self, equipment: Equipment):
        """set the shield mod for 2 if the character wields a shield"""
        self.shield = 0
        if equipment.shield:
            self.shield = 2

    def set_fighting_style(self, fighting_style: FightingStyle):
        """set other bonus +1 if the fighting style is defense"""
        self.other_bonus = 0
        if fighting_style.name == 'defense':
            self.other_bonus = 1

    def calc_armor_class(self):
        """calculate the json_files class with all variables"""
        self.ac = self.base_armor + self.dexterity_bonus + self.shield + self.other_bonus

    def print_armor_class(self):
        """print the Armor Class"""
        print('Base Armor + Dexterity Bonus + Shield + Other Bonus = AC (Armor Class)')
        print('{} + {} + {} + {} = {}'.format(self.base_armor, self.dexterity_bonus, self.shield, self.other_bonus,
                                              self.ac))
