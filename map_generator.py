from maps import MapRoom, Zone
from enemy_data import make_spider, make_goblin

def generate_test_map():
    """
    Construct a small static test map with three rooms,
    each with multiple descriptive zones and adjacency info.
    """

    room1 = MapRoom(
        id="entrance_hall",
        name="Entrance Hall",
        description="Dusty stonework with signs of age.",
        exits={"guardpost_doorway": "guard_post"},
        zones={
            "zone1": Zone(
                internal_name="zone1",
                display_name="Entrance Hall Doorway"
            ),
            "zone2": Zone(
                internal_name="zone2",
                display_name="Crate Stack",
                features=["crates"],
                hidden_items=["old key"]
            ),
            "zone3": Zone(
                internal_name="zone3",
                display_name="Broken Pillar"
            ),
            "zone4": Zone(
                internal_name="zone4",
                display_name="Shadowy Corner"
            ),
            "zone5": Zone(
                internal_name="zone5",
                display_name="Guardpost Doorway",
                enemies=[make_spider()]
            ),
            "zone6": Zone(
                internal_name="zone6",
                display_name="Center"
            )
        },
        zone_adjacency={
            "zone1": ["zone6"],
            "zone2": ["zone6"],
            "zone3": ["zone4"],
            "zone4": ["zone3", "zone6"],
            "zone5": ["zone6"],
            "zone6": ["zone1", "zone2", "zone4", "zone5"]
        }
    )

    # Assign enemy zone location
    for enemy in room1.zones["zone5"].enemies:
        enemy.current_zone = "zone5"

    room2 = MapRoom(
        id="guard_post",
        name="Guard Post",
        description="A watchful silence lingers here.",
        exits={"entrance_hall_doorway": "entrance_hall", "collapsed_chamber_doorway": "collapsed_chamber"},
        zones={
            "zone1": Zone(
                internal_name="zone1",
                display_name="Entrance Hall Doorway"
            ),
            "zone2": Zone(
                internal_name="zone2",
                display_name="Broken Weapon Rack",
                features=["broken weapon rack"]
            ),
            "zone3": Zone(
                internal_name="zone3",
                display_name="Collapsed Chamber Doorway",
                enemies=[make_goblin()]
            ),
            "zone4": Zone(
                internal_name="zone4",
                display_name="Center"
            )
        },
        zone_adjacency={
            "zone1": ["zone4"],
            "zone2": ["zone4"],
            "zone3": ["zone4"],
            "zone4": ["zone1", "zone2", "zone3"]
        }
    )

    for enemy in room2.zones["zone3"].enemies:
        enemy.current_zone = "zone3"

    room3 = MapRoom(
        id="collapsed_chamber",
        name="Collapsed Chamber",
        description="The ceiling has partially caved in.",
        exits={"guard_post_doorway": "guard_post"},
        zones={
            "zone1": Zone(
                internal_name="zone1",
                display_name="Collapsed Chamber Doorway"
            ),
            "zone2": Zone(
                internal_name="zone2",
                display_name="Rubble",
                features=["rubble"]
            ),
            "zone3": Zone(
                internal_name="zone3",
                display_name="South Alcove",
                hidden_items=["medkit"]
            )
        },
        zone_adjacency={
            "zone1": ["zone2"],
            "zone2": ["zone1", "zone3"],
            "zone3": ["zone2"]
        }
    )

    # No enemies here to assign zones

    return {
        room1.id: room1,
        room2.id: room2,
        room3.id: room3
    }, room1.id