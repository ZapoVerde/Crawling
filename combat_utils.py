# combat_utils.py
import random
from typing import Tuple, List

def roll_d6() -> int:
    return random.randint(1, 6)

def roll_2d6() -> Tuple[int, int]:
    return roll_d6(), roll_d6()

def roll_multiplier(total: int, half: bool = False, crit_fail_softener: float = 0.0) -> float:
    if total <= 2:
        return 0.0 if crit_fail_softener == 0 else 0.1 * (1 - crit_fail_softener)
    elif total <= 5:
        return 0.0
    elif total == 6:
        return 0.25
    elif total == 7:
        return 0.40
    elif total == 8:
        return 0.60
    elif total == 9:
        return 0.75
    elif total == 10:
        return 0.90
    elif total == 11:
        return 1.0
    elif total == 12:
        return 1.1
    elif total == 13:
        return 1.25
    elif total >= 14:
        return 1.5
    return 0.0

def calculate_damage(base: int, multiplier: float, attacker, target) -> int:
    return max(0, int(base * multiplier))

def get_weapon_stats(entity) -> Tuple[int, str, dict, bool, str]:
    weapon = getattr(entity, "weapon", None)
    if not weapon:
        if getattr(entity, "is_player", False):
            # Fallback for player: no weapon = no attack
            return 0, "none", {}, False, "no weapon equipped"
        else:
            # Fallback for legacy enemies using attack_min/max
            damage_min = getattr(entity, "attack_min", 1)
            damage_max = getattr(entity, "attack_max", 2)
            base = random.randint(damage_min, damage_max)
            return base, "blunt", {}, False, "unarmed strike"

    traits = weapon.get("traits", {})
    damage_min = weapon.get("damage_min", 1)
    damage_max = weapon.get("damage_max", 2)
    damage_type = weapon.get("damage_type", "blunt")
    requirements = weapon.get("requirements", {})
    name = weapon.get("name", "weapon")

    penalized = False
    for stat, required in requirements.items():
        if getattr(entity, "stats", {}).get(stat, 0) < required:
            penalized = True
            break

    base = random.randint(damage_min, damage_max)
    if penalized:
        base = max(1, int(base * 0.5))

    return base, damage_type, traits, penalized, name

def apply_status_effects(attacker, target, roll: int, traits: dict) -> List[dict]:
    effects = []
    for trait, data in traits.items():
        if trait == "poison_on_hit":
            chance = data.get("chance", 1.0)
            if roll >= 6 and random.random() <= chance:
                dmg = data.get("damage", 2)
                dur = data.get("duration", 3)
                effect = {"type": "poison", "damage": dmg, "duration": dur}
                if hasattr(target, "status_effects"):
                    target.status_effects.append(effect)
                effects.append({
                    "type": "poison",
                    "target": target,
                    "amount": dmg
                })
    return effects

def generate_attack_log(attacker, target, damage: int, hit_type: str) -> List[str]:
    lines = []
    atk_you = getattr(attacker, "is_player", False)
    verb_hit = "hit" if atk_you else "hits"
    verb_miss = "miss" if atk_you else "misses"

    if hit_type == "miss":
        lines.append(f"{attacker.name} {verb_miss} completely.")
    elif hit_type == "critfail":
        lines.append(f"{attacker.name} {verb_miss} and loses balance!")
    else:
        lines.append(f"{attacker.name} {verb_hit} {target.name} for {damage} damage!")
        if target.health <= 0:
            lines.append(f"💀 {target.name} is defeated!")

    return lines
