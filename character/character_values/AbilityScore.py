class AbilityScore:
    """the ability score represents the ability score of the character like strength dexterity and so on"""
    value: int
    mod: int
    race_mod: int

    def __init__(self):
        """initialize an instance of the class AbilityScore"""
        self.value = 0
        self.mod = 0
        self.race_mod = 0

    def set_value(self, value: int):
        """set the ability score value"""
        self.value = value

    def set_race_mod(self, mod: int):
        """set the racial modification"""
        self.race_mod = mod
        self.value = self.value + mod

    def calc_mod(self):
        """calculate the ability modification based on the value"""
        if self.value == 1:
            self.mod = -5
        elif self.value == 2 or self.value == 3:
            self.mod = -4
        elif self.value == 4 or self.value == 5:
            self.mod = -3
        elif self.value == 6 or self.value == 7:
            self.mod = -2
        elif self.value == 8 or self.value == 9:
            self.mod = -1
        elif self.value == 10 or self.value == 11:
            self.mod = 0
        elif self.value == 12 or self.value == 13:
            self.mod = 1
        elif self.value == 14 or self.value == 15:
            self.mod = 2
        elif self.value == 16 or self.value == 17:
            self.mod = 3
        elif self.value == 18 or self.value == 19:
            self.mod = 4
        elif self.value == 20 or self.value == 21:
            self.mod = 5
