import json
from typing import List, Dict


class Race:
    """a race represents the species of the character"""
    name: str
    speed: int
    dark_vision: bool
    size: str
    additional_defense: bool
    ability_bonuses: Dict[str, int]
    starting_proficiencies: List[str]
    subrace: str
    has_subrace: int

    traits: List[str]

    def __init__(self):
        """Initialize an instance of the class Race"""
        self.traits = []
        self.ability_bonuses = {}
        self.starting_proficiencies = []

    def set_race(self, race: int):
        self.traits.clear()
        self.ability_bonuses.clear()
        self.starting_proficiencies.clear()
        self.subrace = ""
        self.has_subrace = 0
        self.dark_vision = False
        self.additional_defense = False
        self.get_race_mapping(race)
        self.get_race_from_file(self.name, 0)
        if self.has_subrace is not 0:
            self.get_race_from_file(self.subrace, self.has_subrace)

    def get_race_from_file(self, race: str, is_subrace: int):
        """get all informations for the given race or subrace from json file"""
        with open('race/json_files/{}.json'.format(race)) as f:
            # check if race is half-elf because half-elf has special rules
            if race == 'half-elf' and is_subrace > 0:
                # self.starting_proficiencies.append('Athletics')
                # self.starting_proficiencies.append('Perception')
                if is_subrace == 1:
                    self.ability_bonuses['STR'] = 1
                    self.ability_bonuses['DEX'] = 1
                elif is_subrace == 2:
                    self.ability_bonuses['STR'] = 1
                    self.ability_bonuses['CON'] = 1
                elif is_subrace == 3:
                    self.ability_bonuses['STR'] = 1
                    self.ability_bonuses['INT'] = 1
                elif is_subrace == 4:
                    self.ability_bonuses['STR'] = 1
                    self.ability_bonuses['WIS'] = 1
                elif is_subrace == 5:
                    self.ability_bonuses['DEX'] = 1
                    self.ability_bonuses['CON'] = 1
                elif is_subrace == 6:
                    self.ability_bonuses['DEX'] = 1
                    self.ability_bonuses['INT'] = 1
                elif is_subrace == 7:
                    self.ability_bonuses['DEX'] = 1
                    self.ability_bonuses['WIS'] = 1
                elif is_subrace == 8:
                    self.ability_bonuses['CON'] = 1
                    self.ability_bonuses['INT'] = 1
                elif is_subrace == 9:
                    self.ability_bonuses['CON'] = 1
                    self.ability_bonuses['WIS'] = 1
            else:
                # load file and get race specific informations
                race = json.load(f)
                if is_subrace is 0:
                    self.speed = race['speed']
                    self.size = race['size']

                # check if race has darkvision
                if 'traits' in race:
                    for t in race['traits']:
                        trait = t['index']
                        self.get_additional_defense(trait)
                        if trait == 'darkvision':
                            self.dark_vision = True
                        self.traits.append(trait)

                # check if race has additional defense
                if 'racial_traits' in race:
                    for t in race['racial_traits']:
                        trait = t['index']
                        self.get_additional_defense(trait)
                        self.traits.append(trait)

                # get the ability bonus for the race
                ability_bonuses_api = race['ability_bonuses']
                for ability in ability_bonuses_api:
                    name = ability['ability_score']['name']
                    bonus = ability['bonus']
                    self.ability_bonuses[name] = bonus

                # get the sarting proficiencies for the race
                starting_proficiencies_api = race['starting_proficiencies']
                for skill in starting_proficiencies_api:
                    name = skill['name']
                    name_skill = name.split(': ')
                    if len(name_skill) == 2:
                        name = name.split(': ')
                        name = name[1]
                    self.starting_proficiencies.append(name)

    def get_additional_defense(self, trait: str):
        """check if racial trait can be mapped to additional defense group"""
        if trait == 'hellish-resistance':
            self.additional_defense = True
        elif trait == 'gnome-cunning':
            self.additional_defense = True
        elif trait == 'dwarven-resilience':
            self.additional_defense = True
        elif trait == 'fey-ancestry':
            self.additional_defense = True
        elif trait == 'brave':
            self.additional_defense = True
        elif trait == 'damage-resistance':
            self.additional_defense = True
        elif trait == 'relentless-endurance':
            self.additional_defense = True

    def get_race_mapping(self, race: int):
        """map the DNA number to the correct string to load the json file"""
        if race == 0:
            self.name = 'human'
        elif race == 1:
            self.name = 'elf'
            self.subrace = 'high-elf'
            self.has_subrace = 1
        elif race == 2:
            self.name = 'half-orc'
        elif race == 3:
            self.name = 'dwarf'
            self.subrace = 'hill-dwarf'
            self.has_subrace = 1
        elif race == 4:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 1
        elif race == 5:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 2
        elif race == 6:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 3
        elif race == 7:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 4
        elif race == 8:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 5
        elif race == 9:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 6
        elif race == 10:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 7
        elif race == 11:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 8
        elif race == 12:
            self.name = 'half-elf'
            self.subrace = 'half-elf'
            self.has_subrace = 9
        elif race == 13:
            self.name = 'halfling'
            self.subrace = 'lightfoot-halfling'
            self.has_subrace = 1
        elif race == 14:
            self.name = 'gnome'
            self.subrace = 'rock-gnome'
            self.has_subrace = 1
        elif race == 15:
            self.name = 'dragonborn'
        elif race == 16:
            self.name = 'tiefling'
