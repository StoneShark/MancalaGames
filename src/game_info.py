# -*- coding: utf-8 -*-
"""Provide the interface methods required by a mancala
game for the mancala_ui. Constants and paramters used to
control game play are also included.

IntEnums are used for enums that are stored in the
config files

Created on Thu Mar  9 08:38:28 2023
@author: Ann"""


# %% imports

import dataclasses as dc
import enum

import cfg_keys as ckey


# %%  constants

PASS_TOKEN = 0xffff

PLAYER_NAMES = ['South', 'North']

DIFF_LEVELS = 4

NO_CH_OWNER = 3   # children that do not have owner's

T_STORE = -2
F_STORE = -1

# given turn look up the index
STORE_INDEX = [F_STORE, T_STORE]
STORE_NAME = ['F_STORE', 'T_STORE']


# %%  errors

class GameInfoError(Exception):
    """Error in game info construction or use."""

class GameVariantError(Exception):
    """Error in Game Variant configuration."""

class UInputError(Exception):
    """Generally, a user configuration file error.

     A User Input Error e.g., the user provided invalid data of
     some sort possibly in a game config file or mancala.ini.

     Not likely a software error, but it could be."""

class DataError(Exception):
    """An error was found in a table that a user is not expected
    to edit."""


# %%  enums

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
    MOVE_ALL_HOLES_FIRST = 9
    NOT_XFROM_1S = 10
    OCCUPIED = 11
    RIGHT_HALF_FIRSTS = 12
    RIGHT_HALF_1ST_OPE = 13

    def no_moves(self):
        """Return True if the allow rule could prevent all moves
        even when a player has seeds."""

        return self in {AllowRule.SINGLE_TO_ZERO,
                        AllowRule.SINGLE_ALL_TO_ZERO,
                        AllowRule.NOT_XFROM_1S,
                        AllowRule.OCCUPIED}

@enum.unique
class CaptDir(enum.IntEnum):
    """Capture direction in relation to the sow direction."""

    OPP_SOW = 0
    SOW = 1
    BOTH = 2


@enum.unique
class CaptExtraPick(enum.IntEnum):
    """Pick extra's over the captured seeds."""

    NONE = 0
    PICKCROSS = 1
    PICKOPPBASIC = 2
    PICKLASTSEEDS = 3      # must match ROUNDS.END_S_SEEDS (or fix pick_rend_agree)
    PICK2XLASTSEEDS = 4   # must match ROUNDS.END_2S_SEEDS
    PICKFINAL = 5
    PICKCROSSMULT = 6


@enum.unique
class CaptRTurn(enum.IntEnum):
    """Repeat turns allowed."""

    NO_REPEAT = 0
    ALWAYS = 1        # be consistent with True settings
    ONCE = 2


@enum.unique
class CaptSide(enum.IntEnum):
    """The sides that captures may be done on."""

    BOTH = 0
    OPP_SIDE = 1
    OWN_SIDE = 2
    OPP_CONT = 3    # opp side but continue onto own side
    OWN_CONT = 4    # own side but continue onto opp side
    OPP_TERR = 5
    OWN_TERR = 6


@enum.unique
class CaptType(enum.IntEnum):
    """Additional capture mechanisms."""

    NONE = 0
    NEXT = 1
    TWO_OUT = 2
    MATCH_OPP = 3
    SINGLETONS = 4
    CAPT_OPP_1CCW = 5
    PASS_STORE_CAPT = 6
    PULL_ACROSS = 7
    END_OPP_STORE_CAPT = 8
    SANDWICH_CAPT = 9


@enum.unique
class ChildLocs(enum.IntEnum):
    """Defines where children may be made.
    Child Rules are also applied."""

    ANYWHERE = 0
    ENDS_ONLY = 1
    NO_ENDS = 2
    INV_ENDS_PLUS_MID = 3
    ENDS_PLUS_ONE_OPP = 4
    NO_OWN_RIGHT = 5
    NO_OPP_RIGHT = 6
    NO_OPP_LEFT = 7
    NOT_SYM_OPP = 8
    NOT_FACING = 9
    ENDS_PLUS_ALL_OPP = 10
    FIXED_ONE_RIGHT = 11


@enum.unique
class ChildRule(enum.IntEnum):
    """Defines additional child restrictions."""

    NONE = 0
    OPP_SIDE_ONLY = 1
    OWN_SIDE_ONLY = 2
    OPPS_ONLY_NOT_1ST = 3
    OPP_OWNER_ONLY = 4
    OWN_OWNER_ONLY = 5
    NOT_1ST_OPP = 6


@enum.unique
class ChildType(enum.IntEnum):
    """Type of children."""

    NOCHILD = 0
    NORMAL = 1
    # WALDA = 2  not different than NORMAL (now with child_locs)
    ONE_CHILD = 3
    WEG = 4
    BULL = 5
    QUR = 6
    RAM = 7

    def child_but_not_ram(self):
        """Child type is not NOCHILD or RAM."""

        return self and self != self.RAM


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
    EVEN_ODD_DIR = 3
    TOCENTER = 4

    def opp_dir(self):
        """Return the opposite direction of self."""
        if self == self.CW:
            return self.CCW

        if self == self.CCW:
            return self.CW

        raise GameInfoError("Can't take opposite of " + self.name)


@enum.unique
class EndGameCond(enum.IntEnum):
    """Additional conditions that end the game."""

    NO_ADDTL = 0
    CLEARED_OWN = 1
    CLEARED_OPP = 2
    SEEDS_LIMIT = 3           # seeds in play < param
    HOLE_SEED_LIMIT = 4           # all holes < param


@enum.unique
class EndGameSeeds(enum.IntEnum):
    """what to do with unclaimed seeds at the end game."""

    HOLE_OWNER = 0
    DONT_SCORE = 1
    LAST_MOVER = 2
    UNFED_PLAYER = 3
    DIVVIED = 4


@enum.unique
class Goal(enum.IntEnum):
    """Goal of the game."""

    MAX_SEEDS = 0
    DEPRIVE = 1
    TERRITORY = 2
    CLEAR = 3
    RND_WIN_COUNT_MAX = 4
    RND_SEED_COUNT = 5
    RND_EXTRA_SEEDS = 6
    RND_POINTS = 7
    RND_WIN_COUNT_CLR = 8
    RND_WIN_COUNT_DEP = 9
    IMMOBILIZE = 10
    RND_WIN_COUNT_IMB = 11

    def eliminate(self):
        """Return True if goal involves eliminating seeds or moves."""

        return self in {Goal.DEPRIVE,
                        Goal.CLEAR,
                        Goal.IMMOBILIZE,
                        Goal.RND_WIN_COUNT_CLR,
                        Goal.RND_WIN_COUNT_DEP,
                        Goal.RND_WIN_COUNT_IMB}

    def rnd_win_count(self):
        """Return True if goal involves winning a number of
        simple rounds."""

        return self in {Goal.RND_WIN_COUNT_MAX,
                        Goal.RND_WIN_COUNT_CLR,
                        Goal.RND_WIN_COUNT_DEP,
                        Goal.RND_WIN_COUNT_IMB}


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
    LEGAL_SHARE = 6


@enum.unique
class LapSower(enum.IntEnum):
    """Defines if or what kind of lap sowing to do."""

    OFF = 0
    LAPPER = 1
    LAPPER_NEXT = 2


@enum.unique
class PlayLocs(enum.IntEnum):
    """Define what locations are in play."""

    BOARD_ONLY = 0
    BRD_OWN_STR_ALL = 1    # sow all seeds from store
    BRD_OWN_STR_CHS = 2    # choose # seeds to sow from store


@enum.unique
class PreSowCapt(enum.IntEnum):
    """Define a type of presow capture."""

    NONE = 0
    CAPT_ONE = 1
    ALL_SINGLE_XCAPT = 2
    DRAW_1_XCAPT = 3


@enum.unique
class Rounds(enum.IntEnum):
    """Game played in rounds and how it ends."""

    NO_ROUNDS = 0
    HALF_SEEDS = 1
    NO_MOVES = 2   # mustpass determines if only current player or both
    END_S_SEEDS = 3
    END_2S_SEEDS = 4


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
    UCHOWN = 8
    SHORTEN_ALL = 9
    LOSER_ONLY = 10
    TERR_EX_RANDOM = 11
    TERR_EX_LOSER = 12
    TERR_EX_EMPTY = 13


@enum.unique
class RoundStarter(enum.IntEnum):
    """Who starts each round."""

    ALTERNATE = 0
    LOSER = 1
    WINNER = 2
    LAST_MOVER = 3


@enum.unique
class SowLapCont(enum.IntEnum):
    """Defines when to continue lap sowing."""

    NONE = 0   # no additional criteria
    ON_PARAM = 1
    GREQ_PARAM = 2
    OWN_SIDE = 3
    OPP_SIDE = 4
    VISIT_OPP = 5
    STOP_STORE = 6
    NOT_FROM_STORE = 7


@enum.unique
class StartPattern(enum.IntEnum):
    """Defines the start patterns for the game."""

    ALL_EQUAL = 0
    GAMACHA = 1
    ALTERNATES = 2
    ALTS_WITH_1 = 3
    CLIPPEDTRIPLES = 4
    TWOEMPTY = 5
    RANDOM = 6
    ALTS_SPLIT = 7
    RIGHTMOST_PLUS_ONE = 8
    MOVE_RIGHTMOST = 9
    MOVE_RANDOM = 10
    NO_REPEAT_SOW_OWN = 11
    RANDOM_ZEROS = 12
    AZIGO = 13


@enum.unique
class SowPrescribed(enum.IntEnum):
    """Define a prescribed opening."""

    NONE = 0
    BASIC_SOWER = 1
    MLAPS_SOWER = 2
    SOW1OPP = 3
    PLUS1MINUS1 = 4
    ARNGE_LIMIT = 5   # arrange seeds or limit children and captures
    NO_UDIR_FIRSTS = 6


@enum.unique
class SowRule(enum.IntEnum):
    """Defines special rules for sowing."""

    NONE = 0
    SOW_BLKD_DIV = 1
    SOW_BLKD_DIV_NR = 2
    OWN_SOW_CAPT_ALL = 3
    SOW_CAPT_ALL = 4
    NO_SOW_OPP_NS = 5
    CHANGE_DIR_LAP = 6
    MAX_SOW = 7
    LAP_CAPT = 8
    NO_OPP_CHILD = 9
    LAP_CAPT_OPP_GETS = 10
    OPP_CHILD_ONLY1 = 11
    LAP_CAPT_SEEDS = 12
    NO_CHILDREN = 13


@enum.unique
class SowStores(enum.IntEnum):
    """Which stores to sow."""

    NEITHER = 0
    OWN = 1
    BOTH = 2
    OWN_NR = 3               #  no repeat turn
    BOTH_NR = 4
    BOTH_NR_OWN = 5
    BOTH_NR_OPP = 6

    def sow_both(self):
        """Return true if sowing both sides."""

        return self in (self.BOTH,
                        self.BOTH_NR,
                        self.BOTH_NR_OPP,
                        self.BOTH_NR_OWN)

    def repeat_turn(self):
        """Return true if there is a possiblity of repeat turns."""

        return self in (self.OWN,
                        self.BOTH,
                        self.BOTH_NR_OWN,
                        self.BOTH_NR_OPP)


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
        """Has the game ended?"""
        return self is not WinCond.REPEAT_TURN

    def is_win(self):
        """Did the game or round end with win?"""
        return self in (WinCond.WIN, WinCond.ROUND_WIN)

    def is_tie(self):
        """Did the game or round end in a tie?"""
        return self in (WinCond.TIE, WinCond.ROUND_TIE)

    def is_game_over(self):
        """Is the game over (not a round)?"""
        return self in (WinCond.WIN, WinCond.TIE)

    def is_round_over(self):
        """Is the game over (not a round)?"""
        return self in (WinCond.ROUND_WIN, WinCond.ROUND_TIE)


@enum.unique
class XCaptType(enum.IntEnum):
    """The type cross capture to do."""

    NONE = 0
    ONE_ZEROS = 1
    ANY = 2
    ONE_ANY = 3


# %%   dataclasses and classes

@dc.dataclass(frozen=True, kw_only=True)
class GameInfo:
    """Named tuple providing static game information."""

    name: str = 'Mancala'
    help_file: str = ''
    about: str = ''

    # **** game dynamics
    goal: Goal = Goal.MAX_SEEDS
    end_cond: EndGameCond = EndGameCond.NO_ADDTL
    end_param: int = 0
    mustpass: bool = False
    rounds: Rounds = Rounds.NO_ROUNDS
    round_starter: RoundStarter = RoundStarter.ALTERNATE
    round_fill: RoundFill = RoundFill.NOT_APPLICABLE
    no_sides: bool = False
    stores: bool = False
    start_pattern: StartPattern = StartPattern.ALL_EQUAL
    prescribed: SowPrescribed = SowPrescribed.NONE
    unclaimed: EndGameSeeds = EndGameSeeds.HOLE_OWNER
    quitter: EndGameSeeds = EndGameSeeds.DIVVIED

    # **** allowable moves
    play_locs: PlayLocs = PlayLocs.BOARD_ONLY
    min_move: int = 1
    allow_rule: AllowRule = AllowRule.NONE
    mustshare: bool = False

    # **** sowing
    sow_direct: Direct = Direct.CCW

    sow_start: bool = False
    move_one: bool = False
    skip_start: bool = False
    sow_stores: SowStores = SowStores.NEITHER
    blocks: bool = False
    mlaps: LapSower = LapSower.OFF
    mlap_cont: SowLapCont = SowLapCont.NONE
    mlap_param: int = 0
    child_cvt: int = 0
    child_type: ChildType = ChildType.NOCHILD
    child_rule: ChildRule = ChildRule.NONE
    child_locs: ChildLocs = ChildLocs.ANYWHERE
    goal_param: int = 0
    presowcapt: PreSowCapt = PreSowCapt.NONE
    sow_rule: SowRule = SowRule.NONE
    sow_param: int = 0
    # list of bi-directional holes
    udir_holes: list[int] = dc.field(default_factory=list)

    # **** capture
    capt_dir: CaptDir = CaptDir.OPP_SOW
    capt_side: CaptSide = CaptSide.BOTH
    moveunlock: bool = False
    evens: bool = False
    capt_min: int = 0
    capt_max: int = 0
    nosinglecapt: bool = False
    nocaptmoves: int = 0
    capt_type: CaptType = CaptType.NONE

    crosscapt: XCaptType = XCaptType.NONE
    xc_sown: bool = False
    xcpickown: CrossCaptOwn = CrossCaptOwn.LEAVE
    pickextra: CaptExtraPick = CaptExtraPick.NONE

    multicapt: int = 0
    grandslam: GrandSlam = GrandSlam.LEGAL
    capt_rturn: CaptRTurn = CaptRTurn.NO_REPEAT

    # list of seed counts to capture on (after sow)
    capt_on: list[int] = dc.field(default_factory=list)

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

        rules(self, nbr_holes)


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


    @property
    def repeat_turn(self):
        """Return True if the game options allow repeat turns.

        Note that game classes SameSide, Ohojichi and ShareOne
        also use repeat turn, but that can't be tested here."""

        return (self.capt_rturn
                or self.sow_stores.repeat_turn()
                or self.xc_sown
                or self.grandslam == GrandSlam.LEGAL_SHARE)

    @property
    def basic_capt(self):
        """Return True if the game includes a basic capture."""

        return any([self.evens,
                    self.capt_on,
                    self.capt_max,
                    self.capt_min])


    @property
    def any_captures(self):
        """Return True if the game includes any capture mechanism."""

        return any([self.basic_capt,
                    self.crosscapt,
                    self.capt_type,
                    self.child_type == ChildType.WEG])

    @property
    def capt_stores(self):
        """Return True if we infer that store captures might
        happen."""

        return (self.sow_stores
                and self.play_locs
                and any([self.basic_capt and not self.crosscapt,
                         self.capt_type == CaptType.TWO_OUT,
                         self.capt_type == CaptType.NEXT]))


    def total_seeds_ok(self, seed_total, holes):
        """Test the seed_total against the number of holes.

        Territory decos for end_move and new_game rely on the
        total number of seeds being a multiple of the
        number of holes.

        If the start pattern is not ALL_EQUAL, this might not
        be the case.  nbr_start is used to determine the total
        number of seeds for the start pattern, but it is not
        available in the game_info rule tester.
        Thus, this must be tested when Mancala is created."""

        if self.goal == Goal.TERRITORY and seed_total % holes:
            msg = """For Territory games, the total number of seeds
                  must be a multiple of the number of holes."""
            raise GameInfoError(msg)


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
        used for games where a player can choose the sow direction
    if three args: row, pos, direct
        used for any game where a player can move from both rows
        games even if no udirect"""

    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __str__(self):

        if self[0] < 0:
            return f'({STORE_NAME[-self[0] - 1]}, {self[1]})'

        if len(self) == 3:
            if self[2]:
                return f'({self[0]}, {self[1]}, {self[2].name})'
            return f'({self[0]}, {self[1]}, None)'

        if self[1]:
            return f'({self[0]}, {self[1].name})'
        return f'({self[0]}, None)'


    def set_dir(self, direct):
        """Return a new MoveTpl with a new direction."""

        return MoveTpl(*self[:-1], direct)
