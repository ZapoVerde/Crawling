# status_effects.py
from typing import List
from collections import defaultdict, Counter

# Define stackable status effect types
STACKING_EFFECTS = {"poison", "bleeding"}

def apply_effect(target, effect: dict):
    """
    Applies a status effect to the target.
    Stackable effects (like poison) add multiple entries.
    Non-stackable effects (like blind) replace or refresh.
    """
    effect_type = effect.get("type")

    if effect_type in STACKING_EFFECTS:
        target.status_effects.append(effect)
    else:
        for e in target.status_effects:
            if e["type"] == effect_type:
                e.update(effect)  # Refresh duration or value
                return
        target.status_effects.append(effect)

def process_effects(target) -> List[str]:
    lines = []
    expired = []

    # Step 1: Group and apply stackable effects before ticking durations
    stack_groups = defaultdict(list)
    for effect in target.status_effects:
        if effect["type"] in STACKING_EFFECTS:
            stack_groups[effect["type"]].append(effect)

    for effect_type, stack in stack_groups.items():
        total_damage = sum(e.get("damage", 1) for e in stack)
        count = len(stack)
        name = "You" if getattr(target, "is_player", False) else target.name
        target.health -= total_damage
        lines.append(f"☠️ {name} suffers {total_damage} {effect_type} damage (x{count}).")

        # Tick durations for stackable effects after applying damage
        for e in stack:
            if "duration" in e:
                e["duration"] -= 1
                if e["duration"] <= 0:
                    expired.append(e)

    # Step 2: Handle non-stackable effects (apply, then tick)
    for effect in target.status_effects:
        if effect["type"] in STACKING_EFFECTS:
            continue  # already processed

        name = "You" if getattr(target, "is_player", False) else target.name

        if effect["type"] == "regen":
            heal = effect.get("heal", 3)
            target.health += heal
            lines.append(f"💚 {name} regenerates {heal} health.")

        elif effect["type"] == "blind":
            lines.append(f"👁️ {name} is blinded.")

        elif effect["type"] == "maim":
            lines.append(f"🦴 {name} is maimed.")

        # Tick non-stackable durations
        if "duration" in effect:
            effect["duration"] -= 1
            if effect["duration"] <= 0:
                expired.append(effect)

    # Step 3: Remove expired effects and group logs
    expired_counts = Counter()
    for e in expired:
        target.status_effects.remove(e)
        expired_counts[e["type"]] += 1

    # Correctly gather all relevant effect types (active and expired)
    active_types = {e["type"] for e in target.status_effects}
    expired_types = set(expired_counts.keys())
    all_types = active_types | expired_types  # union of both

    for effect_type in all_types:
        count = expired_counts.get(effect_type, 0)
        remaining = sum(1 for e in target.status_effects if e["type"] == effect_type)
        name = "You" if getattr(target, "is_player", False) else target.name

        if count > 0:
            stack_text = f"{count} stack{'s' if count > 1 else ''} of {effect_type}"
            remain_text = f"{remaining} stack{'s' if remaining != 1 else ''} remain" if remaining > 0 else "none remain"
            lines.append(f"⏳ {stack_text} have worn off from {name}. {remain_text}.")
        else:
            lines.append(f"⏳ No {effect_type} stacks expired for {name}. {remaining} remain.")

    return lines
