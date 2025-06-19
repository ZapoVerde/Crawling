#player.py
import math


class Player:

    def __init__(self, name):
        self.name = name

        # Core stats
        self.stats = {
            "STR": 4,  # Strength
            "DEX": 4,  # Dexterity
            "AGI": 4,  # Agility
            "PER": 4,  # Perception
            "PSI": 4,  # Psionics / Magic
            "CHA": 4,  # Charisma
            "END": 4,  # Endurance
        }

        # Derived attributes
        self.max_health = 50 + self.scaled_stat("END", scale=7.5)
        self.health = self.max_health

        self.power = self.scaled_stat("STR", scale=1.5)
        self.skill = self.scaled_stat("DEX", scale=0.5)
        self.accuracy = self.scaled_stat("PER", scale=0.5)

        # Buffs, debuffs, and effects
        self.buffs = {}
        self.status_effects = []

    def scaled_stat(self, stat: str, scale: float = 1.0) -> int:
        """
        Returns a diminishing scaled value of a stat.
        Example: scale=1.5 means STR 10 → ~9
        """
        value = self.stats.get(stat, 0)
        return int(scale * (1 - math.exp(-value / 5)) * 10)
