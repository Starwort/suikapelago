from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    Toggle,
)


class Scoresanity(Toggle):
    """
    Earn checks for various score thresholds
    """

    display_name = "Scoresanity"

    default = 1


class ScoresanityDifficulty(Choice):
    """
    How difficult the Scoresanity checks should be
    """

    display_name = "Scoresanity Difficulty"

    option_very_easy = 0
    option_easy = 1
    option_easier_than_normal = 2
    option_normal = 3
    option_harder_than_normal = 4
    option_hard = 5
    option_very_hard = 6

    default = 3


class TrapChance(Range):
    """
    Chance, in percent, that any given filler item will be replaced with a trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 10


class InstaDropTrapWeight(Range):
    """
    The relative weight that any given trap will be an Instant Drop Trap.

    Note that this is relative to the weights of other traps; if you have
    Instant Drop Trap set to 50, Shuffle Trap set to 25, and all other traps set
    to 0, there will be a 2/3 chance of Instant Drop trap being selected when a
    trap is generated
    """

    display_name = "Instant Drop Trap weight"

    range_start = 0
    range_end = 100

    default = 50


class ShuffleTrapWeight(Range):
    """
    The relative weight that any given trap will be an Shuffle Trap.

    Note that this is relative to the weights of other traps; if you have
    Instant Drop Trap set to 50, Shuffle Trap set to 25, and all other traps set
    to 0, there will be a 2/3 chance of Instant Drop trap being selected when a
    trap is generated
    """

    display_name = "Shuffle Trap weight"

    range_start = 0
    range_end = 100

    default = 50


class ImpulseTrapWeight(Range):
    """
    The relative weight that any given trap will be an Impulse Trap.

    Note that this is relative to the weights of other traps; if you have
    Instant Drop Trap set to 50, Shuffle Trap set to 25, and all other traps set
    to 0, there will be a 2/3 chance of Instant Drop trap being selected when a
    trap is generated
    """

    display_name = "Impulse Trap weight"

    range_start = 0
    range_end = 100

    default = 50


class ThanosTrapWeight(Range):
    """
    The relative weight that any given trap will be an Thanos Trap.

    Note that this is relative to the weights of other traps; if you have
    Instant Drop Trap set to 50, Shuffle Trap set to 25, and all other traps set
    to 0, there will be a 2/3 chance of Instant Drop trap being selected when a
    trap is generated
    """

    display_name = "Thanos Trap weight"

    range_start = 0
    range_end = 100

    default = 50


class BonusPointsChance(Range):
    """
    Chance, in percent, that any given filler item will be replaced with some
    bonus points.
    """

    display_name = "Bonus Points Chance"

    range_start = 0
    range_end = 100
    default = 10


class StartingMaxFruitSize(Range):
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


class NextNeedsUnlock(Toggle):
    """
    Does the ability to see the next fruit need unlocking?
    """

    display_name = "Next needs unlock"

    default = 1


class CooldownUpgradeCount(Range):
    """
    How many Progressive Cooldown Reduction items to add into the pool. When set
    to 0, disables the feature. When non-zero, you start with a 60 second cooldown
    between each fruit drop, which reduces linearly to zero with each Progressive
    Cooldown Reduction
    """

    display_name = "Progressive Cooldown Reduction Count"

    range_start = 0
    range_end = 10

    default = 5


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


option_groups = [
    OptionGroup(
        "Game Options",
        [
            DeathLink,
            Goal,
            ShuffleFruitOrder,
            StartingMaxFruitSize,
            Scoresanity,
            ScoresanityDifficulty,
            HeightUpgradeCount,
            CooldownUpgradeCount,
            NextNeedsUnlock,
        ],
    ),
    OptionGroup(
        "Item Options",
        [
            BonusPointsChance,
            TrapChance,
            InstaDropTrapWeight,
            ShuffleTrapWeight,
            ImpulseTrapWeight,
            ThanosTrapWeight,
        ],
    ),
]


@dataclass
class SuikapelagoOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    scoresanity: Scoresanity
    scoresanity_difficulty: ScoresanityDifficulty
    starting_max_fruit_size: StartingMaxFruitSize
    shuffle_fruit_order: ShuffleFruitOrder
    height_upgrade_count: HeightUpgradeCount
    cooldown_upgrade_count: CooldownUpgradeCount
    next_needs_unlock: NextNeedsUnlock
    bonus_points_chance: BonusPointsChance
    trap_chance: TrapChance
    insta_drop_trap_weight: InstaDropTrapWeight
    shuffle_trap_weight: ShuffleTrapWeight
    impulse_trap_weight: ImpulseTrapWeight
    thanos_trap_weight: ThanosTrapWeight
