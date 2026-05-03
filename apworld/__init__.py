from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as suika_options  # rename due to a name conflict with World.options

if TYPE_CHECKING:
    from BaseClasses import MultiWorld

class SuikapelagoWorld(World):
    """
    Suikapelago is a clone of Suika Game, modified to work with Archipelago.
    """

    game = "Suikapelago"

    web = web_world.SuikapelagoWebWorld()

    options_dataclass = suika_options.SuikapelagoOptions
    options: suika_options.SuikapelagoOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    def __init__(self, mw: "MultiWorld", player: int):
        super().__init__(mw, player)
        self.fruit_order = list(range(11))
        if self.options.shuffle_fruit_order:
            self.random.shuffle(self.fruit_order)

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, the same one that create_items is in.
    def create_item(self, name: str) -> items.SuikapelagoItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return {
            "shuffle_fruit": self.fruit_order if self.options.shuffle_fruit_order else None,
            "height_upgrade_count": self.options.height_upgrade_count,
            "scoresanity": bool(self.options.scoresanity),
        }
