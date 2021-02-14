class Diophant:
    count = 0
    costs = [0, 1, 2, 3, 4, 5, 7, 9]
    points = 27

    def __init__(self):
        self.calc_diophant()
        print('Count of possibilities: {}'.format(self.count))

    def calc_diophant(self):
        for str in self.costs:
            for dex in self.costs:
                for con in self.costs:
                    for int in self.costs:
                        for wis in self.costs:
                            for cha in self.costs:
                                if str + dex + con + int + wis + cha == self.points:
                                    self.count += 1
