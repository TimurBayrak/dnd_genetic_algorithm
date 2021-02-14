from typing import List


class DNA:
    """The DNA represents the chromosom of the solution candidate"""
    dna: List[int]

    def __init__(self):
        """initialize an instance of the class DNA"""
        self.dna = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def set_dna(self, dna: List[int]):
        self.dna = dna

    def print_dna(self):
        """print the DNA"""
        print('dna = |{} | {} |{} |{} | {} |{}'.format(self.get_ability_scores(), self.dna[6],
                                                       self.get_proficiencies(),
                                                       self.get_background(), self.dna[11], self.get_equipment()))

    def get_dna_value(self, index: int):
        """get a value from the DNA from index"""
        return self.dna[index]

    def set_dna_value(self, value: int, index: int):
        """set a DNA value at index"""
        self.dna[index] = value

    def get_ability_scores(self):
        """get all ability scores"""
        s = ''
        for i in range(6):
            s += ' ' + str(self.dna[i])
        return s

    def get_proficiencies(self):
        """get all proficiencies"""
        s = ''
        for i in range(7, 9):
            s += ' ' + str(self.dna[i])
        return s

    def get_background(self):
        """get the background values"""
        s = ''
        for i in range(9, 11):
            s += ' ' + str(self.dna[i])
        return s

    def get_equipment(self):
        """get the equipment values"""
        s = ''
        for i in range(12, 16):
            s += ' ' + str(self.dna[i])
        return s

    def set_ability_scores(self, scores: List[int]):
        """set all ability scores"""
        for s in range(6):
            self.dna[s] = scores[s]

    def set_proficiency_choice(self, prof_1: int, prof_2: int):
        """set the proficiencies"""
        self.dna[7] = prof_1
        self.dna[8] = prof_2

    def set_equipment(self, armor: int, weapon: int, shield: int, second_weapon: int):
        """set the equipment"""
        self.dna[12] = armor
        self.dna[13] = weapon
        self.dna[14] = shield
        self.dna[15] = second_weapon

    def set_fighting_style(self, style: int):
        """set the fighting style"""
        self.dna[11] = style

    def set_background(self, prof_1: int, prof_2: int):
        """set the background"""
        self.dna[9] = prof_1
        self.dna[10] = prof_2

    def set_race(self, race: int):
        """set the race"""
        self.dna[6] = race
