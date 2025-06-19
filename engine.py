# engine.py
from dataclasses import dataclass, field
import random
import math
from typing import Dict, List, Optional

from player import Player
from room import Room
from enemy import Enemy

DICE_UNICODE = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}


def roll_multiplier(roll: float, half: bool = False) -> float:
    """
    Uses a lookup curve for rolls <= 10.5 and smooth exponential for high rolls (>10.5).
    Applies optional half-scaling for enemies.
    """
    roll = min(12.0, max(2.0, roll))

    if roll <= 10.5:
        if roll <= 2:
            base = 0.0
        elif roll <= 3:
            base = 0.25
        elif roll <= 4:
            base = 0.42
        elif roll <= 5:
            base = 0.57
        elif roll <= 6:
            base = 0.73
        elif roll <= 7:
            base = 0.85
        elif roll <= 8:
            base = 1.00
        elif roll <= 9:
            base = 1.25
        elif roll <= 10:
            base = 1.67
        else:  # roll == 10.5
            base = 2.08
    else:
        exponent_base = math.exp((roll - 10.5) / 1.0)
        normalized = 2.5 * (exponent_base / math.exp(1.5))
        base = normalized

    return base * 0.5 if half else base

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
    
    def get_effective_perception(self) -> int:
        base_per = self.player.stats.get("PER", 0)
        bonus = 3 if self.search_bonus_turns > 0 else 0
        return base_per + bonus
    
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

    def roll_2d6_verbose(self, mod: int = 0) -> tuple[int, str, str]:
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        base_total = die1 + die2
        modified_total = base_total + mod
        symbols = f"{DICE_UNICODE[die1]} {DICE_UNICODE[die2]}"
        return modified_total, symbols, f"🎲 Roll: {symbols} → {base_total} + {mod} = {modified_total}"

    def interpret_roll(self, total: int, buffs: dict = {}) -> str:
        if buffs.get("no_crit") and total == 12:
            return "🎯 Solid hit (crit blocked by debuff)"
        if total == 2:
            return "💀 Critical Failure! You stumble badly."
        elif total in (3, 4):
            return "⚠️ Glancing Blow. You barely connect."
        elif total == 12:
            return "💥 Critical Hit! Devastating strike!"
        else:
            return "✅ Hit!"

    def attack(self) -> List[str]:
        alive = [e for e in self.room.enemies if e.is_alive()]
        if not alive:
            return ["There is nothing to fight."]

        target = alive[0]
        lines = []

        roll_mod = self.player.skill + self.player.buffs.get("attack_bonus", 0)
        total, symbols, display = self.roll_2d6_verbose(roll_mod)
        lines.append(display)

        outcome = self.interpret_roll(total, self.player.buffs)
        lines.append(outcome)

        if total == 2:
            lines.append("You miss and lose your balance.")
        else:
            base = 10 + self.player.power
            dmg = int(base * roll_multiplier(total))
            lines.append(f"You hit the {target.name} for {dmg} damage.")

        if not target.is_alive():
            lines.append(f"The {target.name} is defeated!")

        # Enemies retaliate
        for enemy in alive:
            if enemy.is_alive():

                roll, _, _ = self.roll_2d6_verbose()
                mult = roll_multiplier(roll, half=True)
                damage = int(enemy.attack() * mult)
                self.player.health -= damage
                lines.append(f"The {enemy.name} hits you for {damage} damage!")

                # Apply poison if enemy has the trait
                if "poison_on_hit" in enemy.traits:
                    poison = enemy.traits["poison_on_hit"]
                    effect = {
                        "type": "poison",
                        "damage": poison.get("damage", 2),
                        "duration": poison.get("duration", 3)
                    }
                    self.player.status_effects.append(effect)
                    lines.append(f"☠️ The {enemy.name}'s bite poisons you!")

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

        expired = []
        for effect in self.player.status_effects:
            if "duration" in effect:
                effect["duration"] -= 1
                if effect["duration"] <= 0:
                    expired.append(effect)

            if effect["type"] == "poison":
                dmg = effect.get("damage", 2)
                self.player.health -= dmg
                lines.append(f"☠️ You suffer {dmg} poison damage.")

            if effect["type"] == "regen":
                heal = effect.get("heal", 3)
                self.player.health += heal
                lines.append(f"💚 You regenerate {heal} health.")

        for e in expired:
            lines.append(f"⏳ {e['type'].capitalize()} has worn off.")
            self.player.status_effects.remove(e)

        return lines


def build_game(player_name: str) -> Game:
    from map_generator import generate_map
    from player import Player

    player = Player(name=player_name)
    rooms, starting_key = generate_map()
    return Game(player=player, rooms=rooms, current_key=starting_key)
