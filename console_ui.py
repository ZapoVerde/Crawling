# console_ui.py
from engine import build_game

def main():
    name = "Bob"
    game = build_game(name)
    game.player.debug_mode = True

    from item_data import get_basic_weapons
    game.player.weapon = get_basic_weapons()["knife"]

    def print_room():
        for line in game.look():
            print(line)

    print_room()

    while True:
        if game.is_game_over():
            for line in game.get_game_over_message():
                print(line)
            break

        if game.room.visible_enemies():
            cmd = input("\n(a=attack, r=run, q=quit) > ").lower().strip()[:1]
        else:
            available_dirs = "".join(game.room.exits.keys())
            cmd = input(f"\n({available_dirs}, q=quit) > ").lower().strip()[:1]

        if cmd in "nesw":
            for line in game.move(cmd):
                print(line)
            print_room()
        elif cmd == "a":
            for line in game.attack():
                print(line)
        elif cmd == "r":
            for line in game.flee():
                print(line)
        elif cmd == "q":
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
