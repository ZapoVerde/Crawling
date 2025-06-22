# combat.py
from combat_utils import (
    roll_2d6,
    roll_multiplier,
    get_weapon_stats,
    calculate_damage,
    apply_status_effects
)

from messaging import format_roll, format_attack_result, describe_roll

def resolve_attack(attacker, target, roll_mod=0, half=False, buffs=None):
    # Roll dice
    d1, d2 = roll_2d6()
    base = d1 + d2
    total = base + roll_mod

    # Format roll message for player
    roll_msg = format_roll(d1, d2, base, roll_mod, total)

    # Determine hit description
    desc_data = describe_roll(total)
    desc = desc_data["text"]
    hit_type = desc_data["type"]

    # Calculate damage and traits
    if hasattr(attacker, "attack_modes") and attacker.attack_modes:
        # Use the attacker's chosen attack mode damage and traits
        raw_damage = attacker.attack()  # Enemy picks attack mode and returns base damage
        traits = getattr(attacker, "current_attack_traits", {})
        multiplier = roll_multiplier(total)
        damage = calculate_damage(raw_damage, multiplier, attacker, target)
    else:
        # Player or attackers without attack modes
        base_dmg, _, traits, _, _ = get_weapon_stats(attacker)
        multiplier = roll_multiplier(total)
        damage = calculate_damage(base_dmg, multiplier, attacker, target)

    # Apply damage to target
    target.health -= damage

    # Apply status effects based on attack traits and roll
    status_events = apply_status_effects(attacker, target, total, traits)

    # Grant XP for player if hit was successful
    if hasattr(attacker, "is_player") and attacker.is_player:
        hit_success = total >= 6
        attacker.gain_xp_from_attack(hit_success, list(traits.keys()))

    # Package event data for messaging
    event = {
        "attacker": attacker,
        "target": target,
        "damage": damage,
        "roll": base,
        "total": total,
        "desc": desc,
        "multiplier": multiplier,
        "status_events": status_events,
        "hit_type": hit_type,
        "attack_name": getattr(attacker, "current_attack_mode", None),
    }

    # Return combined roll and attack messages
    return [roll_msg] + format_attack_result(event)

