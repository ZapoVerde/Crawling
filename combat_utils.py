# combat_utils.py
import random
from typing import Tuple, List
from item_utils import check_weapon_requirements

def get_weapon_stats(attacker) -> Tuple[int, str, dict, bool]:
    """
    Returns (base_damage, damage_type, traits, penalized)
    Penalized is True if requirements are unmet and damage is halved.
    """
    if hasattr(attacker, "weapon") and attacker.weapon:
        weapon = attacker.weapon
        base = random.randint(weapon["damage_min"], weapon["damage_max"])
        damage_type = weapon.get("damage_type", "generic")
        traits = weapon.get("traits", {})
        penalized = False

        if hasattr(attacker, "stats"):
            meets, _ = check_weapon_requirements(attacker, weapon)
            if not meets:
                base = int(base * 0.5)
                penalized = True

        return base, damage_type, traits, penalized

    # fallback: enemy or unarmed player
    if hasattr(attacker, 'power'):
        base = 10 + attacker.power
    else:
        base = (attacker.attack_min + attacker.attack_max) // 2

    return base, "generic", {}, False
