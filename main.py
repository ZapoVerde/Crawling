import sys
import random  
from player import Player
from room import Room
from map_generator import generate_map
from enemy import Enemy  # Add to the top of main.py

def welcome():
    print("🧱 Welcome to Dungeon Crawler 🗡️")
    name = input("Enter your adventurer's name: ")
    print(f"\nGreetings, {name}! Your journey begins...\n")
    return name

def main():
    player_name = welcome()
    player = Player(name=player_name)
    dungeon_map, starting_room = generate_map()
    current_room = dungeon_map[starting_room]
    previous_room = None
    in_combat = False

    while True:
        print("\n" + "=" * 40)

        alive_enemies = [e for e in current_room.enemies if e.is_alive()] if current_room.enemies else []

        if alive_enemies:
            # Combat mode - show only combat info
            in_combat = True
            print(f"You are in combat in the {current_room.name}!")
            for enemy in alive_enemies:
                print(f"- {enemy.name} (HP: {enemy.health})")

            action = input("Do you want to (a)ttack or (r)un? ").lower().strip()

            if action == "a":
                # Attack first alive enemy
                target = alive_enemies[0]
                damage = 10  # Or your damage calculation
                target.health -= damage
                print(f"You hit the {target.name} for {damage} damage!")

                if not target.is_alive():
                    print(f"You defeated the {target.name}!")

                # Enemies retaliate
                for enemy in alive_enemies:
                    if enemy.is_alive():
                        enemy_damage = enemy.attack()
                        player.health -= enemy_damage
                        print(f"The {enemy.name} hits you for {enemy_damage} damage!")
                        if player.health <= 0:
                            print("💀 You have been slain. Game over.")
                            return

                print(f"💖 Your health: {player.health}")

            elif action == "r":
                print("You flee back the way you came!")
                # Move player back to previous room if possible
                if previous_room:
                    current_room = previous_room
                else:
                    print("No way back! You must fight.")
                in_combat = False

            else:
                print("Invalid action.")

        else:
            # Exploration mode - show full room info
            in_combat = False
            print(type(current_room))
            print(dir(current_room))
            print(current_room.describe())
            available_dirs = ", ".join(current_room.exits.keys())
            command = input(f"\nWhat do you want to do? ({available_dirs}/quit): ").lower().strip()

            if command == "quit":
                print("Thanks for playing!")
                break
            elif command in current_room.exits:
                previous_room = current_room
                next_room_key = current_room.exits[command]
                current_room = dungeon_map[next_room_key]
            else:
                print("You can't go that way.")

if __name__ == "__main__":
    main()