# -*- coding: utf-8 -*-
"""Provide the interface methods required by a mancala game
for the mancala_ui. Constants and paramters used to
control game play are also included.

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
class Direct(enum.IntEnum):
    """Direction of sowing. 2nd Param to move on bi-directional holes."""
    CW = -1
    CCW = 1

    SPLIT = 0

    def opp_dir(self):
        """Return the opposite direction of self."""
        if self == self.CW:
            return self.CCW

        if self == self.CCW:
            return self.CW

        raise GameInfoError("Can't take opposite of " + self.name)


@enum.unique
class GrandSlam(enum.IntEnum):
    """Possible options for dealing with a grand slam (capturing
    all of an opponents seeds)."""

    LEGAL = 0
    NOT_LEGAL = 1
    NO_CAPT = 2
    OPP_GETS_REMAIN = 3
    LEAVE_LEFT = 4
    LEAVE_RIGHT = 5


@enum.unique
class RoundStarter(enum.IntEnum):
    """Who starts each round."""

    ALTERNATE = 0
    LOSER = 1
    WINNER = 2


@enum.unique
class CrossCaptOwn(enum.IntEnum):
    """What to do with own seed on cross capture."""

    LEAVE = 0
    PICK_ON_CAPT = 1
    ALWAYS_PICK = 2


@enum.unique
class Goal(enum.IntEnum):
    """Goal of the game."""

    MAX_SEEDS = 0
    DEPRIVE = 1
    TERRITORY = 2


@enum.unique
class WinCond(enum.Enum):
    """Win conditions."""

    WIN = enum.auto()
    TIE = enum.auto()

    ROUND_WIN = enum.auto()
    ROUND_TIE = enum.auto()

    GAME_OVER = enum.auto()     # return this when game ended w/o winner (see NamNam)
    ENDLESS = enum.auto()       # return this when multi-lap games get stuck
    END_STORE = enum.auto()     # last seed sown was in the store

    def is_ended(self):
        """Has the game ended."""
        return self is not WinCond.END_STORE


@dc.dataclass(frozen=True, kw_only=True)
class Scorer:
    """Multipliers for the different scorers, 0 turns it off.
    easy_rand is the +- error introduced on easy difficulty.
    access_m if positive, is only used on Hard or Expert."""

    stores_m: int = 4
    access_m: int = 0
    seeds_m: int = 0
    empties_m: int = 0
    child_cnt_m: int = 0
    evens_m: int = 0
    easy_rand: int = 20
    repeat_turn: int = 0


@dc.dataclass(frozen=True, kw_only=True)
class GameInfo:
    """Named tuple providing static game information."""

    name: str = 'Mancala'
    difficulty: int = 1
    help_file: str = ''
    about: str = ''

    # **** game dynamics
    goal: Goal = Goal.MAX_SEEDS
    mustpass: bool = False
    rounds: bool = False
    round_starter: RoundStarter = RoundStarter.ALTERNATE
    rnd_left_fill: bool = False
    rnd_umove: bool = False
    no_sides: bool = False     # changes how the UI works, but not supported
    stores: bool = False

    # **** sowing
    min_move: int = 1
    sow_direct: Direct = Direct.CCW
    udirect: bool = False

    sow_start: bool = False
    move_one: bool = False
    mustshare: bool = False
    skip_start: bool = False
    sow_own_store: bool = False
    blocks: bool = False
    mlaps: bool = False
    visit_opp: bool = False
    child: bool = False
    convert_cnt: int = 0
    sow_blkd_div: bool = False

    # **** capture
    capsamedir: bool = False

    oppsidecapt: bool = False
    moveunlock: bool = False
    evens: bool = False
    capt_min: int = 0
    capt_max: int = 0
    nosinglecapt: bool = False
    capttwoout: bool = False

    crosscapt: bool = False
    xcpickown: CrossCaptOwn = CrossCaptOwn.LEAVE

    multicapt: bool = False
    grandslam: int = GrandSlam.LEGAL
    waldas: bool = False
    one_child: bool = False

    # list of seed counts to capture on (after sow)
    capt_on: list[int] = dc.field(default_factory=list)

    # list of bi-directional holes
    udir_holes: list[int] = dc.field(default_factory=list)

    # a dictionary of param : list[4]
    # where param is used by the ai_player to select the parameter
    # and list is indexed by difficulty to choose the value
    ai_params: dict = dc.field(default_factory=dict)
    scorer: Scorer = Scorer()

    # used only for initialization, not added to the dataclass
    nbr_holes: dc.InitVar[int]
    rules: dc.InitVar[dict]


    def __post_init__(self, nbr_holes, rules):
        """Do post init (any derived values) and apply the rules.
        rules.test raises exceptions and warnings."""

        object.__setattr__(self, 'udirect', bool(self.udir_holes))
        if ckey.MM_DEPTH not in self.ai_params:
            self.ai_params[ckey.MM_DEPTH] = [1, 1, 3, 5]

        rules.test(nbr_holes, self)

    @classmethod
    def get_fields(cls):
        """return the field names."""

        return [field.name for field in dc.fields(cls)]


@dc.dataclass(kw_only=True)
class HoleProps:
    """Dynamic properties for each hole
    that the mancala class knows about."""

    seeds: int
    unlocked: bool
    blocked: bool
    ch_owner: bool  # child owner; actually one of False, True or None


class MoveTpl(tuple):
    """A class to print the move tuples nicely.
    Override new so the contructor can take multiple arguements
    if two args: pos, direct
    if three args: row, pos, direct
        used for all no_sides games even if no udirect"""

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


# %%  game interface abstract base class -- the UI requires these

class GameInterface(abc.ABC):
    """A mixin of interfaces required by the UI for a mancala game.
    The mancala_ui calls these -- the only interface between the game
    logic and the UI.

    This is interface methods only, NO __init__"""

    @abc.abstractmethod
    def get_game_info(self):
        """Return: GameInfo -- describe the game"""

    @abc.abstractmethod
    def get_store(self, row):
        """row: int - 0 top row, 1 bottom row
        Return: the number of seeds in the store for player"""

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
    def set_blocked(self, loc, blocked):
        """Set the blocked status location..
        Interface for button behavior."""

    @abc.abstractmethod
    def get_hole_props(self, row, pos):
        """Used to the properties of the specified hole, used for refresh.
        row: int - 0 top row, 1 bottom row
        pos:  int -  range 0..nbr_holes//2
        Return: HoleProps"""

    @abc.abstractmethod
    def get_allowable_holes(self):
        """Return: a list of positions that can be played by
        the current player"""

    @abc.abstractmethod
    def set_difficulty(self, diff):
        """Set the difficulty.
        diff:  int 0..3 - 0 easy to 3 expert"""

    @abc.abstractmethod
    def new_game(self, win_cond=None, new_round_ok=False):
        """Reset the game to new state or
        if new_round_ok is set, check to start a new round."""

    @abc.abstractmethod
    def end_game(self):
        """User requested to end the game.
        The difficulty tester uses this interface so support it even if
        there is not a user option to end the game.
        Return: WinCond"""

    @abc.abstractmethod
    def move(self, move):
        """Select seeds from hole (pos) on the current player's
        side of the board and sow per game rules.
        move:  int -  range 0..nbr_holes//2 (pos)  or
              unique object to game
        Return: None or WinCond enum"""

    @abc.abstractmethod
    def test_pass(self):
        """If no valid moves, swap turn and return True.
        Can't put this in game move or it will break the minimaxer.
        Return: Boolean - current player must pass"""

    @abc.abstractmethod
    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message strings."""

    @abc.abstractmethod
    def params_str(self):
        """Return a string describing the parameters of the
        game."""

    @abc.abstractmethod
    def get_ai_move(self):
        """Return: the move for the AI player"""

    @abc.abstractmethod
    def get_ai_move_desc(self):
        """Return: the description of the AI move selection"""
