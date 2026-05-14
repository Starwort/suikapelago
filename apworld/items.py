from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import SuikapelagoWorld


### PROGRESSION ###
PROG_HEIGHT = "Progressive Field Height"
PROG_FRUIT = "Progressive Max Fruit"
PROG_NEXT = "Next Fruit View"

### USEFUL ###
USEF_DROP_COOLDOWN = "Progressive Drop Cooldown Reduction"
USEF_POINTS = "Progressive Bonus Points"

### TRAPS ###
# causes the lined-up fruit to be dropped instantly
TRAP_INSTA_DROP = "Instant Drop Trap"
# the position of each fruit is swapped with another fruit, at random (FY-shuffle?)
TRAP_SHUFFLE = "Shuffle Trap"
# applies a large impulse to the bottom of the board
TRAP_IMPULSE = "Impulse Trap"
# deletes 50% of fruits on the board, at random
TRAP_THANOS = "Thanos Trap"

### FILLER ###
FILL_SMOOTHIE = "Fruit Smoothie"

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {
    PROG_HEIGHT: 1,
    PROG_FRUIT: 2,
    PROG_NEXT: 3,
    USEF_DROP_COOLDOWN: 4,
    USEF_POINTS: 5,
    TRAP_INSTA_DROP: 6,
    TRAP_SHUFFLE: 7,
    TRAP_IMPULSE: 8,
    TRAP_THANOS: 9,
    FILL_SMOOTHIE: 10,
}

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
DEFAULT_ITEM_CLASSIFICATIONS = {
    PROG_HEIGHT: ItemClassification.progression,
    PROG_FRUIT: ItemClassification.progression,
    PROG_NEXT: ItemClassification.progression,
    USEF_DROP_COOLDOWN: ItemClassification.useful,
    USEF_POINTS: ItemClassification.useful,
    TRAP_INSTA_DROP: ItemClassification.trap,
    TRAP_SHUFFLE: ItemClassification.trap,
    TRAP_IMPULSE: ItemClassification.trap,
    TRAP_THANOS: ItemClassification.trap,
    FILL_SMOOTHIE: ItemClassification.filler,
}


# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class SuikapelagoItem(Item):
    game = "Suikapelago"


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: SuikapelagoWorld) -> str:
    item_class = world.random.randrange(100)
    if item_class < world.options.trap_chance:
        return world.random.choices(
            [TRAP_INSTA_DROP, TRAP_SHUFFLE, TRAP_IMPULSE, TRAP_THANOS],
            weights=[
                +world.options.insta_drop_trap_weight,
                +world.options.shuffle_trap_weight,
                +world.options.impulse_trap_weight,
                +world.options.thanos_trap_weight,
            ],
        )[0]
    elif item_class < world.options.trap_chance + world.options.bonus_points_chance:
        return USEF_POINTS
    else:
        # todo: more filler?
        return world.random.choice([FILL_SMOOTHIE])


def create_item_with_correct_classification(
    world: SuikapelagoWorld, name: str
) -> SuikapelagoItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return SuikapelagoItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: SuikapelagoWorld) -> None:
    itempool: list[Item] = [
        *(
            world.create_item(PROG_FRUIT)
            for _ in range(11 - world.options.starting_max_fruit_size)
        ),
        *(
            world.create_item(PROG_HEIGHT)
            for _ in range(world.options.height_upgrade_count)
        ),
        *(
            world.create_item(USEF_DROP_COOLDOWN)
            for _ in range(world.options.cooldown_upgrade_count)
        ),
        *(world.create_item(PROG_NEXT) for _ in range(world.options.next_needs_unlock)),
    ]
    assert len(itempool) == world.min_num_items, (
        f"Expected to create {world.min_num_items};"
        f" actually created {len(itempool)} ({itempool})"
    )

    num_unfilled = len(world.multiworld.get_unfilled_locations(world.player))

    assert num_unfilled == world.num_locations, (
        f"Expected to have {world.num_locations} unfilled locations;"
        f" actually had {num_unfilled}"
    )

    itempool += [
        world.create_filler() for _ in range(world.num_locations - world.min_num_items)
    ]

    world.multiworld.itempool += itempool
