# engine.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from player import Player
from room import Room
from enemy import Enemy
from combat import resolve_attack
from status_effects import process_effects

@dataclass
class Game:
    player: Player
    rooms: Dict[str, Room]
    current_key: str
    previous_key: Optional[str] = None
    turns: int = 0
    move_progress: int = 0
    target_direction: Optional[str] = None
    search_bonus_turns: int = 0

    def get_effective_perception(self) -> int:
        base_per = self.player.stats.get("PER", 0)
        bonus = 3 if self.search_bonus_turns > 0 else 0
        return base_per + bonus

    def is_enemy_visible(self, enemy: Enemy) -> bool:
        perception = self.get_effective_perception()
        detection_score = perception - enemy.stealth + (enemy.size - 5)
        return detection_score >= 0

    def flee(self) -> List[str]:
        if not self.previous_key:
            return ["You have nowhere to run!"]

        self.current_key, self.previous_key = self.previous_key, self.current_key
        lines = ["🏃 You flee back to the previous room."]
        lines += self.advance_turn()
        lines += self.look()
        return lines

    def search(self) -> List[str]:
        self.search_bonus_turns = 2
        return ["🔍 You carefully examine your surroundings. Perception increased temporarily."]

    def move(self, direction: str) -> List[str]:
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
    def room(self) -> Room:
        return self.rooms[self.current_key]

    def look(self) -> List[str]:
        room = self.room
        lines = [
            f"📍 {room.name}",
            room.description,
            f"Exits: {room.exit_list()}",
        ]
        if room.enemies:
            enemies = [e.name for e in room.enemies if e.is_alive()]
            if enemies:
                lines.append("Enemies here: " + ", ".join(enemies))
        return lines

    def attack(self) -> List[str]:
        alive = [e for e in self.room.enemies if e.is_alive()]
        
        if not alive:
            lines = ["There is nothing to fight."]
            lines += self.advance_turn()
            return lines

        lines = []

        # Player attacks first living enemy
        target = alive[0]
        roll_mod = self.player.skill + self.player.buffs.get("attack_bonus", 0)
        lines += resolve_attack(self.player, target, roll_mod=roll_mod, half=False, buffs=self.player.buffs)

        # Enemies retaliate
        for enemy in alive:
            if enemy.is_alive():
                lines += resolve_attack(enemy, self.player, roll_mod=0, half=True)

        lines.append(f"💖 Your health: {self.player.health}")
        if self.player.health <= 0:
            lines.append("💀 You have been slain!")

        lines += self.advance_turn()
        return lines

    def advance_turn(self) -> List[str]:
        self.turns += 1
        lines = []

        if self.search_bonus_turns > 0:
            self.search_bonus_turns -= 1

        # Always process player effects
        lines += process_effects(self.player)

        # Only process enemy effects if any are alive
        alive_enemies = [enemy for enemy in self.room.enemies if enemy.is_alive()]
        for enemy in alive_enemies:
            lines += process_effects(enemy)

        # Optional: append a summary if no enemies remain
        if not alive_enemies:
            lines.append("🧘 The room is quiet...")

        return lines

def build_game(player_name: str) -> Game:
    from map_generator import generate_map
    from player import Player

    player = Player(name=player_name)
    rooms, starting_key = generate_map()
    return Game(player=player, rooms=rooms, current_key=starting_key)
