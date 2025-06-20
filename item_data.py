# item_data.py

def make_weapon(name, damage_min, damage_max, damage_type,
                traits=None, requirements=None, tags=None):
    return {
        "name": name,
        "damage_min": damage_min,
        "damage_max": damage_max,
        "damage_type": damage_type,
        "traits": traits or {},         # e.g. {"poison_on_hit": {...}}
        "requirements": requirements or {},  # e.g. {"STR": 6, "DEX": 4}
        "tags": tags or []              # Optional: ["starter", "alien", "relic"]
    }

def get_basic_weapons():
    return {
        "knife": make_weapon("Hunting Knife", 3, 6, "sharp"),
        "mace": make_weapon("Iron Mace", 6, 10, "blunt", requirements={"STR": 6}),
        "eldritch_blade": make_weapon("Eldritch Blade", 8, 16, "psychic", traits={"bleed": {"chance": 1.0}}, requirements={"PSI": 7, "DEX": 5}),
    }