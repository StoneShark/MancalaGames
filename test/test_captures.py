# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:31:23 2023
@author: Ann"""

import collections
import enum

import pandas as pd
import pytest
pytestmark = pytest.mark.unittest

import utils

from context import animator
from context import capturer
from context import game_constants as gconsts
from context import game_info as gi
from context import make_child
from context import mancala
from context import move_data


# %% constants

TEST_COVERS = ['src\\capturer.py']

T = True
F = False
N = None
R = gi.NO_CH_OWNER


# %% read test cases

CASE = 0    # leave as string
BOARD = 1
CHILD = 5
LOCKS = 9
STORE = 13
INDIV = 15
CAPT_ON = 19   # needed to translate to list
MCAPT = 20
EBOARD = 33
ECHILD = 37
ESTORE = 41
RESULT = 43
END = 44

FALSE_DEFAULTS = (18, 22, 23, 30, 31, 32)

SKEEP = slice(0, END)
SBOARD = slice(BOARD, CHILD)
SCHILD = slice(CHILD, LOCKS)
SLOCKS = slice(LOCKS, STORE)
SSTORE = slice(STORE, INDIV)
SINDIV = slice(INDIV, EBOARD)
SEBOARD = slice(EBOARD, ECHILD)
SECHILD = slice(ECHILD, ESTORE)
SESTORE = slice(ESTORE, RESULT)


CONVERT_DICT = {'N': None,
                'T': True,
                'TRUE': True,
                'True': True,
                'F': False,
                'FALSE': False,
                'False': False,

                'CCW': gi.Direct.CCW,
                'CW': gi.Direct.CW,
                'SPLIT': gi.Direct.SPLIT,

                'PICKCAPT': gi.CrossCaptOwn.PICK_ON_CAPT,
                'ALWAYS': gi.CrossCaptOwn.ALWAYS_PICK,

                'LEGAL': gi.GrandSlam.LEGAL,    # the default
                'NO_CAPT': gi.GrandSlam.NO_CAPT,
                'OPP_GETS': gi.GrandSlam.OPP_GETS_REMAIN,
                'KLEFT': gi.GrandSlam.LEAVE_LEFT,
                'KRIGHT': gi.GrandSlam.LEAVE_RIGHT,
                'LSHARE': gi.GrandSlam.LEGAL_SHARE,

                'NEXT': gi.CaptType.NEXT,
                'TWOOUT': gi.CaptType.TWO_OUT,
                'MOPP': gi.CaptType.MATCH_OPP,
                'SINGLES': gi.CaptType.SINGLETONS,
                'OPP1CCW': gi.CaptType.CAPT_OPP_1CCW,

                'SOW': gi.CaptDir.SOW,
                'BOTH': gi.CaptDir.BOTH,
                }


def bool_none(val):
    """Boolean with default of None"""

    if val in CONVERT_DICT:
        return CONVERT_DICT[val]

    if pd.isna(val):
        return None
    return bool(val)


def bool_true(val):
    """Boolean with default of True"""

    if val in CONVERT_DICT:
        return CONVERT_DICT[val]

    if pd.isna(val):
        return True
    return bool(val)


def bool_false(val):
    """Boolean with default of False"""

    if val in CONVERT_DICT:
        return CONVERT_DICT[val]

    if pd.isna(val):
        return False
    return bool(val)


def int_none(val):
    """interger with default of None"""

    if pd.isna(val):
        return None
    return int(val)


def convert(val, col, line):

    if col == CASE:
        return str(val)

    if (SBOARD.start <= col < SBOARD.stop
            or SEBOARD.start <= col < SEBOARD.stop):
        return int(val)

    if (SCHILD.start <= col < SCHILD.stop
            or SECHILD.start <= col < SECHILD.stop):
        return bool_none(val)

    if SLOCKS.start <= col < SLOCKS.stop:
        return bool_true(val)

    if (SSTORE.start <= col < SSTORE.stop
            or SESTORE.start <= col < SESTORE.stop):
        return int_none(val)

    if col == CAPT_ON:
        capts = []
        if isinstance(val, str):
            for ival in val.split(' '):
                if ival.isdigit():
                    capts += [int(ival)]
                else:
                    raise ValueError(f"Non-integer found for capt {line}.")
        elif (isinstance(val, int)
                  or (isinstance(val, float) and pd.notna(val))):
            capts = [int(val)]
        return capts

    if val in CONVERT_DICT:
        return CONVERT_DICT[val]

    if val in FALSE_DEFAULTS:
        return bool_false(val)

    # we should ints or unspecified enums left
    if pd.isna(val):
        return 0

    if isinstance(val, int):
        return val

    if isinstance(val, float):
        return int(val)

    if isinstance(val, str):
        if val.replace('.0', '').isdigit() :
            return int(val.replace('.0', ''))

        if val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
            return int(val)

    raise ValueError(f"Unknown value type at line/col {line}/{col}: {val}")



def read_test_cases():

    global FIELD_NAMES, CASES

    cases_df = pd.read_excel('test/capture_test_data.xlsx', header=None)

    CASES = []
    for idx, row in cases_df.iterrows():

        if idx in [0, 1, 3]:
            continue

        elif idx == 2:
            FIELD_NAMES = [fname for fname in row if pd.notna(fname)]
            Case = collections.namedtuple('Case', FIELD_NAMES)

        elif not idx % 2:
            line_one = [convert(val, col, idx)
                        for col, val in enumerate(row[SKEEP])]

        else:
            line_two = [convert(val, col, idx)
                        for col, val in enumerate(row[SKEEP])]

            board = utils.build_board(line_one[SBOARD], line_two[SBOARD])
            child = utils.build_board(line_one[SCHILD], line_two[SCHILD])
            locks = utils.build_board(line_one[SLOCKS], line_two[SLOCKS])
            store = line_one[SSTORE]

            eboard = utils.build_board(line_one[SEBOARD], line_two[SEBOARD])
            echild = utils.build_board(line_one[SECHILD], line_two[SECHILD])
            estore = line_one[SESTORE]

            CASES += [Case(line_one[CASE], board, child, locks, store,
                           *(line_one[SINDIV]),
                           eboard, echild, estore, line_one[RESULT])]


read_test_cases()


# %%  test capture via table

@pytest.mark.filterwarnings("ignore")
def test_no_capturer():
    game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
    game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game = mancala.Mancala(game_consts, game_info)
    mdata = move_data.MoveData(game, None)
    mdata.direct = gi.Direct.CCW
    mdata.capt_start = 5
    game.deco.capturer.do_captures(mdata)
    assert not mdata.captured
    assert game.board == [3] * 8
    assert game.store == [0, 0]


class TestNoCaptures:

    def test_no_capture(self):
        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(nocaptmoves=1,
                                stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = 3
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = True
        assert game.movers == 0
        game.inhibitor.clear_if(game, mdata)
        assert game.inhibitor.stop_me_capt(game.turn)

        game.deco.capturer.do_captures(mdata)
        assert not mdata.captured

        game.movers = 1
        game.inhibitor.clear_if(game, mdata)
        assert not game.inhibitor.stop_me_capt(game.turn)

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured


class TestCaptTable:

    @staticmethod
    def make_game(case, *, split=False, mlaps=gi.LapSower.OFF):
        """nosingleseed capt is always true, the first time
        throught the table (test_capturer) it will never
        activate because mdata.seeds is set to 3.
        If is actually tested with test_no_singles."""

        child_type = gi.ChildType.NORMAL \
            if case.child_cvt else gi.ChildType.NOCHILD
        child_rule = gi.ChildRule.OPPS_ONLY_NOT_1ST \
            if case.oppside else gi.ChildRule.NONE
        sow_direct = gi.Direct.SPLIT if split else case.direct

        pickextra = gi.CaptExtraPick.NONE
        if case.capt_type == gi.CaptType.CAPT_OPP_1CCW:
            pickextra = gi.CaptExtraPick.PICKOPPBASIC

        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(mlaps=mlaps,
                                stores=True,
                                sow_direct=sow_direct,
                                capt_on=case.capt_on,
                                capt_dir=case.capt_dir,
                                child_cvt=case.child_cvt,
                                child_type=child_type,
                                crosscapt=case.xcapt,
                                capt_min=case.capt_min,
                                evens=case.evens,
                                capt_type=case.capt_type,
                                grandslam=case.gslam,
                                moveunlock=case.moveunlock,
                                multicapt=case.multicapt,
                                nosinglecapt=True,
                                capt_side=case.oppside,
                                pickextra=pickextra,
                                child_rule=child_rule,
                                skip_start=case.skip_start,
                                xcpickown=case.xcapt_pick_own,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        game.turn = case.turn
        game.board = case.board.copy()
        game.child = case.children.copy()
        game.unlocked = case.unlocked.copy()
        game.store = case.store.copy()

        return game



    @pytest.fixture(params=CASES,
                    ids=['case_' + case.case for case in CASES])
    def case(self, request):
        return request.param


    # @pytest.mark.usefixtures("logger")
    def test_capturer(self, case):

        game = self.make_game(case, split=False)
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
            f"Game setup error: board={sum(game.board)} stores={sum(game.store)}"

        mdata = move_data.MoveData(game, None)
        mdata.direct = case.direct
        mdata.capt_start = case.loc
        mdata.board = tuple(case.board)  # not quite right, but ok
        mdata.seeds = 3
        print(game.deco.capturer)
        print(game)

        game.deco.capturer.do_captures(mdata)
        print(game)
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds

        # TODO rework the test cases to test these individually
        assert (mdata.captured | mdata.capt_changed) == case.erval
        assert game.board == case.eboard
        assert game.store == case.estore
        assert game.child == case.echild


    def test_no_singles(self, case):

        game = self.make_game(case, split=True)

        mdata = move_data.MoveData(game, None)
        mdata.direct = case.direct
        mdata.capt_start = case.loc
        mdata.board = tuple(case.board)
        mdata.seeds = 1

        game.deco.capturer.do_captures(mdata)
        assert not mdata.captured
        assert game.board == case.board
        assert game.store == case.store
        assert game.child == case.children

    MLAP_CASES = [case for case in CASES
                  if (case.capt_type == gi.CaptType.NEXT
                      and case.capt_dir != gi.CaptDir.BOTH)]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('case', MLAP_CASES,
                             ids=['case_' + case.case for case in MLAP_CASES])
    def test_mlap_capt_next(self, case):

        game = self.make_game(case, mlaps=gi.LapSower.LAPPER)

        mdata = move_data.MoveData(game, None)
        mdata.direct = case.direct
        mdata.capt_start = case.loc
        mdata.board = tuple(case.board)  # not quite right, but ok
        mdata.seeds = 3
        # print('params', game.params_str(), sep='\n')
        print('capturer', game.deco.capturer, sep='\n')
        # print('capt_basic', game.deco.capt_basic, sep='\n')
        print(game)

        game.deco.capturer.do_captures(mdata)
        print(game)
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds

        assert (mdata.captured | mdata.capt_changed) == case.erval
        assert game.board == case.eboard
        assert game.store == case.estore
        assert game.child == case.echild


@pytest.mark.parametrize('gstype',
                         [gi.GrandSlam.LEGAL,
                          gi.GrandSlam.NO_CAPT,
                          gi.GrandSlam.OPP_GETS_REMAIN,
                          gi.GrandSlam.LEAVE_LEFT,
                          gi.GrandSlam.LEAVE_RIGHT,
                          gi.GrandSlam.LEGAL_SHARE])
def test_no_gs(gstype):
    """Exercise the else to is_grandslam for gs done by capturer."""

    game_consts = gconsts.GameConsts(nbr_start=3, holes=2)
    game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                            stores=True,
                            capt_on=[1],
                            multicapt=-1,
                            grandslam=gstype,
                            rules=mancala.Mancala.rules)
    game = mancala.Mancala(game_consts, game_info)
    game.store = [3, 4]
    game.turn = False

    mdata = move_data.MoveData(game, None)
    mdata.direct = gi.Direct.CCW
    mdata.capt_start = 3
    mdata.board = (3, 2, 0, 0)
    mdata.seeds = 2

    game.board = [3, 0, 1, 1]
    game.deco.capturer.do_captures(mdata)
    assert mdata.captured
    assert game.board == [3, 0, 0, 0]
    assert game.store == [5, 4]



def test_gs_lshare():
    """Confirm repeat turn is set on legal share grand slam."""

    game_consts = gconsts.GameConsts(nbr_start=3, holes=2)
    game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                            stores=True,
                            evens=True,
                            multicapt=-1,
                            grandslam=gi.GrandSlam.LEGAL_SHARE,
                            rules=mancala.Mancala.rules)
    game = mancala.Mancala(game_consts, game_info)

    game.board = [2, 4, 1, 0]
    game.store = [2, 3]
    game.turn = False

    game.move(0)

    assert game.mdata.captured is gi.WinCond.REPEAT_TURN
    assert game.turn is False
    assert game.board == [0, 5, 0, 0]
    assert game.store == [4, 3]


# %% children

class TestWalda:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=5)
        game_info = gi.GameInfo(child_cvt=4,
                                child_type=gi.ChildType.NORMAL,
                                child_locs=gi.ChildLocs.ENDS_PLUS_ONE_OPP,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    WALDA_CASES = [(0, False, True),
                   (1, False, False),
                   (2, False, False),
                   (3, False, False),
                   (4, False, True),
                   (5, False, True),
                   (6, False, True),
                   (7, False, False),
                   (8, False, True),
                   (9, False, True),
                   (0, True, True),
                   (1, True, True),
                   (2, True, False),
                   (3, True, True),
                   (4, True, True),
                   (5, True, True),
                   (6, True, False),
                   (7, True, False),
                   (8, True, False),
                   (9, True, True),
                   ]

    @pytest.mark.parametrize('loc, turn, ewalda', WALDA_CASES)
    def test_walda_creation(self, game, turn, loc, ewalda):
        """Test making of walda by both players in every hole."""

        game.board = [4] * game.cts.dbl_holes
        game.turn = turn

        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert mdata.capt_changed == ewalda

        assert game.board[loc] == 4
        assert game.child[loc] == (turn if ewalda else None)


    @pytest.mark.parametrize('loc, turn, ewalda', WALDA_CASES)
    def test_no_waldas(self, game, turn, loc, ewalda):
        """no waldas, no creations or captures."""

        game.board = [3] * game.cts.dbl_holes
        game.turn = turn

        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert not mdata.captured
        assert game.board[loc] == 3
        assert game.child[loc] == None


    @pytest.mark.parametrize('turn', (False, True))
    def test_waldas_capts(self, game, turn):
        """Each has a walda (leftmost hole),
        capt on 4 from middle hole"""

        game.turn = turn
        game.board = [4] * game.cts.dbl_holes
        wloc = turn * game.cts.holes
        game.child[wloc] = turn

        loc = game.cts.xlate_pos_loc(not turn, 2)
        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured
        assert game.board[loc] == 0
        assert game.board[wloc] == 8
        assert game.child[loc] == None


    @pytest.mark.parametrize('turn', (False, True))
    def test_waldas_no_capts(self, game, turn):
        """each has a walda (leftmost hole),
        capt on 4 from middle hole"""

        game.turn = turn
        game.board = [3] * game.cts.dbl_holes
        wloc = turn * game.cts.holes
        game.child[wloc] = turn

        loc = game.cts.xlate_pos_loc(not turn, 2)
        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert not mdata.captured
        assert game.board[loc] == 3
        assert game.board[wloc] == 3
        assert game.child[loc] == None


class TestTuzdek:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=3,
                                child_type=gi.ChildType.ONE_CHILD,
                                child_rule=gi.ChildRule.OPP_SIDE_ONLY,
                                child_locs=gi.ChildLocs.NOT_SYM_OPP,
                                sow_direct=gi.Direct.CW,
                                stores=True,
                                capt_on=[3],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('loc, turn, eowner',
                             [(0, False, None),
                              (3, False, None),
                              (4, False, False),
                              (7, False, None),
                              (0, True, True),
                              (3, True, None),
                              (4, True, None),
                              (7, True, None),
                              ])
    def test_tuzdek_creation(self, game, turn, loc, eowner):

        game.turn = turn

        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        if eowner is None:
            assert mdata.captured
        else:
            assert not mdata.captured
            assert mdata.capt_changed

        assert game.board[loc] == 0 if eowner is None else 3
        assert game.child[loc] == eowner


    @pytest.mark.parametrize('loc, turn',
                             [(7, False),
                              (3, True),
                              ])
    def test_only_one(self, game, turn, loc):

        game.turn = turn
        game.child = utils.build_board([None, None, False, None],
                                       [None, True, None, None])
        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured

        assert game.board[loc] == 0
        assert not game.child[loc]


    @pytest.mark.parametrize('loc, turn, child',
                             [(6, False, 2),
                              (5, True, 1),
                              ])
    def test_not_opp(self, game, turn, loc, child):

        game.turn = turn
        game.child[child] = True

        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured

        assert game.board[loc] == 0


class TestWeg:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(stores=True,
                                goal=gi.Goal.TERRITORY,
                                goal_param=8,
                                child_cvt=3,
                                child_type=gi.ChildType.WEG,
                                child_rule=gi.ChildRule.OPP_OWNER_ONLY,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([2, 3, 2, 1],
                                       [2, 3, 2, 1])
        game.store = [3, 5]
        game.owner = utils.build_board([F, F, T, T],
                                       [T, T, F, F])
        game.child = utils.build_board([N, N, F, F],
                                       [N, N, T, T])
        return game

    # putting this here keeps it out of the error trace
    WEG_CASES = [(0, T, F, 0),
                 (1, T, F, 0),
                 (2, T, F, 0),
                 (3, T, F, 0),
                 (4, T, F, 1),
                 (5, T, F, 2),
                 (6, T, T, 0),
                 (7, T, F, 0),
                 (0, F, F, 0),
                 (1, F, T, 0),
                 (2, F, F, 2),
                 (3, F, F, 1),
                 (4, F, F, 0),
                 (5, F, F, 0),
                 (6, F, F, 0),
                 (7, F, F, 0),
                ]

    @pytest.mark.parametrize('loc, turn, eweg, ecapt', WEG_CASES)
    def test_wegs(self, game, loc, turn, eweg, ecapt):
        """Test eweg making and captures:
        eweg - should weg/child have been created
        ecapt - how many seeds should have been captured"""

        game.turn = turn
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        start_seeds = game.board[loc]
        start_store = game.store[turn]

        game.deco.capturer.do_captures(mdata)

        if eweg:
            assert mdata.capt_changed
            assert not mdata.captured
            assert game.child[loc] == turn
            assert tuple(game.board) == mdata.board

        elif ecapt:
            assert not mdata.capt_changed
            assert mdata.captured

            assert game.board[loc] == start_seeds - ecapt
            assert game.store[turn] == start_store + ecapt

        else:
            assert not mdata.capt_changed
            assert not mdata.captured
            assert tuple(game.board) == mdata.board


class TestBull:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=4,
                                child_type=gi.ChildType.BULL,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 0, 4, 0],
                                       [3, 4, 3, 0])
        game.store = [7, 7]
        return game

    BULL_CASES = [(0, (0, 7)),
                  (1, (0, 1)),
                  (2, (1, 2)),
                  (3, None),
                  (4, None),
                  (5, [5]),
                  (6, None),
                  (7, [7]),
                ]

    @pytest.mark.parametrize('turn', (False, True))
    @pytest.mark.parametrize('loc, ebulls', BULL_CASES)
    def test_bull(self, game, turn, loc, ebulls):
        """Test basic bull making in the absence of
        existing bulls."""

        game.turn = turn
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)

        assert not mdata.captured
        assert tuple(game.board) == mdata.board

        if ebulls:
            assert mdata.capt_changed
            for idx in range(game.cts.holes):
                if idx in ebulls:
                    assert game.child[idx] == turn
                else:
                    assert game.child[idx] == None

        else:
            assert not mdata.capt_changed
            assert all(game.child[idx] == None
                           for idx in range(game.cts.holes))


    WBULL_CASES = [(0, None),
                   (1, [1]),
                   (2, (1, 2)),
                   (3, None),
                   (4, None),
                   (5, [5]),
                   (6, None),
                   (7, None),
                  ]
    @pytest.mark.parametrize('loc, ebulls', WBULL_CASES)
    def test_with_bulls(self, game, loc, ebulls):
        """Test same basic cases but set holes 0 and 7
        to already be bulls."""

        game.turn = True
        game.child[0] = False
        game.child[7] = True

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)

        assert not mdata.captured
        assert tuple(game.board) == mdata.board

        if ebulls:
            assert mdata.capt_changed
            for idx in ebulls:
                assert game.child[idx] == True

        else:
            assert not mdata.capt_changed
            assert all(game.child[idx] == None for idx in range(1, 7))


class TestQur:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(stores=True,
                                child_cvt=3,
                                child_type=gi.ChildType.QUR,
                                crosscapt=True,
                                xcpickown=1,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([2, 3, 1, 1],
                                       [1, 1, 3, 2])
        game.store = [1, 1]
        return game

    QCASES = [
        (False, 0, [], False, [4, 1]),  # don't make, opp side wrong, but capt
        (False, 3, [], False, None),  # don't make, not single seed
        (False, 1, [], True, None),   # make
        (False, 1, [1], False, None),  # don't make or capt, already child

        (True, 0, [], False, None),  # don't make, not single seed
        (True, 2, [], True, None),   # make
        (True, 2, [2], False, None),  # don't make or capt, already child
        (True, 3, [], False, [1, 4]),  # don't make, opp side wrong, but capt

              ]
    @pytest.mark.parametrize('turn, pos, child_cols, emake, estore',
                             QCASES,
                             ids=[f'case_{f}' for f in range(len(QCASES))])
    def test_makin_qur(self, game, turn, pos, child_cols, emake, estore):

        game.turn = turn
        for col in child_cols:
            cross = game.cts.cross_from_loc(col) # pos == loc for False
            game.child[col] = True
            game.child[cross] = True

        saved_child = tuple(game.child)
        saved_store = tuple(game.store)

        loc = game.cts.xlate_pos_loc(not turn, pos)
        cross = game.cts.cross_from_loc(loc)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)

        if emake:
            assert game.child[loc] == turn and game.child[cross] == turn
        else:
            assert tuple(game.child) == saved_child

        if estore:
            assert game.store == estore
            assert game.board[loc] == 0 and game.board[cross] == 0
        else:
            assert tuple(game.store) == saved_store
            assert tuple(game.board) == mdata.board


class TestRam:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(stores=True,
                                child_type=gi.ChildType.RAM,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        return game

    CASES = [([1, 2, 4, 5, 8, 7, 6, 5],
              [N, R, R, N, N, R, N, N],
              [1, 2, 0, 5, 8, 7, 6, 5],
              [N, N, N, R, R, R, R, R]),
             ]

    @pytest.mark.parametrize('board, rams, eboard, erams',
                             CASES)
    def test_ram(self, game, board, rams, eboard, erams):

        game.board = board
        game.child = rams

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = 2
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)

        assert game.board == eboard
        assert game.child == erams


class TestCaptureToChild:
    """Test CaptureToChild with all child types and with a picker"""

    CASES = [[case[0], ctype] + case[1:]
             for ctype in [gi.ChildType.NORMAL,
                           gi.ChildType.ONE_CHILD,
                           gi.ChildType.WEG,
                           gi.ChildType.BULL]
             for case in
                [['capt_wo_child',
                  (3, 0, 4, 4, 4, 3), (N, N, N, N, N, N), (0, 0),
                  (3, 0, 4, 4, 4, 3), (N, N, N, N, N, N)],

                ['make_child',
                 (3, 3, 1, 4, 3, 3), (N, N, N, N, N, N), (1, 0),
                 (3, 3, 1, 4, 3, 3), (N, N, N, N, F, N)],

                # capture with child; stores zeros (2 children)
                ['capt_w_child_0s',
                 (3, 0, 4, 4, 4, 3), (N, N, N, F, N, F), (0, 0),
                 (3, 0, 4, 8, 0, 3), (N, N, N, F, N, F)],

                # capture with child; stores not zeros
                ['capt_w_child',
                 (0, 0, 4, 3, 4, 3), (N, N, N, N, N, F), (1, 3),
                 (0, 0, 4, 3, 0, 7), (N, N, N, N, N, F)],
                ]
            ]

    CASES += [['q_capt_wo_child', gi.ChildType.QUR,
                  (3, 0, 4, 4, 4, 3), (N, N, N, N, N, N), (0, 0),
                  (3, 0, 4, 4, 4, 3), (N, N, N, N, N, N)],

                ['q_make_child', gi.ChildType.QUR,
                 (3, 3, 3, 4, 1, 3), (N, N, N, N, N, N), (1, 0),    # diff case
                 (3, 3, 3, 4, 1, 3), (N, F, N, N, F, N)],

                # capture with child; stores zeros (2 children)
                ['q_capt_w_child_0s', gi.ChildType.QUR,
                 (3, 0, 4, 4, 4, 3), (N, N, N, F, N, F), (0, 0),
                 (3, 0, 4, 8, 0, 3), (N, N, N, F, N, F)],

                # capture with child; stores not zeros
                ['q_capt_w_child', gi.ChildType.QUR,
                 (0, 0, 4, 3, 4, 3), (N, N, N, N, N, F), (1, 3),
                 (0, 0, 4, 3, 0, 7), (N, N, N, N, N, F)],
            ]

    # some cases with picks
    CASES += [# capture with child; stores not zeros
                ['capt_pick_w_child', gi.ChildType.WEG,
                 (0, 2, 4, 2, 4, 3), (N, N, N, N, N, F), (1, 2),
                 (0, 2, 4, 0, 0, 9), (N, N, N, N, N, F)],

                # capture with child
                ['q_capt_pick_w_child_0s', gi.ChildType.QUR,
                 (0, 0, 2,  4, 4, 2), (N, N, N, F, N, N), (2, 4),
                 (0, 0, 2, 10, 0, 0), (N, N, N, F, N, N)],
                ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('ctype, board, child, store, eboard, echild',
                             [case[1:] for case in CASES],
                             ids=[f'{case[1].name}-{case[0]}' for case in CASES])
    def test_child_type(self, ctype, board, child, store, eboard, echild):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(evens=True,
                                child_type=ctype,
                                child_cvt=3,
                                pickextra=gi.CaptExtraPick.PICKOPPBASIC,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert 'CaptureToChild' in str(game.deco.capturer)

        game.turn = False
        game.board = list(board)
        game.store = list(store)
        game.child = list(child)
        # print(game)

        loc = 4
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = game.board[loc]

        game.deco.capturer.do_captures(mdata)
        # print(game)

        assert game.store == list(store)
        assert game.board == list(eboard)
        assert game.child == list(echild)


# %% capt wrappers and non-capt table tests

class TestRepeatTurn:
    """Test repeat turn due to capt_rturn."""

    @pytest.fixture
    def gamea(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_rturn=gi.CaptRTurn.ALWAYS,
                                stores=True,
                                capt_on=[3],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_repeat_turn_always(self, gamea):

        gamea.turn = True
        gamea.board = utils.build_board([2, 2, 3, 3],
                                        [2, 1, 0, 3])

        for cloc in range(3, 6):
            mdata = move_data.MoveData(gamea, None)
            mdata.direct = gi.Direct.CCW
            mdata.capt_start = cloc
            gamea.deco.capturer.do_captures(mdata)
            gamea.rturn_cnt += 1  # this is done at the end of move
            assert mdata.captured == gi.WinCond.REPEAT_TURN

        mdata = move_data.MoveData(gamea, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = 1
        gamea.deco.capturer.do_captures(mdata)
        assert mdata.captured != gi.WinCond.REPEAT_TURN


    @pytest.fixture
    def game1(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_rturn=gi.CaptRTurn.ONCE,
                                stores=True,
                                capt_on=[3],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_repeat_turn_once(self, game1):

        game1.turn = True
        game1.board = utils.build_board([2, 2, 3, 3],
                                        [2, 1, 0, 3])

        for cloc, repeat in [(3, True), (4, False), (5, False)]:
            mdata = move_data.MoveData(game1, None)
            mdata.direct = gi.Direct.CCW
            mdata.capt_start = cloc
            game1.deco.capturer.do_captures(mdata)
            game1.rturn_cnt += 1  # this is done at the end of move
            if repeat:
                assert mdata.captured == gi.WinCond.REPEAT_TURN
            else:
                assert mdata.captured != gi.WinCond.REPEAT_TURN


    def test_rturn_once_move(self, game1):
        """Test with full move."""

        game1.turn = True
        game1.board = utils.build_board([2, 2, 3, 3],
                                        [2, 2, 3, 5])
        game1.store = [2, 0]

        for move, repeat in [(3, True), (2, False)]:

            game1.move(move)

            if repeat:
                assert game1.mdata.captured == gi.WinCond.REPEAT_TURN
                assert game1.turn
            else:
                assert game1.mdata.captured != gi.WinCond.REPEAT_TURN
                assert game1.mdata.captured
                assert not game1.turn


class TestCaptCrossVisited:
    """Only testing the result of do_captures because,
    CaptCrossVisited doesn't actually do the capturing.

    Also, tests that CaptMultiple properly wraps
    CaptCrossVisited (REPEAT_TURN returned)."""

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(crosscapt=True,
                                xc_sown=True,
                                stores=True,
                                multicapt=-1,
                                capt_dir=gi.CaptDir.SOW,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    CASES = [([4, 4, 4, 4, 4, 4], [5, 4, 0, 5, 5, 5], 0, False),  # cycle board, not end in one
             ([4, 4, 4, 4, 4, 4], [4, 0, 5, 5, 5, 5], 5, False),  # end on opp side

             ([1, 6, 6, 6, 5, 0], [2, 1, 7, 7, 6, 1], 1, True),  # cross capt
             ([2, 3, 0, 1, 3, 1], [1, 4, 1, 1, 0, 1], 2, True),  # opp sow not cross hole, capt

             ([2, 3, 0, 1, 5, 1], [0, 4, 1, 1, 5, 1], 2, gi.WinCond.REPEAT_TURN),
             ([1, 6, 3, 2, 0, 2], [0, 7, 3, 2, 0, 2], 1, False)  # end on own sidee, but no repeat turn
             ]

    @pytest.mark.parametrize('before_sow, after_sow, capt_loc, eresult',
                             CASES)
    def test_xc_visited(self, game, before_sow, after_sow, capt_loc, eresult):

        mdata = move_data.MoveData(game, None)
        mdata.board = tuple(before_sow)
        mdata.capt_start = capt_loc
        mdata.direct = game.info.sow_direct
        game.board = after_sow
        game.turn = False

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured == eresult


class TestCaptTwoOut:

    test_cases = [

        ([3, 3, 3, 4, 0, 2], False, 3, [0, 3, 3, 4, 0, 0],
         {'capt_dir': gi.CaptDir.SOW,
          'capt_type': gi.CaptType.TWO_OUT}),

        ([3, 3, 3, 4, 0, 2], False, 3, [0, 3, 3, 4, 0, 0],
         {'capt_dir': gi.CaptDir.SOW,
          'capt_type': gi.CaptType.TWO_OUT,
          'multicapt': -1}),

        ([0, 3, 0, 4, 0, 2], False, 3, [0] * 6,
         {'capt_dir': gi.CaptDir.SOW,
          'capt_type': gi.CaptType.TWO_OUT,
          'multicapt': -1}),

        ]

    @pytest.mark.parametrize('board, turn, loc, eboard, options',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_capts(self, board, turn, loc, eboard, options):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=gi.CaptExtraPick.PICKCROSS,
                                mlaps=True,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        # print(game.deco.capturer)
        # print(game)
        game.deco.capturer.do_captures(mdata)
        # print(game)

        assert mdata.captured
        assert game.board == eboard


# %% pickers

class TestPickCross:

    # actual captures are all on True side, picks on false side
    test_cases = [
        ([3, 3, 3, 2, 2, 2], True, 4, [3, 0, 3, 2, 0, 2], {'evens': True}),

        ([3, 3, 3, 2, 2, 2], True, 4, [3, 0, 3, 0, 0, 2], {'evens': True,
                                                           'multicapt': -1}),

        pytest.param(
            [3, 1, 3, 2, 2, 2], True, 1, [3, 1, 3, 2, 0, 2], {'crosscapt': True},
            marks=pytest.mark.filterwarnings("ignore")),

        ([3, 3, 3, 4, 4, 2], False, 4, [3, 0, 3, 4, 0, 2], {'capt_on': [4]}),
        ([3, 3, 3, 4, 0, 2], False, 3, [0, 3, 3, 4, 0, 0],
         {'capt_dir': gi.CaptDir.SOW,
          'capt_type': gi.CaptType.TWO_OUT}),
        ]

    @pytest.mark.parametrize('board, turn, loc, eboard, options',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_capts(self, board, turn, loc, eboard, options):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=gi.CaptExtraPick.PICKCROSS,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        # print(game)
        game.deco.capturer.do_captures(mdata)
        # print(mdata)
        # print(game)

        assert mdata.captured
        assert game.board == eboard


    @pytest.mark.parametrize('board, turn, loc, eboard, options',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_locks(self, board, turn, loc, eboard, options):
        """capts from true side, pick from false side in data;
        lock false side there should be no picks."""

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=gi.CaptExtraPick.PICKCROSS,
                                moveunlock=True,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        game.unlocked = [False] * 3 + [True] * 3  # false side locked
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        game.deco.capturer.do_captures(mdata)

        assert mdata.captured
        assert game.board[:3] == board[:3]
        assert game.board[3:] == eboard[3:]


    @pytest.mark.parametrize('board, turn, loc, eboard, options',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_child(self, board, turn, loc, eboard, options):
        """capts from true side, pick from false side in data;
        false side are children there should be no picks."""

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=gi.CaptExtraPick.PICKCROSS,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        game.child = [False] * 3 + [None] * 3  # false side children
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        game.deco.capturer.do_captures(mdata)

        assert mdata.captured
        assert game.board[:3] == board[:3]
        assert game.board[3:] == eboard[3:]


    def test_no_capt(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=gi.CaptExtraPick.PICKCROSS,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = [3, 3, 3, 3, 3, 3]
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = 4
        game.deco.capturer.do_captures(mdata)

        assert not mdata.captured
        assert game.board == [3, 3, 3, 3, 3, 3]


class TestPickFinal:

    test_cases = [
        ([2, 0, 1, 2, 2, 1, 2, 1], True, 2, False, [2, 0, 1, 2, 2, 1, 2, 1]),

        # this second test case also tests the capture across the boundary
        # with CaptNext and LAPPER (final seed on opp side, but capture is
        # on own side)
        ([2, 0, 1, 2, 2, 1, 2, 1], True, 3, True,  [2, 0, 1, 0, 0, 1, 2, 1]),

        ]
    @pytest.mark.parametrize('board, turn, caploc, eres, eboard',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_capts(self, board, turn, caploc, eres, eboard):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(stores=True,
                                capt_side=1,
                                capt_on=[2],
                                capt_dir=gi.CaptDir.SOW,
                                mlaps=gi.LapSower.LAPPER,   # loc is tested for capt
                                capt_type=gi.CaptType.NEXT,
                                pickextra=gi.CaptExtraPick.PICKFINAL,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = board.copy()
        game.turn = turn

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = caploc
        game.deco.capturer.do_captures(mdata)
        # print(game)

        assert mdata.captured == eres
        assert game.board == eboard


class TestPickOppBasic:

    test_cases = [
        ([0, 0, 1, 2, 1, 2, 3, 2], False, 2, True,  [0, 0, 1, 2, 1, 0, 3, 0]),
        ([2, 2, 2, 2, 2, 1, 0, 0], True,  5, True,  [0, 0, 0, 0, 2, 1, 0, 0]),
        ([2, 2, 0, 2, 2, 1, 0, 0], True,  5, False, [2, 2, 0, 2, 2, 1, 0, 0]),
        ([3, 1, 2, 1, 2, 1, 0, 0], True,  5, True,  [3, 1, 0, 1, 2, 1, 0, 0]),

        ]
    @pytest.mark.parametrize('board, turn, caploc, eres, eboard',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_capts(self, board, turn, caploc, eres, eboard):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(stores=True,
                                crosscapt=True,
                                capt_on=[2],
                                pickextra=gi.CaptExtraPick.PICKOPPBASIC,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = board.copy()
        game.turn = turn

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = caploc
        game.deco.capturer.do_captures(mdata)

        assert mdata.captured == eres
        assert game.board == eboard


class TestPickLastSeeds:

    test_cases = [
        ([2, 2, 2, 2], [0, 0], [N, N, N, N], True,
         gi.CaptExtraPick.PICKLASTSEEDS,
         False, [2, 2, 2, 2], [0, 0]),
        ([2, 2, 2, 2], [0, 0], [N, N, N, N], True,
         gi.CaptExtraPick.PICKLASTSEEDS,
         False, [2, 2, 2, 2], [0, 0]),

        ([1, 1, 0, 0], [3, 3], [N, N, N, N], True,
         gi.CaptExtraPick.PICKLASTSEEDS,
         True, [0, 0, 0, 0], [3, 5]),
        ([1, 1, 0, 0], [3, 3], [N, N, N, N], False,
         gi.CaptExtraPick.PICKLASTSEEDS,
         True, [0, 0, 0, 0], [5, 3]),

        ([1, 1, 0, 0], [3, 3], [T,F, N, N], False,   # same test but both child
         gi.CaptExtraPick.PICKLASTSEEDS,
         False, [1, 1, 0, 0], [3, 3]),
        ([1, 1, 0, 0], [3, 3], [T, N, N, N], False, # only one child
         gi.CaptExtraPick.PICKLASTSEEDS,
         True, [1, 0, 0, 0], [4, 3]),

        ([2, 1, 0, 0], [2, 3], [N, N, N, N], True,
         gi.CaptExtraPick.PICK2XLASTSEEDS,
         True, [0, 0, 0, 0], [5, 3]),           # seeds got round starter for 2x
        ([2, 1, 0, 0], [2, 3], [N, N, N, N], False,
         gi.CaptExtraPick.PICK2XLASTSEEDS,
         True, [0, 0, 0, 0], [2, 6]),

        ([1, 2, 0, 0], [2, 3], [T,F, N, N], False,   #  both child
         gi.CaptExtraPick.PICK2XLASTSEEDS,
         False, [1, 2, 0, 0], [2, 3]),
        ([1, 2, 0, 0], [2, 3], [T, N, N, N], False, # only one child
         gi.CaptExtraPick.PICK2XLASTSEEDS,
         True, [1, 0, 0, 0], [2, 5]),

        ]
    @pytest.mark.parametrize('board, store, child, turn, picker,'
                             'eres, eboard, estore',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_capts(self, board, store, child, turn, picker,
                   eres, eboard, estore):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=2)
        game_info = gi.GameInfo(stores=True,
                                capt_on=[4],
                                sow_rule=gi.SowRule.OWN_SOW_CAPT_ALL,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                pickextra=picker,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = board
        game.child = child
        game.store = store
        game.turn = turn
        game.starter = not turn

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        game.deco.capturer.do_captures(mdata)

        assert mdata.capt_changed == eres
        assert game.board == eboard
        assert game.store == estore


class TestPickCrossMult:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                multicapt=-1,
                                pickextra=gi.CaptExtraPick.PICKCROSSMULT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    # @pytest.mark.usefixtures("logger")
    def test_pcm(self, game):

        game.board = [0, 2, 1, 1, 3, 3, 1, 4]
        game.store = [7, 10]
        game.turn = True

        assert 'PickCross' in str(game.deco.capturer)
        # print(game)
        game.move(0)

        assert game.mdata.captured == True
        assert game.board == [1, 3, 0, 0, 0, 0, 1, 0]
        assert game.store == [7, 20]



# %% make_child only tests


class TestNoChildren:

    def test_opp_child(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = True
        mdata.capt_start = 1
        mdata.seeds = 1
        assert game.deco.make_child.test(mdata) == False


class TestChildInhibitor:
    """Complicated game to get Inhibitor both."""

    def test_inhibited(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(prescribed=gi.SowPrescribed.ARNGE_LIMIT,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                rounds=gi.Rounds.NO_MOVES,
                                blocks=True,
                                round_fill=gi.RoundFill.SHORTEN,
                                stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = 3
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = True
        game.inhibitor.set_on(game.turn)
        assert game.inhibitor.stop_me_child(game.turn)
        assert not game.deco.make_child.test(mdata)

        game.inhibitor.set_off()
        assert not game.inhibitor.stop_me_child(game.turn)
        assert game.deco.make_child.test(mdata)


class TestOppChild:

    def test_opp_child(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OPP_SIDE_ONLY,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = True
        mdata.capt_start = 3
        assert not game.deco.make_child.test(mdata)

        mdata.capt_start = 2
        assert game.deco.make_child.test(mdata)


class TestNotWithOne:

    @pytest.mark.parametrize('turn, hole, seeds, etest',
                             [(False, 3, 1, False),
                              (False, 3, 2, True),
                              (False, 4, 2, True),
                              (True, 0, 1, False),
                              (True, 0, 2, True),
                              (True, 2, 2, True),])
    def test_opp_child(self, turn, hole, seeds, etest):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OPPS_ONLY_NOT_1ST,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = turn
        mdata.capt_start = hole
        mdata.seeds = seeds
        assert game.deco.make_child.test(mdata) == etest


# %% bad enums

class TestBadEnums:

    def test_bad_cross_capt(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'crosscapt', True)
        object.__setattr__(game_info, 'xcpickown', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_capt_type(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'capt_type', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_grand_slam(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'grandslam', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_child_type(self):

        class BadChild(enum.IntEnum):

            BAD = 25

            def child_but_not_ram(self):
                return False

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'child_type', BadChild.BAD)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_child_type_decos(self):
        """Two decos should raise the error, check both"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        object.__setattr__(game.info, 'child_type', 12)

        with pytest.raises(NotImplementedError):
            make_child.deco_child(game)

        with pytest.raises(NotImplementedError):
            capturer.deco_capturer(game)


    def test_bad_child_rule(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        object.__setattr__(game.info, 'child_type', gi.ChildType.NORMAL)
        object.__setattr__(game.info, 'child_rule', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_pick_extra(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(stores=True,
                                capt_on=[4],
                                sow_rule=gi.SowRule.OWN_SOW_CAPT_ALL,
                                pickextra=gi.CaptExtraPick.PICK2XLASTSEEDS,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        object.__setattr__(game.info, 'pickextra', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


# %% animator

class TestAnimator:

    @pytest.mark.animator
    def test_animator(self, mocker):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                pickextra=gi.CaptExtraPick.PICK2XLASTSEEDS,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mocker.patch('animator.ANIMATOR.change')
        mobj = mocker.patch('animator.one_step')

        game = mancala.Mancala(game_consts, game_info)

        game.starter = False
        game.turn = False
        game.board = [0, 1, 2, 1, 1, 0]
        game.store = [3, 4]

        mdata = move_data.MoveData(game, 0)
        mdata.direct = gi.Direct.CCW
        mdata.seeds = 2
        mdata.capt_start = 2
        game.deco.capturer.do_captures(mdata)

        assert game.board.copy() == [0, 0, 0, 0, 0, 0]
        assert game.store.copy() == [8, 4]

        mobj.assert_called_once()


    @pytest.mark.animator
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('gstype',
                             [gi.GrandSlam.NO_CAPT,
                              gi.GrandSlam.OPP_GETS_REMAIN,
                              gi.GrandSlam.LEAVE_LEFT,
                              gi.GrandSlam.LEAVE_RIGHT,
                              gi.GrandSlam.LEGAL_SHARE])
    def test_grandslam(self, mocker, gstype):

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mocker.patch('animator.one_step')
        mocker.patch('animator.ANIMATOR.change')
        mobj = mocker.patch('animator.ANIMATOR.do_message')

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                stores=True,
                                capt_on=[1, 2],
                                multicapt=-1,
                                grandslam=gstype,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = [3, 2, 3, 0, 0, 1]
        game.store = [3, 6]
        game.turn = False

        # print(game.deco.capturer)

        game.move(2)
        # print(game)
        # print(game.mdata)

        if gstype == gi.GrandSlam.NO_CAPT:
            assert not game.mdata.captured
        else:
            assert game.mdata.captured
        mobj.assert_called_once()


    def test_no_animator(self, mocker):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                pickextra=gi.CaptExtraPick.PICK2XLASTSEEDS,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        assert not animator.ENABLED
        mobj = mocker.patch('animator.one_step')

        game = mancala.Mancala(game_consts, game_info)
        game.starter = False
        game.turn = False
        game.board = [0, 1, 2, 1, 1, 0]
        game.store = [3, 4]

        mdata = move_data.MoveData(game, 0)
        mdata.direct = gi.Direct.CCW
        mdata.seeds = 2
        mdata.capt_start = 2
        game.deco.capturer.do_captures(mdata)

        assert game.board == [0, 0, 0, 0, 0, 0]
        assert game.store == [8, 4]

        assert len(mobj.mock_calls) == 0


# %%

"""
pytest.main(['test_captures.py::TestPickTwo[case_1]'])
"""
