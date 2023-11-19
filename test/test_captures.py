# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:31:23 2023
@author: Ann"""

import collections

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import capturer
from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import CaptExtraPick
from game_interface import ChildType
from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import GrandSlam
from game_interface import WinCond
from mancala import MoveData


# %%

TEST_COVERS = ['src\\capturer.py']


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

    if val.isdigit():
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

        CASES += [Case(line_one[CASE], board, child, locks, store,
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
    game.deco.capturer.do_captures(mdata)
    assert not mdata.captured
    assert game.board == [3] * 8
    assert game.store == [0, 0]


class TestCaptTable:

    @staticmethod
    def make_game(case):

        child_type = ChildType.NORMAL if case.child_cvt else ChildType.NOCHILD

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
                                ch_opp_only=case.oppside,
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

        print(game)
        print(case)
        game.deco.capturer.do_captures(mdata)
        print(game)
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


class TestWaldas:

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


class TestRepeatTurn:

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
        ([3, 1, 3, 2, 2, 2], True, 1, [3, 1, 3, 2, 0, 2], {'crosscapt': True}),
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


# %%

"""
pytest.main(['test_captures.py::TestPickTwo[case_1]'])
"""
