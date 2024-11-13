# -*- coding: utf-8 -*-
"""Provide the interface methods required by a mancala
game for the mancala_ui. Constants and paramters used to
control game play are also included.

IntEnums are used for enums that are stored in the
config files

Created on Thu Mar  9 08:38:28 2023
@author: Ann"""


# %% imports

import abc
import dataclasses as dc
import enum

import cfg_keys as ckey


# %%  constants

PASS_TOKEN = 0xffff

# %%  error, enums and dataclasses


class GameInfoError(Exception):
    """Error in GameInfo."""


@enum.unique
class AllowRule(enum.IntEnum):
    """Defines special rules for allowable holes."""

    NONE = 0
    OPP_OR_EMPTY = 1
    SINGLE_TO_ZERO = 2
    SINGLE_ONLY_ALL = 3
    SINGLE_ALL_TO_ZERO = 4
    TWO_ONLY_ALL = 5
    TWO_ONLY_ALL_RIGHT = 6
    FIRST_TURN_ONLY_RIGHT_TWO = 7
    RIGHT_2_1ST_THEN_ALL_TWO = 8


@enum.unique
class CaptExtraPick(enum.IntEnum):
    """Pick extra's over the captured seeds."""

    NONE = 0
    PICKCROSS = 1
    PICKTWOS = 2
    PICKLASTSEEDS = 3
    PICK2XLASTSEEDS = 4


@enum.unique
class ChildRule(enum.IntEnum):
    """Defines additional child restrictions."""

    NONE = 0
    OPP_ONLY = 1
    NOT_1ST_OPP = 2


@enum.unique
class ChildType(enum.IntEnum):
    """Type of children."""

    NOCHILD = 0
    NORMAL = 1
    WALDA = 2
    ONE_CHILD = 3
    WEG = 4
    BULL = 5
    QUR = 6


@enum.unique
class CrossCaptOwn(enum.IntEnum):
    """What to do with own seed on cross capture."""

    LEAVE = 0
    PICK_ON_CAPT = 1
    ALWAYS_PICK = 2


@enum.unique
class Direct(enum.IntEnum):
    """Direction of sowing. 2nd Param to move on bi-directional holes."""
    CW = -1
    CCW = 1

    SPLIT = 0
    PLAYALTDIR = 2

    def opp_dir(self):
        """Return the opposite direction of self."""
        if self == self.CW:
            return self.CCW

        if self == self.CCW:
            return self.CW

        raise GameInfoError("Can't take opposite of " + self.name)


@enum.unique
class Goal(enum.IntEnum):
    """Goal of the game."""

    MAX_SEEDS = 0
    DEPRIVE = 1
    TERRITORY = 2
    CLEAR = 3
    RND_WIN_COUNT = 4
    RND_SEED_COUNT = 5
    RND_EXTRA_SEEDS = 6
    RND_POINTS = 7


@enum.unique
class GrandSlam(enum.IntEnum):
    """Possible options for dealing with a grand slam (capturing
    all of an opponents seeds on one move)."""

    LEGAL = 0
    NOT_LEGAL = 1
    NO_CAPT = 2
    OPP_GETS_REMAIN = 3
    LEAVE_LEFT = 4
    LEAVE_RIGHT = 5


@enum.unique
class LapSower(enum.IntEnum):
    """Defines if or what kind of lap sowing to do."""

    OFF = 0
    LAPPER = 1
    LAPPER_NEXT = 2


@enum.unique
class Rounds(enum.IntEnum):
    """Game played in rounds and how it ends."""

    NO_ROUNDS = 0
    HALF_SEEDS = 1
    NO_MOVES = 2   # mustpass determines if only current player or both


@enum.unique
class RoundFill(enum.IntEnum):
    """How rounds are filled when a new round starts."""

    NOT_APPLICABLE = 0
    LEFT_FILL = 1
    RIGHT_FILL = 2
    OUTSIDE_FILL = 3
    EVEN_FILL = 4
    SHORTEN = 5
    UCHOOSE = 6
    UMOVE = 7


@enum.unique
class RoundStarter(enum.IntEnum):
    """Who starts each round."""

    ALTERNATE = 0
    LOSER = 1
    WINNER = 2
    LAST_MOVER = 3


@enum.unique
class SowPrescribed(enum.IntEnum):
    """Define a prescribed opening."""

    NONE = 0
    BASIC_SOWER = 1
    MLAPS_SOWER = 2
    SOW1OPP = 3
    PLUS1MINUS1 = 4
    ARNGE_LIMIT = 5   # arrange seeds or limit children and captures


@enum.unique
class SowRule(enum.IntEnum):
    """Defines special rules for sowing."""

    NONE = 0
    SOW_BLKD_DIV = 1
    SOW_BLKD_DIV_NR = 2
    OWN_SOW_CAPT_ALL = 3
    SOW_SOW_CAPT_ALL = 4
    NO_SOW_OPP_2S = 5
    CHANGE_DIR_LAP = 6


@enum.unique
class StartPattern(enum.IntEnum):
    """Defines the start patterns for the game."""

    ALL_EQUAL = 0
    GAMACHA = 1
    ALTERNATES = 2
    ALTS_WITH_1 = 3
    CLIPPEDTRIPLES = 4
    TWOEMPTY = 5


@enum.unique
class WinCond(enum.Enum):
    """Win conditions.
    Not used in the config files."""

    WIN = enum.auto()
    TIE = enum.auto()

    ROUND_WIN = enum.auto()
    ROUND_TIE = enum.auto()

    ENDLESS = enum.auto()       # return this when multi-lap games get stuck
    REPEAT_TURN = enum.auto()   # must be truthy

    def is_ended(self):
        """Has the game ended."""
        return self is not WinCond.REPEAT_TURN

    def is_win(self):
        """Did the game or round end winner."""
        return self in (WinCond.WIN, WinCond.ROUND_WIN)


@dc.dataclass(frozen=True, kw_only=True)
class GameInfo:
    """Named tuple providing static game information."""

    name: str = 'Mancala'
    help_file: str = ''
    about: str = ''

    # **** game dynamics
    goal: Goal = Goal.MAX_SEEDS
    mustpass: bool = False
    rounds: Rounds = Rounds.NO_ROUNDS
    round_starter: RoundStarter = RoundStarter.ALTERNATE
    round_fill: RoundFill = RoundFill.NOT_APPLICABLE
    no_sides: bool = False
    stores: bool = False
    start_pattern: StartPattern = StartPattern.ALL_EQUAL
    prescribed: SowPrescribed = SowPrescribed.NONE

    # **** allowable moves
    min_move: int = 1
    allow_rule: AllowRule = AllowRule.NONE
    mustshare: bool = False

    # **** sowing
    sow_direct: Direct = Direct.CCW

    sow_start: bool = False
    move_one: bool = False
    skip_start: bool = False
    sow_own_store: bool = False
    blocks: bool = False
    mlaps: LapSower = LapSower.OFF
    visit_opp: bool = False
    child_cvt: int = 0
    child_type: ChildType = ChildType.NOCHILD
    child_rule: ChildRule = ChildRule.NONE
    goal_param: int = 0
    sow_rule: SowRule = SowRule.NONE

    # **** capture
    capsamedir: bool = False

    oppsidecapt: bool = False
    moveunlock: bool = False
    evens: bool = False
    capt_min: int = 0
    capt_max: int = 0
    nosinglecapt: bool = False
    nocaptfirst: bool = False
    capt_next: bool = False
    capttwoout: bool = False

    crosscapt: bool = False
    xc_sown: bool = False
    xcpickown: CrossCaptOwn = CrossCaptOwn.LEAVE
    pickextra: CaptExtraPick = CaptExtraPick.NONE

    multicapt: bool = False
    grandslam: int = GrandSlam.LEGAL
    capt_rturn: bool = False

    # list of seed counts to capture on (after sow)
    capt_on: list[int] = dc.field(default_factory=list)

    # list of bi-directional holes
    udir_holes: list[int] = dc.field(default_factory=list)

    #  derived parameters created from others in post init
    udirect: bool = False
    mlength: int = 0

    # used only for initialization, not added to the dataclass
    nbr_holes: dc.InitVar[int]
    rules: dc.InitVar[dict]


    def __post_init__(self, nbr_holes, rules):
        """Do post init (any derived values) and apply the rules.
        rules which raise exceptions and warnings."""

        if self.sow_direct == Direct.PLAYALTDIR:
            object.__setattr__(self, ckey.UDIR_HOLES, list(range(nbr_holes)))
        object.__setattr__(self, ckey.UDIRECT, bool(self.udir_holes))

        mlength = 1
        if self.no_sides or self.goal == Goal.TERRITORY:
            mlength = 3
        elif self.udirect:
            mlength = 2
        object.__setattr__(self, ckey.MLENGTH, mlength)

        rules.test(self, nbr_holes)


    @classmethod
    def get_fields(cls):
        """Return the field names."""

        return [field.name for field in dc.fields(cls)]


    @classmethod
    def get_default(cls, fname):
        """Lookup the default value for the field."""

        for field in dc.fields(cls):
            if field.name == fname:
                if field.default == dc.MISSING:
                    return field.default_factory()

                return field.default
        return None


@dc.dataclass(kw_only=True)
class HoleProps:
    """Dynamic properties for each hole
    that the mancala class knows about."""

    seeds: int
    unlocked: bool
    blocked: bool
    ch_owner: bool  # child owner; actually one of False, True or None
    owner: bool     # owner: Territory games: {False, True}; Else None


class MoveTpl(tuple):
    """A class to print the move tuples nicely.
    Override new so the contructor can take multiple arguements
    if two args: pos, direct
    if three args: row, pos, direct
        used for any game where a player can move from both rows
        games even if no udirect"""

    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __str__(self):

        if len(self) == 3:
            if self[2]:
                return f'({self[0]}, {self[1]}, {self[2].name})'
            return f'({self[0]}, {self[1]}, None)'

        if self[1]:
            return f'({self[0]}, {self[1].name})'
        return f'({self[0]}, None)'


    def set_dir(self, direct):
        """Return a new MoveTpl with a new direction."""

        tmove = list(self)
        tmove[-1] = direct
        return MoveTpl(*tmove)


# %%  game interface abstract base class -- the UI requires these

class GameInterface(abc.ABC):
    """A mixin of interfaces required by the UI for a mancala game.
    The mancala_ui calls these -- the only interface between the game
    logic and the UI."""

    @abc.abstractmethod
    def get_game_info(self):
        """Return: GameInfo -- describe the game"""

    @abc.abstractmethod
    def get_turn(self):
        """Return: True if top player's turn,
        False if bottom player's turn"""

    @abc.abstractmethod
    def get_board(self, loc):
        """Return the seeds at location.
        Interface for button behavior."""

    @abc.abstractmethod
    def set_board(self, loc, seeds):
        """Set the seeds at location..
        Interface for button behavior."""

    @abc.abstractmethod
    def get_store(self, row):
        """Return the number of seeds in the store for side.
        row : 0 for top row, 1 for bottom  (opposite of player)"""

    @abc.abstractmethod
    def set_store(self, row, seeds):
        """Set the store seeds of owner.
        row : 0 for top row, 1 for bottom  (opposite of player)"""

    @abc.abstractmethod
    def set_blocked(self, loc, blocked):
        """Set the blocked status location.
        Interface for button behavior."""

    @abc.abstractmethod
    def get_hole_props(self, row, pos):
        """Used to get the properties of the specified hole,
        used for refresh of UI.
        row: int - 0 top row, 1 bottom row (opposite of player)
        pos:  int -  range 0..nbr_holes//2
        Return: HoleProps"""

    @abc.abstractmethod
    def get_allowable_holes(self):
        """Return: a list of positions that can be played by
        the current player. Each hole is either playable or not,
        it can't be only left or right click playable."""

    @abc.abstractmethod
    def new_game(self, win_cond=None, new_round_ok=False):
        """Reset the game to new state or
        if new_round_ok is set, check to start a new round.
        Return True if a new game is created, False if a new round
        is created."""

    @abc.abstractmethod
    def end_game(self):
        """User requested to end the game or the game ended in an
        ENDLESS looping condition.
        Return: WinCond"""

    @abc.abstractmethod
    def move(self, move):
        """Select seeds from hole (move) and sow per game rules.
        move:  one of:
            int -  range 0..holes (pos)
            pair - pos, direction for user choose holes
            tuple - row, pos, direct for moves from either side
        All steps of a move are performed, including determining
        if the game is over.
        Return: None or WinCond"""

    @abc.abstractmethod
    def test_pass(self):
        """If no valid moves, swap turn and return True.
        Can't put this in game move or it will break the minimaxer.
        Return: True current player must pass"""

    @abc.abstractmethod
    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message string."""

    @abc.abstractmethod
    def rtally_param_func(self):
        """If there is a rount tally return a function
        that returns the true and false tallies for the
        parameter"""

    @abc.abstractmethod
    def params_str(self):
        """Return a string describing the parameters of the game.
        Used in saved game_logs."""
