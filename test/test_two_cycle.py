# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 18:20:19 2025

@author: Ann
"""

# %% imports

import pytest
pytestmark = pytest.mark.unittest

from context import cfg_keys as ckey
from context import game_constants as gconsts
from context import game_interface as gi
from context import ginfo_rules
from context import incrementer
from context import mancala
from context import two_cycle
import utils

# %%

TEST_COVERS = ['src\\two_cycle.py']

# %% constants

T = True
F = False
N = None

CW = gi.Direct.CW
CCW = gi.Direct.CCW



class TestNorthSouthIncr:
    """Test for NorthSouthIncr."""

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=two_cycle.NorthSouthCycle.rules)

        game = two_cycle.NorthSouthCycle(game_consts, game_info)
        game.turn = False
        return game


    def test_incr(self, game):

        object.__setattr__(game.info, ckey.SOW_DIRECT, gi.Direct.CW)
        incr = two_cycle.NorthSouthIncr(game)

        assert incr.incr(0, gi.Direct.CW) == 4
        assert incr.incr(1, gi.Direct.CW) == 0
        assert incr.incr(2, gi.Direct.CW) == 1
        assert incr.incr(3, gi.Direct.CW) == 2
        assert incr.incr(4, gi.Direct.CW) == 3

        assert incr.incr(5, gi.Direct.CW) == 9
        assert incr.incr(6, gi.Direct.CW) == 5
        assert incr.incr(7, gi.Direct.CW) == 6
        assert incr.incr(8, gi.Direct.CW) == 7
        assert incr.incr(9, gi.Direct.CW) == 8

        object.__setattr__(game.info, ckey.SOW_DIRECT, gi.Direct.CCW)
        incr = two_cycle.NorthSouthIncr(game)

        assert incr.incr(0, gi.Direct.CCW) == 1
        assert incr.incr(1, gi.Direct.CCW) == 2
        assert incr.incr(2, gi.Direct.CCW) == 3
        assert incr.incr(3, gi.Direct.CCW) == 4
        assert incr.incr(4, gi.Direct.CCW) == 0


        assert incr.incr(5, gi.Direct.CCW) == 6
        assert incr.incr(6, gi.Direct.CCW) == 7
        assert incr.incr(7, gi.Direct.CCW) == 8
        assert incr.incr(8, gi.Direct.CCW) == 9
        assert incr.incr(9, gi.Direct.CCW) == 5



class TestSowStore:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                sow_own_store=True,
                                goal=gi.Goal.CLEAR,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                udir_holes=[0, 1, 2],
                                nbr_holes=game_consts.holes,
                                rules=two_cycle.NorthSouthCycle.rules)

        game = two_cycle.NorthSouthCycle(game_consts, game_info)
        game.turn = False
        return game


    store_cases = [
        # 0: CCW,  don't pass any stores
        (0, CCW, False, utils.build_board([1, 2, 3],
                                          [2, 3, 4]),
         2, utils.build_board([1, 2, 3],
                              [0, 4, 5]), [0, 0]),

        # 1: CCW, sow past own store
        (1, CCW, False, utils.build_board([1, 2, 3],
                                          [2, 3, 4]),
         0, utils.build_board([1, 2, 3],
                              [3, 0, 5]), [1, 0]),

        # 2: CCW, sow past both stores
        (1, CCW, False, utils.build_board([1, 2, 3],
                                          [2, 6, 0]),
         gi.WinCond.REPEAT_TURN, utils.build_board([1, 2, 3],
                                                   [3, 1, 2]), [2, 0]),

        # 3: CCW, sow past both stores
        (2, CCW, True, utils.build_board([2, 3, 4],
                                         [2, 3, 4]),
         3, utils.build_board([3, 4, 1],
                              [2, 3, 4]), [0, 1]),

        # 4: CW, don't pass any stores
        (1, CW, True, utils.build_board([1, 1, 2],
                                        [2, 3, 4]),
         3, utils.build_board([1, 0, 3],
                              [2, 3, 4]), [0, 0]),

        # 5: CW, sow past both stores
        (0, CW, False, utils.build_board([1, 2, 3],
                                         [7, 3, 2]),
         1, utils.build_board([1, 2, 3],
                              [1, 5, 4]), [2, 0]),
        ]

    # @pytest.mark.usefixtures('logger')
    @pytest.mark.parametrize(
        'start_pos, direct, turn, board, eloc, eboard, estore',
        store_cases,
        ids=[f"case_{idx}" for idx, _ in enumerate(store_cases)])
    def test_store_sower(self, game,
                         start_pos, direct, turn, board,
                         eloc, eboard, estore):

        game.board = board
        game.turn = turn
        # print(game)

        move = (start_pos, direct)
        mdata = game.do_sow(move)

        assert mdata.capt_loc == eloc
        assert game.board == eboard
        assert game.store == estore


class TestEastWestIncr:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=6)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                skip_start=True,
                                capt_side=gi.CaptSide.BOTH,
                                nbr_holes=game_consts.holes,
                                rules=two_cycle.EastWestCycle.rules)

        game = two_cycle.EastWestCycle(game_consts, game_info)
        game.turn = False
        return game


    @pytest.mark.parametrize('direct', gi.Direct)
    def test_ewincr(self, game, direct):
        """incrementing is independent of the direction set in the game."""

        object.__setattr__(game.info, ckey.SOW_DIRECT, direct)
        incr = two_cycle.EastWestIncr(game)

        # CW, west side
        assert incr.incr(0, gi.Direct.CW) == 11
        assert incr.incr(1, gi.Direct.CW) == 0
        assert incr.incr(2, gi.Direct.CW) == 1
        assert incr.incr(9, gi.Direct.CW) == 2
        assert incr.incr(10, gi.Direct.CW) == 9
        assert incr.incr(11, gi.Direct.CW) == 10

        # CW, east side
        assert incr.incr(3, gi.Direct.CW) == 8
        assert incr.incr(4, gi.Direct.CW) == 3
        assert incr.incr(5, gi.Direct.CW) == 4
        assert incr.incr(6, gi.Direct.CW) == 5
        assert incr.incr(7, gi.Direct.CW) == 6
        assert incr.incr(8, gi.Direct.CW) == 7

        # CCW, west side
        assert incr.incr(0, gi.Direct.CCW) == 1
        assert incr.incr(1, gi.Direct.CCW) == 2
        assert incr.incr(2, gi.Direct.CCW) == 9
        assert incr.incr(9, gi.Direct.CCW) == 10
        assert incr.incr(10, gi.Direct.CCW) == 11
        assert incr.incr(11, gi.Direct.CCW) == 0

        # CCW, east side
        assert incr.incr(3, gi.Direct.CCW) == 4
        assert incr.incr(4, gi.Direct.CCW) == 5
        assert incr.incr(5, gi.Direct.CCW) == 6
        assert incr.incr(6, gi.Direct.CCW) == 7
        assert incr.incr(7, gi.Direct.CCW) == 8
        assert incr.incr(8, gi.Direct.CCW) == 3


class TestEWClearEnder:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=gi.Goal.CLEAR,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=two_cycle.EastWestCycle.rules)

        return two_cycle.EastWestCycle(game_consts, game_info)

    END_CASES = [
        # 0: Will be F's turn, they have noseeds and win
        (True, utils.build_board([0, 1, 0, 0],
                                 [0, 3, 0, 0]),
         gi.WinCond.WIN, False),

        # 1: Will be T's turn, the have no seeds and win
        (False, utils.build_board([0, 0, 0, 1],
                                  [0, 0, 3, 0]),
         gi.WinCond.WIN, True),

        # 2: False gave away all seeds but not their turn
        (False, utils.build_board([0, 1, 0, 0],
                                  [1, 0, 0, 0]),
         gi.WinCond.WIN, False),

        # 3: True gave away all seeds but not their turn
        (True, utils.build_board([0, 0, 1, 0],
                                 [0, 0, 1, 0]),
         gi.WinCond.WIN, True),

        # 4: False gave away all seeds but true has seeds
        (False, utils.build_board([0, 1, 0, 0],
                                  [0, 0, 0, 0]),
         gi.WinCond.WIN, False),

        # 5: True gave away all seeds but false has seeds
        (True, utils.build_board([0, 0, 0, 0],
                                 [0, 0, 1, 0]),
         gi.WinCond.WIN, True),

        # 6: game continues
        (True, utils.build_board([0, 0, 3, 0],
                                 [0, 3, 0, 0]),
         None, None),

        # 7: game continues
        (False, utils.build_board([0, 3, 0, 0],
                                  [0, 0, 3, 0]),
         None, None),

    ]

    @pytest.mark.parametrize('turn, board, econd, ewinner',
                             END_CASES)
    def test_end_game(self, game, turn, board, econd, ewinner):
        game.board = board
        game.turn = turn

        mdata = utils.make_ender_mdata(game, False, False)
        game.deco.ender.game_ended(mdata)
        assert mdata.win_cond == econd
        assert mdata.winner == ewinner
