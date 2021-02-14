import time
import dotenv
import os

from character.Character import Character
from genetic_algorithm.DNA import DNA
from genetic_algorithm.DNAGenerator import DNAGenerator
from genetic_algorithm.DNDBit import DNABit
from genetic_algorithm.GenerationManager import GenerationManager

dotenv.load_dotenv()

if __name__ == '__main__':

    ga_amount = int(os.getenv('ga_amount'))
    for i in range(ga_amount):
        start = time.time()
        # get the amount and size for the genetic algorithm from .env
        generation_amount = int(os.getenv('generation_amount'))
        generation_size = int(os.getenv('generation_size'))

        # create 4 types of generationManager (with different selection and rates)
        # if i < ga_amount / 4:
        #     ts = False
        #     dhm_ilc = False
        # elif i < ga_amount / 4 * 2:
        #     ts = True
        #     dhm_ilc = False
        # elif i < ga_amount / 4 * 3:
        #     ts = False
        #     dhm_ilc = True
        # else:
        #     ts = True
        #     dhm_ilc = True
        ts = True
        dhm_ilc = False

        gen = GenerationManager(i, generation_amount, generation_size, ts, dhm_ilc)

        # do the genetic algorithm
        gen.GA()

        end = time.time()
        print('{} Generations , {} Population'.format(generation_amount, generation_size))
        print('time: {}'.format(end - start))

    # d = [14, 15, 13, 13, 8, 1, 2, 6, 7, 4, 10, 4, 2, 2, 0, 13]
    # d = [9, 9, 13, 13, 8, 8, 0, 6, 7, 4, 10, 0, 3, 9, 1, 13]
    # d2 = [10, 15, 10, 12, 9, 12, 7, 0, 2, 5, 15, 3, 0, 0, 0, 0]
    # d1 = [10, 15, 15, 8, 14, 8, 8, 2, 6, 13, 8, 0, 4, 0, 0, 8]
    # d1 = [10, 15, 15, 8, 14, 8, 8, 0, 1, 16, 17, 0, 4, 12, 1, 13]
    # d1 = [9, 15, 15, 8, 14, 9, 8, 0, 11, 7, 13, 1, 4, 6, 0, 13]
    # gen1 = DNAGenerator()
    # dna1 = DNA()
    # dna1.dna = d1
    # gen1.dna = dna1
    #
    # c1 = Character()
    # c1.create_character(gen1)
    # c1.print_character(0)

    # gen2 = DNAGenerator()
    # dna2 = DNA()
    # dna2.dna = d2
    # gen2.dna = dna2
    #
    # c2 = Character()
    # c2.create_character(gen2)
    # c2.print_character(0)
    #
    # l = []
    # l.append(c1)
    # l.append(c2)

    # g = Generation(2)
    # g.print_generation(0)
    #
    # g.crossover()
    #
    # g.print_generation(0)
