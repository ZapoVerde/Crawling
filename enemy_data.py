#enemy_data.py
from enemy import Enemy


def make_goblin():
    return Enemy("Goblin", 20, 4, 8, evasion=15)


def make_spider():
    return Enemy(name="Giant Spider",
                 health=25,
                 attack_min=4,
                 attack_max=7,
                 defense=6,
                 traits={"poison_on_hit": {
                     "damage": 2,
                     "duration": 3
                 }})
