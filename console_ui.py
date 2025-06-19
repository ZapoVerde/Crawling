# console_ui.py
from engine import build_game


def main():
    name = input("Enter your adventurer's name: ")
    game = build_game(name)

    def print_room():
        for line in game.look():
            print(line)

    print_room()

    while True:
        if game.player.health <= 0:
            print("💀 You have died.")
            break

        if game.room.enemies and any(e.is_alive() for e in game.room.enemies):
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
