from typing import List


class Background:
    """the background represents the past of the character
    in this code only gives the background two additional proficiencies
    """
    proficiencies: List[str]
    choices: List[str]

    def __init__(self):
        """initialize an instance of the class Background"""
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

    def choose_proficiencies(self, index_1: int, index_2: int):
        """Choose two proficiencies from DNA"""
        self.choices.clear()
        self.choices.append(self.proficiencies[index_1])
        self.choices.append(self.proficiencies[index_2])
