#player_utils.py

from typing import Dict, Any
from maps import MapRoom, Zone
from enemy import Enemy

def look(player, game) -> Dict[str, Any]:
    """
    Gather all visible information for the player in their current zone.

    Args:
        player: Player instance with stats and modifiers.
        game: Game instance with current room and player_zone.

    Returns:
        dict: Structured data including visible zone name, features, and enemies.
    """
    room: MapRoom = game.room
    zone: Zone = room.zones.get(game.player_zone)

    if not zone:
        return {
            "zone_name": "Unknown",
            "features": [],
            "enemies": []
        }

    perception = player.stats.get("PER", 0)
    # Add any temporary perception bonuses here if needed
    if hasattr(game, "search_bonus_turns") and game.search_bonus_turns > 0:
        perception += 3

    # Filter enemies based on perception
    visible_enemies = []
    for enemy in zone.enemies:
        if enemy.is_alive():
            detection_score = perception - enemy.stealth + (enemy.size - 5)
            if detection_score >= 0:
                visible_enemies.append({
                    "name": enemy.name,
                    "status": "alive"
                })

    # TODO: add feature visibility filtering here if needed
    visible_features = zone.features  # For now, assume all features are visible

    return {
        "zone_name": zone.display_name,
        "features": visible_features,
        "enemies": visible_enemies
    }

# XP + Skill Progression Functions

def gain_xp_on_success(player, tags: list[str]):
    for tag in tags:
        player.skill_xp[tag] += 1
        level = player.skills[tag]
        xp = player.skill_xp[tag]
        threshold = 5 * (level + 1)
        chance = xp / threshold
        if random.random() < chance:
            player.skills[tag] += 1
            player.skill_xp[tag] = 0

def gain_xp_from_attack(player, success: bool, tags: list[str]):
    if success:
        gain_xp_on_success(player, tags)

def skill_roll_bonus(player, tags: list[str]) -> int:
    bonus = 0
    for tag in tags:
        level = player.skills.get(tag, 0)
        if random.random() < min(level, 100) / 100:
            bonus += 1
    return bonus

def get_visible_skills(player):
    return {
        tag: lvl for tag, lvl in player.skills.items()
        if tag in ["melee", "ranged", "unarmed", "tech"] or lvl >= 3
    }