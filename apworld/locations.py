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
    **{
        threshold: 31 + i
        for i, threshold in enumerate(
            (
                f"Extra score threshold {i}-{j}"
                for i in range(5, 20)
                for j in range(1, i // 5 + 1)
            ),
            start=1,
        )
    },
}


class SuikapelagoLocation(Location):
    game = "Suikapelago"


def create_all_locations(world: SuikapelagoWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: SuikapelagoWorld) -> None:
    game = world.get_region("Game")

    def is_location_enabled(location):
        name, _ = location
        return (
            "Best fruit" in name
            or ("Score" in name and world.options.scoresanity)
            or ("Extra" in name and world.options.scoresanity == 2)
        )

    game.add_locations(
        dict(filter(is_location_enabled, LOCATION_NAME_TO_ID.items())),
        SuikapelagoLocation,
    )


def create_events(world: SuikapelagoWorld) -> None:
    game = world.get_region("Game")
    game.add_event(
        "Victory",
        "Victory",
        location_type=SuikapelagoLocation,
        item_type=items.SuikapelagoItem,
    )
