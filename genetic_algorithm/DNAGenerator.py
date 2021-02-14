import copy
import random
from typing import List, Dict
from genetic_algorithm.DNA import DNA


def costs_mapping(score: int) -> int:
    """returns the costs of the given ability score
    is needed for the point by method
    """
    if score == 8:
        return 0
    elif score == 9:
        return 1
    elif score == 10:
        return 2
    elif score == 11:
        return 3
    elif score == 12:
        return 4
    elif score == 13:
        return 5
    elif score == 14:
        return 7
    elif score == 15:
        return 9


def get_available_scores(points: int) -> int:
    """returns the remaining pointsto by scores for the other abilities
        is needed for the point by method
        """
    if points == 0:
        return 8
    elif points <= 1:
        return 9
    elif points <= 2:
        return 10
    elif points <= 3:
        return 11
    elif points <= 4:
        return 12
    elif points <= 5:
        return 13
    elif points >= 7:
        return 14
    elif points >= 9:
        return 15
    else:
        return 15


def p(costs: int, points: int) -> int:
    points = costs + points
    if points >= 9:
        return 15
    elif points >= 7:
        return 14
    elif points >= 5:
        return 13
    elif points >= 4:
        return 12
    elif points >= 3:
        return 11
    elif points >= 2:
        return 10
    elif points >= 1:
        return 9
    else:
        return 8


def get_costs(value_old: int, value_new: int) -> int:
    """returns the costs difference between an old value and a new value
    is needed for the point by method
    """
    costs_old = costs_mapping(value_old)
    costs_new = costs_mapping(value_new)
    costs = costs_old - costs_new
    # if the new value is bigger the the old invert the costs
    if value_new > value_old:
        costs *= -1
    return costs


def get_random_index() -> int:
    """get a random ability index from 0 to 5"""
    return random.randint(0, 5)


def get_random_ability_score(old_score: int, max_score: int) -> int:
    """get a random ability score between the given range"""
    if old_score < max_score:
        return random.randint(old_score, max_score)
    else:
        return old_score


def set_ability_scores_point_by(ability: Dict[int, List[int]] = None, index: int = None) -> List[int]:
    """set the ability scores random with the point by method
    27 point at the beginning or the given scores if this method is used for the mutation
    """
    if not ability:
        ability = {27: [8, 8, 8, 8, 8, 8]}
    # make a deep copy of the ability dict and get its values
    init = copy.deepcopy(ability)
    key_list = list(init.keys())
    points = copy.deepcopy(key_list[0])
    key = points
    scores: List[int] = copy.deepcopy(init[key])
    # print(points, scores)
    # do so long the points != 0 to provide solutions with remaining points
    while points != 0:
        scores = copy.deepcopy(init[key])
        points = key_list[0]
        # list of all ability index
        abilities: List[int] = [0, 1, 2, 3, 4, 5]
        if index:
            abilities.remove(index)
        # do while not all ability index has a value
        while len(abilities) > 0:
            index = random.choice(abilities)
            old_value = scores[index]
            costs_old = costs_mapping(old_value)
            max_value = p(costs_old, points)
            new_value = get_random_ability_score(old_value, max_value)
            costs = get_costs(old_value, new_value)
            points -= costs
            scores[index] = new_value
            abilities.remove(index)
            if points == 0:
                continue
    # pi = 0
    # for i in scores:
    #     pi += costs_mapping(i)
    # print(pi)
    # scores = [10, 15, 15, 8, 14, 8]
    return scores


class DNAGenerator:
    """the DNAGenerator builds the random start DNA and mutate the populations"""
    dna: DNA
    ability_points: int

    def __init__(self):
        """initialize an instance of the class DNAGenerator"""
        self.ability_points = 27
        self.dna = DNA()

    def get_random_character(self):
        """create a random DNA"""
        scores = set_ability_scores_point_by()
        self.dna.set_ability_scores(scores)
        list = self.set_proficiencies()
        self.set_equipment()
        self.set_fighting_style()
        self.set_background(list)
        self.set_race()

    def get_complete_random_character(self):
        for i in range(0, 6):
            a = random.randint(8, 15)
            self.dna.set_dna_value(a, i)
        a = random.randint(0, 16)
        self.dna.set_dna_value(a, 6)
        for i in range(7, 11):
            a = random.randint(0, 17)
            self.dna.set_dna_value(a, i)
        a = random.randint(0, 4)
        self.dna.set_dna_value(a, 11)
        a = random.randint(0, 5)
        self.dna.set_dna_value(a, 12)
        a = random.randint(0, 12)
        self.dna.set_dna_value(a, 13)
        a = random.randint(0, 1)
        self.dna.set_dna_value(a, 14)
        a = random.randint(0, 12)
        self.dna.set_dna_value(a, 15)

    def mutate_random_ability_score(self):
        i = random.randint(0, 5)
        old = self.dna.get_dna_value(i)
        a = random.randint(0, 1)
        if a == 0:
            self.dna.set_dna(old + 1)
        else:
            self.dna.set_dna(old - 1)

    def mutate_random_race(self):
        i = 6
        old = self.dna.get_dna_value(i)
        a = random.randint(0, 1)
        if a == 0:
            self.dna.set_dna(old + 1)
        else:
            self.dna.set_dna(old - 1)

    def get_random_fighting_style(self) -> int:
        """returns a random fightingstyle between 0 and 4"""
        return random.randint(0, 4)

    def set_fighting_style(self):
        """set the fightingstyle to DNA"""
        self.dna.set_fighting_style(self.get_random_fighting_style())

    def reduce_random_ability_score(self, index: int) -> Dict[int, List[int]]:
        """reduce a ability score to get new remaining points to by other values"""
        abilities_init = self.get_ability_scores()
        old_value = abilities_init[index]
        new_value = old_value
        points = 0
        range_value_mod = old_value - 8
        if range_value_mod > 1:
            change_value = 1
            new_value -= change_value
        else:
            new_value = 8
        costs = get_costs(old_value, new_value)
        points += costs
        abilities_init[index] = new_value
        d = {points: abilities_init}
        return d

    def mutate_ability_scores(self):
        """mutate the ability scores with reduce and point by"""
        index = get_random_index()
        abilities = self.reduce_random_ability_score(index)
        scores = set_ability_scores_point_by(abilities, index)
        self.dna.set_ability_scores(scores)

    def set_proficiencies(self) -> List[int]:
        """set random proficiencies to the DNA"""
        new_list: List[int] = []
        proficiencies: List[int] = [0, 1, 3, 5, 6, 7, 11]
        value_1 = random.choice(proficiencies)
        proficiencies.remove(value_1)
        new_list.append(value_1)
        value_2 = random.choice(proficiencies)
        proficiencies.remove(value_2)
        new_list.append(value_2)
        self.dna.set_proficiency_choice(value_1, value_2)
        return new_list

    def set_background(self, list: [int]):
        """set random background to the DNA"""
        proficiencies: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        for skill in list:
            proficiencies.remove(skill)
        value_1 = random.choice(proficiencies)
        proficiencies.remove(value_1)
        value_2 = random.choice(proficiencies)
        proficiencies.remove(value_2)
        self.dna.set_background(value_1, value_2)

    def set_race(self):
        """set random race to the DNA between 0 and 116"""
        races: List[int] = [0, 1, 2, 3, 13, 14, 15, 16]
        race = random.choice(races)
        # race = random.randint(0, 16)
        self.dna.set_race(race)

    def set_ability_scores_standard_array(self):
        """set the ability score with the method standart array"""
        array: List[int] = [15, 14, 13, 12, 10, 8]
        abilities: List[int] = [0, 1, 2, 3, 4, 5]
        while len(abilities) > 0:
            index = random.choice(abilities)
            value = random.choice(array)
            self.dna.set_dna_value(value, index)
            array.remove(value)
            abilities.remove(index)

    def set_equipment(self):
        """set random equipment to the DNA
        Armor, Weapon, Shield, Second Weapon
        """
        weapon_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        second_weapon_list = [0, 8, 9]
        armor_list = [0, 1, 2, 3, 4, 5]
        if self.dna.dna[0] < 13:
            armor_list.remove(3)
        weapon = random.choice(weapon_list)
        armor = random.choice(armor_list)
        shield = 0
        second_weapon = 13
        if weapon == 0 or weapon == 8 or weapon == 9:
            choice = random.randint(0, 2)
            if choice == 0:
                shield = 1
            elif choice == 1:
                second_weapon = random.choice(second_weapon_list)

        elif weapon == 1 or weapon == 7 or weapon == 12:
            choice = random.randint(0, 1)
            if choice == 0:
                shield = 1
        self.dna.set_equipment(armor, weapon, shield, second_weapon)

    def permutate_ability_scores(self):
        """switch two ability score"""
        abilities: List[int] = [0, 1, 2, 3, 4, 5]

        index_1 = random.choice(abilities)
        abilities.remove(index_1)
        value_1 = self.dna.get_dna_value(index_1)

        index_2 = random.choice(abilities)
        abilities.remove(index_2)
        value_2 = self.dna.get_dna_value(index_2)
        self.dna.set_dna_value(value_1, index_2)
        self.dna.set_dna_value(value_2, index_1)

    def get_ability_scores(self) -> List[int]:
        """get the ability scores from DNA"""
        abilities: List[int] = []
        for a in range(6):
            abilities.append(self.dna.get_dna_value(a))
        return abilities

    def mutate_fighting_style(self):
        """mutate the fighting style"""
        styles: List = [0, 1, 2, 3, 4]
        styles.remove(self.dna.get_dna_value(11))

        new_style = random.choice(styles)
        self.dna.set_fighting_style(new_style)

    def mutate_weapon(self):
        """mutate the weapon"""
        equipment = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        armor = self.dna.get_dna_value(12)
        weapon = self.dna.get_dna_value(13)
        shield = self.dna.get_dna_value(14)
        second_weapon = self.dna.get_dna_value(15)
        equipment.remove(weapon)
        weapon = random.choice(equipment)

        # check if the weapon can use a second weapon or shield
        if weapon != 0 or weapon != 8 or weapon != 9:
            second_weapon = 13

        # check if the weapon can use a shield
        if weapon != 1 or weapon != 7 != 12:
            second_weapon = 13
            shield = 0

        self.dna.set_equipment(armor, weapon, shield, second_weapon)

    def mutate_shield(self):
        """mutate the shield"""
        equipment = [0, 1, 7, 8, 9, 12]
        armor = self.dna.get_dna_value(12)
        weapon = self.dna.get_dna_value(13)
        shield = self.dna.get_dna_value(14)
        second_weapon = self.dna.get_dna_value(15)
        if shield != 0:
            shield = 1
            second_weapon = 13

            # check if the weapon ca use a shield
            if weapon != 1 or weapon != 7 or weapon != 0 or weapon != 8 or weapon != 9 or weapon != 12:
                weapon = random.choice(equipment)
        else:
            shield = 0
        self.dna.set_equipment(armor, weapon, shield, second_weapon)

    def mutate_second_weapon(self):
        """mutate the second weapon"""
        second_weapon_list = [13, 0, 8, 9]
        weapon_list = [0, 8, 9]
        armor = self.dna.get_dna_value(12)
        weapon = self.dna.get_dna_value(13)
        shield = self.dna.get_dna_value(14)
        second_weapon = self.dna.get_dna_value(15)
        second_weapon_list.remove(second_weapon)

        # check if not shield and second weapon
        if second_weapon == 13:
            shield = 0
        second_weapon = random.choice(second_weapon_list)

        if second_weapon != 13:

            # check if weapon can use a second weapon
            if weapon != 0 or weapon != 8 or weapon != 9:
                weapon = random.choice(weapon_list)
        self.dna.set_equipment(armor, weapon, shield, second_weapon)

    def mutate_armor(self):
        """mutate the json_files"""
        equipment = [0, 1, 2, 3, 4, 5]
        armor = self.dna.get_dna_value(12)
        equipment.remove(armor)

        # check if strength >= 13 do get heavy json_files
        if armor is not 3 and self.dna.dna[0] < 13:
            equipment.remove(3)
        armor = random.choice(equipment)
        weapon = self.dna.get_dna_value(13)
        shield = self.dna.get_dna_value(14)
        second_weapon = self.dna.get_dna_value(15)
        self.dna.set_equipment(armor, weapon, shield, second_weapon)

    def mutate_race(self):
        """mutate the race"""
        races: List[int] = [0, 1, 2, 3, 13, 14, 15, 16]
        # races: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        race = self.dna.get_dna_value(6)
        races.remove(race)
        new_race = random.choice(races)
        self.dna.set_race(new_race)

    def mutate_proficiencies(self):
        """mutate the proficiencies"""
        proficiencies: List[int] = [0, 1, 3, 5, 6, 7, 11]
        prof: List[int] = []
        for i in range(7, 9):
            value = self.dna.get_dna_value(i)
            prof.append(value)
            if value in proficiencies:
                proficiencies.remove(value)

        index = random.randint(0, 1)
        new_prof = random.choice(proficiencies)

        prof[index] = new_prof

        self.dna.set_proficiency_choice(prof[0], prof[1])

    def mutate_background(self):
        """mutate the background"""
        proficiencies: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        prof: List[int] = []
        for i in range(9, 11):
            value = self.dna.get_dna_value(i)
            prof.append(value)
            if value in proficiencies:
                proficiencies.remove(value)

        index = random.randint(0, 1)
        new_prof = random.choice(proficiencies)

        prof[index] = new_prof

        self.dna.set_background(prof[0], prof[1])
