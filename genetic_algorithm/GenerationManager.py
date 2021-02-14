import operator
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import xlwt
from character.Character import Character
from genetic_algorithm.Generation import Generation


class GenerationManager:
    """The GenerationManager has a list of all generations
    in this class the genetic algorithm is implemented
    """
    generations: List[Generation]
    generations_amount: int
    generation_size: int
    current_generation: int
    name: int
    tournament_selection: bool
    dhm_ilc: bool

    def __init__(self, name: int, amount: int, size: int, tournament_selection: bool, dhm_ilc: bool):
        """initalize an instance of the class GenerationManager
        amount = how manx generations
        size = populationsize per generation
        """
        self.name = name
        self.generations_amount = amount
        self.generation_size = size
        self.tournament_selection = tournament_selection
        self.dhm_ilc = dhm_ilc
        self.generations = []
        self.current_generation = 0
        g = Generation(size)
        if dhm_ilc:
            g.mutation_rate = 1
            g.crossover_rate = 0
        self.generations.append(g)

    def GA(self):
        """The genetic algorithm
        get the top three candidates
        write all generations to file
        generate diagram of the generations
        """
        for i in range(0, self.generations_amount - 1):
            print('Generation_{}'.format(i))
            self.mutation_permutation_crossover()
            self.selection()
            print('---------------------------')
        self.generations[self.generations_amount - 1].create_characters()
        self.write_to_csv()
        # self.show_diagram()
        # self.save_top_3()

    def get_top_3(self) -> List[Character]:
        """get the to three candidates"""
        top_3: List[Character] = []
        for i in range(3):
            f = max(self.generations, key=operator.attrgetter('best_candidate.fitness'))
            c = f.best_candidate
            index = self.generations.index(f)
            top_3.append(c)
            self.generations.remove(f)
            c.print_character(index)
        return top_3

    def print_generations(self):
        """print all generations"""
        for i in self.generations:
            print('Best: {}  Average: {}  Worst: {} size: {}'.format(i.best_fitness, i.average_fitness, i.worst_fitness,
                                                                     len(i.characters)))

    def selection(self):
        """do the selection and create a new generation"""

        if self.tournament_selection:
            new_generation = self.generations[self.current_generation].tournament_selection()
        else:
            new_generation = self.generations[self.current_generation].fitness_proportional_selection()
        g = Generation(self.generation_size, new_generation)
        self.current_generation += 1

        if self.dhm_ilc:
            g.mutation_rate = 1 - (self.current_generation / self.generations_amount)
            g.crossover_rate = self.current_generation / self.generations_amount
        self.generations.append(g)

    def mutation_permutation_crossover(self):
        """do the mutation and crossover for the current generation"""
        self.generations[self.current_generation].crossover()
        self.generations[self.current_generation].mutation_parallel()
        # self.generations[self.current_generation].permutation_parallel()

    def write_to_csv(self):
        """write all generations to an excel file"""
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("generations")
        sheet1.write(0, 0, "Generation Number")
        sheet1.write(0, 1, "Average Fitness")
        sheet1.write(0, 2, "Best Fitness")
        sheet1.write(0, 3, "Worst Fitness")
        i = 1
        for n, g in enumerate(self.generations):
            sheet1.write(i, 0, n)
            sheet1.write(i, 1, g.average_fitness)
            sheet1.write(i, 2, g.best_fitness)
            sheet1.write(i, 3, g.worst_fitness)
            i += 1

        """write the top three to excel file"""
        c = self.get_top_3()
        # book = xlwt.Workbook(encoding="utf-8")
        sheet2 = book.add_sheet("candidates")
        sheet2.write(0, 0, "Fitness")
        sheet2.write(0, 1, "STR")
        sheet2.write(0, 2, "DEX")
        sheet2.write(0, 3, "CON")
        sheet2.write(0, 4, "INT")
        sheet2.write(0, 5, "WIS")
        sheet2.write(0, 6, "CHA")
        sheet2.write(0, 7, "Race")
        sheet2.write(0, 8, "Prof 1")
        sheet2.write(0, 9, "Prof 2")
        sheet2.write(0, 10, "Prof 3")
        sheet2.write(0, 11, "Prof 4")
        sheet2.write(0, 12, "Fighting Style")
        sheet2.write(0, 13, "Armor")
        sheet2.write(0, 14, "Weapon")
        sheet2.write(0, 15, "Shield")
        sheet2.write(0, 16, "Second Weapon")
        i = 1
        for g in c:
            sheet2.write(i, 0, g.fitness)
            sheet2.write(i, 1, g.dna_generator.dna.get_dna_value(0))
            sheet2.write(i, 2, g.dna_generator.dna.get_dna_value(1))
            sheet2.write(i, 3, g.dna_generator.dna.get_dna_value(2))
            sheet2.write(i, 4, g.dna_generator.dna.get_dna_value(3))
            sheet2.write(i, 5, g.dna_generator.dna.get_dna_value(4))
            sheet2.write(i, 6, g.dna_generator.dna.get_dna_value(5))
            sheet2.write(i, 7, g.dna_generator.dna.get_dna_value(6))
            sheet2.write(i, 8, g.dna_generator.dna.get_dna_value(7))
            sheet2.write(i, 9, g.dna_generator.dna.get_dna_value(8))
            sheet2.write(i, 10, g.dna_generator.dna.get_dna_value(9))
            sheet2.write(i, 11, g.dna_generator.dna.get_dna_value(10))
            sheet2.write(i, 12, g.dna_generator.dna.get_dna_value(11))
            sheet2.write(i, 13, g.dna_generator.dna.get_dna_value(12))
            sheet2.write(i, 14, g.dna_generator.dna.get_dna_value(13))
            sheet2.write(i, 15, g.dna_generator.dna.get_dna_value(14))
            sheet2.write(i, 16, g.dna_generator.dna.get_dna_value(15))
            i += 1

        if self.dhm_ilc:
            cm = 'DHM_ILC'
        else:
            cm = '0.03MR0.9CR'
        if self.tournament_selection:
            s = 'TS'
        else:
            s = 'FPS'
        book.save("xls_new/{}_{}_{}_{}_{}.xls".format(s, cm, self.generations_amount, self.generation_size, self.name))

    # def save_top_3(self):
    #     """write the top three to excel file"""
    #     c = self.get_top_3()
    #     book = xlwt.Workbook(encoding="utf-8")
    #     sheet2 = book.add_sheet("candidates")
    #     sheet2.write(0, 0, "Fitness")
    #     sheet2.write(0, 1, "STR")
    #     sheet2.write(0, 2, "DEX")
    #     sheet2.write(0, 3, "CON")
    #     sheet2.write(0, 4, "INT")
    #     sheet2.write(0, 5, "WIS")
    #     sheet2.write(0, 6, "CHA")
    #     sheet2.write(0, 7, "Race")
    #     sheet2.write(0, 8, "Prof 1")
    #     sheet2.write(0, 9, "Prof 2")
    #     sheet2.write(0, 10, "Prof 3")
    #     sheet2.write(0, 11, "Prof 4")
    #     sheet2.write(0, 12, "Fighting Style")
    #     sheet2.write(0, 13, "Armor")
    #     sheet2.write(0, 14, "Weapon")
    #     sheet2.write(0, 15, "Shield")
    #     sheet2.write(0, 16, "Second Weapon")
    #     i = 1
    #     for g in c:
    #         sheet2.write(i, 0, g.fitness)
    #         sheet2.write(i, 1, g.dna_generator.dna.get_dna_value(0))
    #         sheet2.write(i, 2, g.dna_generator.dna.get_dna_value(1))
    #         sheet2.write(i, 3, g.dna_generator.dna.get_dna_value(2))
    #         sheet2.write(i, 4, g.dna_generator.dna.get_dna_value(3))
    #         sheet2.write(i, 5, g.dna_generator.dna.get_dna_value(4))
    #         sheet2.write(i, 6, g.dna_generator.dna.get_dna_value(5))
    #         sheet2.write(i, 7, g.dna_generator.dna.get_dna_value(6))
    #         sheet2.write(i, 8, g.dna_generator.dna.get_dna_value(7))
    #         sheet2.write(i, 9, g.dna_generator.dna.get_dna_value(8))
    #         sheet2.write(i, 10, g.dna_generator.dna.get_dna_value(9))
    #         sheet2.write(i, 11, g.dna_generator.dna.get_dna_value(10))
    #         sheet2.write(i, 12, g.dna_generator.dna.get_dna_value(11))
    #         sheet2.write(i, 13, g.dna_generator.dna.get_dna_value(12))
    #         sheet2.write(i, 14, g.dna_generator.dna.get_dna_value(13))
    #         sheet2.write(i, 15, g.dna_generator.dna.get_dna_value(14))
    #         sheet2.write(i, 16, g.dna_generator.dna.get_dna_value(15))
    #         i += 1
    #     if self.dhm_ilc:
    #         cm = 'dhm_ilc'
    #     else:
    #         cm = '0.03_0.9'
    #     if self.tournament_selection:
    #         s = 'ts'
    #     else:
    #         s = 'fps'
    #     book.save(
    #         "excel_files/{}_{}_{}_{}_{}.xls".format(s, cm, self.generations_amount, self.generation_size, self.name))

    def show_diagram(self):
        """show the generations diagram"""
        x = np.arange(0, self.generations_amount)
        average_fitness = []
        best_fitness = []
        worst_fitness = []
        for g in self.generations:
            average_fitness.append(g.average_fitness)
            best_fitness.append(g.best_fitness)
            worst_fitness.append(g.worst_fitness)
        plt.ylim(0, 100)
        plt.plot(x, average_fitness, label='average_fitness', color='dimgrey', linestyle="--")
        plt.plot(x, best_fitness, label='best_fitness', color='black', linestyle="-")
        plt.plot(x, worst_fitness, label='worst_fitness', color='darkgrey', linestyle=":")
        plt.xlabel('Generations')
        plt.ylabel('Average Fitness')
        plt.title('Generations')
        plt.legend(loc='lower right', borderaxespad=0.1)
        plt.legend()

        if self.dhm_ilc:
            cm = 'dhm_ilc'
        else:
            cm = '0.03_0.9'
        if self.tournament_selection:
            s = 'ts'
        else:
            s = 'fps'
        plt.savefig(
            "graphics/{}_{}_{}_{}_{}.png".format(s, cm, self.generations_amount, self.generation_size, self.name))
        plt.show()
