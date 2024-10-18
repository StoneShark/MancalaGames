# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:31:23 2023
@author: Ann"""

import collections

import pandas as pd
import pytest
pytestmark = pytest.mark.unittest

import utils

from context import capturer
from context import game_constants as gc
from context import game_interface as gi
from context import make_child
from context import mancala

from game_interface import CaptExtraPick
from game_interface import ChildType
from game_interface import ChildRule
from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import GrandSlam
from game_interface import WinCond
from mancala import MoveData


# %% constants

TEST_COVERS = ['src\\capturer.py',
               'src\\make_child.py']

T = True
F = False
N = None


# %% read test cases

CASE = 0    # leave as string
BOARD = 1
CHILD = 5
LOCKS = 9
STORE = 13
INDIV = 15
CAPT_ON = 19   # needed to translate str to list
EBOARD = 33
ECHILD = 37
ESTORE = 41
RESULT = 43
END = 44

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
                '': 0,

                'CCW': Direct.CCW,
                'CW': Direct.CW,
                'SPLIT': Direct.SPLIT,

                'PICKCAPT': CrossCaptOwn.PICK_ON_CAPT,
                'ALWAYS': CrossCaptOwn.ALWAYS_PICK,

                'LEGAL': GrandSlam.LEGAL,    # the default
                'NO_CAPT': GrandSlam.NO_CAPT,
                'OPP_GETS': GrandSlam.OPP_GETS_REMAIN,
                'KLEFT': GrandSlam.LEAVE_LEFT,
                'KRIGHT': GrandSlam.LEAVE_RIGHT,

                }

FIELD_NAMES = {}
CASES= []

def convert(val, col, line):

    if col == CASE:
        return val

    if col == CAPT_ON:
        capts = []
        if val:
            for ival in val.split(' '):
                if ival.isdigit():
                    capts += [int(ival)]
                else:
                    raise ValueError(f"Non-integer found for capt {line}.")
        return capts

    if (SCHILD.start <= col < SCHILD.stop
        or SECHILD.start <= col < SECHILD.stop) and not val:
        return None

    if SLOCKS.start <= col < SLOCKS.stop and not val:
        return True

    if val in CONVERT_DICT:
        return CONVERT_DICT[val]

    if val.replace('.0', '').isdigit() :
        return int(val.replace('.0', ''))

    if not val:
        return 0

    raise ValueError(f"Unknown value type at col/line {col}/{line}: {val}")


def read_test_cases():

    global FIELD_NAMES, CASES

    tfile = 'test/capture_test_data.csv'
    tc_dframe = pd.read_excel('test/capture_test_data.xlsx',
                              header=None)
    with open(tfile, 'w', newline='', encoding='utf-8') as file:
        tc_dframe.to_csv(file, header=False, index=False)


    with open(tfile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines[0] = lines[0][1:]

    field_names = lines[2].split(',')
    FIELD_NAMES = [fname for fname in field_names[:-1] if fname]

    Case = collections.namedtuple('Case', FIELD_NAMES)

    CASES = []
    for lcnt in range(4, len(lines), 2):

        line_one = [convert(val, col, lcnt + 1)
                    for col, val in enumerate(lines[lcnt].split(',')[SKEEP])]
        line_two = [convert(val, col, lcnt + 2)
                    for col, val in enumerate(lines[lcnt + 1].split(',')[SKEEP])]

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


# %%  test capturers

@pytest.mark.filterwarnings("ignore")
def test_no_capturer():
    game_consts = gc.GameConsts(nbr_start=3, holes=4)
    game_info = gi.GameInfo(sow_own_store=True,
                            stores=True,
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game = mancala.Mancala(game_consts, game_info)
    mdata = MoveData(game, None)
    mdata.direct = Direct.CCW
    mdata.capt_loc = 5
    game.deco.capturer.do_captures(mdata)
    assert not mdata.captured
    assert game.board == [3] * 8
    assert game.store == [0, 0]



class TestNoCaptures:

    def test_no_capture(self):
        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(nocaptfirst=True,
                                stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = 3
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = True
        assert game.mcount == 0
        game.inhibitor.clear_if(game, mdata)
        assert game.inhibitor.stop_me_capt(game.turn)

        game.deco.capturer.do_captures(mdata)
        assert not mdata.captured

        game.mcount = 2
        game.inhibitor.clear_if(game, mdata)
        assert not game.inhibitor.stop_me_capt(game.turn)

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured


class TestCaptTable:

    @staticmethod
    def make_game(case):

        child_type = ChildType.NORMAL if case.child_cvt else ChildType.NOCHILD
        child_rule = ChildRule.NOT_1ST_OPP if case.oppside else ChildRule.NONE

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=case.capt_on,
                                capsamedir=case.capsamedir,
                                child_cvt=case.child_cvt,
                                child_type=child_type,
                                crosscapt=case.xcapt,
                                capt_min=case.capt_min,
                                evens=case.evens,
                                capt_next=case.capt_next,
                                capttwoout=case.capttwoout,
                                grandslam=case.gslam,
                                moveunlock=case.moveunlock,
                                multicapt=case.multicapt,
                                nosinglecapt=True,
                                oppsidecapt=case.oppside,
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


    def test_capturer(self, case):

        game = self.make_game(case)
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
            f"Game setup error: board={sum(game.board)} stores={sum(game.store)}"

        mdata = MoveData(game, None)
        mdata.direct = case.direct
        mdata.capt_loc = case.loc
        mdata.board = tuple(case.board)  # not quite right, but ok
        mdata.seeds = 3

        game.deco.capturer.do_captures(mdata)
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds

        # TODO rework the test cases to test these individually
        assert (mdata.captured | mdata.capt_changed) == case.erval
        assert game.board == case.eboard
        assert game.store == case.estore
        assert game.child == case.echild


    def test_no_singles(self, case):

        game = self.make_game(case)

        mdata = MoveData(game, None)
        mdata.direct = case.direct
        mdata.capt_loc = case.loc
        mdata.board = tuple(case.board)
        mdata.seeds = 1

        game.deco.capturer.do_captures(mdata)
        assert not mdata.captured
        assert game.board == case.board
        assert game.store == case.store
        assert game.child == case.children



@pytest.mark.parametrize('gstype',
                         [GrandSlam.LEGAL,
                          GrandSlam.NO_CAPT,
                          GrandSlam.OPP_GETS_REMAIN,
                          GrandSlam.LEAVE_LEFT,
                          GrandSlam.LEAVE_RIGHT])
def test_no_gs(gstype):

    game_consts = gc.GameConsts(nbr_start=3, holes=2)
    game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                            capt_on=[1],
                            multicapt=True,
                            grandslam=gstype,
                            rules=mancala.Mancala.rules)
    game = mancala.Mancala(game_consts, game_info)
    game.store = [3, 4]
    game.turn = False

    mdata = MoveData(game, None)
    mdata.direct = Direct.CCW
    mdata.capt_loc = 3
    mdata.board = (3, 2, 0, 0)
    mdata.seeds = 2

    game.board = [3, 0, 1, 1]
    game.deco.capturer.do_captures(mdata)
    assert mdata.captured
    assert game.board == [3, 0, 0, 0]
    assert game.store == [5, 4]


class TestWalda:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=5)
        game_info = gi.GameInfo(child_cvt=4,
                                child_type=ChildType.WALDA,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_small(self, game):
        """Test computation of walda possibilities."""

        consts = gc.GameConsts(3, 4)
        info = game.info
        info.__post_init__(nbr_holes=4,
                           rules=mancala.Mancala.rules)
        game = mancala.Mancala(consts, info)

        assert game.deco.capturer.walda_poses == \
            [capturer.CaptureToWalda.WALDA_BOTH,
             True,
             True,
             capturer.CaptureToWalda.WALDA_BOTH,
             capturer.CaptureToWalda.WALDA_BOTH,
             False,
             False,
             capturer.CaptureToWalda.WALDA_BOTH]


    def test_smaller(self, game):
        """Test computation of walda possibilities."""

        consts = gc.GameConsts(3, 3)
        info = game.info
        info.__post_init__(nbr_holes=3,
                           rules=mancala.Mancala.rules)
        game = mancala.Mancala(consts, info)

        assert game.deco.capturer.walda_poses == \
            [capturer.CaptureToWalda.WALDA_BOTH,
             True,
             capturer.CaptureToWalda.WALDA_BOTH,
             capturer.CaptureToWalda.WALDA_BOTH,
             False,
             capturer.CaptureToWalda.WALDA_BOTH]


    def test_smallest(self, game):
        """Test computation of walda possibilities."""

        consts = gc.GameConsts(3, 2)
        info = game.info
        info.__post_init__(nbr_holes=2,
                           rules=mancala.Mancala.rules)
        game = mancala.Mancala(consts, info)

        walda_poses = game.deco.capturer.walda_poses
        assert all(walda_poses[i] == capturer.CaptureToWalda.WALDA_BOTH
                   for i in range(4))

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

        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
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

        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
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
        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
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
        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
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
        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=3,
                                child_type=ChildType.ONE_CHILD,
                                child_rule=ChildRule.OPP_ONLY,
								stores=True,
                                capt_on=[3],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('loc, turn, eowner',
                             [(0, False, None),
                              (3, False, None),
                              (4, False, None),
                              (7, False, False),
                              (0, True, None),
                              (3, True, True),
                              (4, True, None),
                              (7, True, None),
                              ])
    def test_tuzdek_creation(self, game, turn, loc, eowner):

        game.turn = turn

        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
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
        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured

        assert game.board[loc] == 0
        assert not game.child[loc]


    @pytest.mark.parametrize('loc, turn, child',
                             [(6, False, 1),
                              (2, True, 5),
                              ])
    def test_not_opp(self, game, turn, loc, child):

        game.turn = turn
        game.child[child] = True

        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured

        assert game.board[loc] == 0



class TestWeg:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(stores=True,
                                goal=2,
                                gparam_one=8,
                                child_cvt=3,
                                child_type=ChildType.WEG,
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
        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
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
        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=4,
                                child_type=ChildType.BULL,
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
        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
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

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
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
        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(child_cvt=3,
                                child_type=ChildType.QUR,
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

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
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


class TestRepeatTurn:
    """Test repeat turn due to capt_rturn."""

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_rturn=True,
                                stores=True,
                                capt_on=[3],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_repeat_turn(self, game):

        game.turn = True
        game.board = utils.build_board([2, 2, 3, 0],
                                       [2, 1, 0, 3])
        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = 5
        game.deco.capturer.do_captures(mdata)
        assert mdata.captured == WinCond.REPEAT_TURN

        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = 1
        game.deco.capturer.do_captures(mdata)
        assert mdata.captured != WinCond.REPEAT_TURN


class TestCaptCrossVisited:
    """Only testing the result of do_captures because,
    CaptCrossVisited doesn't actually do the capturing."""

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(crosscapt=True,
                                xc_sown=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    CASES = [([4, 4, 4, 4, 4, 4], [5, 4, 0, 5, 5, 5], 0, False),  # cycle board, not end in one
             ([4, 4, 4, 4, 4, 4], [4, 0, 5, 5, 5, 5], 5, False),  # end on opp side

             ([1, 6, 6, 6, 5, 0], [2, 1, 7, 7, 6, 1], 1, True),  # cross capt
             ([2, 3, 0, 1, 3, 1], [1, 4, 1, 1, 0, 1], 2, True),  # opp sow not cross hole, capt

             ([2, 3, 0, 1, 5, 1], [0, 4, 1, 1, 5, 1], 2, WinCond.REPEAT_TURN),
             ([1, 6, 3, 2, 0, 2], [0, 7, 3, 2, 0, 2], 1, False)  # end on own sidee, but no repeat turn
             ]

    @pytest.mark.parametrize('before_sow, after_sow, capt_loc, eresult',
                             CASES)
    def test_xc_visited(self, game, before_sow, after_sow, capt_loc, eresult):

        mdata = MoveData(game, None)
        mdata.board = tuple(before_sow)
        mdata.capt_loc = capt_loc
        mdata.direct = game.info.sow_direct
        game.board = after_sow
        game.turn = False

        game.deco.capturer.do_captures(mdata)
        assert mdata.captured == eresult



class TestCaptTwoOut:

    # actual captures are all on True side, picks on false side
    test_cases = [

        ([3, 3, 3, 4, 0, 2], False, 3, [0, 3, 3, 4, 0, 0], {'capsamedir': True,
                                                            'capttwoout': True}),

        ([3, 3, 3, 4, 0, 2], False, 3, [0, 3, 3, 4, 0, 0], {'capsamedir': True,
                                                            'capttwoout': True,
                                                            'multicapt': True}),
        ([0, 3, 0, 4, 0, 2], False, 3, [0] * 6, {'capsamedir': True,
                                                 'capttwoout': True,
                                                 'multicapt': True}),

        ]

    @pytest.mark.parametrize('board, turn, loc, eboard, options',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_capts(self, board, turn, loc, eboard, options):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=CaptExtraPick.PICKCROSS,
                                mlaps=True,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
        game.deco.capturer.do_captures(mdata)

        assert mdata.captured
        assert game.board == eboard


class TestPickCross:

    # actual captures are all on True side, picks on false side
    test_cases = [
        ([3, 3, 3, 2, 2, 2], True, 4, [3, 0, 3, 2, 0, 2], {'evens': True}),
        ([3, 3, 3, 2, 2, 2], True, 4, [3, 0, 3, 0, 0, 2], {'evens': True,
                                                           'multicapt': True}),

        pytest.param(
            [3, 1, 3, 2, 2, 2], True, 1, [3, 1, 3, 2, 0, 2], {'crosscapt': True},
            marks=pytest.mark.filterwarnings("ignore")),

        ([3, 3, 3, 4, 4, 2], False, 4, [3, 0, 3, 4, 0, 2], {'capt_on': [4]}),
        ([3, 3, 3, 4, 0, 2], False, 3, [0, 3, 3, 4, 0, 0], {'capsamedir': True,
                                                            'capttwoout': True})
        ]

    @pytest.mark.parametrize('board, turn, loc, eboard, options',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_capts(self, board, turn, loc, eboard, options):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=CaptExtraPick.PICKCROSS,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
        game.deco.capturer.do_captures(mdata)

        assert mdata.captured
        assert game.board == eboard


    @pytest.mark.parametrize('board, turn, loc, eboard, options',
                             test_cases,
                             ids=[f'case_{f}'
                                  for f in range(len(test_cases))])
    def test_locks(self, board, turn, loc, eboard, options):
        """capts from true side, pick from false side in data;
        lock false side there should be no picks."""

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=CaptExtraPick.PICKCROSS,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        game.unlocked = [False] * 3 + [True] * 3  # false side locked
        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
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

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=CaptExtraPick.PICKCROSS,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = board.copy()
        game.child = [False] * 3 + [None] * 3  # false side children
        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = loc
        game.deco.capturer.do_captures(mdata)

        assert mdata.captured
        assert game.board[:3] == board[:3]
        assert game.board[3:] == eboard[3:]


    def test_no_capt(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                pickextra=CaptExtraPick.PICKCROSS,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.board = [3, 3, 3, 3, 3, 3]
        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = 4
        game.deco.capturer.do_captures(mdata)

        assert not mdata.captured
        assert game.board == [3, 3, 3, 3, 3, 3]


class TestPickTwos:

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

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(stores=True,
                                crosscapt=True,
                                capt_on=[2],
                                oppsidecapt=True,
                                pickextra=CaptExtraPick.PICKTWOS,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = board.copy()
        game.turn = turn

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = caploc
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

        game_consts = gc.GameConsts(nbr_start=2, holes=2)
        game_info = gi.GameInfo(stores=True,
                                capt_on=[4],
                                sow_rule=gi.SowRule.OWN_SOW_CAPT_ALL,
                                pickextra=picker,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = board
        game.child = child
        game.store = store
        game.turn = turn
        game.starter = not turn

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        game.deco.capturer.do_captures(mdata)

        assert mdata.capt_changed == eres
        assert game.board == eboard
        assert game.store == estore


# %% make_child only tests


class TestNoChildren:

    def test_opp_child(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = True
        mdata.capt_loc = 1
        mdata.seeds = 1
        assert game.deco.make_child.test(mdata) == False


class TestChildInhibitor:
    """Complicated game to get Inhibitor both."""

    def test_inhibited(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
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

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_loc = 3
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

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OPP_ONLY,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = True
        mdata.capt_loc = 3
        assert not game.deco.make_child.test(mdata)

        mdata.capt_loc = 2
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

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.NOT_1ST_OPP,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = turn
        mdata.capt_loc = hole
        mdata.seeds = seeds
        assert game.deco.make_child.test(mdata) == etest



class TestBadEnums:

    def test_bad_cross_capt(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'crosscapt', True)
        object.__setattr__(game_info, 'xcpickown', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_grand_slam(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'grandslam', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_child_type(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'child_type', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_child_type_decos(self):
        """Two decos should raise the error, check both"""

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
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

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
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

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
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


# %%

"""
pytest.main(['test_captures.py::TestPickTwo[case_1]'])
"""
