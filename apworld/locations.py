from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from . import SuikapelagoWorld

BEST_FRUIT_LOCS = [
    "Best fruit: Cherry or better",
    "Best fruit: Strawberry or better",
    "Best fruit: Grapes or better",
    "Best fruit: Dekopon or better",
    "Best fruit: Persimmon or better",
    "Best fruit: Apple or better",
    "Best fruit: Pear or better",
    "Best fruit: Peach or better",
    "Best fruit: Pineapple or better",
    "Best fruit: Melon or better",
    "Best fruit: Watermelon or better",
]

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Best fruit: Cherry or better": 1,
    "Best fruit: Strawberry or better": 2,
    "Best fruit: Grapes or better": 3,
    "Best fruit: Dekopon or better": 4,
    "Best fruit: Persimmon or better": 5,
    "Best fruit: Apple or better": 6,
    "Best fruit: Pear or better": 7,
    "Best fruit: Peach or better": 8,
    "Best fruit: Pineapple or better": 9,
    "Best fruit: Melon or better": 10,
    "Best fruit: Watermelon or better": 11,
    **{f"Score threshold {i}": 11 + i for i in range(1, 21)},
}


class SuikapelagoLocation(Location):
    game = "Suikapelago"


def create_all_locations(world: SuikapelagoWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: SuikapelagoWorld) -> None:
    game = world.get_region("Game")
    game.add_locations(LOCATION_NAME_TO_ID, SuikapelagoLocation)


def create_events(world: SuikapelagoWorld) -> None:
    game = world.get_region("Game")
    game.add_event(
        "Victory",
        "Victory",
        location_type=SuikapelagoLocation,
        item_type=items.SuikapelagoItem,
    )
