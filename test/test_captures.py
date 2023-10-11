# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:31:23 2023
@author: Ann"""

import collections
import re

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import capturer
from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import GrandSlam
from mancala import MoveData


# %%

TEST_COVERS = ['src\\capturer.py']


# %% read test cases

SKEEP = slice(0, 42)
SBOARD = slice(0, 4)
SCHILD = slice(4, 8)
SLOCKS = slice(8, 12)
SSTORE = slice(12, 14)
SINDIV = slice(14, 31)
SEBOARD = slice(31, 35)
SECHILD = slice(35, 39)
SESTORE = slice(39, 41)

CAPT_ON = 18
RESULT = 41

CONVERT_DICT = {'N': None,
                'T': True,
                'TRUE': True,
                'F': False,
                'FALSE': False,
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

def convert(val, col, line):

    if col == CAPT_ON:
        capts = []
        if val:
            for ival in val.split(' '):
                if re.match('[0-9]+$', ival):
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

    if re.match('[0-9]+$', val):
        return int(val)

    if not val:
        return 0

    raise ValueError(f"Unknown value type at col/line {col}/{line}: {val}")


def read_test_cases():

    global FIELD_NAMES, CASES

    with open('test/capture_test_data.csv', 'r', encoding='utf-8') as file:
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

        CASES += [Case(board, child, locks, store,
                       *(line_one[SINDIV]),
                       eboard, echild, estore, line_one[RESULT])]


read_test_cases()


# %%  the tests

@pytest.mark.filterwarnings("ignore")
def test_no_capturer():
    game_consts = gc.GameConsts(nbr_start=3, holes=4)
    game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game = mancala.Mancala(game_consts, game_info)
    mdata = MoveData(game, None)
    mdata.direct = Direct.CCW
    mdata.capt_loc = 5
    assert not game.deco.capturer.do_captures(mdata)
    assert game.board == [3] * 8
    assert game.store == [0, 0]


class TestCaptTable:

    @staticmethod
    def make_game(case):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=case.capt_on,
                                capsamedir=case.capsamedir,
                                child=case.child,
                                convert_cnt=case.convert_cnt,
                                crosscapt=case.xcapt,
                                capt_min=case.capt_min,
                                evens=case.evens,
                                capttwoout=case.capttwoout,
                                grandslam=case.gslam,
                                moveunlock=case.moveunlock,
                                multicapt=case.multicapt,
                                nosinglecapt=True,
                                oppsidecapt=case.oppside,
                                skip_start=case.skip_start,
                                xcpickown=case.xcapt_pick_own,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        game.turn = case.turn
        game.board = case.board.copy()
        game.child = case.children.copy()
        game.unlocked = case.unlocked.copy()
        game.store = case.store.copy()

        return game


    @pytest.fixture(params=CASES)
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

        captures = game.deco.capturer.do_captures(mdata)

        assert sum(game.store) + sum(game.board) == game.cts.total_seeds
        assert bool(captures) == case.erval
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

        assert not game.deco.capturer.do_captures(mdata)
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
    assert game.deco.capturer.do_captures(mdata)
    assert game.board == [3, 0, 0, 0]
    assert game.store == [5, 4]


class TestWaldas:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=5)
        game_info = gi.GameInfo(child=True,
                                convert_cnt=4,
                                waldas=True,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_small(self, game):

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

        game.board = [4] * game.cts.dbl_holes
        game.turn = turn

        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.capt_loc = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert game.deco.capturer.do_captures(mdata) == ewalda

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

        assert not game.deco.capturer.do_captures(mdata)
        assert game.board[loc] == 3
        assert game.child[loc] == None


    @pytest.mark.parametrize('turn', (False, True))
    def test_waldas_capts(self, game, turn):
        """each has a walda (leftmost hole),
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

        assert game.deco.capturer.do_captures(mdata)
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

        assert not game.deco.capturer.do_captures(mdata)
        assert game.board[loc] == 3
        assert game.board[wloc] == 3
        assert game.child[loc] == None


class TestTuzdek:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child=True,
                                convert_cnt=3,
                                one_child=True,
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

        assert game.deco.capturer.do_captures(mdata)

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

        assert game.deco.capturer.do_captures(mdata)
        print(game)

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

        assert game.deco.capturer.do_captures(mdata)
        print(game)

        assert game.board[loc] == 0


# %%

"""
pytest.main(['test_captures.py::TestTuzdek'])
"""
