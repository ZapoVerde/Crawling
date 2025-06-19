#enemy.py
import random


class Enemy:
    def __init__(self, name, health, attack_min, attack_max,
                 evasion=0, defense=0, traits=None,
                 size=5, stealth=0, perception=0):
        self.name = name
        self.health = health
        self.attack_min = attack_min
        self.attack_max = attack_max
        self.evasion = evasion
        self.defense = defense
        self.traits = traits if traits else {}
        self.size = size  # 1 (ant) to 10 (elephant)
        self.stealth = stealth  # How sneaky the enemy is
        self.perception = perception  # How good it is at detecting others

    def attack(self):
        return random.randint(self.attack_min, self.attack_max)

    def is_alive(self):
        return self.health > 0
