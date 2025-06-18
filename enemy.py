import random

class Enemy:
    def __init__(self, name, health, attack_min, attack_max, evasion=0):
        self.name = name
        self.health = health
        self.attack_min = attack_min
        self.attack_max = attack_max
        self.evasion = evasion  # % chance to dodge

    def attack(self):
        return random.randint(self.attack_min, self.attack_max)

    def is_alive(self):
        return self.health > 0