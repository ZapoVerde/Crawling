# engine.py
# NOTE: Game loop and player interaction logic for room traversal, combat, and perception

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from player import Player
from maps import MapRoom
from enemy import Enemy
from combat import resolve_attack
from status_effects import process_effects
from messaging import format_status_effect
from messaging import msg_game_over
from messaging import format_zone_description
import movement

@dataclass
class Game:
    player: Player
    rooms: Dict[str, MapRoom]  # All known rooms keyed by room id
    current_key: str           # ID of current room
    previous_key: Optional[str] = None
    turns: int = 0
    move_progress: int = 0
    target_direction: Optional[str] = None
    search_bonus_turns: int = 0
    player_zone: str = "center"  # default starting zone

    def move_player_to_keyword(self, keyword: str) -> list[str]:
        """
        Delegate player movement by keyword to movement.py and return messages.
        """
        success, messages = movement.move_player_to_keyword(self, keyword)
        return messages

    def is_game_over(self) -> bool:
        return self.player.health <= 0

    def get_game_over_message(self) -> List[str]:
        return [msg_game_over()] if self.is_game_over() else []
    

    def get_effective_perception(self) -> int:
        """Compute current perception, factoring in temporary bonuses."""
        base_per = self.player.stats.get("PER", 0)
        bonus = 3 if self.search_bonus_turns > 0 else 0
        return base_per + bonus

    def describe_player_current_zone(self) -> dict:
        """
        Generate a structured description of the player's current zone,
        filtered to only include what the player can perceive.

        Returns:
            dict: Data structure describing visible features and enemies.
        """
        zone = self.room.zones.get(self.player_zone)
        if not zone:
            return {
                "zone_name": "Unknown",
                "features": [],
                "enemies": []
            }

        perception = self.get_effective_perception()

        # Filter enemies by perception
        visible_enemies = []
        for enemy in zone.enemies:
            if enemy.is_alive():
                detection_score = perception - enemy.stealth + (enemy.size - 5)
                if detection_score >= 0:
                    visible_enemies.append({
                        "name": enemy.name,
                        "status": "alive"
                    })

        # Optionally, you can filter features here too if you add stealth or hidden flags
            # Stub: Filter features based on visibility
        visible_features = self.filter_visible_features(zone.features, perception)

        return {
            "zone_name": zone.display_name,
            "features": visible_features,
            "enemies": visible_enemies
        }

    def filter_visible_features(self, features: list[str], perception: int) -> list[str]:
        """
        Stub for filtering features based on player perception or other criteria.

        Args:
            features (list[str]): List of all features in the zone.
            perception (int): Player's effective perception score.

        Returns:
            list[str]: Filtered list of features visible to the player.
        """
        # TODO: Implement visibility logic for features here.
        # For now, return all features unfiltered.
        return features

    def is_enemy_visible(self, enemy: Enemy) -> bool:
        """Determine whether an enemy is currently visible to the player."""
        perception = self.get_effective_perception()
        detection_score = perception - enemy.stealth + (enemy.size - 5)
        return detection_score >= 0

    def flee(self) -> List[str]:
        """Attempt to flee to the previously visited room."""
        if not self.previous_key:
            return ["You have nowhere to run!"]

        self.current_key, self.previous_key = self.previous_key, self.current_key
        lines = ["🏃 You flee back to the previous room."]
        lines += self.advance_turn()
        lines += self.look()
        return lines

    def search(self) -> List[str]:
        """Activate temporary perception bonus."""
        self.search_bonus_turns = 2
        return ["🔍 You carefully examine your surroundings. Perception increased temporarily."]

    def move(self, direction: str) -> List[str]:
        """Initiate or continue movement in a given direction."""
        lines = []

        if self.target_direction is None:
            self.target_direction = direction
            self.move_progress = 1
            lines.append(f"🚶 You start moving {direction.upper()}...")
        elif self.target_direction == direction:
            self.move_progress += 1
            lines.append(f"🚶 You continue moving {direction.upper()}... ({self.move_progress}/3)")
        else:
            self.target_direction = direction
            self.move_progress = 1
            lines.append(f"🔄 You change direction and start moving {direction.upper()}.")

        if self.move_progress >= 3:
            self.previous_key = self.current_key
            self.current_key = self.room.exits[self.target_direction]
            lines.append(f"➡️ You arrive at the {self.room.name}.")
            self.move_progress = 0
            self.target_direction = None
            lines += self.look()

        lines += self.advance_turn()
        return lines

    @property
    def room(self) -> MapRoom:
        """Convenience accessor for the current room."""
        return self.rooms[self.current_key]

    def look(self) -> List[str]:
        """Describe the current room, its exits, and any visible enemies."""
        room = self.room
        lines = [
            f"📍 {room.name}",
            room.description,
            f"Exits: {room.exit_list()}",
        ]
        visible = room.visible_enemies()
        if visible:
            lines.append("Enemies here: " + ", ".join(e.name for e in visible))
        return lines

    def attack(self) -> List[str]:
        """Resolve combat against visible enemies in the room."""
        enemies = self.room.visible_enemies()

        if not enemies:
            lines = ["There is nothing to fight."]
            lines += self.advance_turn()
            return lines

        lines = []

        # Player attacks first visible enemy
        target = enemies[0]
        roll_mod = self.player.skill + self.player.buffs.get("attack_bonus", 0)
        lines += resolve_attack(self.player, target, roll_mod=roll_mod, half=False, buffs=self.player.buffs)

        # Enemies retaliate
        for enemy in enemies:
            if enemy.is_alive():
                lines += resolve_attack(enemy, self.player, roll_mod=0, half=True)

        lines.append(f"💖 Your health: {self.player.health}")
        if self.player.health <= 0:
            lines.append("💀 You have been slain!")

        lines += self.advance_turn()
        return lines

    def advance_turn(self) -> List[str]:
        """Advance the game clock and apply status effects to all actors."""
        self.turns += 1
        lines = []

        if self.search_bonus_turns > 0:
            self.search_bonus_turns -= 1

        for event in process_effects(self.player):
            lines.extend(format_status_effect(event))

        for enemy in self.room.visible_enemies():
            for event in process_effects(enemy):
                lines.extend(format_status_effect(event))

        if not self.room.visible_enemies():
            lines.append("🧘 The room is quiet...")

        return lines

def build_game(player_name: str) -> Game:
    """Construct the initial Game state from the generated map."""
    from map_generator import generate_test_map
    from player import Player

    player = Player(name=player_name)
    rooms, starting_key = generate_test_map()
    return Game(player=player, rooms=rooms, current_key=starting_key)


#Todo move out all the player facing messages to messaging.py