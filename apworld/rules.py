from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has

from .items import PROG_FRUIT
from .locations import BEST_FRUIT_LOCS

if TYPE_CHECKING:
    from . import SuikapelagoWorld


def set_all_rules(world: SuikapelagoWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: SuikapelagoWorld) -> None:
    for upgrades_req, fruit in enumerate(
        world.fruit_order[world.options.starting_max_fruit_size :], start=1
    ):
        world.set_rule(
            world.get_location(BEST_FRUIT_LOCS[fruit]),
            Has(PROG_FRUIT, count=upgrades_req),
        )
    if world.options.scoresanity:
        for upgrades_req, score_threshold in enumerate(
            range(world.options.starting_max_fruit_size - 1, 10), start=1
        ):
            world.set_rule(
                world.get_location(f"Score threshold {2 * score_threshold}"),
                Has(PROG_FRUIT, count=upgrades_req),
            )
            world.set_rule(
                world.get_location(f"Score threshold {2 * score_threshold + 1}"),
                Has(PROG_FRUIT, count=upgrades_req),
            )
    victory = world.get_location("Victory")
    world.set_rule(
        victory, Has(PROG_FRUIT, count=11 - world.options.starting_max_fruit_size)
    )


def set_completion_condition(world: SuikapelagoWorld) -> None:
    world.set_completion_rule(Has("Victory"))
