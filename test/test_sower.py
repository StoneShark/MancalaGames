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

from game_interface import ChildType
from game_interface import Direct
from game_interface import Goal
from game_interface import WinCond
# from game_log import game_log
from mancala import MoveData

# %%

TEST_COVERS = ['src\\sower.py']


# %% consts

HOLES = 3

T = True
F = False
N = None


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
                                oppsidecapt=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


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


    @pytest.fixture
    def base_sower(self, game):
        object.__setattr__(game.info, 'sow_own_store', False)
        object.__setattr__(game.info, 'mlaps', False)
        object.__setattr__(game.info, 'child_type', ChildType.NOCHILD)
        object.__setattr__(game.info, 'child_cvt', 0)
        object.__setattr__(game.info, 'visit_opp', False)
        return sower.deco_sower(game)


    @pytest.mark.parametrize('start_pos, direct, turn, board, eloc, eboard',
                             [(0, Direct.CCW, False,
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
                              ])

    def test_base_sower(self, game, base_sower,
                        start_pos, direct, turn, board, eloc, eboard):

        game.board = board
        game.turn = turn

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.starter.start_sow(start_pos)
        mdata.direct = direct
        mdata = base_sower.sow_seeds(mdata)

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


    @pytest.mark.parametrize(
        'start_pos, turn, board, eloc, eboard, estore',
         #  don't pass any stores
        [(2, False, utils.build_board([2, 1, 1, 2],
                                      [2, 1, 1, 2]),
          3,        utils.build_board([2, 1, 1, 2],
                                      [2, 1, 0, 3]), [0, 0]),
         # sow past own store
         (3, False, utils.build_board([2, 1, 1, 2],
                                      [2, 1, 1, 2]),
          4,        utils.build_board([2, 1, 1, 3],
                                      [2, 1, 1, 0]), [1, 0]),

         (0, True,  utils.build_board([2, 1, 1, 2],
                                      [2, 1, 1, 2]),
          0,        utils.build_board([0, 1, 1, 2],
                                      [3, 1, 1, 2]), [0, 1]),

         # sow past opp store
         (0, False, utils.build_board([2, 1, 1, 2],
                                      [2, 1, 1, 2]),
          6,        utils.build_board([3, 2, 1, 2],
                                      [0, 1, 1, 2]), [0, 0]),

         (3, True,  utils.build_board([2, 1, 1, 2],
                                      [2, 1, 1, 2]),
          2,        utils.build_board([2, 1, 1, 0],
                                      [2, 1, 2, 3]), [0, 0]),
         # end in own store
         (2, False,          utils.build_board([2, 2, 2, 2],
                                               [2, 2, 2, 2]),
          WinCond.END_STORE, utils.build_board([2, 2, 2, 2],
                                               [2, 2, 0, 3]), [1, 0]),

         (1, True,           utils.build_board([2, 2, 2, 2],
                                               [2, 2, 2, 2]),
          WinCond.END_STORE, utils.build_board([3, 0, 2, 2],
                                               [2, 2, 2, 2]), [0, 1]),
          ])

    def test_store_split_sower(self, esgame,
                               start_pos, turn, board, eloc, eboard, estore):

        esgame.board = board
        esgame.turn = turn
        mdata = esgame.do_sow(start_pos)

        assert mdata.capt_loc == eloc
        assert esgame.board == eboard
        assert esgame.store == estore


    @pytest.mark.parametrize(
        'start_pos, direct, turn, board, eloc, eboard, estore',
        # 0: CCW,  don't pass any stores
        [(0, Direct.CCW, False, utils.build_board([1, 2, 3],
                                                  [2, 3, 4]),
          2,                    utils.build_board([1, 2, 3],
                                                  [0, 4, 5]), [0, 0]),
         # 1: CCW, sow past own store
         (1, Direct.CCW, False, utils.build_board([1, 2, 3],
                                                  [2, 3, 4]),
          3,                    utils.build_board([1, 2, 4],
                                                  [2, 0, 5]), [1, 0]),
         # 2: CCW, sow past both stores
         (1, Direct.CCW, False, utils.build_board([1, 2, 3],
                                                  [2, 6, 4]),
          0,                    utils.build_board([2, 3, 4],
                                                  [3, 0, 5]), [1, 0]),
         # 3: CCW, sow past opp store
         (2, Direct.CCW, True,  utils.build_board([1, 2, 2],
                                                  [2, 3, 4]),
          5,                    utils.build_board([2, 3, 0],
                                                  [2, 3, 4]), [0, 0]),
         # 4: CCW, end in own store
         (1, Direct.CCW, True,  utils.build_board([1, 2, 2],
                                                  [2, 3, 4]),
          WinCond.END_STORE,    utils.build_board([2, 0, 2],
                                                  [2, 3, 4]), [0, 1]),

         # 5: CW, don't pass any stores
         (1, Direct.CW,  True,  utils.build_board([1, 1, 2],
                                                  [2, 3, 4]),
          3,                    utils.build_board([1, 0, 3],
                                                  [2, 3, 4]), [0, 0]),

         # 6: CW, sow past own store
         (2, Direct.CW,  True,  utils.build_board([1, 2, 6],
                                                  [2, 3, 4]),
          4,                    utils.build_board([2, 3, 0],
                                                  [3, 4, 5]), [0, 1]),
         # 7: CW, sow past both stores
         (0, Direct.CW,  False, utils.build_board([1, 2, 3],
                                                  [5, 3, 4]),
          2,                    utils.build_board([2, 3, 4],
                                                  [0, 3, 5]), [1, 0]),
         # 8: CW, sow past opp store
         (2, Direct.CW,  True,  utils.build_board([1, 2, 2],
                                                  [2, 3, 4]),
          1,                    utils.build_board([1, 2, 0],
                                                  [2, 4, 5]), [0, 0]),
         # 9: CW, end in own store
         (1, Direct.CW,  False, utils.build_board([1, 2, 3],
                                                  [2, 5, 4]),
          WinCond.END_STORE,    utils.build_board([2, 3, 4],
                                                  [3, 0, 4]), [1, 0]),
          ])

    def test_store_sower(self, game,
                         start_pos, direct, turn, board, eloc, eboard, estore):

        # can't use fixture because sow_direct is used in the construction
        object.__setattr__(game.info, 'sow_own_store', True)
        object.__setattr__(game.info, 'mlaps', False)
        object.__setattr__(game.info, 'child_type', ChildType.NOCHILD)
        object.__setattr__(game.info, 'child_cvt', 0)
        object.__setattr__(game.info, 'visit_opp', False)
        object.__setattr__(game.info, 'sow_direct', direct)
        store_sower = sower.deco_sower(game)

        game.board = board
        game.turn = turn

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.starter.start_sow(start_pos)
        mdata.direct = direct
        mdata = store_sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


    @pytest.mark.parametrize('end_loc, board, eresult',
                             [(WinCond.END_STORE, utils.build_board([1, 0, 3],
                                                                    [0, 3, 4]),
                              False),
                              (0, utils.build_board([1, 0, 3],
                                                    [1, 3, 4]), False),
                              (1, utils.build_board([1, 0, 3],
                                                    [1, 3, 4]), True),
                              (WinCond.END_STORE, utils.build_board([1, 0, 3],
                                                                    [0, 3, 4]),
                               False),
                              ])
    def test_simple_lap(self, game, end_loc, board, eresult):

        game.board = board
        mdata = MoveData(game, None)
        mdata.capt_loc = end_loc

        lap_cont = sower.SimpleLapCont(game)
        assert lap_cont.do_another_lap(mdata) == eresult


    @pytest.mark.parametrize('end_loc, sown_seeds, board, child, eresult',
                             # 0: not on end store
                             [(WinCond.END_STORE, 2,
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

                              ])
    def test_child_lap_with_opp(self, game, end_loc, sown_seeds,
                                board, child, eresult):

        game.turn = False
        game.board = board
        game.child = child

        mdata = MoveData(game, None)
        mdata.capt_loc = end_loc
        mdata.seeds = sown_seeds

        lap_cont = sower.ChildLapCont(game)
        assert lap_cont.do_another_lap(mdata) == eresult


    @pytest.mark.parametrize('end_loc, sown_seeds, board, child, eresult',
                             # 0: not on end store
                             [(WinCond.END_STORE, 2,
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

                              ])
    def test_child_lap_not_opp(self, nogame, end_loc, sown_seeds,
                       board, child, eresult):

        nogame.turn = False
        nogame.board = board
        nogame.child = child

        mdata = MoveData(nogame, None)
        mdata.capt_loc = end_loc
        mdata.seeds = sown_seeds

        lap_cont = sower.ChildLapCont(nogame)
        assert lap_cont.do_another_lap(mdata) == eresult


class TestMlap:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                sow_direct=Direct.CW,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def mlap_sower(self, game):
        # deco_sower(game, sow_own_store, mlaps, visit_opp, child)

        object.__setattr__(game.info, 'sow_own_store', False)
        object.__setattr__(game.info, 'mlaps', True)
        object.__setattr__(game.info, 'child', False)
        object.__setattr__(game.info, 'visit_opp', False)
        return sower.deco_sower(game)


    @pytest.mark.parametrize(
        'start_pos, board, eloc, eboard',
        # 0: no lapping
        [(2, utils.build_board([1, 2, 3],
                               [0, 3, 2]),
          0, utils.build_board([1, 2, 3],
                               [1, 4, 0])),
         # 1: sow two laps
         (0, utils.build_board([1, 2, 3],
                               [2, 0, 4]),
          1, utils.build_board([2, 0, 4],
                               [0, 1, 5])),
         # 2: endless
         (4, utils.build_board([1, 3, 1],
                               [0, 1, 0]),
          WinCond.ENDLESS,
             utils.build_board([2, 1, 0],
                               [0, 0, 1])),
          ])

    def test_mlap_sower(self, game, mlap_sower,
                        start_pos, board, eloc, eboard):

        game.board = board
        game.turn = False

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.starter.start_sow(start_pos)
        mdata.direct = game.info.sow_direct
        mdata = mlap_sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == [0, 0]


class TestVMlap:
    """Interesting that the game flags needed to match all those
    for the sower.  Child sowing didn't work right w/o it."""

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                sow_direct=Direct.CW,
                                stores=True,
                                sow_own_store=True,
                                mlaps=True,
                                visit_opp=True,
                                child_type=ChildType.NORMAL,
                                child_cvt=4,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'start_pos, board, eloc, eboard, estore',
        # 0: no visit opp
        [(2, utils.build_board([1, 2, 3],
                               [0, 3, 2]),
          0, utils.build_board([1, 2, 3],
                               [1, 4, 0]), [0, 0]),
        # 1: end_store
         (2, utils.build_board([1, 2, 3],
                               [2, 3, 6]),
          WinCond.END_STORE,
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
          WinCond.END_STORE,
             utils.build_board([0, 3, 4],
                               [1, 4, 0]), [1, 0]),
        # 4: visit opp -> no lapping
         (2, utils.build_board([0, 2, 3],
                               [0, 3, 3]),
          5, utils.build_board([1, 2, 3],
                               [1, 4, 0]), [0, 0]),
          ])

    def test_vmlap_sower(self, game,
                        start_pos, board, eloc, eboard, estore):

        game.board = board
        game.turn = False

        mdata = MoveData(game, start_pos)
        mdata.sow_loc, mdata.seeds = game.deco.starter.start_sow(start_pos)
        mdata.direct = Direct.CW
        mdata =game.deco.sower.sow_seeds(mdata)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


class TestBlckDivertSower:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(sow_direct=Direct.CW,
                                goal=Goal.DEPRIVE,
                                sow_blkd_div=True,
                                blocks=True,
                                convert_cnt=3,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.mark.parametrize(
        'turn, spos, board, store, block, eloc, eboard, estore, eblock',
        [(False, 1,
          utils.build_board([2, 2, 2],
                            [2, 2, 2]), [0, 0],
          utils.build_board([F, F, F],
                            [F, F, F]),
          5,
          utils.build_board([0, 2, 2],
                            [3, 0, 2]), [3, 0],
          utils.build_board([T, F, F],
                            [F, F, F])),
         (False, 0,
          utils.build_board([0, 2, 2],
                            [3, 0, 2]), [3, 0],
          utils.build_board([T, F, F],
                            [F, F, F]),
          3,
          utils.build_board([0, 3, 0],
                            [0, 0, 2]), [7, 0],
          utils.build_board([T, F, T],
                            [F, F, F])),
         (False, 0,
          utils.build_board([0, 2, 2],
                            [4, 0, 0]), [3, 0],
          utils.build_board([T, F, F],
                            [F, F, T]),
          1,
          utils.build_board([0, 3, 3],
                            [0, 1, 0]), [4, 0],
          utils.build_board([T, F, F],
                            [F, F, T])),
         (False, 0,
          utils.build_board([0, 0, 2],
                            [2, 0, 0]), [3, 0],
          utils.build_board([T, T, F],
                            [F, F, T]),
          4,
          utils.build_board([0, 0, 2],
                            [0, 0, 0]), [5, 0],
          utils.build_board([T, T, F],
                            [F, F, T])),
         ])
    def test_divert_sower(self, game,
                          turn, spos, board, store, block,
                                eloc, eboard, estore, eblock):

        game.board = board
        game.store = store
        game.blocked = block
        game.turn = turn
        print(game)

        mdata = MoveData(game, spos)
        mdata.sow_loc, mdata.seeds = game.deco.starter.start_sow(spos)
        mdata.direct = game.info.sow_direct
        mdata = game.deco.sower.sow_seeds(mdata)
        print('after sow')
        print(game)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore
        assert game.blocked == eblock


    @pytest.fixture
    def mlgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(sow_direct=Direct.CW,
                                sow_blkd_div=True,
                                goal=Goal.DEPRIVE,
                                blocks=True,
                                mlaps=True,
                                convert_cnt=3,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)



    @pytest.mark.parametrize(
        'turn, spos, board, store, block, eloc, eboard, estore, eblock',
        [(False, 1,
          utils.build_board([2, 2, 2],
                            [2, 2, 2]), [0, 0],
          utils.build_board([F, F, F],
                            [F, F, F]),
          5,
          utils.build_board([0, 3, 3],
                            [4, 1, 0]), [1, 0],
          utils.build_board([T, F, F],
                            [F, F, F])),
         ])
    def test_divert_laps_sower(self, mlgame,
                               turn, spos, board, store, block,
                                     eloc, eboard, estore, eblock):
        mlgame.board = board
        mlgame.store = store
        mlgame.blocked = block
        mlgame.turn = turn
        print(mlgame)

        mdata = MoveData(mlgame, spos)
        mdata.sow_loc, mdata.seeds = mlgame.deco.starter.start_sow(spos)
        mdata.direct = mlgame.info.sow_direct
        mdata = mlgame.deco.sower.sow_seeds(mdata)
        print('after sow')
        print(mlgame)

        assert mdata.capt_loc == eloc
        assert mlgame.board == eboard
        assert mlgame.store == estore
        assert mlgame.blocked == eblock
