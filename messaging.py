# messaging.py
import random

def display_name(entity, capitalize=False):
    if hasattr(entity, "is_player") and entity.is_player:
        return "You" if capitalize else "you"
    return entity.name

def format_attack_result(event):
    attacker = event["attacker"]
    target = event["target"]
    atk_you = getattr(attacker, "is_player", False)
    tgt_you = getattr(target, "is_player", False)
    lines = []

    attacker_name = display_name(attacker, capitalize=True)
    target_name = display_name(target)

    attack_name = event.get("attack_name")
    if attack_name:
        lines.append(f"{attacker_name} uses {attack_name}!")

    verb_hit = "hit" if atk_you else "hits"
    verb_miss = "miss" if atk_you else "misses"

    if event["hit_type"] == "miss":
        lines.append(f"{attacker_name} {verb_miss} completely.")
    elif event["hit_type"] == "critfail":
        lines.append(f"{attacker_name} {verb_miss} and lose balance!")
    else:
        dmg_line = f"{attacker_name} {verb_hit} {target_name} for {event['damage']} damage!"
        lines.append(dmg_line)

        if event.get("defeated"):
            if tgt_you:
                lines.append("You are defeated!")
            else:
                lines.append(random.choice([
                    f"{target.name} is defeated!",
                    f"You bring {target.name} down!",
                    f"You land the killing blow on {target.name}!"
                ]))

    # Status effects
    for effect in event.get("status_events", []):
        lines.extend(format_status_effect(effect))

    return lines

def format_status_effect(effect):
    target = effect["target"]
    tgt_you = getattr(target, "is_player", False)
    lines = []

    if effect["type"] == "poison":
        if tgt_you:
            lines.append(f"You suffer {effect['amount']} poison damage.")
        else:
            lines.append(f"{target.name} suffers {effect['amount']} poison damage.")
    elif effect["type"] == "expire":
        if tgt_you:
            lines.append(f"Your {effect['effect']} has worn off.")
        else:
            lines.append(f"{effect['effect'].capitalize()} has worn off from {target.name}.")
    elif effect["type"] == "regen":
        if tgt_you:
            lines.append(f"You regain {effect['amount']} health.")
        else:
            lines.append(f"{target.name} regenerates {effect['amount']} health.")

    return lines

def describe_roll(roll: int) -> dict:
    if roll <= 2:
        return {"type": "critfail", "text": "💀 Critical Failure! You stumble badly."}
    elif roll <= 5:
        return {"type": "miss", "text": "❌ The attack misses completely."}
    elif roll <= 7:
        return {"type": "glancing", "text": "⚠️ Glancing Blow. You barely connect."}
    elif roll <= 9:
        return {"type": "hit", "text": "✅ A clean hit!"}
    elif roll <= 13:
        return {"type": "hit", "text": "✅ Hit!"}
    else:
        return {"type": "crit", "text": "💥 Critical Hit! Devastating strike!"}

def format_roll(d1: int, d2: int, base: int, mod: int, total: int) -> str:
    symbols = "⚀⚁⚂⚃⚄⚅"
    symbol_str = f"{symbols[d1 - 1]} {symbols[d2 - 1]}"
    return f"🎲 Roll: {symbol_str} → Base: {base} + Mod: {mod} = Total: {total}"

def msg_game_over() -> str:
    return "💀 You have died."

def format_zone_description(data: dict) -> list[str]:
    """
    Format structured zone data into player-facing messages.

    Args:
        data (dict): Should contain keys:
            - 'zone_name' (str): Descriptive name of the zone.
            - 'features' (list[str]): Visible features in the zone.
            - 'enemies' (list[dict]): List of enemies with at least 'name' and 'status'.

    Returns:
        list[str]: Formatted message lines for display.
    """
    lines = [f"You move to the {data.get('zone_name', 'unknown area')}."]
    
    features = data.get('features', [])
    if features:
        lines.append("You notice " + ", ".join(features) + ".")

    enemies = data.get('enemies', [])
    alive_enemies = [e for e in enemies if e.get('status') == 'alive']
    if alive_enemies:
        enemy_names = ", ".join(e['name'] for e in alive_enemies)
        lines.append(f"You see {enemy_names} here.")
    else:
        lines.append("The area seems clear.")

    return lines