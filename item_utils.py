# item_utils.py
from typing import Tuple, List

def check_weapon_requirements(player, weapon) -> Tuple[bool, List[Tuple[str, int, int]]]:
    failed = []
    for stat, req in weapon.get("requirements", {}).items():
        if player.stats.get(stat, 0) < req:
            failed.append((stat, req, player.stats.get(stat, 0)))
    return (len(failed) == 0), failed