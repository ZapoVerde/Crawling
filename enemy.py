# enemy.py
import random

class Enemy:
    def __init__(self, name, health, attack_min, attack_max,
                 evasion=0, defense=0, traits=None,
                 size=5, stealth=0, perception=0,
                 attack_modes=None):
        self.name = name
        self.health = health
        self.attack_min = attack_min
        self.attack_max = attack_max
        self.evasion = evasion
        self.defense = defense
        self.traits = traits if traits else {}
        self.size = size
        self.stealth = stealth
        self.perception = perception
        self.status_effects = []
        self.attack_modes = attack_modes
        self.current_zone = "center"

    def is_alive(self):
        return self.health > 0