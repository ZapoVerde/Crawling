# status_effects.py
from typing import List
from collections import defaultdict

STACKING_EFFECTS = {"poison", "burn", "bleed"}  # Example set, adjust as needed

def process_effects(target) -> List[dict]:
    events = []
    expired = []

    stack_groups = defaultdict(list)
    for effect in target.status_effects:
        if effect["type"] in STACKING_EFFECTS:
            stack_groups[effect["type"]].append(effect)

    for effect_type, stack in stack_groups.items():
        total_damage = sum(e.get("damage", 1) for e in stack)
        count = len(stack)
        target.health -= total_damage
        events.append({
            "type": effect_type,
            "target": target,
            "amount": total_damage,
            "count": count
        })
        for e in stack:
            if "duration" in e:
                e["duration"] -= 1
                if e["duration"] <= 0:
                    expired.append(e)

    for effect in target.status_effects:
        if effect["type"] in STACKING_EFFECTS:
            continue

        if effect["type"] == "regen":
            heal = effect.get("heal", 3)
            target.health += heal
            events.append({
                "type": "regen",
                "target": target,
                "amount": heal
            })

        elif effect["type"] in {"blind", "maim"}:
            events.append({
                "type": effect["type"],
                "target": target
            })

        if "duration" in effect:
            effect["duration"] -= 1
            if effect["duration"] <= 0:
                expired.append(effect)

    # Track expired effects
    for e in expired:
        target.status_effects.remove(e)
        events.append({
            "type": "expire",
            "target": target,
            "effect": e["type"]
        })

    return events
