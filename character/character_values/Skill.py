from character.character_values import AbilityScore


class Skill:
    """a Skill is the skill of a character in acrobatics, athletics and so on"""
    mod: int
    proficiency: bool = False
    attribute: AbilityScore
    average_check: float

    def __init__(self, attribute: AbilityScore):
        """initialize an instance of the class Skill"""
        self.mod = 0
        self.attribute = attribute
        self.average_check = 0

    def set_proficiency(self, prof):
        """set skill proficiencies"""
        self.proficiency = prof

    def calc_mod(self):
        """calculate mod with proficiency bonus"""
        if self.proficiency:
            self.mod = self.attribute.mod + 2
        else:
            self.mod = self.attribute.mod

    def calc_average_check(self, difficult_level: int, disadvantage: bool):
        """calculate average chance for a successful ability check"""
        if disadvantage:
            self.average_check = round(pow(((difficult_level + self.mod) / 20), 2), 4)
        else:
            self.average_check = round(((difficult_level + self.mod) / 20), 4)