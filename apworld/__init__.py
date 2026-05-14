from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from BaseClasses import Region
from Options import OptionError
from worlds.AutoWorld import World

from . import items, locations, rules, web_world
from . import (
    options as suika_options,
)  # rename due to a name conflict with World.options

if TYPE_CHECKING:
    from BaseClasses import MultiWorld


class SuikapelagoWorld(World):
    """
    Suikapelago is a clone of Suika Game, modified to work with Archipelago.
    """

    game = "Suikapelago"

    web = web_world.SuikapelagoWebWorld()

    options_dataclass = suika_options.SuikapelagoOptions
    options: suika_options.SuikapelagoOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Game"

    def __init__(self, mw: "MultiWorld", player: int):
        super().__init__(mw, player)
        self.fruit_order = list(range(11))

    def generate_early(self) -> None:
        if self.options.shuffle_fruit_order:
            self.random.shuffle(self.fruit_order)
        if self.options.goal != suika_options.Goal.option_watermelon:
            self.options.scoresanity = suika_options.Scoresanity(1)
        if self.options.trap_chance + self.options.bonus_points_chance > 100:
            raise OptionError("Trap chance + Bonus Points chance is greater than 100%!")
        self.num_locations = 11 + (
            20 if self.options.scoresanity else 0
        )  # one for each fruit size + 20 target scores
        self.min_num_items = (
            (11 - self.options.starting_max_fruit_size)
            + self.options.height_upgrade_count
            + self.options.cooldown_upgrade_count
            + self.options.next_needs_unlock
        )
        if self.min_num_items > self.num_locations:
            raise OptionError(
                "Current settings would generate more items than exist locations!"
                "\n\nTry turning on scoresanity, increasing your starting maximum"
                " fruit size, or lowering the number of height/cooldown upgrades"
            )

    def create_regions(self) -> None:
        self.multiworld.regions.append(Region("Game", self.player, self.multiworld))
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.SuikapelagoItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "deathlink": bool(self.options.death_link),
            "shuffle_fruit": (
                self.fruit_order if self.options.shuffle_fruit_order else None
            ),
            "height_upgrade_count": +self.options.height_upgrade_count,
            "cooldown_upgrade_count": +self.options.cooldown_upgrade_count,
            "goal": +self.options.goal,
            "scoresanity": bool(self.options.scoresanity),
            "difficulty": +self.options.scoresanity_difficulty,
            "max_fruit_size": +self.options.starting_max_fruit_size,
            "next_needs_unlock": bool(self.options.next_needs_unlock),
        }
