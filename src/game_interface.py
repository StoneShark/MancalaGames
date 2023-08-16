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
import warnings

# %%  constants

DIFF_LEVELS = 4
MAX_MIN_MOVES = 5

MAX_MINIMAX_DEPTH = 15

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
class WinCond(enum.Enum):
    """Win conditions."""

    WIN = enum.auto()
    TIE = enum.auto()

    ROUND_WIN = enum.auto()
    ROUND_TIE = enum.auto()

    ENDLESS = enum.auto()    # return this when multi-lap games get stuck
    END_STORE = enum.auto()     # last seed sown was in the store

    def is_ended(self):
        """Has the game ended."""
        return self is not WinCond.END_STORE


@dc.dataclass(frozen=True, kw_only=True)
class GameFlags:
    """Flags to control the game"""

    mustpass: bool = False
    rounds: bool = False
    stores: bool = False

    # **** sowing flags
    sow_direct: Direct = Direct.CCW
    udirect: bool = False

    sow_start: bool = False
    mustshare: bool = False
    skip_start: bool = False
    sow_own_store: bool = False
    blocks: bool = False
    mlaps: bool = False
    visit_opp: bool = False
    child: bool = False
    convert_cnt: int = 0

    # **** capture flags
    capsamedir: bool = False

    oppsidecapt: bool = False
    moveunlock: bool = False
    evens: bool = False

    crosscapt: bool = False
    xcpickown: bool = False

    multicapt: bool = False
    grandslam: int = GrandSlam.LEGAL


    def __post_init__(self):
        """Do consistency check of flags."""

        self._check_sow_params()
        self._check_capture_params()


    def _check_sow_params(self):
        """Check consistency of the sowing parameters."""

        if not isinstance(self.sow_direct, Direct):
            raise GameInfoError(
                'SOW_DIRECT not valid type, expected Direct.')

        if self.sow_own_store and not self.stores:
            raise GameInfoError('SOW_OWN_STORE set without STORES set.')

        if self.skip_start and self.mlaps:
            raise GameInfoError('SKIP_START not compatible with MULTI_LAP.')

        if self.visit_opp and not self.mlaps:
            raise GameInfoError('VISIT_OPP requires MULTI_LAP.')

        if self.sow_direct == Direct.SPLIT and self.mustshare:
            # supporting this would make allowables and get_moves
            # more complicated--the deco chain could be expanded,
            # BUT the UI would be really difficult
            raise NotImplementedError(
                'SPLIT and MUSTSHARE are currently incompatible.')

        if (self.sow_direct == Direct.SPLIT
                and self.grandslam == GrandSlam.NOT_LEGAL):
            raise NotImplementedError(
                'SPLIT and GRANDSLAM of Not Legal is not implemented.')

        if self.sow_start and self.skip_start:
            raise GameInfoError(
                'SOW_START and SKIP_START do not make sense together.')

        if self.rounds and not self.blocks:
            raise GameInfoError(
                'ROUNDS without BLOCKS is not supported.')


    def _check_capture_params(self):
        """Check consistency of capture parameters."""

        if self.capsamedir and not self.multicapt:
            warnings.warn("CAPSAMEDIR without MULTICAPT has no effect.")

        if self.crosscapt and self.evens:
            warnings.warn(
                'CROSSCAPT with EVENS might be confusing '
                '(conditions are ANDed).')

        if self.xcpickown and not self.crosscapt:
            raise GameInfoError(
                "XCPICKOWN without CROSSCAPT doesn't do anything.")


    @classmethod
    def get_fields(cls):
        """return the field names."""

        return [field.name for field in dc.fields(cls)]


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

    def __post_init__(self):
        """check the scorer vals."""

        score_vals = vars(self).values()

        if all(not val for val in score_vals):
            raise GameInfoError(
                'At least one scorer value should be non-zero'
                'to prevent random play.')


@dc.dataclass(frozen=True, kw_only=True)
class GameInfo:
    """Named tuple providing static game information."""

    name: str = 'Mancala'
    nbr_holes: int               # use only to test other params
    difficulty: int = 1
    help_file: str = ''
    about: str = ''
    flags: GameFlags = GameFlags()
    scorer: Scorer = Scorer()
    min_move: int = 1

    # list of seed counts to capture on (after sow)
    capt_on: list[int] = dc.field(default_factory=list)

    # list of bi-directional holes
    udir_holes: list[int] = dc.field(default_factory=list)

    mm_depth: list[int] = (1, 1, 3, 5)

    def __post_init__(self):
        """Set any derived data and
        check the consistency and correctness of the game info."""

        self._check_existances()
        object.__setattr__(self.flags, 'udirect', bool(self.udir_holes))

        cap_flags_set = any([self.flags.evens,
                             self.flags.crosscapt,
                             self.flags.sow_own_store,
                             self.capt_on,
                             self.flags.convert_cnt])   # for deka
        if not cap_flags_set:
            warnings.warn(
                "No capture mechanism provided.")

        if self.flags.evens and self.capt_on:
            warnings.warn('CAPT_ON and EVENS conditions are ANDed.')

        if self.flags.crosscapt and self.capt_on:
            warnings.warn(
                'CROSSCAPT with CAPT_ON conditions are ANDed.')

        if self.min_move == 1 and self.flags.sow_start:
            raise GameInfoError(
                'MIN_MOVE of 1 with SOW_START play is confusing.')

        if self.flags.mlaps and self.capt_on:
            raise GameInfoError('CAPT_ON with MULTI_LAP never captures.')

        if (self.flags.grandslam == GrandSlam.OPP_GETS_REMAIN
                and 1 in self.capt_on):
            warnings.warn(
                'GRANDSLAM OPP TAKES with captures on 1, '
                'can result in unfortunate end games.')

        self._check_minimaxer_score()
        self._check_split_udir()


    def _check_existances(self):
        """Confirm needed data was provided."""

        if not self.nbr_holes or not isinstance(self.nbr_holes, int):
            raise GameInfoError('Holes must > 0.')

        if not self.name:
            raise GameInfoError('Mising Name.')

        if not self.flags or not isinstance(self.flags, GameFlags):
            raise GameInfoError('Missing or bad game flags.')

        if not self.scorer or not isinstance(self.scorer, Scorer):
            raise GameInfoError('Missing or bad scorer.')

        if not self.mm_depth:
            raise GameInfoError('Missing minimaxer depths.')


    def _check_split_udir(self):
        """check consistency of split_sow and udirect holes"""

        ucnt = len(self.udir_holes)
        if ucnt > self.nbr_holes:
            raise GameInfoError('Too many udir_holes specified.')

        if any(udir < 0 or udir >= self.nbr_holes for udir in self.udir_holes):
            raise GameInfoError('Udir_holes value out of range '
                                ' 0..nbr_holes-1.')

        if self.flags.udirect and self.flags.mustshare:
            # see SPLIT / MUSHSHARE above
            raise NotImplementedError(
                'UDIRECT and MUSTSHARE are currently incompatible.')

        if self.flags.udirect and self.flags.grandslam == GrandSlam.NOT_LEGAL:
            # see SPLIT / MUSHSHARE above
            raise NotImplementedError(
                'UDIRECT and GRANDLAM=Not Legal are currently incompatible.')

        quot, rem = divmod(self.nbr_holes, 2)
        if (self.flags.sow_direct == Direct.SPLIT
                and rem
                and quot not in self.udir_holes):

            raise GameInfoError(
                'SPLIT with odd number of holes, '
                'but center hole not listed in udir_holes.')

        if (self.flags.udirect and ucnt != self.nbr_holes
                and self.flags.sow_direct != Direct.SPLIT):
            dname = self.flags.sow_direct.name
            warnings.warn(
                f'Odd choice of {dname} when udir_holes != nbr_holes.')


    def _check_minimaxer_score(self):
        """check difficulty, minimaxer and scorer vals."""

        if self.difficulty not in range(DIFF_LEVELS):
            raise GameInfoError('Difficulty not 0, 1, 2 or 3.')

        if self.min_move not in range(1, MAX_MIN_MOVES + 1):
            raise GameInfoError(
                f'Min_move seems wrong  (1<= convention <={MAX_MIN_MOVES}).')

        if len(self.mm_depth) != DIFF_LEVELS:
            raise GameInfoError(
                'Exactly 4 minimaxer depths are expected (easy..expert).')

        if min(self.mm_depth) <= 0:
            raise GameInfoError('All minimaxer depths must be > 0.')

        if max(self.mm_depth) >= MAX_MINIMAX_DEPTH:
            warnings.warn(
                'Max Minimaxer depth is large, AI moves might be slow.')

        if self.scorer.access_m and self.flags.mlaps:
            raise GameInfoError(
                'Access scorer not supported for multilap games.')

        if self.scorer.child_cnt_m and not self.flags.child:
            raise GameInfoError(
                'Child count scorer not supported without child flag.')


@dc.dataclass(kw_only=True)
class HoleProps:
    """Dynamic properties for each hole
    that the mancala class knows about."""

    seeds: int
    unlocked: bool
    blocked: bool
    ch_owner: bool  # actually one of False, True or None


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
    def new_game(self, new_round_ok=False):
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
    def get_ai_move(self):
        """Return: the move for the AI player"""

    @abc.abstractmethod
    def get_ai_move_desc(self):
        """Return: the description of the AI move selection"""
