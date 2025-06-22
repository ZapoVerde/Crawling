# player.py
import math
from collections import defaultdict

class Player:
    def __init__(self, name):
        self.name = name
        self.weapon = None
        self.is_player = True
        self.debug_mode = False

        # Core stats
        self.stats = {
            "STR": 4, "DEX": 4, "AGI": 4,
            "PER": 4, "PSI": 4, "CHA": 4, "END": 4,
        }

        # Derived attributes
        self.max_health = self.scaled_stat("END", scale=7.5) + 50
        self.health = self.max_health
        self.power = self.scaled_stat("STR", scale=1.5)
        self.skill = self.scaled_stat("DEX", scale=0.5)
        self.accuracy = self.scaled_stat("PER", scale=0.5)

        # Buffs, debuffs, and effects
        self.buffs = {}
        self.status_effects = []

        # Skills and XP tracking
        self.skills = defaultdict(int)
        self.skill_xp = defaultdict(int)

    def scaled_stat(self, stat: str, scale: float = 1.0) -> int:
        val = self.stats.get(stat, 0)
        return int(scale * (1 - math.exp(-val / 5)) * 10)