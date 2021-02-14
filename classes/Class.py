import json
from typing import List


class Class:
    """The Class represents the Class of the Character like Fighter or Ranger"""
    name: str
    hit_die: int
    proficiency_choices_amount: int
    proficiency_choices_list: List[str]
    starting_proficiencies: List[str]
    proficiencies: List[str]
    choices: List[str]

    def __init__(self):
        """initialize an instance of the class Class"""
        self.proficiency_choices_list = []
        self.starting_proficiencies = []
        self.choices = []
        self.proficiencies = []
        self.proficiencies.append("Acrobatics")
        self.proficiencies.append("Animal Handling")
        self.proficiencies.append("Arcana")
        self.proficiencies.append("Athletics")
        self.proficiencies.append("Deception")
        self.proficiencies.append("History")
        self.proficiencies.append("Insight")
        self.proficiencies.append("Intimidation")
        self.proficiencies.append("Investigation")
        self.proficiencies.append("Medicine")
        self.proficiencies.append("Nature")
        self.proficiencies.append("Perception")
        self.proficiencies.append("Performance")
        self.proficiencies.append("Persuasion")
        self.proficiencies.append("Religion")
        self.proficiencies.append("Sleight of Hand")
        self.proficiencies.append("Stealth")
        self.proficiencies.append("Survival")

    def get_class_from_file(self, cl: str):
        """get all informations for the given class from json file"""
        self.name = cl
        self.starting_proficiencies.clear()
        self.proficiency_choices_list.clear()
        with open('classes/fighter/{}.json'.format(cl)) as f:
            cl = json.load(f)
            self.hit_die = cl['hit_die']
            proficiency_choices_api = cl['proficiency_choices'][0]['from']
            for skill in proficiency_choices_api:
                name = skill['name']
                name = name.split(': ')
                name = name[1]
                self.proficiency_choices_list.append(name)

            starting_proficiencies_api = cl['proficiencies']
            for skill in starting_proficiencies_api:
                name = skill['name']
                if name == 'Simple weapons':
                    name = 'DEX Weapons'
                elif name == 'Martial weapons':
                    name = 'STR Weapons'
                self.starting_proficiencies.append(name)
            self.proficiency_choices_amount = cl['proficiency_choices'][0]['choose']

    def choose_proficiencies(self, index_1: int, index_2: int):
        """Choose two proficiencies from DNA"""
        self.choices.clear()
        self.choices.append(self.proficiencies[index_1])
        self.choices.append(self.proficiencies[index_2])