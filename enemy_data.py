#enemy_data.py
from enemy import Enemy


def make_goblin():
    return Enemy("Goblin", 20, 4, 8, evasion=15)


def make_spider():
    return Enemy(
        name="Giant Spider",
        health=25,
        attack_min=0,
        attack_max=0,
        defense=6,
        attack_modes=[
            {
                "name": "Venomous Bite",
                "damage_min": 2,
                "damage_max": 4,
                "traits": {"poison_on_hit": {"damage": 2, "duration": 4, "chance": 1.0}},
                "weight": 3
            },
            {
                "name": "Web Wrap",
                "damage_min": 0,
                "damage_max": 0,
                "traits": {"maim": {"chance": 0.5}},
                "weight": 1
            }
        ]
    )

def make_scyther():
    return Enemy(
        name="Scyther Drone",
        health=40,
        attack_min=0,
        attack_max=0,
        defense=10,
        attack_modes=[
            {
                "name": "Mono-blade Slash",
                "damage_min": 6,
                "damage_max": 10,
                "traits": {"bleed": {"chance": 1.0}},
                "weight": 3
            },
            {
                "name": "Charge Ram",
                "damage_min": 4,
                "damage_max": 8,
                "traits": {"maim": {"chance": 0.5}},
                "weight": 1
            }
        ]
    )

def make_chitin_bug():
    return Enemy(
        name="Chitin Bug",
        health=30,
        attack_min=0,
        attack_max=0,
        defense=8,
        attack_modes=[
            {
                "name": "Mandible Clamp",
                "damage_min": 3,
                "damage_max": 5,
                "traits": {"bleed": {"chance": 0.7}},
                "weight": 2
            },
            {
                "name": "Acid Spit",
                "damage_min": 2,
                "damage_max": 4,
                "traits": {"poison_on_hit": {"damage": 2, "duration": 2, "chance": 1.0}},
                "weight": 3
            }
        ]
    )

def make_psylink_aberrant():
    return Enemy(
        name="Psylink Aberrant",
        health=28,
        attack_min=0,
        attack_max=0,
        defense=5,
        attack_modes=[
            {
                "name": "Mind Shatter",
                "damage_min": 5,
                "damage_max": 8,
                "traits": {"blind": {"duration": 2}},
                "weight": 2
            },
            {
                "name": "Neural Lash",
                "damage_min": 3,
                "damage_max": 6,
                "traits": {"maim": {"chance": 1.0}},
                "weight": 1
            }
        ]
    )

def make_burned_thrall():
    return Enemy(
        name="Burned Thrall",
        health=20,
        attack_min=0,
        attack_max=0,
        defense=4,
        attack_modes=[
            {
                "name": "Charred Swipe",
                "damage_min": 2,
                "damage_max": 5,
                "traits": {},
                "weight": 3
            },
            {
                "name": "Molten Touch",
                "damage_min": 3,
                "damage_max": 6,
                "traits": {"burn": {"damage": 1, "duration": 3}},
                "weight": 2
            }
        ]
    )

def make_ancient_mech_core():
    return Enemy(
        name="Ancient Mech Core",
        health=60,
        attack_min=0,
        attack_max=0,
        defense=12,
        attack_modes=[
            {
                "name": "Pulse Beam",
                "damage_min": 8,
                "damage_max": 12,
                "traits": {},
                "weight": 3
            },
            {
                "name": "Neural Feedback",
                "damage_min": 0,
                "damage_max": 0,
                "traits": {"blind": {"duration": 2}, "maim": {"chance": 1.0}},
                "weight": 1
            }
        ]
    )