class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.steps = 0
        self.accuracy = 90  # percent chance to land a hit