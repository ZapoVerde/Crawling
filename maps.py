# maps.py
# NOTE: This module defines MapRoom and Zone, replacing the legacy Room class used in engine.py and map_generator.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from enemy import Enemy

@dataclass
class Zone:
    internal_name: str
    display_name: str
    features: List[str] = field(default_factory=list)
    enemies: List[Enemy] = field(default_factory=list)
    hidden_items: List[str] = field(default_factory=list)
    visible: bool = False

@dataclass
class MapRoom:
    id: str  # unique key used internally
    name: str
    description: str
    exits: Dict[str, str]  # e.g. {'n': 'guard_post'}
    zones: Dict[str, Zone]  # e.g. {'center': Zone(...), 'west': Zone(...) }
    zone_adjacency: Dict[str, List[str]] = field(default_factory=dict)  # Add this line
    
    def visible_enemies(self) -> List[Enemy]:
        return [enemy for zone in self.zones.values() for enemy in zone.enemies if enemy.is_alive()]

    def exit_list(self) -> str:
        return ", ".join(self.exits.keys())

    def describe(self) -> str:
        return f"{self.name}\n{self.description}\nExits: {self.exit_list()}"

# TODO: 1. Add example procedural room templates for prototyping
# TODO: 2. Add perception-based visibility toggles and mechanics
# TODO: 4. Route all map and room descriptions through messaging.py
# TODO: 3. Implement generate_map() that produces MapRoom instances
