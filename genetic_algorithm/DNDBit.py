import random

from genetic_algorithm.DNA import DNA


class DNABit:
    d: DNA
    dna: str

    def __init__(self, d: DNA):
        self.d = d
        self.dna = convert_ability_scores(d.dna[0]) + convert_ability_scores(d.dna[1]) + \
                   convert_ability_scores(d.dna[2]) + convert_ability_scores(d.dna[3]) + \
                   convert_ability_scores(d.dna[4]) + convert_ability_scores(d.dna[5]) + \
                   convert_race(d.dna[6]) + convert_proficiency(d.dna[7]) + convert_proficiency(d.dna[8]) + \
                   convert_proficiency(d.dna[9]) + convert_proficiency(d.dna[10]) + convert_fighting_style(d.dna[11]) + \
                   convert_armor(d.dna[12]) + convert_weapon(d.dna[13]) + convert_shield(d.dna[14]) + \
                   convert_second_weapon(d.dna[15])

    def print_bit(self):
        print(self.dna)

    def mutate(self):
        index = random.randint(0, 57)
        if self.dna[index] == '0':
            self.dna = replacer(self.dna, '1', index)
        else:
            self.dna = replacer(self.dna, '0', index)


def replacer(s, newstring, index):
    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]


def convert_ability_scores(value: int) -> str:
    if value == 8:
        return '000'
    elif value == 9:
        return '001'
    elif value == 10:
        return '010'
    elif value == 11:
        return '011'
    elif value == 12:
        return '100'
    elif value == 13:
        return '101'
    elif value == 14:
        return '110'
    elif value == 15:
        return '111'


def convert_race(value: int) -> str:
    if value == 0:
        return '00000'
    elif value == 1:
        return '00001'
    elif value == 2:
        return '00010'
    elif value == 3:
        return '00011'
    elif value == 4:
        return '00100'
    elif value == 5:
        return '00101'
    elif value == 6:
        return '00111'
    elif value == 7:
        return '01000'
    elif value == 8:
        return '01001'
    elif value == 9:
        return '01010'
    elif value == 10:
        return '01011'
    elif value == 11:
        return '01100'
    elif value == 12:
        return '01101'
    elif value == 13:
        return '01110'
    elif value == 14:
        return '01111'
    elif value == 15:
        return '10000'
    elif value == 16:
        return '10001'


def convert_armor(value: int) -> str:
    if value == 0:
        return '000'
    elif value == 1:
        return '001'
    elif value == 2:
        return '010'
    elif value == 3:
        return '011'
    elif value == 4:
        return '100'
    elif value == 5:
        return '101'


def convert_weapon(value: int) -> str:
    if value == 0:
        return '0000'
    elif value == 1:
        return '0001'
    elif value == 2:
        return '0010'
    elif value == 3:
        return '0011'
    elif value == 4:
        return '0100'
    elif value == 5:
        return '0101'
    elif value == 6:
        return '0111'
    elif value == 7:
        return '1000'
    elif value == 8:
        return '1001'
    elif value == 9:
        return '1010'
    elif value == 10:
        return '1011'
    elif value == 11:
        return '1100'
    elif value == 12:
        return '1101'


def convert_second_weapon(value: int) -> str:
    if value == 0:
        return '000'
    elif value == 8:
        return '001'
    elif value == 9:
        return '010'
    elif value == 13:
        return '011'


def convert_shield(value: int) -> str:
    if value == 0:
        return '0'
    elif value == 1:
        return '1'


def convert_fighting_style(value: int) -> str:
    if value == 0:
        return '000'
    elif value == 1:
        return '001'
    elif value == 2:
        return '010'
    elif value == 3:
        return '011'


def convert_proficiency(value: int) -> str:
    if value == 0:
        return '00000'
    elif value == 1:
        return '00001'
    elif value == 2:
        return '00010'
    elif value == 3:
        return '00011'
    elif value == 4:
        return '00100'
    elif value == 5:
        return '00101'
    elif value == 6:
        return '00111'
    elif value == 7:
        return '01000'
    elif value == 8:
        return '01001'
    elif value == 9:
        return '01010'
    elif value == 10:
        return '01011'
    elif value == 11:
        return '01100'
    elif value == 12:
        return '01101'
    elif value == 13:
        return '01110'
    elif value == 14:
        return '01111'
    elif value == 15:
        return '10000'
    elif value == 16:
        return '10001'
    elif value == 17:
        return '10010'
