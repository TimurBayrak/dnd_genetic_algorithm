from typing import Dict
from character.character_values.AbilityScore import AbilityScore
from equipment.Equipment import Equipment
from classes.fighter.FightingStyle import FightingStyle
from race.Race import Race
from character.character_values.Skill import Skill

# 20 - 13 + 1 = dc difficult level
dc = 8


def get_attack_bonus(equipment: Equipment, fighting_style: FightingStyle, skills: Dict[str, Skill]) -> tuple:
    """get the attack bonus to hit with equipment, fighting style and ability"""
    attack_1 = skills['STR Weapons'].mod
    attack_2 = skills['STR Weapons'].mod
    if not equipment.second_weapon:
        if equipment.weapon.ranged:
            if fighting_style.name == 'archery':
                attack_1 = skills['DEX Weapons'].mod + 2
            else:
                attack_1 = skills['DEX Weapons'].mod
        if skills['DEX Weapons'].mod > skills['STR Weapons'].mod:
            if equipment.weapon.finesse:
                attack_1 = skills['DEX Weapons'].mod
    else:
        if skills['DEX Weapons'].mod > skills['STR Weapons'].mod:
            if equipment.weapon.finesse:
                attack_1 = skills['DEX Weapons'].mod
                if equipment.second_weapon.finesse:
                    attack_2 = skills['DEX Weapons'].mod
    return attack_1, attack_2


def get_base_weapon_damage(amount: int, dice: int, fighting_style: FightingStyle, equipment: Equipment) -> float:
    if fighting_style.name == 'great-weapon-fighting' and equipment.weapon.two_handed:
        if dice == 4:
            return 3 * amount
        if dice == 6:
            return 4.16 * amount
        elif dice == 8:
            return 5.25 * amount
        elif dice == 10:
            return 6.3 * amount
        elif dice == 12:
            return 7.33 * amount
    else:
        if dice == 4:
            return 2.5 * amount
        elif dice == 6:
            return 3.5 * amount
        elif dice == 8:
            return 4.5 * amount
        elif dice == 10:
            return 5.5 * amount
        elif dice == 12:
            return 6.5 * amount


class DamagePerRound:
    critical_chance: float
    base_damage_1: float
    base_damage_2: float
    hit_chance_1: float
    hit_chance_2: float
    additional_bonus_1: float
    additional_bonus_2: float

    dpr: float

    def __init__(self):
        self.dpr = 0

    def calc_dpr(self, race: Race, fighting_style: FightingStyle, equipment: Equipment, ability_scores: [AbilityScore],
                 skills: [Skill]):
        self.base_damage_2 = 0
        self.get_base_damage(equipment, fighting_style)
        self.get_hit_chance(get_attack_bonus(equipment, fighting_style, skills), 13, race)
        self.get_critical_chance(20, race)
        self.get_additional_bonus(equipment, fighting_style, ability_scores)
        if 'savage-attacks' in race.traits and not equipment.weapon.ranged:
            mult = 2
        else:
            mult = 1
        if not equipment.second_weapon:
            self.dpr = round((self.critical_chance * (self.base_damage_1 * mult) + self.hit_chance_1 * (
                    self.base_damage_1 + self.additional_bonus_1)), 3)
        else:
            damage_1 = round((self.critical_chance * (self.base_damage_1 * mult) + self.hit_chance_1 * (
                    self.base_damage_1 + self.additional_bonus_1)), 3)
            if fighting_style.name == 'two-weapon-fighting':
                damage_2 = round((self.critical_chance * (self.base_damage_2 * mult) + self.hit_chance_2 * (
                        self.base_damage_2 + self.additional_bonus_2)), 3)
            else:
                damage_2 = round(
                    (self.critical_chance * (self.base_damage_2 * mult) + self.hit_chance_2 * self.base_damage_2),
                    3)

            self.dpr = damage_1 + damage_2

    def get_base_damage(self, equipment: Equipment, fighting_style: FightingStyle):
        damage = equipment.weapon.damage
        damage = damage.split('d')
        amount = damage[0]
        dice = damage[1]

        self.base_damage_1 = get_base_weapon_damage(int(amount), int(dice), fighting_style, equipment)
        if equipment.second_weapon:
            damage = equipment.second_weapon.damage
            damage = damage.split('d')
            amount = damage[0]
            dice = damage[1]
            self.base_damage_2 = get_base_weapon_damage(int(amount), int(dice), fighting_style, equipment)

    def get_critical_chance(self, chance: int, race: Race):
        bonus = 0
        if 'lucky' in race.traits:
            bonus = 0.025
        if chance >= 20:
            self.critical_chance = round((0.05 + bonus), 3)
        elif chance >= 19:
            self.critical_chance = round((0.1 + bonus), 3)
        elif chance >= 18:
            self.critical_chance = round((0.15 + bonus), 3)

    def get_hit_chance(self, attack: tuple, ac: int, race: Race):
        if 'lucky' in race.traits:
            self.hit_chance_1 = round((((dc + attack[0]) / 20) + 0.025), 3)
            self.hit_chance_2 = round((((dc + attack[1]) / 20) + 0.025), 3)
        else:
            self.hit_chance_1 = round(((dc + attack[0]) / 20), 3)
            self.hit_chance_2 = round(((dc + attack[0]) / 20), 3)

    def get_additional_bonus(self, equipment: Equipment, fighting_style: FightingStyle,
                             ability_scores: Dict[str, AbilityScore]):
        bonus = 0
        additional_bonus_1 = ability_scores['STR'].mod
        additional_bonus_2 = ability_scores['STR'].mod
        if fighting_style.name == 'dueling' and not equipment.weapon.ranged and not equipment.weapon.two_handed \
                and not equipment.second_weapon:
            bonus = 2
        if equipment.weapon.ranged:
            additional_bonus_1 = ability_scores['DEX'].mod + bonus
        if ability_scores['DEX'].mod > ability_scores['STR'].mod:
            if equipment.weapon.finesse:
                additional_bonus_1 = ability_scores['DEX'].mod + bonus
            if equipment.second_weapon:
                if equipment.second_weapon.finesse:
                    additional_bonus_2 = ability_scores['DEX'].mod + bonus
        self.additional_bonus_1 = additional_bonus_1
        self.additional_bonus_2 = additional_bonus_2

    def print_dpr_function(self):
        """print the dpr calculation"""
        print('C = Critical Chance; D = Base Damage; H = Hit Chance; B = Additional Bonus')
        print('Attack 1 = C {} * D {} + H {} * (D {} + B {})'.format(self.critical_chance, self.base_damage_1,
                                                                     self.hit_chance_1,
                                                                     self.base_damage_1, self.additional_bonus_1))
        print('= DPR ==> {}'.format(self.dpr))
        if self.hit_chance_2 and self.base_damage_2:
            print('Attack 1 = C {} * D {} + H {} * (D {} + B {})'.format(self.critical_chance, self.base_damage_2,
                                                                         self.hit_chance_2,
                                                                         self.base_damage_2, self.additional_bonus_2))
            print('                         Attack_1 + Attack_2 = DPR ==> {}'.format(self.dpr))
