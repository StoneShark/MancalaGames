# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 17:31:59 2023
@author: Ann
"""


# %% imports

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_interface as gi
from context import game_constants as gc
from context import mancala
from context import sower
from context import sower_decos as sowd
from context import sower_mlap_decos as msowd

from game_interface import CaptSide
from game_interface import ChildType
from game_interface import ChildRule
from game_interface import Direct
from game_interface import Goal
from game_interface import LapSower
from game_interface import PreSowCapt
from game_interface import SowPrescribed
from game_interface import SowRule
from game_interface import WinCond
from mancala import MoveData

# %%

TEST_COVERS = ['src\\sower.py',
               'src\\sower_decos.py',
               'src\\sower_mlap_decos.py']


# %% consts

HOLES = 3

T = True
F = False
N = None

CCW = gi.Direct.CCW
CW = gi.Direct.CW



# %%

class TestSower:
    """Call sow_starter to set the start hole to zero.
    Can do all of these tests with default sow_starter and incrementer,
    they are tested in different tests."""

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(capt_on=[2],
                                child_type=ChildType.NORMAL,
                                child_cvt=4,
                                child_rule=ChildRule.NOT_1ST_OPP,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def base_sower(self, game):
        object.__setattr__(game.info, 'sow_own_store', False)
        object.__setattr__(game.info, 'mlaps', LapSower.OFF)
        object.__setattr__(game.info, 'child_type', ChildType.NOCHILD)
        object.__setattr__(game.info, 'child_cvt', 0)
        object.__setattr__(game.info, 'visit_opp', False)
        return sower.deco_sower(game)


    bsower_cases = [(0, Direct.CCW, False,
                     utils.build_board([1, 2, 3],
                                       [2, 3, 4]), 2,
                     utils.build_board([1, 2, 3],
                                       [0, 4, 5])),
                    (1, Direct.CCW, False,
                     utils.build_board([1, 2, 3],
                                       [2, 3, 4]), 4,
                     utils.build_board([1, 3, 4],
                                       [2, 0, 5])),
                    (2, Direct.CCW, True,
                     utils.build_board([1, 2, 2],
                                       [2, 3, 4]), 5,
                     utils.build_board([2, 3, 0],
                                       [2, 3, 4])),
                    (1, Direct.CCW, True,
                     utils.build_board([1, 2, 2],
                                       [2, 3, 4]), 0,
                     utils.build_board([2, 0, 2],
                                       [3, 3, 4])),
                    ]

    @pytest.mark.parametrize('start_pos, direct, turn, board, eloc, eboard',
                             bsower_cases)
    def test_base_sower(self, game, base_sower,
                        start_pos, direct, turn, board, eloc, eboard):

        game.board = board
        game.turn = turn

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = direct
        base_sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == [0, 0]


    @pytest.fixture
    def esgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                stores=True,
                                sow_own_store=True,
                                sow_direct=Direct.SPLIT,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    str_split_cases = [
        #  don't pass any stores
        (2, False, utils.build_board([2, 1, 1, 2],
                                     [2, 1, 1, 2]),
         3, utils.build_board([2, 1, 1, 2],
                              [2, 1, 0, 3]), [0, 0]),
        # sow past own store
        (3, False, utils.build_board([2, 1, 1, 2],
                                     [2, 1, 1, 2]),
            4, utils.build_board([2, 1, 1, 3],
                                 [2, 1, 1, 0]), [1, 0]),

        (0, True, utils.build_board([2, 1, 1, 2],
                                    [2, 1, 1, 2]),
            0, utils.build_board([0, 1, 1, 2],
                                 [3, 1, 1, 2]), [0, 1]),

        # sow past opp store
        (0, False, utils.build_board([2, 1, 1, 2],
                                     [2, 1, 1, 2]),
            6, utils.build_board([3, 2, 1, 2],
                                 [0, 1, 1, 2]), [0, 0]),

        (3, True, utils.build_board([2, 1, 1, 2],
                                    [2, 1, 1, 2]),
            2, utils.build_board([2, 1, 1, 0],
                                 [2, 1, 2, 3]), [0, 0]),
        # end in own store
        (2, False, utils.build_board([2, 2, 2, 2],
                                     [2, 2, 2, 2]),
            WinCond.REPEAT_TURN, utils.build_board([2, 2, 2, 2],
                                                   [2, 2, 0, 3]), [1, 0]),

        (1, True, utils.build_board([2, 2, 2, 2],
                                    [2, 2, 2, 2]),
            WinCond.REPEAT_TURN, utils.build_board([3, 0, 2, 2],
                                                   [2, 2, 2, 2]), [0, 1]),
    ]

    @pytest.mark.parametrize(
        'start_pos, turn, board, eloc, eboard, estore',
        str_split_cases)
    def test_store_split_sower(self, esgame,
                               start_pos, turn, board, eloc, eboard, estore):

        esgame.board = board
        esgame.turn = turn
        mdata = esgame.do_sow(start_pos)

        assert mdata.capt_loc == eloc
        assert esgame.board == eboard
        assert esgame.store == estore


    store_cases = [
        # 0: CCW,  don't pass any stores
        (0, Direct.CCW, False, utils.build_board([1, 2, 3],
                                                 [2, 3, 4]),
         2, utils.build_board([1, 2, 3],
                              [0, 4, 5]), [0, 0]),
        # 1: CCW, sow past own store
        (1, Direct.CCW, False, utils.build_board([1, 2, 3],
                                                 [2, 3, 4]),
         3, utils.build_board([1, 2, 4],
                              [2, 0, 5]), [1, 0]),
        # 2: CCW, sow past both stores
        (1, Direct.CCW, False, utils.build_board([1, 2, 3],
                                                 [2, 6, 4]),
         0, utils.build_board([2, 3, 4],
                              [3, 0, 5]), [1, 0]),
        # 3: CCW, sow past opp store
        (2, Direct.CCW, True, utils.build_board([1, 2, 2],
                                                [2, 3, 4]),
         5, utils.build_board([2, 3, 0],
                              [2, 3, 4]), [0, 0]),
        # 4: CCW, end in own store
        (1, Direct.CCW, True, utils.build_board([1, 2, 2],
                                                [2, 3, 4]),
         WinCond.REPEAT_TURN, utils.build_board([2, 0, 2],
                                                [2, 3, 4]), [0, 1]),

        # 5: CW, don't pass any stores
        (1, Direct.CW, True, utils.build_board([1, 1, 2],
                                               [2, 3, 4]),
         3, utils.build_board([1, 0, 3],
                              [2, 3, 4]), [0, 0]),

        # 6: CW, sow past own store
        (2, Direct.CW, True, utils.build_board([1, 2, 6],
                                               [2, 3, 4]),
         4, utils.build_board([2, 3, 0],
                              [3, 4, 5]), [0, 1]),
        # 7: CW, sow past both stores
        (0, Direct.CW, False, utils.build_board([1, 2, 3],
                                                [5, 3, 4]),
         2, utils.build_board([2, 3, 4],
                              [0, 3, 5]), [1, 0]),
        # 8: CW, sow past opp store
        (2, Direct.CW, True, utils.build_board([1, 2, 2],
                                               [2, 3, 4]),
         1, utils.build_board([1, 2, 0],
                              [2, 4, 5]), [0, 0]),
        # 9: CW, end in own store
        (1, Direct.CW, False, utils.build_board([1, 2, 3],
                                                [2, 5, 4]),
         WinCond.REPEAT_TURN, utils.build_board([2, 3, 4],
                                                [3, 0, 4]), [1, 0]),
    ]

    @pytest.mark.parametrize(
        'start_pos, direct, turn, board, eloc, eboard, estore',
        store_cases)
    def test_store_sower(self, game,
                         start_pos, direct, turn, board, eloc, eboard, estore):

        # can't use fixture because sow_direct is used in the construction
        object.__setattr__(game.info, 'sow_own_store', True)
        object.__setattr__(game.info, 'mlaps', LapSower.OFF)
        object.__setattr__(game.info, 'child_type', ChildType.NOCHILD)
        object.__setattr__(game.info, 'child_cvt', 0)
        object.__setattr__(game.info, 'visit_opp', False)
        object.__setattr__(game.info, 'sow_direct', direct)
        store_sower = sower.deco_sower(game)

        game.board = board
        game.turn = turn

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = direct
        store_sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


    skip_cases = [
        ([0, 0, 3, 3, 2, 2, 2, 2], 3, [1, 1, 4, 0, 2, 2, 2, 2], 2),
        ([0, 0, 3, 3, 2, 1, 0, 2], 3, [1, 0, 3, 0, 2, 2, 1, 2], 0),
        ([0, 0, 3, 3, 1, 1, 1, 1], 3, [0, 0, 3, 0, 2, 2, 2, 1], 6),
        ([0, 0, 3, 5, 1, 1, 1, 1], 3, [1, 0, 3, 0, 2, 2, 2, 2], 0),
        ([0, 2, 0, 0, 2, 2, 2, 2], 1, [0, 0, 1, 1, 2, 2, 2, 2], 3),

        ]
    @pytest.mark.parametrize('board, spos, eboard, ecloc',
                             skip_cases)
    def test_skip_opp_n(self, board, spos, eboard, ecloc):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                sow_rule=SowRule.NO_SOW_OPP_NS,
                                sow_param=2,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.board = board
        game.store[0] = game.cts.total_seeds - sum(board)

        mdata = MoveData(game, spos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(spos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)

        assert game.board == eboard
        assert mdata.capt_loc == ecloc


    @pytest.mark.parametrize('end_loc, board, eresult',
                             [(WinCond.REPEAT_TURN, utils.build_board([1, 0, 3],
                                                                    [0, 3, 4]),
                              False),
                              (0, utils.build_board([1, 0, 3],
                                                    [1, 3, 4]), False),
                              (1, utils.build_board([1, 0, 3],
                                                    [1, 3, 4]), True),
                              (WinCond.REPEAT_TURN, utils.build_board([1, 0, 3],
                                                                    [0, 3, 4]),
                               False),
                              ])
    def test_simple_lap(self, game, end_loc, board, eresult):

        game.board = board
        mdata = MoveData(game, None)
        mdata.capt_loc = end_loc

        lap_cont = msowd.StopSingleSeed(game, msowd.LapContinue(game))
        lap_cont = msowd.StopRepeatTurn(game, lap_cont)

        assert lap_cont.do_another_lap(mdata) == eresult


    @pytest.mark.parametrize('end_loc, board, eresult, cloc',
                             [(WinCond.REPEAT_TURN, utils.build_board([1, 0, 3],
                                                                    [0, 3, 4]),
                              False, False),
                              (0, utils.build_board([1, 0, 3],
                                                    [1, 3, 4]), True, 1),
                              (2, utils.build_board([1, 2, 3],
                                                    [1, 3, 4]), True, 3),
                              (0, utils.build_board([1, 0, 3],
                                                    [1, 0, 4]), False, False),
                              ])
    def test_next_lap(self, game, end_loc, board, eresult, cloc):

        game.board = board
        mdata = MoveData(game, None)
        mdata.direct = Direct.CCW
        mdata.cont_sow_loc = 3
        mdata.capt_loc = end_loc

        lap_cont = msowd.NextLapCont(game)
        lap_cont = msowd.StopRepeatTurn(game, lap_cont)

        assert lap_cont.do_another_lap(mdata) == eresult
        if cloc:
            assert mdata.capt_loc == cloc

    chi_lap_cases = [
        # 0: not on end store
        (WinCond.REPEAT_TURN, 2,
         utils.build_board([1, 4, 4],
                           [1, 3, 0]),
         utils.build_board([N, N, N],
                           [N, N, N]), False),
        # 1: not on end in child
        (1, 2,
         utils.build_board([1, 4, 4],
                           [0, 3, 0]),
         utils.build_board([N, N, N],
                           [N, T, N]), False),
        # 2: my side of the board
        (1, 2,
         utils.build_board([1, 4, 4],
                           [0, 4, 0]),
         utils.build_board([N, N, N],
                           [N, N, N]), True),
        # 3: no child on opps first hole and one seed
        (3, 1,
         utils.build_board([1, 4, 4],
                           [0, 3, 0]),
         utils.build_board([N, N, N],
                           [N, N, N]), True),
        # 4: not first hole with > 1 seed, make child
        (3, 3,
         utils.build_board([1, 4, 4],
                           [0, 3, 4]),
         utils.build_board([N, T, N],
                           [N, N, N]), False),
        # 5: not if we should make a child
        (4, 3,
         utils.build_board([1, 4, 4],
                           [0, 3, 4]),
         utils.build_board([N, N, N],
                           [N, N, N]), False),
        # 6: not if only one seed
        (5, 3,
         utils.build_board([1, 4, 4],
                           [0, 3, 4]),
         utils.build_board([N, N, N],
                           [N, N, N]), False),
        # 7: not if already a child
        (5, 3,
         utils.build_board([1, 4, 4],
                           [0, 3, 4]),
         utils.build_board([N, T, N],
                           [N, N, N]), False),
        # 8: seeds > 1 seed, not child, opp side
        (4, 3,
         utils.build_board([1, 5, 4],
                           [0, 3, 4]),
         utils.build_board([N, N, N],
                           [N, N, N]), True),
    ]


    @pytest.mark.parametrize('end_loc, sown_seeds, board, child, eresult',
                            chi_lap_cases)
    def test_child_lap_with_opp(self, game, end_loc, sown_seeds,
                                board, child, eresult):

        game.turn = False
        game.board = board
        game.child = child

        mdata = MoveData(game, None)
        mdata.capt_loc = end_loc
        mdata.seeds = sown_seeds

        lap_cont = msowd.ChildLapCont(game)
        lap_cont = msowd.StopSingleSeed(game, lap_cont)
        lap_cont = msowd.StopOnChild(game, lap_cont)
        lap_cont = msowd.StopRepeatTurn(game, lap_cont)

        assert lap_cont.do_another_lap(mdata) == eresult


    chi_lap_not_cases = [
        # 0: not on end store
         (WinCond.REPEAT_TURN, 2,
          utils.build_board([1, 4, 4],
                            [1, 3, 0]),
          utils.build_board([N, N, N],
                            [N, N, N]), False),
         # 1: not on end in child
         (1, 2,
          utils.build_board([1, 4, 4],
                            [0, 3, 0]),
          utils.build_board([N, N, N],
                            [N, T, N]), False),
         # 2: my side of the board
         (1, 2,
          utils.build_board([1, 4, 4],
                            [0, 4, 0]),
          utils.build_board([N, N, N],
                            [N, N, N]), False),
         # 3: child on opps first hole and one seed
         (3, 1,
          utils.build_board([1, 4, 4],
                            [0, 3, 0]),
          utils.build_board([N, N, N],
                            [N, N, N]), False),
         # 4: not first hole with > 1 seed, make child
         (3, 3,
          utils.build_board([1, 4, 4],
                            [0, 3, 4]),
          utils.build_board([N, T, N],
                            [N, N, N]), False),
         # 5: not if we should make a child
         (4, 3,
          utils.build_board([1, 4, 4],
                            [0, 3, 4]),
          utils.build_board([N, N, N],
                            [N, N, N]), False),
         # 6: not if only one seed
         (5, 3,
          utils.build_board([1, 4, 4],
                            [0, 3, 4]),
          utils.build_board([N, N, N],
                            [N, N, N]), False),
         # 7: not if already a child
         (5, 3,
          utils.build_board([1, 4, 4],
                            [0, 3, 4]),
          utils.build_board([N, T, N],
                            [N, N, N]), False),
         # 8: seeds > 1 seed, not child, opp side
         (4, 3,
          utils.build_board([1, 5, 4],
                            [0, 3, 4]),
          utils.build_board([N, N, N],
                            [N, N, N]), True),
         ]

    @pytest.fixture
    def nogame(self):
        """not opp for conversion."""

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(capt_on=[2],
                                child_type=ChildType.NORMAL,
                                child_cvt=4,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)



    @pytest.mark.parametrize('end_loc, sown_seeds, board, child, eresult',
                             chi_lap_not_cases)
    def test_child_lap_not_opp(self, nogame, end_loc, sown_seeds,
                               board, child, eresult):

        nogame.turn = False
        nogame.board = board
        nogame.child = child

        mdata = MoveData(nogame, None)
        mdata.capt_loc = end_loc
        mdata.seeds = sown_seeds

        lap_cont = msowd.ChildLapCont(nogame)
        lap_cont = msowd.StopSingleSeed(nogame, lap_cont)
        lap_cont = msowd.StopOnChild(nogame, lap_cont)
        lap_cont = msowd.StopRepeatTurn(nogame, lap_cont)

        assert lap_cont.do_another_lap(mdata) == eresult



    @pytest.fixture
    def maxgame(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_rule=7,
                                sow_param=5,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    max_cases = [# normal sow cases
                 (0, Direct.CCW, False, (2, 3, 4, 3, 2, 1), 2,
                                        (0, 4, 5, 3, 2, 1)),
                 (0, Direct.CW, False, (2, 3, 4, 3, 2, 1), 4,
                                       (0, 3, 4, 3, 3, 2)),

                 # skip one five
                 (2, Direct.CCW, False, (0, 0, 3, 4, 5, 4), 0,
                                        (1, 0, 0, 5, 5, 5)),

                 # skip all op side
                 (2, Direct.CCW, False, (0, 0, 3, 5, 5, 5), 2,
                                        (1, 1, 1, 5, 5, 5)),
                    ]

    @pytest.mark.parametrize('start_pos, direct, turn, board, eloc, eboard',
                             max_cases)
    def test_max_sower(self, maxgame, base_sower,
                        start_pos, direct, turn, board, eloc, eboard):

        maxgame.board = list(board)
        maxgame.turn = turn

        mdata = MoveData(maxgame, start_pos)
        mdata.sow_loc, mdata.seeds = maxgame.deco.drawer.draw(start_pos)
        mdata.direct = direct
        maxgame.deco.sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert maxgame.board == list(eboard)
        assert maxgame.store == [0, 0]


    # @pytest.mark.usefixtures("logger")
    def test_no_sow_child(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                child_type = gi.ChildType.NORMAL,
                                child_cvt = 6,
                                sow_rule=gi.SowRule.NO_OPP_CHILD,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)

        game.board = [0, 5, 2, 2, 2, 2]
        game.child = [T, N, T, F, T, N]
        # print(game)

        sow_pos = 1
        mdata = MoveData(game, sow_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(sow_pos)
        mdata.direct = gi.Direct.CCW
        game.deco.sower.sow_seeds(mdata)
        # print(game)

        assert game.board == [0, 1, 2, 4, 2, 4]
        assert mdata.capt_loc == 5



class TestMlap:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(crosscapt=True,
                                mlaps=LapSower.LAPPER,
                                sow_direct=Direct.CW,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def nlgame(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                mlaps=LapSower.LAPPER_NEXT,
                                sow_direct=Direct.CCW,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def evgame(self):
        """capt on even # seeds, should stop sowing to capt"""
        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                mlaps=LapSower.LAPPER,
                                sow_direct=Direct.CCW,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def xcevgame(self):
        """cross capt but only even # seeds, do not stop on evens"""
        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(crosscapt=True,
                                evens=True,
                                mlaps=LapSower.LAPPER,
                                sow_direct=Direct.CCW,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def moppgame(self):
        """match opposite capture -- should stop mlapping"""
        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(stores=True,
                                mlaps=LapSower.LAPPER,
                                sow_direct=Direct.CCW,
                                capt_type=gi.CaptType.MATCH_OPP,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    MLCASES = [
        # 0: no lapping
        ('game',
         2, utils.build_board([1, 2, 3],
                              [0, 3, 2]),
         0, utils.build_board([1, 2, 3],
                              [1, 4, 0])),
        # 1: sow two laps
        ('game',
         0, utils.build_board([1, 2, 3],
                              [2, 0, 4]),
         1, utils.build_board([2, 0, 4],
                              [0, 1, 5])),
        # 2: endless
        ('game',
         4, utils.build_board([1, 3, 1],
                              [0, 1, 0]),
         WinCond.ENDLESS,
         utils.build_board([2, 1, 0],
                           [0, 0, 1])),

        # 3
        ('nlgame',
         4, utils.build_board([1, 2, 3],
                              [2, 0, 4]),
         0, utils.build_board([2, 0, 3],
                              [3, 0, 4])),
        # 4:  laps
        ('nlgame',
         1, utils.build_board([2, 2, 3],
                              [0, 3, 2]),
         1, utils.build_board([1, 4, 5],
                              [0, 2, 0])),

        # 5:  laps
        ('evgame',
         1, utils.build_board([0, 1, 0],
                              [1, 3, 0]),
         4, utils.build_board([0, 2, 1],
                              [1, 0, 1])),

        # 6:  laps
        ('xcevgame',
         1, utils.build_board([0, 1, 0],
                              [1, 3, 0]),
         4, utils.build_board([1, 1, 2],
                              [0, 1, 0])),

        # 7:  laps, stop on single seed, capt will occur
        ('moppgame',
         1, utils.build_board([0, 1, 0],
                              [1, 3, 0]),
         4, utils.build_board([1, 1, 2],
                              [0, 1, 0])),

        # 8:  laps, stop on one
        ('moppgame',
         1, utils.build_board([1, 1, 0],
                              [0, 3, 0]),
         0, utils.build_board([2, 0, 1],
                              [1, 0, 1])),

        # 7:  laps, stop for simul capt
        ('moppgame',
         1, utils.build_board([1, 0, 1],
                              [2, 2, 1]),
         3, utils.build_board([1, 0, 2],
                              [2, 0, 2])),

    ]
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('game_fixt, start_pos, board, eloc, eboard',
                             MLCASES)
    def test_mlap_sower(self, request, game_fixt,
                        start_pos, board, eloc, eboard):

        game = request.getfixturevalue(game_fixt)

        game.board = board
        game.turn = False
        # print(game.deco.sower)

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)
        # print(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == [0, 0]


    # @pytest.mark.usefixtures("logger")
    def test_mlap_mopp_inhibit(self):
        """This is case 7 above that stopped for simul capture:
                # 7:  laps, stop for simul capt
                ('moppgame',
                 1, utils.build_board([1, 0, 1],
                                      [2, 2, 1]),

        But it doesn't stop for the capture because they are inhibited
        on the first turn."""

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(stores=True,
                                mlaps=LapSower.LAPPER,
                                sow_direct=Direct.CCW,
                                nocaptmoves=1,
                                capt_type=gi.CaptType.MATCH_OPP,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        start_pos = 1
        game.board = utils.build_board([1, 0, 1],
                                       [2, 2, 1])
        game.turn = False
        # print(game.deco.sower)

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)
        # print(mdata)

        assert mdata.capt_loc == 1
        assert game.board == utils.build_board([0, 1, 0],
                                               [3, 1, 2])
        assert game.store == [0, 0]


    @pytest.fixture
    def opgame(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[1],
                                mlaps=gi.LapSower.LAPPER,
                                sow_rule=gi.SowRule.CHANGE_DIR_LAP,
                                udir_holes=[0, 1, 2, 3],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)



    @pytest.mark.parametrize('turn, spos, sdirect, eboard, eloc',
                             [(T, 0, CCW, utils.build_board([2, 0, 3, 3],
                                                            [6, 6, 1, 3]), 2),
                              (T, 0, CW, utils.build_board([2, 6, 6, 1],
                                                           [0, 3, 3, 3]), 4),
                              (F, 2, CW, utils.build_board([1, 3, 3, 3],
                                                           [6, 6, 2, 0]), 7),
                              (F, 2, CCW, utils.build_board([3, 3, 1, 6],
                                                            [3, 0, 2, 6]), 5)
                              ],
                             ids=['T_7_CCW', 'T_7_CW', 'F_2_CW', 'F_2_CCW'])
    def test_change_dir(self, opgame, turn, spos, sdirect, eboard, eloc):
        """Test changing directions on each lap."""

        opgame.turn = turn
        move = gi.MoveTpl(spos, sdirect)
        mdata = MoveData(opgame, move)
        mdata.sow_loc, mdata.seeds = opgame.deco.drawer.draw(move)
        mdata.direct = sdirect
        opgame.deco.sower.sow_seeds(mdata)

        assert opgame.board == eboard
        assert mdata.capt_loc == eloc


class TestGetSingle:
    """Test get single sower."""

    @pytest.mark.parametrize('lapper', (False, True))
    def test_get_single(self, lapper):

        mlaps = LapSower.LAPPER if lapper else LapSower.OFF

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                mlaps=mlaps,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        assert isinstance(game.deco.sower.get_single_sower(),
                          sowd.SowSeeds)

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_own_store=True,
                                mlaps=mlaps,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        assert isinstance(game.deco.sower.get_single_sower(),
                          sowd.SowSeedsNStore)

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_rule=SowRule.OWN_SOW_CAPT_ALL,
                                mlaps=mlaps,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        assert isinstance(game.deco.sower.get_single_sower(),
                          sowd.SowCaptOwned)

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                blocks=True,
                                goal_param=2,
                                sow_rule=SowRule.SOW_BLKD_DIV,
                                mlaps=mlaps,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        if lapper:
            assert isinstance(game.deco.sower.get_single_sower(),
                              sowd.DivertSkipBlckdSower)
            # might seem like an error but single sow is used in
            # opp_or_empty, we don't care if the hole is closed or not
            # only where the sow ended
        else:
            assert isinstance(game.deco.sower.get_single_sower(),
                              sowd.SowClosed)

        if lapper:
            # test one with visit opp
            game_consts = gc.GameConsts(nbr_start=4, holes=4)
            game_info = gi.GameInfo(evens=True,
                                    stores=True,
                                    mlaps=mlaps,
                                    child_type=ChildType.NORMAL,
                                    child_cvt=3,
                                    visit_opp=True,
                                    nbr_holes=game_consts.holes,
                                    rules=mancala.Mancala.rules)
            game = mancala.Mancala(game_consts, game_info)
            assert isinstance(game.deco.sower.get_single_sower(),
                              sowd.SowSeeds)


class TestVMlap:
    """Interesting that the game flags needed to match all those
    for the sower.  Child sowing didn't work right w/o it."""

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(sow_direct=Direct.CW,
                                stores=True,
                                sow_own_store=True,
                                mlaps=LapSower.LAPPER,
                                visit_opp=True,
                                child_type=ChildType.NORMAL,
                                child_cvt=4,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    vmlap_cases = [
        # 0: no visit opp
        (2, utils.build_board([1, 2, 3],
                              [0, 3, 2]),
         0, utils.build_board([1, 2, 3],
                              [1, 4, 0]), [0, 0]),
        # 1: end_store
        (2, utils.build_board([1, 2, 3],
                              [2, 3, 6]),
         WinCond.REPEAT_TURN,
         utils.build_board([2, 3, 4],
                           [3, 4, 0]), [1, 0]),
        # 2: visit opp -> stop for child
        (2, utils.build_board([3, 2, 3],
                              [0, 3, 3]),
         5, utils.build_board([4, 2, 3],
                              [1, 4, 0]), [0, 0]),
        # 3: visit opp -> lapping
        (2, utils.build_board([2, 2, 3],
                              [0, 3, 3]),
         WinCond.REPEAT_TURN,
         utils.build_board([0, 3, 4],
                           [1, 4, 0]), [1, 0]),
        # 4: visit opp -> no lapping
        (2, utils.build_board([0, 2, 3],
                              [0, 3, 3]),
         5, utils.build_board([1, 2, 3],
                              [1, 4, 0]), [0, 0]),
    ]

    @pytest.mark.parametrize(
        'start_pos, board, eloc, eboard, estore',
        vmlap_cases)
    def test_vmlap_sower(self, game,
                        start_pos, board, eloc, eboard, estore):

        game.board = board
        game.turn = False

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = Direct.CW
        game.deco.sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


class TestBlckDivertSower:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(sow_direct=Direct.CW,
                                goal=Goal.DEPRIVE,
                                sow_rule=SowRule.SOW_BLKD_DIV,
                                blocks=True,
                                goal_param=3,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def game_nr(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(sow_direct=Direct.CW,
                                goal=Goal.DEPRIVE,
                                sow_rule=SowRule.SOW_BLKD_DIV_NR,
                                blocks=True,
                                goal_param=3,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    divert_cases = [('game', False, 1,
                     utils.build_board([2, 2, 2],
                                       [2, 2, 2]), [0, 0],
                     utils.build_board([F, F, F],
                                       [F, F, F]),
                     5,
                     utils.build_board([0, 2, 2],
                                       [3, 0, 2]), [3, 0],
                     utils.build_board([T, F, F],
                                       [F, F, F])),
                    ('game', False, 0,
                     utils.build_board([0, 2, 2],
                                       [3, 0, 2]), [3, 0],
                     utils.build_board([T, F, F],
                                       [F, F, F]),
                     3,
                     utils.build_board([0, 3, 0],
                                       [0, 0, 2]), [7, 0],
                     utils.build_board([T, F, T],
                                       [F, F, F])),
                    ('game', False, 0,
                     utils.build_board([0, 2, 2],
                                       [4, 0, 0]), [3, 0],
                     utils.build_board([T, F, F],
                                       [F, F, T]),
                     1,
                     utils.build_board([0, 3, 3],
                                       [0, 1, 0]), [4, 0],
                     utils.build_board([T, F, F],
                                       [F, F, T])),
                    ('game', False, 0,
                     utils.build_board([0, 0, 2],
                                       [2, 0, 0]), [3, 0],
                     utils.build_board([T, T, F],
                                       [F, F, T]),
                     4,
                     utils.build_board([0, 0, 2],
                                       [0, 0, 0]), [5, 0],
                     utils.build_board([T, T, F],
                                       [F, F, T])),

                    ('game_nr', False, 1,   # don't close True's  right
                     utils.build_board([2, 2, 2],
                                       [2, 2, 2]), [0, 0],
                     utils.build_board([F, F, F],
                                       [F, F, F]),
                     5,
                     utils.build_board([3, 2, 2],
                                       [3, 0, 2]), [0, 0],
                     utils.build_board([F, F, F],
                                       [F, F, F])),

                    ('game_nr', False, 0,   # divert sow & close left
                     utils.build_board([0, 0, 2],
                                       [3, 0, 2]), [3, 0],
                     utils.build_board([F, T, F],
                                       [F, F, F]),
                     3,
                     utils.build_board([1, 0, 0],
                                       [0, 0, 2]), [7, 0],
                     utils.build_board([F, T, T],
                                       [F, F, F])),

                    ('game_nr', True, 1,   # don't close False's right
                     utils.build_board([2, 2, 2],
                                       [2, 2, 2]), [0, 0],
                     utils.build_board([F, F, F],
                                       [F, F, F]),
                     2,
                     utils.build_board([2, 0, 3],
                                       [2, 2, 3]), [0, 0],
                     utils.build_board([F, F, F],
                                       [F, F, F])),
                    ]

    @pytest.mark.parametrize(
        'game_fixt, turn, spos, board, store, block, eloc, eboard, estore, eblock',
        divert_cases)
    def test_divert_sower(self, request, game_fixt,
                          turn, spos, board, store, block,
                                eloc, eboard, estore, eblock):

        game = request.getfixturevalue(game_fixt)

        game.board = board
        game.store = store
        game.blocked = block
        game.turn = turn

        mdata = MoveData(game, spos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(spos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore
        assert game.blocked == eblock


    @pytest.fixture
    def mlgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(sow_direct=Direct.CW,
                                sow_rule=SowRule.SOW_BLKD_DIV,
                                goal=Goal.DEPRIVE,
                                blocks=True,
                                mlaps=LapSower.LAPPER,
                                goal_param=3,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def mlgame_nr(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(sow_direct=Direct.CW,
                                sow_rule=SowRule.SOW_BLKD_DIV_NR,
                                goal=Goal.DEPRIVE,
                                blocks=True,
                                mlaps=LapSower.LAPPER,
                                goal_param=3,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.mark.parametrize(
        'game_fixt, turn, spos, board, store, block,'
        ' eloc, eboard, estore, eblock',
        [('mlgame', False, 1,
          utils.build_board([2, 2, 2],
                            [2, 2, 2]), [0, 0],
          utils.build_board([F, F, F],
                            [F, F, F]),
          5,
          utils.build_board([0, 3, 3],
                            [4, 1, 0]), [1, 0],
          utils.build_board([T, F, F],
                            [F, F, F])),

         ('mlgame_nr', False, 1,
           utils.build_board([2, 2, 2],
                             [2, 2, 2]), [0, 0],
           utils.build_board([F, F, F],
                             [F, F, F]),
           5,
           utils.build_board([1, 3, 3],
                             [4, 1, 0]), [0, 0],
           utils.build_board([F, F, F],
                             [F, F, F]))
         ])

    def test_divert_laps_sower(self, request, game_fixt,
                               turn, spos, board, store, block,
                                     eloc, eboard, estore, eblock):
        mlgame = request.getfixturevalue(game_fixt)
        mlgame.board = board
        mlgame.store = store
        mlgame.blocked = block
        mlgame.turn = turn

        mdata = MoveData(mlgame, spos)
        mdata.sow_loc, mdata.seeds = mlgame.deco.drawer.draw(spos)
        mdata.direct = mlgame.info.sow_direct
        mlgame.deco.sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert mlgame.board == eboard
        assert mlgame.store == estore
        assert mlgame.blocked == eblock

        # print(mlgame.deco.sower.lap_cont)
        assert 'SowMlap' in str(mlgame.deco.sower)
        assert 'CloseOp' in str(mlgame.deco.sower.end_lap_op)
        assert 'Divert' in str(mlgame.deco.sower.lap_cont)


class TestSowCaptOwned:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                sow_rule=SowRule.OWN_SOW_CAPT_ALL,
                                sow_direct=Direct.CCW,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'start_pos, board, eloc, eboard, estore',
        [(1, utils.build_board([2, 2, 3],
                               [0, 3, 2]),
          4, utils.build_board([2, 3, 0],
                               [0, 0, 3]), [0, 4]),
           (1, utils.build_board([2, 3, 3],
                                 [0, 3, 2]),
            4, utils.build_board([2, 0, 0],
                                 [0, 0, 3]), [0, 8]),
          ])
    def test_goal_mseeds(self, game, start_pos, board, eloc, eboard, estore):

        game.board = board
        game.turn = False

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


    @pytest.fixture
    def game2(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                sow_rule=SowRule.OWN_SOW_CAPT_ALL,
                                goal=Goal.TERRITORY,
                                goal_param=4,
                                stores=True,
                                sow_direct=Direct.CCW,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    def test_goal_terr_seeds(self, game2):
        game2.board = utils.build_board([2, 3, 3],
                                        [0, 3, 3])
        game2.turn = False

        move = gi.MoveTpl(not game2.turn, 1, None)
        mdata = MoveData(game2, move)
        mdata.sow_loc, mdata.seeds = game2.deco.drawer.draw(move)
        mdata.direct = game2.info.sow_direct
        game2.deco.sower.sow_seeds(mdata)

        assert mdata.capt_loc == 4
        assert game2.board == utils.build_board([2, 0, 0],
                                                [0, 0, 0])
        assert game2.store == [4, 8]


    @pytest.fixture
    def game_ss(self, request):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_rule=SowRule.SOW_CAPT_ALL,
                                capt_side=request.param,
                                sow_direct=Direct.CCW,
                                mlaps=gi.LapSower.LAPPER,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    SSCASES = [
        (CaptSide.OPP_SIDE,                 # two laps, pick 4
         1, utils.build_board([2, 2, 3],
                              [0, 3, 2]),
         1, utils.build_board([3, 0, 0],
                              [1, 1, 3]), [4, 0]),

        (CaptSide.OPP_SIDE,                 # stop 1st lap for capture @  4
         1, utils.build_board([2, 3, 3],
                              [0, 3, 2]),
         4, utils.build_board([2, 4, 0],
                              # capture not done yet
                              [0, 0, 3]), [4, 0]),

        (CaptSide.OPP_SIDE,                 # don't capt 4 on own side
         1, utils.build_board([2, 3, 3],
                              [0, 3, 3]),
         4, utils.build_board([2, 4, 0],
                              [0, 0, 4]), [4, 0]),

        (CaptSide.OWN_SIDE,                 # pick 4 @ 2, no capture @ 4 cont sow
         1, utils.build_board([2, 2, 3],
                              [0, 2, 3]),
         1, utils.build_board([3, 3, 0],
                              [1, 1, 0]), [4, 0]),

        (CaptSide.OWN_SIDE,                 # stop for capt @ 2
         1, utils.build_board([2, 3, 3],
                              [0, 3, 2]),
         2, utils.build_board([3, 0, 4],
                              # capture not done yet
                              [1, 1, 4]), [0, 0]),

        (CaptSide.OWN_SIDE,                 #
         1, utils.build_board([2, 3, 3],
                              [0, 3, 3]),
         2, utils.build_board([3, 0, 4],
                              [1, 1, 1]), [4, 0]),


        (CaptSide.BOTH,                 # stop for capture at 4
         1, utils.build_board([2, 2, 3],
                              [0, 2, 3]),
         3, utils.build_board([2, 2, 4],
                              [0, 0, 0]), [4, 0]),

        (CaptSide.BOTH,                 # pick 4, stop for capt @ 5
         1, utils.build_board([2, 3, 3],
                              [0, 3, 2]),
         4, utils.build_board([2, 4, 0],
                              [0, 0, 3]), [4, 0]),

        (CaptSide.BOTH,                 # pick 3 & 4, stop for capt @ 5
         1, utils.build_board([2, 3, 3],
                              [0, 3, 3]),
         4, utils.build_board([2, 4, 0],
                              [0, 0, 0]), [8, 0]),

    ]
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize(
        'game_ss, start_pos, board, eloc, eboard, estore',
        SSCASES, ids=[f"case_{i}" for i in range(len(SSCASES))],
        indirect=['game_ss'])
    def test_ss_goal_mseeds(self, game_ss, start_pos, board,
                            eloc, eboard, estore):

        game_ss.board = board
        game_ss.turn = False
        # print(game_ss)

        mdata = MoveData(game_ss, start_pos)
        mdata.sow_loc, mdata.seeds = game_ss.deco.drawer.draw(start_pos)
        mdata.direct = game_ss.info.sow_direct
        game_ss.deco.sower.sow_seeds(mdata)
        # print('after', game_ss, sep='\n')

        assert mdata.capt_loc == eloc
        assert game_ss.board == eboard
        assert game_ss.store == estore


    @pytest.fixture
    def game2_ss(self, request):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_rule=SowRule.SOW_CAPT_ALL,
                                capt_side=request.param,
                                goal=Goal.TERRITORY,
                                goal_param=4,
                                sow_direct=Direct.CCW,
                                mlaps=gi.LapSower.LAPPER,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    TSSCASES = [
        (CaptSide.OPP_SIDE,
         1, utils.build_board([2, 3, 3],
                              [0, 3, 3]),
         4, utils.build_board([2, 4, 0],
                              [0, 0, 4]), [4, 0]),

        (CaptSide.OWN_SIDE,
         1, utils.build_board([2, 3, 3],
                              [0, 3, 3]),
         2, utils.build_board([3, 0, 4],
                              [1, 1, 1]), [4, 0]),
        (CaptSide.BOTH,
         1, utils.build_board([2, 3, 0],
                              [0, 3, 0]),
         4, utils.build_board([2, 4, 0],
                              [0, 0, 0]), [0, 0]),
        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize(
        'game2_ss, start_pos, board, eloc, eboard, estore',
        TSSCASES, ids=[f"case_{i}" for i in range(len(TSSCASES))],
        indirect=['game2_ss'])
    def test_ss_goal_terr_seeds(self, game2_ss, start_pos, board,
                            eloc, eboard, estore):
        game2_ss.board = board
        game2_ss.turn = False

        move = gi.MoveTpl(not game2_ss.turn, 1, None)
        mdata = MoveData(game2_ss, move)
        mdata.sow_loc, mdata.seeds = game2_ss.deco.drawer.draw(move)
        mdata.direct = game2_ss.info.sow_direct
        game2_ss.deco.sower.sow_seeds(mdata)
        # print(game2_ss)

        assert mdata.capt_loc == eloc
        assert game2_ss.board == board
        assert game2_ss.store == estore



class TestPrescribed:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    def test_mechanic(self, game, mocker):

        mpresc = mocker.patch('sower_decos.SowOneOpp.do_prescribed')
        msower = mocker.patch('sower_decos.SowSeeds.sow_seeds')

        swr = sowd.SowSeeds(game)
        swr = sowd.SowOneOpp(game, 2, swr)

        move = 1
        mdata = MoveData(game, move)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(move)
        mdata.direct = game.info.sow_direct

        game.mcount += 1           # done at the top of _move
        swr.sow_seeds(mdata)

        mpresc.assert_called_once()
        msower.assert_not_called()

        # do_prescribed should be called again
        game.mcount += 1
        swr.sow_seeds(mdata)

        assert len(mpresc.mock_calls) == 2
        msower.assert_not_called()

        # sower should be called
        game.mcount += 1
        swr.sow_seeds(mdata)

        assert len(mpresc.mock_calls) == 2
        msower.assert_called_once()

        # confirm new_game resets behavior
        game.new_game()
        mpresc.reset_mock()
        msower.reset_mock()

        move = 1
        mdata = MoveData(game, move)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(move)
        mdata.direct = game.info.sow_direct

        game.mcount += 1           # done at the top of _move
        swr.sow_seeds(mdata)

        mpresc.assert_called_once()
        msower.assert_not_called()

        # do_prescribed should be called again
        game.mcount += 1
        swr.sow_seeds(mdata)

        assert len(mpresc.mock_calls) == 2
        msower.assert_not_called()

        # sower should be called
        game.mcount += 1
        swr.sow_seeds(mdata)

        assert len(mpresc.mock_calls) == 2
        msower.assert_called_once()


    def test_basic_pres(self, mocker):
        """the prescribed sower is SowSeeds, confirm it's called"""

        msower = mocker.patch('sower_decos.SowSeeds.sow_seeds')

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                prescribed=SowPrescribed.BASIC_SOWER,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = 1
        mdata = MoveData(game, move)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(move)
        mdata.direct = game.info.sow_direct

        game.mcount += 1           # done at the top of _move
        game.deco.sower.sow_seeds(mdata)

        msower.assert_called_once()


    def test_mlaps_pres(self, mocker):
        """the prescribed sower is SowMlapSeeds, confirm it's called"""

        msower = mocker.patch('sower_mlap_decos.SowMlapSeeds.sow_seeds')

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                mlaps=True,
                                stores=True,
                                prescribed=SowPrescribed.MLAPS_SOWER,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = 1
        mdata = MoveData(game, move)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(move)
        mdata.direct = game.info.sow_direct

        game.mcount += 1           # done at the top of _move
        game.deco.sower.sow_seeds(mdata)

        msower.assert_called_once()


    @pytest.fixture
    def game_1opp(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                prescribed=SowPrescribed.SOW1OPP,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    sow1opp_cases = [
        (False, [0, 3, 2, 2, 3, 2, 2, 2], 0),
        (False, [2, 0, 3, 2, 3, 2, 2, 2], 1),
        (False, [2, 2, 0, 3, 3, 2, 2, 2], 2),
        (False, [2, 2, 2, 0, 3, 3, 2, 2], 3),
        (True, [3, 2, 2, 2, 0, 3, 2, 2], 3),
        (True, [3, 2, 2, 2, 2, 0, 3, 2], 2),
        (True, [3, 2, 2, 2, 2, 2, 0, 3], 1),
        (True, [3, 3, 2, 2, 2, 2, 2, 0], 0),
        ]

    @pytest.mark.parametrize('turn, eboard, move', sow1opp_cases)
    def test_sow1opp(self, game_1opp, turn, move, eboard):

        game_1opp.turn = turn
        game_1opp.move(move)
        assert game_1opp.board == eboard


    @pytest.fixture
    def game_p1m1(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                prescribed=SowPrescribed.PLUS1MINUS1,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    sowp1m1_cases = [
        (False, [2, 1, 3, 1, 3, 1, 3, 0], 0),
        (False, [1, 2, 1, 3, 1, 3, 0, 3], 1),
        (True, [0, 3, 1, 3, 1, 3, 1, 2], 0),
        (True, [3, 0, 3, 1, 3, 1, 2, 1], 1),
        ]

    @pytest.mark.parametrize('turn, eboard, move', sowp1m1_cases)
    def test_sowp1m1(self, game_p1m1, turn, move, eboard):

        game_p1m1.turn = turn
        game_p1m1.move(move)
        assert game_p1m1.board == eboard


class TestCaptMlap:

    @pytest.fixture
    def ccgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(crosscapt=True,
                                stores=True,
                                sow_direct=Direct.CW,
                                mlaps=LapSower.LAPPER,
                                sow_rule=SowRule.LAP_CAPT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def evgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_direct=Direct.CCW,
                                mlaps=LapSower.LAPPER,
                                sow_rule=SowRule.LAP_CAPT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def c1game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(capt_on=[1],
                                stores=True,
                                sow_direct=Direct.CCW,
                                mlaps=LapSower.LAPPER,
                                sow_rule=SowRule.LAP_CAPT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def gapgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(capt_type=gi.CaptType.TWO_OUT,
                                capsamedir=True,
                                stores=True,
                                sow_direct=Direct.CCW,
                                mlaps=LapSower.LAPPER,
                                sow_rule=SowRule.LAP_CAPT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def nextgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(capt_type=gi.CaptType.NEXT,
                                capsamedir=True,
                                stores=True,
                                sow_direct=Direct.CCW,
                                mlaps=LapSower.LAPPER,
                                sow_rule=SowRule.LAP_CAPT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    CASES = [
        ('ccgame', 0, F, [2, 2, 2, 2, 2, 2, 2, 2],
         7, [0, 3, 3, 0, 3, 3, 0, 1], [3, 0]),

        ('evgame', 3, F, [2, 2, 2, 2, 2, 2, 2, 2],
         3, [0, 3, 3, 1, 3, 0 ,3, 3], [0, 0]),

        ('evgame', 3, T, [3, 1, 3, 0, 3, 3, 0, 3],
         3, [0, 2, 4, 1, 0, 4, 1, 0], [0, 4]),

        # basic capture of 1s (StopSingleSeed was in wrong place on deco chain)
        ('c1game', 1, F, [1, 3, 1, 1, 0, 1, 0, 1],
         6, [0, 1, 0, 3, 1, 0, 0, 0], [3, 0]),

        # 4: end in hole with one seed and capture left for capturer
        ('nextgame', 2, F, [3, 1, 2, 1, 0, 1, 1, 1],
         4, [3, 1, 0, 2, 1, 1, 1, 1], [0, 0]),

        # 5: end in hole with one seed but no capture
        ('nextgame', 2, F, [3, 1, 2, 1, 0, 0, 1, 1],
         4, [3, 1, 0, 2, 1, 0, 1, 1], [0, 0]),

        # 6: end in hole with one seed and capture left for capturer
        ('nextgame', 2, F, [3, 1, 2, 1, 0, 0, 1, 1],
         4, [3, 1, 0, 2, 1, 0, 1, 1], [0, 0]),

        # 7: end in hole with one seed but no capture
        ('gapgame', 2, F, [3, 1, 2, 1, 0, 1, 1, 1],
         4, [3, 1, 0, 2, 1, 1, 1, 1], [0, 0]),

        # 8: actual mlap sow with captures
        ('nextgame', 1, F, [3, 1, 2, 1, 0, 1, 1, 1],
         1, [1, 1, 0, 1, 1, 0, 1, 0], [5, 0]),

        # 9: actual mlap sow with captures
        ('gapgame', 1, F, [3, 1, 2, 0, 1, 1, 1, 0],
         7, [3, 0, 0, 1, 1, 0, 2, 1], [1, 0]),

    ]

    @pytest.mark.usefixtures('logger')
    @pytest.mark.parametrize('game_fixt, start_pos, turn, board, ' \
                             'eloc, eboard, estore',
                             CASES, ids=[f"{case[0]}-case{idx}"
                                         for idx, case in enumerate(CASES)])
    def test_mlap_sower(self, request, game_fixt,
                        start_pos, turn, board,
                        eloc, eboard, estore):

        game = request.getfixturevalue(game_fixt)
        game.board = board
        game.turn = turn
        print(game.deco.sower)
        print(game)
        print(start_pos)

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)

        print(game)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


class TestSCapt:

    @pytest.fixture
    def c1game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_direct=Direct.CW,
                                mlaps=LapSower.LAPPER,
                                presowcapt=PreSowCapt.CAPT_ONE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def a1game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_direct=Direct.CCW,
                                presowcapt=PreSowCapt.ALL_SINGLE_XCAPT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def d1game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_direct=Direct.CCW,
                                presowcapt=PreSowCapt.DRAW_1_XCAPT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    CASES = [
        ('c1game', 0, F, [2, 2, 2, 2, 2, 2, 2, 2],
         7, [1, 0, 3, 0, 3, 0, 3, 1], [5, 0]),

        # no capt
        ('a1game', 0, F, [2, 2, 2, 2, 2, 2, 2, 2],
         2, [0, 3, 3, 2, 2, 2 ,2, 2], [0, 0]),

        # capt & sow
        ('a1game', 0, F, [2, 1, 2, 1, 2, 2, 2, 2],
         2, [0, 2, 3, 1, 0, 2, 0, 2], [4, 0]),

        # no capt, sow
        ('d1game', 0, F, [2, 1, 2, 1, 2, 2, 2, 2],
         2, [0, 2, 3, 1, 2, 2, 2, 2], [0, 0]),

        # capt & sow
        ('d1game', 1, F, [2, 1, 2, 1, 2, 2, 2, 2],
         2, [2, 0, 3, 1, 2, 2, 0, 2], [2, 0]),

        ]
    # @pytest.mark.usefixtures('logger')
    @pytest.mark.parametrize('game_fixt, start_pos, turn, board, ' \
                             'eloc, eboard, estore',
                             CASES, ids=[f"{case[0]}-case{idx}"
                                         for idx, case in enumerate(CASES)])
    def test_mlap_sower(self, request, game_fixt,
                        start_pos, turn, board,
                        eloc, eboard, estore):

        game = request.getfixturevalue(game_fixt)
        game.board = board
        game.turn = turn
        # print(game.deco.sower)
        # print(game)
        # print(start_pos)

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)
        # print(game)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


class TestCaptOppOwnLast:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                sow_direct=Direct.CCW,
                                mlaps=LapSower.LAPPER,
                                sow_rule=SowRule.OPP_GETS_OWN_LAST,
                                sow_param=6,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    CASES = [
        # 0 & 1: two test cases from LAP_CAPT for evens game
        (3, F, [2, 2, 2, 2, 2, 2, 2, 2], [0, 0],
         3,    [0, 3, 3, 1, 3, 0 ,3, 3], [0, 0]),

        (3, T, [3, 1, 3, 0, 3, 3, 0, 3], [0, 0],
         3,    [0, 2, 4, 1, 0, 4, 1, 0], [0, 4]),

        # 2: capture so final loc is 5 not 4 (i.e., try to sow from next hole)
        (3, F, [0, 0, 3, 1, 3, 0, 3, 0], [3, 3],
         5,    [0, 0, 3, 0, 0, 0, 3, 0], [7, 3]),

        # 3: sow one own hole, one opp -> opp captures, final even -> sow capts
        # end loc is next hole
        (2, F, [0, 1, 3, 0, 0, 1, 0, 0], [4, 7],
         6,    [0, 1, 0, 1, 0, 0, 0, 0], [6, 8]),

        # 4: wrap opp side -> all capt, no final capt so end on last hole sown
        (3, F, [0, 0, 0, 6, 0, 0, 0, 0], [6, 4],
         1,    [1, 1, 0, 0, 0, 0, 0, 0], [6, 8]),

        ]
    # @pytest.mark.usefixtures('logger')
    @pytest.mark.parametrize('start_pos, turn, board, store, ' \
                             'eloc, eboard, estore',
                             CASES, ids=[f"case{idx}"
                                         for idx, case in enumerate(CASES)])
    def test_ogol_sower(self, game, start_pos, turn, board, store,
                        eloc, eboard, estore):

        game.board = board
        game.store = store
        game.turn = turn
        # print(game.deco.sower)
        # print(game)
        # print(start_pos)

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.drawer.draw(start_pos)
        mdata.direct = game.info.sow_direct
        game.deco.sower.sow_seeds(mdata)

        # print(game)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore



class TestBadEnums:

    def test_bad_sow_rule(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'sow_rule', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_mlaps(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'mlaps', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_prescribed(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        # sower doesn't handle
        object.__setattr__(game_info, 'prescribed', SowPrescribed.ARNGE_LIMIT)
        mancala.Mancala(game_consts, game_info)

        object.__setattr__(game_info, 'prescribed', 12)
        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_presowcapt(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'presowcapt', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)
