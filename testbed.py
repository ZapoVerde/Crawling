def test_generate_test_map_structure():
    rooms, start = generate_test_map()
    assert isinstance(rooms[start], MapRoom)
    assert "center" in rooms[start].zones
    assert isinstance(rooms[start].zones["center"], Zone)

def test_room_access_and_look():
    game = build_game("TestGuy")
    look_lines = game.look()
    assert any("Entrance Hall" in line for line in look_lines)
    assert any("Exits:" in line for line in look_lines)

def test_enemy_visibility_and_attack():
    game = build_game("TestGuy")
    enemies = game.room.visible_enemies()
    assert enemies, "Expected at least one visible enemy in starting room"
    result = game.attack()
    assert any("damage" in line or "hit" in line for line in result)

def test_movement_between_rooms():
    game = build_game("TestGuy")
    result = game.move("e")
    assert any("arrive" in line for line in result), "Expected arrival message"
    assert game.room.id == "guard_post"

def test_flee_to_previous_room():
    game = build_game("TestGuy")
    game.move("e")
    result = game.flee()
    assert game.room.id == "entrance_hall"
    assert any("flee" in line for line in result)
