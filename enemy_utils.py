# enemy_utils.py
import random
from enemy import Enemy

def make_multiple_enemies(factory_func, count):
    """Create a list of enemies using the given factory function."""
    return [factory_func() for _ in range(count)]

def perform_attack(enemy: Enemy) -> int:
    """
    Perform an enemy attack, either simple or from attack_modes.
    
    Modifies enemy's current attack state and returns damage dealt.
    """
    if not enemy.attack_modes:
        damage = random.randint(enemy.attack_min, enemy.attack_max)
        enemy.current_attack_mode = None
        enemy.current_attack_traits = {}
        return damage

    weights = [mode.get("weight", 1) for mode in enemy.attack_modes]
    chosen = random.choices(enemy.attack_modes, weights=weights, k=1)[0]
    damage = random.randint(chosen["damage_min"], chosen["damage_max"])
    enemy.current_attack_mode = chosen["name"]
    enemy.current_attack_traits = chosen.get("traits", {})
    return damage