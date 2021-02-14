class FightingStyle:
    """the fighting style is a class specific rule for fighters
    it represents the art of the fighting and gives a lot of benefits
    """
    name: str

    def __init__(self):
        """initialize an instance of the class FightingStyle"""

    def set_fighting_style(self, style: int):
        if style == 0:
            self.name = 'defense'
        elif style == 1:
            self.name = 'archery'
        elif style == 2:
            self.name = 'dueling'
        elif style == 3:
            self.name = 'two-weapon-fighting'
        elif style == 4:
            self.name = 'great-weapon-fighting'
