from enemy import Enemy

def make_goblin():
    return Enemy("Goblin", 20, 4, 8, evasion=15)

def make_spider():
    return Enemy("Giant Spider", 15, 2, 6, evasion=30)