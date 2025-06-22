# map_utils.py
# Utility functions for querying MapRoom data structures.
# Focused on raw zone and adjacency data retrieval, agnostic of perception.
# All player-facing messaging should be handled in messaging.py.

from typing import List, Optional
from maps import MapRoom, Zone
from enemy import Enemy

def get_adjacent_zone_names(room: MapRoom, zone_name: str) -> List[str]:
    """
    Retrieve the internal names of zones adjacent to the specified zone within the room.

    Args:
        room (MapRoom): The current room object.
        zone_name (str): The internal name of the current zone.

    Returns:
        List[str]: List of adjacent zone internal names.
    """
    return room.zone_adjacency.get(zone_name, [])

def get_adjacent_zones(room: MapRoom, zone_name: str) -> List[Zone]:
    """
    Retrieve Zone objects adjacent to the specified zone.

    Args:
        room (MapRoom): The current room object.
        zone_name (str): The internal name of the current zone.

    Returns:
        List[Zone]: List of adjacent Zone instances.
    """
    adj_names = get_adjacent_zone_names(room, zone_name)
    return [room.zones[name] for name in adj_names if name in room.zones]

def find_zone_by_feature(room: MapRoom, feature_keyword: str) -> Optional[Zone]:
    """
    Search all zones in the room to find the first containing a feature matching the keyword.

    Args:
        room (MapRoom): The current room object.
        feature_keyword (str): Keyword to match against zone features.

    Returns:
        Optional[Zone]: The first matching Zone or None if no match found.
    """
    keyword = feature_keyword.lower()
    for zone in room.zones.values():
        if any(keyword in feat.lower() for feat in zone.features):
            return zone
    return None

def find_zone_by_enemy_name(room: MapRoom, enemy_keyword: str) -> Optional[Zone]:
    """
    Search all zones in the room to find the first containing an enemy whose name matches the keyword.

    Args:
        room (MapRoom): The current room object.
        enemy_keyword (str): Keyword to match against enemy names.

    Returns:
        Optional[Zone]: The first matching Zone or None if no match found.
    """
    keyword = enemy_keyword.lower()
    for zone in room.zones.values():
        for enemy in zone.enemies:
            if keyword in enemy.name.lower():
                return zone
    return None

def visible_enemies(room: MapRoom) -> List[Enemy]:
    """
    Return all living enemies in all zones of the room.
    """
    return [enemy for zone in room.zones.values() for enemy in zone.enemies if enemy.is_alive()]

def describe_room(room: MapRoom) -> str:
    """
    Return a formatted room description.
    NOTE: Replace with call to messaging.py later.
    """
    exits = ", ".join(room.exits.keys())
    return f"{room.name}\n{room.description}\nExits: {exits}"