import time
from typing import Dict
from character.character_values.AbilityScore import AbilityScore
from equipment.armor.ArmorClass import ArmorClass
from character.Background import Background
from classes.Class import Class
from genetic_algorithm.DNA import DNA
from genetic_algorithm.DNAGenerator import DNAGenerator
from character.character_values.DamagePerRound import DamagePerRound
from equipment.Equipment import Equipment
from classes.fighter.FightingStyle import FightingStyle
from race.Race import Race
from character.character_values.Skill import Skill

# all weight (340)
all_weight = 305

# sum of all skill weights (40.67)
weight_skills = 37.5

# sum of all saving throw weights (22)
weight_saving_throws = 21.5

# weight ac (Armor Class) (5)
ac_weight = 5

# hp weight (Hit Points) (4.67)
hp_weight = 4.5

# dpr weight (Damage per Round) (4.33)
dpr_weight = 4.5

# ini weight (Initiative) (3)
ini_weight = 3

# Darkvision weight (2.5)
da_weight = 2.5

# Additional Defense weight (3.5)
ad_weigth = 3

# Saving Throws weight (3.83)
st_weight = 3.5

# skill weight (3.5)
all_skills_weight = 3.5

# size weight (0.83)
size_weight = 0

# speed weight (2.83)
speed_weight = 3

# equipment costs weight (-1.83) -2
costs_weight = 0

# the max value of the normalized weights
normalize = 10

# weight for all skills
skill_weight = {'Acrobatics': 4, 'Animal Handling': 0, 'Arcana': 0.5, 'Athletics': 5.5, 'Deception': 1.5,
                'History': 1, 'Insight': 3, 'Intimidation': 3, 'Investigation': 2, 'Medicine': 1,
                'Nature': 0, 'Perception': 5, 'Performance': 0, 'Persuasion': 1.5, 'Religion': 1,
                'Sleight of Hand': 1.5, 'Stealth': 4, 'Survival': 3}

# all saving throws
saving_throws_weight = {'STR': 3, 'DEX': 5.5, 'CON': 4, 'INT': 2.5, 'WIS': 5, 'CHA': 1.5}

# 20 - difficult level + 1
dc = 8

# dpr
max_dpr = 9.3
min_dpr = 1.375

# equipment costs
max_costs = 126
min_costs = 30

# skills
max_skill = 1
min_skill = 1

# stealth with disadvantage
max_skill_da = 1
min_skill_da = 1

# skills mapped to their abilities
skills = {'Acrobatics': 'DEX', 'Animal Handling': 'WIS', 'Arcana': 'INT', 'Athletics': 'STR', 'Deception': 'CHA',
          'History': 'INT', 'Insight': 'WIS', 'Intimidation': 'CHA', 'Investigation': 'INT', 'Medicine': 'WIS',
          'Nature': 'INT', 'Perception': 'WIS', 'Performance': 'CHA', 'Persuasion': 'CHA', 'Religion': 'INT',
          'Sleight of Hand': 'DEX', 'Stealth': 'DEX', 'Survival': 'WIS', 'STR Weapons': 'STR', 'DEX Weapons': 'DEX'}

# all abilities
abilities = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']


class Character:
    """a character represents a solution candidate with all variables and numbers"""
    name: str
    hit_points: int
    initiative: int
    armor_class: ArmorClass
    average_damage: DamagePerRound
    ability_scores: Dict[str, AbilityScore]
    skills: Dict[str, Skill]
    saving_throws: Dict[str, int]
    race: Race
    character_class: Class
    equipment = Equipment
    fighting_style: FightingStyle
    background: Background
    dna_generator: DNAGenerator
    gp: int

    fitness: float

    def __init__(self, index: str = 0, dna_generator: DNAGenerator = None):
        """Initialize an instance of the class class"""
        self.name = "Fighter_{}".format(index)
        self.hit_points = 0
        self.initiative = 0
        self.ability_scores = {}
        self.skills = {}
        self.saving_throws = {}
        self.initialise_ability_scores()
        self.initialise_skills()
        self.character_class = Class()
        self.background = Background()
        self.race = Race()
        self.fighting_style = FightingStyle()
        self.equipment = Equipment()
        self.dna_generator = DNAGenerator()
        if dna_generator:
            self.dna_generator = dna_generator
        self.gp = 0
        self.fitness = 0
        self.average_damage = DamagePerRound()
        self.armor_class = ArmorClass()

    def set_equipment_cost(self):
        """set equipment costs"""
        if self.equipment.shield:
            self.gp = self.equipment.weapon.cost + self.equipment.armor.cost + self.equipment.shield.cost
        elif self.equipment.second_weapon:
            self.gp = self.equipment.weapon.cost + self.equipment.armor.cost + self.equipment.second_weapon.cost
        else:
            self.gp = self.equipment.weapon.cost + self.equipment.armor.cost

    def initialise_ability_scores(self):
        """initialize all ability score from list"""
        for ability in abilities:
            self.ability_scores[ability] = AbilityScore()

    def initialise_skills(self):
        """initialize all skills from dict"""
        for skill, ability in skills.items():
            self.skills[skill] = Skill(self.ability_scores[ability])

    def set_saving_throws(self):
        """set saving throws for all abilities"""
        self.saving_throws.clear()
        for ability in abilities:
            if ability == 'STR' or ability == 'CON':
                self.saving_throws[ability] = self.ability_scores[ability].mod + 2
            else:
                self.saving_throws[ability] = self.ability_scores[ability].mod

    def create_character(self, dna_generator: DNAGenerator):
        """create character - build instance of all variables"""
        # s = time.time()
        dna = dna_generator.dna.dna
        self.dna_generator = dna_generator
        self.set_ability_scores(dna_generator.dna)
        self.skills.clear()
        self.initialise_skills()
        self.set_race(dna[6])
        self.set_class('fighter')
        self.choose_class_proficiencies(dna[7], dna[8])
        self.set_background(dna[9], dna[10])
        self.set_fighting_style(dna[11])
        self.set_equipment(dna[12], dna[13], dna[14], dna[15])
        self.update_character()
        self.set_saving_throws()
        self.set_hit_points()
        self.set_initiative()
        self.set_armor_class()
        self.set_average_damage()
        self.set_equipment_cost()
        self.calc_fitness()
        # self.print_character()
        e = time.time()
        # print("     - character: ", e - s)

    def set_ability_scores(self, dna: DNA):
        """set ability scores from DNA"""
        for index, ability in enumerate(abilities):
            self.set_ability(ability, dna.dna[index])

    def set_race(self, race: int):
        """set race from DNA"""
        for k, v in self.ability_scores.items():
            v.set_race_mod(0)
        self.race.set_race(race)
        # = Race(race)
        self.get_race_ability_bonuses()
        self.get_race_proficiencies()

    def set_class(self, name: str):
        """set class from DNA"""
        self.character_class.get_class_from_file(name)
        self.get_class_proficiencies()

    def set_fighting_style(self, style: int):
        """set fighting style from DNA"""
        self.fighting_style.set_fighting_style(style)
        # = FightingStyle(style)

    def reset_proficiencies(self):
        for k, v in self.skills.items():
            self.skills[k].set_proficiency(False)

    def choose_class_proficiencies(self, index_1: int, index_2: int):
        """set class proficiencies from DNA"""
        self.character_class.choose_proficiencies(index_1, index_2)
        for skill in self.character_class.choices:
            if skill in self.skills:
                self.set_skill_proficiency(skill, True)
        # self.set_skill_proficiency(self.character_class.proficiency_choices_list[index_1], True)
        # self.set_skill_proficiency(self.character_class.proficiency_choices_list[index_2], True)

    def set_background(self, prof_1: int, prof_2: int):
        """set background proficiencies from DNA"""
        # self.background = Background()
        self.background.choose_proficiencies(prof_1, prof_2)
        for skill in self.background.choices:
            if skill in self.skills:
                self.set_skill_proficiency(skill, True)

    def set_equipment(self, armor: int, weapon: int, shield: int, second_weapon: int):
        """set equipmnet from DNA"""
        self.equipment.set_equipment(armor, weapon, shield, second_weapon)
        # = Equipment(armor, weapon, shield, second_weapon)

    def set_armor_class(self):
        """set json_files class"""
        self.armor_class.set_armor_class(self.equipment, self.fighting_style, self.ability_scores['DEX'])
        # = ArmorClass(self.equipment, self.fighting_style, self.ability_scores['DEX'])

    def set_initiative(self):
        """set initiative"""
        self.initiative = self.ability_scores["DEX"].mod

    def set_average_damage(self):
        """set DPR (average damage per round)"""
        self.average_damage.calc_dpr(self.race, self.fighting_style, self.equipment, self.ability_scores, self.skills)
        # = DamagePerRound(self.race, self.equipment, self.fighting_style, self.ability_scores,
        #                                      self.skills)

    def set_hit_points(self):
        """set Hit Points (HP)"""
        if 'dwarven-toughness' in self.race.traits:
            self.hit_points = self.ability_scores["CON"].mod + self.character_class.hit_die + 1
        else:
            self.hit_points = self.ability_scores["CON"].mod + self.character_class.hit_die

    def calc_fitness(self):
        """calculate fitness with weighted sum of all functions"""
        self.fitness = (self.get_ac_weight(ac_weight) + self.get_hp_weight(hp_weight) + \
                        self.get_dpr_weight(dpr_weight) + self.get_ini_weight(ini_weight) + self.get_speed_weight(
                    speed_weight) + \
                        self.get_size_weight(size_weight) + self.get_dark_vision_weight(da_weight) + \
                        self.get_additional_defense_weight(ad_weigth) + self.get_saving_throw_weight(st_weight) + \
                        self.get_skills_weight(all_skills_weight) + self.get_equipment_cost_weight(
                    costs_weight)) * 100 / all_weight

    def get_skills_weight(self, fak: float) -> float:
        """calculate and normalize all skill modifications weight"""
        weight: int = 0
        bonus = 0
        if 'lucky' in self.race.traits:
            bonus = 0.025
        for k, v in self.skills.items():
            # calc for all normal skills
            if k != 'STR Weapons' and k != 'DEX Weapons' and k != 'Stealth':
                mod = skill_weight[k]
                v.calc_average_check(dc, False)
                check_norm = (v.average_check + bonus - 0.35) * normalize / (0.675 - 0.35)
                weight += mod * check_norm
            # calc for Stealth, disadvantage
            elif k == 'Stealth':
                mod = skill_weight[k]
                disadvantage = self.equipment.armor.stealth_disadvantage
                v.calc_average_check(dc, disadvantage)
                check_norm = (v.average_check + bonus - 0.1225) * normalize / (0.675 - 0.1225)
                weight += mod * check_norm
        weight /= weight_skills
        return weight * fak

    def get_saving_throw_weight(self, fak: float) -> float:
        """calculate and normalize all saving throws weight"""
        weight: int = 0
        bonus = 0
        if 'lucky' in self.race.traits:
            bonus = 0.025
        for k, v in self.saving_throws.items():
            mod = v
            weight_mod = saving_throws_weight[k]
            avg_check = round(((dc + mod) / 20), 3)
            check_norm = (avg_check + bonus - 0.35) * normalize / (0.675 - 0.35)
            weight += weight_mod * check_norm
        weight /= weight_saving_throws
        return weight * fak

    def get_ac_weight(self, fak: float) -> float:
        """calculate and normalize json_files class weight"""
        ac = self.armor_class.ac
        ac -= 10
        ac *= normalize / 9
        return ac * fak

    def get_hp_weight(self, fak: float) -> float:
        """calculate and normalize hit points (HP) weight"""
        # min_hp = 9, max_hp = 14, diff = 5
        hp = self.hit_points
        hp -= 9
        hp *= normalize / 5
        return hp * fak

    def get_dpr_weight(self, fak: float) -> float:
        """calculate and normalize damage per round weight"""
        dpr = self.average_damage.dpr
        dpr -= min_dpr
        dpr *= normalize / (max_dpr - min_dpr)
        return dpr * fak

    def get_ini_weight(self, fak: float) -> float:
        """calculate and normalize initiative weight"""
        # min_ini = -1 map to 0, max_ini = 3 map to 4
        ini = self.initiative
        ini += 1
        ini *= normalize / 4
        return ini * fak

    def get_speed_weight(self, fak: float) -> float:
        """calculate and normalize speed weight"""
        speed = self.race.speed
        if speed == 25:
            return (normalize / 2) * fak
        elif speed == 30:
            return normalize * fak

    def get_size_weight(self, fak: float) -> float:
        """calculate and normalize size weight"""
        size = self.race.size
        if size == 'Medium':
            return normalize * fak
        elif size == 'Small':
            return (normalize / 2) * fak

    def get_additional_defense_weight(self, fak: float) -> float:
        """calculate and normalize additional defense weight"""
        additional_defense = self.race.additional_defense
        if additional_defense:
            return normalize * fak
        else:
            return 0 * fak

    def get_dark_vision_weight(self, fak: float) -> float:
        """calculate and normalize darkvision weight"""
        dark_vision = self.race.dark_vision
        if dark_vision:
            return normalize * fak
        else:
            return 0 * fak

    def get_equipment_cost_weight(self, fak: float) -> float:
        """calculate and normalize equipment costs weight"""
        cost = self.gp
        cost -= min_costs
        cost *= normalize / (max_costs - min_costs)
        return cost * fak

    def update_character(self):
        """update characters attributes and skills"""
        self.calc_attributes()
        self.calc_skills()

    def calc_skills(self):
        """calculate skill mods"""
        for skill, value in self.skills.items():
            value.calc_mod()

    def calc_attributes(self):
        """calculate attribute mods"""
        for attribute, value in self.ability_scores.items():
            value.calc_mod()
            value.calc_mod()

    def set_ability(self, ability: str, value: int):
        """set ability score"""
        self.ability_scores[ability].set_value(value)

    def set_ability_race_bonus(self, ability: str, value: int):
        """set ability race bonus"""
        self.ability_scores[ability].set_race_mod(value)

    def set_skill_proficiency(self, skill: str, value: int):
        """set skill proficiencies"""
        self.skills[skill].set_proficiency(value)

    def get_race_ability_bonuses(self):
        """get ability bonus from race"""
        for ability, bonus in self.race.ability_bonuses.items():
            self.set_ability_race_bonus(ability, bonus)

    def get_race_proficiencies(self):
        """get race proficiencies"""
        for skill in self.race.starting_proficiencies:
            if skill in self.skills:
                self.set_skill_proficiency(skill, True)

    def get_class_proficiencies(self):
        """get proficiencies from class"""
        for skill in self.character_class.starting_proficiencies:
            if skill in self.skills:
                self.set_skill_proficiency(skill, True)

    def print_character(self, generation: int):
        """print character"""
        print("-----Generation_{}__{}-----".format(generation, self.name))
        self.dna_generator.dna.print_dna()
        print("Fitness = {}".format(self.fitness))
        print("Race = {} - {}".format(self.race.name, self.race.subrace))
        print("Speed = {}".format(self.race.speed))
        print("Size = {}".format(self.race.size))
        print("Darkvision = {}".format(self.race.dark_vision))
        print("Additional Defense = {}".format(self.race.additional_defense))
        print("traits = {}".format(self.race.traits))
        print("Fighting Style = {}".format(self.fighting_style.name))
        print("Hit Points = {}".format(self.hit_points))
        print("Initiative = {}".format(self.initiative))
        self.armor_class.print_armor_class()
        print("Average Damage per Round = {}".format(self.average_damage.dpr))
        self.average_damage.print_dpr_function()
        self.print_equipment()
        print('Equipment Cost = {}'.format(self.gp))
        self.print_attributes()
        self.print_skills()

    def print_attributes(self):
        """print attributes"""
        print("-----Ability Scores-----")
        for attribute, mod in self.ability_scores.items():
            print("{} {} ({}) = {}".format(attribute, mod.value, mod.race_mod, mod.mod))
        print("")

    def print_skills(self):
        """print skills"""
        print("-----Skills-----")
        for skill, mod in self.skills.items():
            if mod.proficiency:
                print("{} {} (prof)".format(skill, mod.mod))
            else:
                print("{} {}".format(skill, mod.mod))
        print("")

    def print_equipment(self):
        """print equipment"""
        self.equipment.print_equipment()
