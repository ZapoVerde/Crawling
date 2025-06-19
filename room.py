class Room:

    def __init__(self, name, description, exits, enemies=None):
        self.name = name
        self.description = description
        self.exits = exits
        self.enemies = enemies if enemies else []

    def describe(self):
        direction_names = {
            'n': 'north',
            's': 'south',
            'e': 'east',
            'w': 'west'
        }
        exits_list = ", ".join(
            direction_names.get(dir, dir) for dir in self.exits.keys())
        desc = f"{self.name}\n{self.description}\nExits: {exits_list}"
        if self.enemies:
            alive_enemies = [e.name for e in self.enemies if e.is_alive()]
            if alive_enemies:
                desc += f"\nEnemies here: {', '.join(alive_enemies)}"
        return desc

    def exit_list(self) -> str:
        return ", ".join(self.exits.keys())
