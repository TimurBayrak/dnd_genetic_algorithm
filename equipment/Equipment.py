from equipment.armor.Armor import Armor
from equipment.weapon.Weapon import Weapon


class Equipment:
    """The class Equipment combines a weapon, an json_files, a shield and a second weapon"""
    weapon: Weapon
    second_weapon: Weapon = None
    armor: Armor
    shield: Armor = None

    def __init__(self):
        """Initialize an instance of the class Equipment"""
        self.weapon = Weapon()
        self.armor = Armor()

    def set_equipment(self, armor: int, weapon: int, shield: int, second_weapon: int):
        armor_name = self.armor_mapping(armor)
        weapon_name = self.weapon_mapping(weapon)
        self.armor.get_armor_from_file(armor_name)
        self.weapon.get_weapon_from_file(weapon_name)
        if shield != 0:
            shield_name = 'shield'
            self.shield = Armor()
            self.shield.get_armor_from_file(shield_name)
        else:
            if self.shield:
                del self.shield
        if second_weapon == 13:
            if self.second_weapon:
                del self.second_weapon
        elif second_weapon != 13:
            second_weapon_name = self.weapon_mapping(second_weapon)
            self.second_weapon = Weapon()
            self.second_weapon.get_weapon_from_file(second_weapon_name)

    def armor_mapping(self, armor: int) -> str:
        """map the DNA number to the correct string to load the json file"""
        if armor == 0:
            return 'leather'
        elif armor == 1:
            return 'chain-shirt'
        elif armor == 2:
            return 'ring-mail'
        elif armor == 3:
            return 'chain-mail'
        elif armor == 4:
            return 'scale-mail'
        elif armor == 5:
            return 'studded-leather'

    def weapon_mapping(self, weapon: int) -> str:
        """map the DNA number to the correct string to load the json file"""
        if weapon == 0:
            return 'shortsword'
        elif weapon == 1:
            return 'longsword'
        elif weapon == 2:
            return 'greatsword'
        elif weapon == 3:
            return 'halberd'
        elif weapon == 4:
            return 'longbow'
        elif weapon == 5:
            return 'greataxe'
        elif weapon == 6:
            return 'crossbow-heavy'
        elif weapon == 7:
            return 'battleaxe'
        elif weapon == 8:
            return 'handaxe'
        elif weapon == 9:
            return 'light-hammer'
        elif weapon == 10:
            return 'maul'
        elif weapon == 11:
            return 'glaive'
        elif weapon == 12:
            return 'rapier'

    def print_equipment(self):
        """print the Eqipment"""
        self.weapon.print_weapon()
        self.armor.print_armor()
        if self.second_weapon:
            self.second_weapon.print_weapon()
        if self.shield:
            self.shield.print_armor()
