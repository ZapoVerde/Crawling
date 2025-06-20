# testbed.py

from player import Player
from enemy_data import make_spider
from status_effects import apply_effect, process_effects
from combat import resolve_attack

def log_section(title):
    print("\n" + "═" * 50)
    print(f"🔬 {title}")
    print("═" * 50)

def test_poison_stacking():
    log_section("Poison stacking and expiry")

    player = Player(name="TestSubject")
    player.health = 100
    player.is_player = True

    # Apply 3 poison stacks with duration 3
    for _ in range(3):
        apply_effect(player, {"type": "poison", "damage": 2, "duration": 3})

    # Simulate 4 turns
    for turn in range(1, 5):
        print(f"\n🔄 Turn {turn}")
        logs = process_effects(player)
        for line in logs:
            print(line)
        print(f"❤️ Health: {player.health}")

def test_regen_vs_poison():
    log_section("Regen vs Poison over time")

    player = Player(name="RegenTank")
    player.health = 90
    player.is_player = True

    # Apply poison and regen
    for _ in range(2):
        apply_effect(player, {"type": "poison", "damage": 2, "duration": 2})
    apply_effect(player, {"type": "regen", "heal": 3, "duration": 3})

    for turn in range(1, 5):
        print(f"\n🔄 Turn {turn}")
        logs = process_effects(player)
        for line in logs:
            print(line)
        print(f"❤️ Health: {player.health}")

def test_bleeding_stub():
    log_section("Bleeding (stub for future effect)")

    player = Player(name="Bleeder")
    player.health = 100
    player.is_player = True

    # You can implement bleeding just like poison when ready
    apply_effect(player, {"type": "bleeding", "damage": 1, "duration": 3})

    for turn in range(1, 5):
        print(f"\n🔄 Turn {turn}")
        logs = process_effects(player)
        for line in logs:
            print(line)
        print(f"❤️ Health: {player.health}")

def test_combat_roll():
    log_section("Basic Combat Roll")

    player = Player(name="BladeMan")
    player.health = 100
    player.skill = 2
    player.is_player = True

    enemy = make_spider()
    enemy.health = 25
    enemy.is_player = False

    logs = resolve_attack(player, enemy, roll_mod=2, half=False)
    for line in logs:
        print(line)

if __name__ == "__main__":
    test_poison_stacking()
    test_regen_vs_poison()
    test_bleeding_stub()
    test_combat_roll()
