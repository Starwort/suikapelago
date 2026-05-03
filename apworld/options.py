from dataclasses import dataclass

from Options import Choice, DeathLink, PerGameCommonOptions, Range, Toggle


class Scoresanity(Toggle):
    """
    Earn checks for various score thresholds
    """

    display_name = "Scoresanity"

    default = 1


class TrapChance(Range):
    """
    Chance, in percent, that any given filler item will be replaced with a trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 10


class StartingFruitSizeCount(Range):
    """
    How many sizes of fruit to start with access to. Fewer starting fruit means fewer sphere 1 checks.
    """

    display_name = "Initial number of sizes of fruit"

    range_start = 1
    range_end = 11

    default = 2

class HeightUpgradeCount(Range):
    """
    How many Progressive Field Height items to add into the pool. When set to 0,
    disables the feature. When non-zero, the field starts at 50% of its normal
    height and increases linearly to its normal height with each Progressive Field
    Height
    """

    display_name = "Progressive Field Height Count"

    range_start = 0
    range_end = 10

    default = 5


class ShuffleFruitOrder(Toggle):
    """
    Shuffle the fruit order. Fruit will still be the same size, but will use the
    name and sprite of other fruit
    """

    display_name = "Shuffle Fruit Order"

    default = 0

class Goal(Choice):
    """
    Which condition(s) are required for victory. If score or both is chosen,
    will turn on Scoresanity
    """
    display_name = "Goal"

    option_watermelon = 0
    option_score = 1
    option_both = 2

    default = 0


@dataclass
class SuikapelagoOptions(PerGameCommonOptions):
    death_link: DeathLink
    scoresanity: Scoresanity
    trap_chance: TrapChance
    starting_fruit_size_count: StartingFruitSizeCount
    shuffle_fruit_order: ShuffleFruitOrder
    height_upgrade_count: HeightUpgradeCount

