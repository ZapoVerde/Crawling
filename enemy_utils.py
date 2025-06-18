# enemy_utils.py

def make_multiple_enemies(factory_func, count):
    """
    Create a list of enemies using the given factory function.

    Args:
        factory_func (function): The enemy factory function, e.g., make_goblin.
        count (int): Number of enemies to create.

    Returns:
        list: A list of enemy instances.
    """
    return [factory_func() for _ in range(count)]