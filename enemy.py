#enemy.py
import random


class Enemy:

    def __init__(self,
                 name,
                 health,
                 attack_min,
                 attack_max,
                 evasion=0,
                 defense=0,
                 traits=None):
        self.name = name
        self.health = health
        self.attack_min = attack_min
        self.attack_max = attack_max
        self.evasion = evasion  # % chance to dodge
        self.defense = defense  # Optional: affects damage resistance
        self.traits = traits if traits else {
        }  # Optional: poison, resistances, etc.

    def attack(self):
        return random.randint(self.attack_min, self.attack_max)

    def is_alive(self):
        return self.health > 0
