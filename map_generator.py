#map_generator.py
from enemy_utils import make_multiple_enemies
from enemy_data import make_goblin, make_spider
from room import Room


def generate_map():
    room1 = Room("Entrance Hall",
                 "Dark and musty, with cobwebs in the corners.",
                 {"e": "room2"})

    room2 = Room("Torchlit Corridor",
                 "Dim torches flicker on the walls.", {
                     "w": "room1",
                     "s": "room3"
                 },
                 enemies=make_multiple_enemies(make_spider, 2))

    room3 = Room("Goblin Lair",
                 "You hear snarling in the dark...", {"n": "room2"},
                 enemies=make_multiple_enemies(make_goblin, 1) +
                 make_multiple_enemies(make_spider, 1))

    dungeon_map = {"room1": room1, "room2": room2, "room3": room3}

    return dungeon_map, "room1"
