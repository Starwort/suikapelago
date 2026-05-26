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
        scoresanity_requirements = {
            i: max(0, (i + 1) // 2 - world.options.starting_max_fruit_size)
            for i in range(1, 21)
        }
        for threshold, upgrades_req in scoresanity_requirements.items():
            if upgrades_req == 0:
                continue
            world.set_rule(
                world.get_location(f"Score threshold {threshold}"),
                Has(PROG_FRUIT, count=upgrades_req),
            )
            if world.options.scoresanity == 2 and threshold != 20:
                for i in range(1, threshold // 5 + 1):
                    world.set_rule(
                        world.get_location(f"Extra score threshold {threshold}-{i}"),
                        Has(PROG_FRUIT, count=upgrades_req),
                    )
    victory = world.get_location("Victory")
    world.set_rule(
        victory, Has(PROG_FRUIT, count=11 - world.options.starting_max_fruit_size)
    )


def set_completion_condition(world: SuikapelagoWorld) -> None:
    world.set_completion_rule(Has("Victory"))
