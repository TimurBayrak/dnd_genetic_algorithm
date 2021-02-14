import random
import time
import copy
from typing import List, Dict
import operator
from joblib.numpy_pickle_utils import xrange
from character.Character import Character
from genetic_algorithm.DNAGenerator import DNAGenerator
import os
import multiprocessing as mp
import numpy as np


def generate_character(i: int) -> Character:
    """generate random character with index i"""
    gen = DNAGenerator()
    gen.get_random_character()
    c = Character(str(i))
    c.dna_generator = gen
    return c


def create_character(c: Character) -> Character:
    """create character for the selection"""
    c.create_character(c.dna_generator)
    return c


class Generation:
    """The Generation is a population at time t"""
    characters: List[Character]
    size: int
    average_fitness: float
    best_fitness: float
    worst_fitness: float
    best_candidate: Character
    sum_fitness: float
    mutation_rate: float
    crossover_rate: float
    diversity: float

    def __init__(self, size: int, g: List[Character] = None):
        """initialize a generation object random or with the given population"""
        self.size = size
        self.characters = []
        self.best_candidate = Character()
        self.mutation_rate = float(os.getenv('mutation_rate'))
        self.crossover_rate = float(os.getenv('crossover_rate'))
        if not g:
            pool = mp.Pool(mp.cpu_count())
            self.characters = pool.map(generate_character, [i for i in range(0, self.size)])
            pool.close()
        else:
            self.characters = g

    def print_generation(self, index: int):
        """print the generation"""
        for c in self.characters:
            c.print_character(index)

    def calc_sum_fitness(self):
        """calculate the sum of all fitness values"""
        fitness: float = 0
        for c in self.characters:
            fitness += c.fitness
        self.sum_fitness = round(fitness, 3)

    def calc_average_fitness(self):
        """calculate the average fitness values"""
        fitness: float = 0
        for c in self.characters:
            fitness += c.fitness
        self.average_fitness = round((fitness / self.size), 3)

    def get_best_fitness(self):
        """get the best fitness value and the best candidate"""
        f = max(self.characters, key=operator.attrgetter('fitness'))
        self.best_fitness = round(f.fitness, 3)
        self.best_candidate = f

    def get_worst_fitness(self):
        """get the worst fitness value"""
        f = min(self.characters, key=operator.attrgetter('fitness'))
        self.worst_fitness = round(f.fitness, 3)

    def crossover_two_candidates(self, character_1: int, character_2: int):
        """do crossover for the two given candidates"""
        p = [(0, 5), (0, 6), (0, 11), (0, 12), (6, 6), (6, 11), (6, 12), (6, 15), (7, 11), (7, 12), (7, 15),
             (12, 12), (12, 15)]

        candidate_1 = self.characters[character_1]
        candidate_2 = self.characters[character_2]

        cut = random.choice(p)
        # generate list with values 0
        c_1_list: List = list(np.zeros(16))
        c_2_list: List = list(np.zeros(16))

        # fill the list with the correct values
        for i in range(cut[0], cut[1]+1):
            c_1_list[i] = candidate_1.dna_generator.dna.get_dna_value(i)
            c_2_list[i] = candidate_2.dna_generator.dna.get_dna_value(i)

        # change the candidates with the list values
        for i in range(cut[0], cut[1]+1):
            candidate_1.dna_generator.dna.set_dna_value(c_2_list[i], i)
            candidate_2.dna_generator.dna.set_dna_value(c_1_list[i], i)

        self.characters[character_1] = candidate_1
        self.characters[character_2] = candidate_2

    def crossover(self):
        """do the crossover for the whole generation"""
        print(' - crossover')
        s = time.time()

        # make a list with all index
        tmp_list = list(range(0, self.size))
        while len(tmp_list) > 0:
            candidate_1 = random.choice(tmp_list)
            tmp_list.remove(candidate_1)
            candidate_2 = random.choice(tmp_list)
            tmp_list.remove(candidate_2)

            # ceck if the two candidates will crossover
            chance = random.uniform(0, 1)
            if chance <= self.crossover_rate:
                self.crossover_two_candidates(candidate_1, candidate_2)

        e = time.time()
        print("     - time: ", e - s)

    def mutation_parallel(self):
        """do the mutation with multiprocessing"""
        print(' - mutation')
        s = time.time()
        # make pool with the amount of cpu cores
        pool = mp.Pool(mp.cpu_count())

        # do the mutation for all characters with multi cores
        self.characters = pool.map(self.mutation, [i for i in range(0, self.size)])

        # close the pool and release the cores
        pool.close()

        e = time.time()
        print("     - time: ", e - s)

    def mutation(self, i: int) -> Character:
        """mutation of a single character at position i"""
        chance = random.uniform(0, 1)
        if chance <= self.mutation_rate:
            return self.mutate_candidate(i)
        else:
            return self.characters[i]

    def permutation_parallel(self):
        print(' - permutation')
        s = time.time()
        pool = mp.Pool(mp.cpu_count())
        self.characters = pool.map(self.permutation, [i for i in range(0, self.size)])
        pool.close()

        e = time.time()
        print("     - time: ", e - s)

    def permutation(self, i: int) -> Character:
        chance = random.uniform(0, 1)
        if chance <= self.mutation_rate:
            return self.permutate_candidate(i)
        return self.characters[i]

    def mutate_candidate(self, i: int) -> Character:
        """mutation for a character i
        make a random mutation
        """
        candidate = self.characters[i]
        # candidate.dna_generator.dna.print_dna()
        mutation = random.randint(0, 8)
        # mutation = 0
        if mutation == 0:
            candidate.dna_generator.mutate_ability_scores()
        elif mutation == 1:
            candidate.dna_generator.mutate_race()
        elif mutation == 2:
            candidate.dna_generator.mutate_proficiencies()
        elif mutation == 3:
            candidate.dna_generator.mutate_background()
        elif mutation == 4:
            candidate.dna_generator.mutate_fighting_style()
        elif mutation == 5:
            candidate.dna_generator.mutate_armor()
        elif mutation == 6:
            candidate.dna_generator.mutate_weapon()
        elif mutation == 7:
            candidate.dna_generator.mutate_shield()
        elif mutation == 8:
            candidate.dna_generator.mutate_second_weapon()
        return candidate

    def permutate_candidate(self, i: int) -> Character:
        candidate = self.characters[i]

        candidate.dna_generator.permutate_ability_scores()

        return candidate

    def create_characters(self):
        """create c list of characters with multiprocessing"""
        # open pool the the amount of cpu cores
        pool = mp.Pool(mp.cpu_count())

        # create a character at each position of the characters list
        new_list = pool.map(create_character, [i for i in self.characters])

        # close pool and release the cores
        pool.close()
        self.characters = new_list
        self.calc_sum_fitness()
        self.calc_average_fitness()
        self.get_best_fitness()
        self.get_worst_fitness()

    def fitness_proportional_selection(self) -> List[Character]:
        """the fitness-proportional selection with elitism and multiprocessing"""
        print(' - selection')
        st = time.time()

        # open pool the the amount of cpu cores
        pool = mp.Pool(mp.cpu_count())

        # create a character at each position of the characters list
        new_list = pool.map(create_character, [i for i in self.characters])

        # close pool and release the cores
        pool.close()

        self.characters = new_list
        self.get_diversity()
        self.calc_sum_fitness()
        self.calc_average_fitness()
        self.get_best_fitness()
        self.get_worst_fitness()

        # create the wheel as dict with the selection chance and the character
        wheel: Dict[float, Character] = {}

        # the new generation
        new_generation: List[Character] = []
        fit_c_generation: float = 0
        new_wheel = {}
        """get the chance of all characters to be selected
    
        """
        for c in self.characters:
            p_chance = c.fitness / self.sum_fitness
            chance = p_chance * self.size
            s = str(chance)
            s = s.split('.')
            r = int(s[0])
            f_c = '0.' + s[1]
            f_c = float(f_c)
            fit_c_generation += f_c
            if r <= 0:
                wheel[f_c] = c
            while r > 0:
                new_character = copy.deepcopy(c)
                new_generation.append(new_character)
                r -= 1

        for k, v in wheel.items():
            new_key = (k / fit_c_generation) * self.size
            new_wheel[new_key] = v

        while len(new_generation) < self.size:
            for k in sorted(new_wheel, reverse=True):
                chance = random.uniform(0, fit_c_generation)
                if chance <= k:
                    new_character = copy.deepcopy(new_wheel[k])
                    new_generation.append(new_character)
                    if len(new_generation) >= self.size:
                        break
                    continue
        e = time.time()
        print("     - time: ", e - st)

        return new_generation

    def tournament_selection(self) -> List[Character]:
        print(' - selection')
        st = time.time()

        # open pool the the amount of cpu cores
        pool = mp.Pool(mp.cpu_count())

        # create a character at each position of the characters list
        new_list = pool.map(create_character, [i for i in self.characters])

        # close pool and release the cores
        pool.close()

        self.characters = new_list

        self.calc_sum_fitness()
        self.calc_average_fitness()
        self.get_best_fitness()
        self.get_worst_fitness()

        new_generation: List[Character] = []

        for i in range(0, self.size):
            candidate_1 = None
            candidate_2 = None
            even = True
            while even:
                candidate_1 = random.choice(self.characters)
                candidate_2 = random.choice(self.characters)
                if candidate_1 != candidate_2:
                    even = False

            # check who wins the fight
            if candidate_1.fitness >= candidate_2.fitness:
                new_character = copy.deepcopy(candidate_1)
            else:
                new_character = copy.deepcopy(candidate_2)

            new_generation.append(new_character)

        e = time.time()
        print("     - time: ", e - st)

        return new_generation

    def get_diversity(self):
        div = []
        for i in self.characters:
            if i.name not in div:
                div.append(i.name)
        self.diversity = len(div) / self.size
