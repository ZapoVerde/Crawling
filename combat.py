# combat.py
import random
import math
from typing import List, Union
from player import Player
from enemy import Enemy
from status_effects import apply_effect
from combat_utils import get_weapon_stats

DICE_UNICODE = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

def roll_2d6_verbose(mod: int = 0):
    """
    Rolls 2d6 and adds a modifier. Returns base roll, modifier, total, dice symbols, and a debug string.
    """
    die1, die2 = random.randint(1, 6), random.randint(1, 6)
    base_total = die1 + die2
    modified_total = base_total + mod
    symbols = f"{DICE_UNICODE[die1]} {DICE_UNICODE[die2]}"
    debug = f"🎲 Roll: {symbols} → Base: {base_total} + Mod: {mod} = Total: {modified_total}"
    return base_total, mod, modified_total, symbols, debug

def roll_multiplier(roll: float, half: bool = False, crit_fail_softener: float = 0.0) -> float:
    """
    Damage multiplier based on 2d6 roll.
    - 2: Critical fail, softened by skill
    - 3–5: Miss
    - 6–7: Glancing
    - 8–9: Normal
    - 10–13.999: Exponential ramp
    - 14+: Flattened gain
    """
    roll = max(2.0, roll)

    if roll == 2:
        softened = max(-1.0 + crit_fail_softener, 0.0)
        base = softened
    elif roll <= 5:
        base = 0.0
    elif roll <= 6:
        base = 0.4
    elif roll <= 7:
        base = 0.4 + 0.3 * (roll - 6)
    elif roll <= 8:
        base = 0.7 + 0.3 * (roll - 7)
    elif roll <= 9:
        base = 1.0 + 0.3 * (roll - 8)
    elif roll <= 13.999:
        base = 1.3 * math.exp((roll - 9) / 4)
    else:
        flat_start = 1.3 * math.exp((14 - 9) / 4)
        base = flat_start + 0.15 * (roll - 14)

    return round(base * 0.5, 3) if half else round(base, 3)

def interpret_player_roll(natural_roll: int, buffs: dict = {}) -> str:
    """
    Describes the result of a player's attack roll from the player's perspective.
    """
    if buffs.get("no_crit") and natural_roll == 12:
        return "🎯 Solid hit (crit blocked by debuff)"
    if natural_roll == 2:
        return "💀 Critical Failure! You stumble badly."
    elif natural_roll in (3, 4, 5):
        return "❌ You missed!"
    elif natural_roll in (6, 7):
        return "⚠️ Glancing Blow. You barely connect."
    elif natural_roll == 12:
        return "💥 Critical Hit! Devastating strike!"
    else:
        return "✅ Hit!"

def interpret_enemy_roll(natural_roll: int) -> str:
    """
    Describes the result of an enemy's attack roll from the player's perspective.
    """
    if natural_roll == 2:
        return "💀 It stumbles and fails miserably!"
    elif natural_roll in (3, 4, 5):
        return "❌ The attack misses you."
    elif natural_roll in (6, 7):
        return "⚠️ It grazes you with a glancing blow."
    elif natural_roll == 12:
        return "💥 A devastating blow!"
    else:
        return "✅ A clean hit!"

def roll_initiative(player, enemies):
    """
    Rolls initiative for player and enemies. Stores both order and value.
    """
    def score(actor):
        agi = actor.stats.get("AGI", 0)
        per = actor.stats.get("PER", 0)
        roll = random.randint(1, 6) + random.randint(1, 6)
        bonus = agi * 0.5 + per * 0.3
        total = roll + bonus
        return total, f"🎲 {actor.name}: 2d6 + stats = {total:.1f}"

    participants = [player] + [e for e in enemies if e.is_alive()]
    scored = [(actor, *score(actor)) for actor in participants]

    initiative_order = [actor for actor, _, _ in sorted(scored, key=lambda x: x[1], reverse=True)]
    initiative_value = {actor: score for actor, score, _ in scored}
    debug_lines = [msg for _, _, msg in scored]

    return initiative_order, initiative_value, debug_lines

def apply_initiative_drift(initiative_order, initiative_value):
    """
    Adjusts initiative values based on actor stats, simulating speed drift.
    """
    for actor in initiative_order:
        agi = actor.stats.get("AGI", 0)
        per = actor.stats.get("PER", 0)
        drift = agi * 0.3 + per * 0.2
        initiative_value[actor] += drift

    return sorted(initiative_order, key=lambda a: initiative_value[a], reverse=True)

def resolve_attack(
    attacker: Union[Player, Enemy],
    target: Union[Player, Enemy],
    roll_mod: int = 0,
    half: bool = False,
    buffs: dict = None
) -> List[str]:

    """
    Handles a single attack instance from attacker to target.
    Returns display lines.
    """
    buffs = buffs or {}
    lines = []

    base_roll, mod, total, symbols, debug = roll_2d6_verbose(roll_mod)
    lines.append(debug)

    # Interpret the roll (natural)
    if isinstance(attacker, Player):
        outcome = interpret_player_roll(base_roll, buffs)
    else:
        outcome = interpret_enemy_roll(base_roll)


    lines.append(outcome)

    if base_roll == 2:
        lines.append(f"{attacker.name} misses and loses balance!")
        return lines

    if base_roll <= 5:
        lines.append(f"{attacker.name} misses completely.")
        return lines

    # Compute base damage
    if hasattr(attacker, 'power'):
        base = 10 + attacker.power
        crit_soft = attacker.skill * 0.05 + attacker.stats.get("DEX", 0) * 0.03
    else:
        base = (attacker.attack_min + attacker.attack_max) / 2
        crit_soft = 0.0

    dmg = int(base * roll_multiplier(total, half=half, crit_fail_softener=crit_soft))
    target.health -= dmg

    # Apply status effects if the total roll was good enough (6+)
    successful_hit = total >= 6

    if successful_hit and hasattr(attacker, "traits") and "poison_on_hit" in attacker.traits and isinstance(target, Player):
        poison = attacker.traits["poison_on_hit"]
        effect = {
            "type": "poison",
            "damage": poison.get("damage", 2),
            "duration": poison.get("duration", 3)
        }
        apply_effect(target, effect)
        lines.append(f"☠️ {attacker.name}'s attack poisons you!")

    if isinstance(target, Player):
        # Scale crit threshold with target's health
        crit_threshold = max(1, target.health * 0.1)
        if base_roll == 12 and dmg >= crit_threshold:
            lines.append(f"💥 {attacker.name} lands a Critical Hit!")
        elif base_roll == 12:
            lines.append(f"⚠️ {attacker.name} strikes cleanly but weakly.")
        else:
            lines.append(f"{attacker.name} hits you for {dmg} damage!")
    else:
        lines.append(f"You hit the {target.name} for {dmg} damage. ({target.health} HP remaining)")
        if not target.is_alive():
            lines.append(f"The {target.name} is defeated!")

    return lines
