# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 18:20:19 2025

@author: Ann
"""

# %% imports

import pytest
pytestmark = pytest.mark.unittest

from context import allowables
from context import cfg_keys as ckey
from context import game_constants as gconsts
from context import game_info as gi
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

        assert incr.incr(0, gi.Direct.CW, None) == 4
        assert incr.incr(1, gi.Direct.CW, None) == 0
        assert incr.incr(2, gi.Direct.CW, None) == 1
        assert incr.incr(3, gi.Direct.CW, None) == 2
        assert incr.incr(4, gi.Direct.CW, None) == 3

        assert incr.incr(5, gi.Direct.CW, None) == 9
        assert incr.incr(6, gi.Direct.CW, None) == 5
        assert incr.incr(7, gi.Direct.CW, None) == 6
        assert incr.incr(8, gi.Direct.CW, None) == 7
        assert incr.incr(9, gi.Direct.CW, None) == 8

        object.__setattr__(game.info, ckey.SOW_DIRECT, gi.Direct.CCW)
        incr = two_cycle.NorthSouthIncr(game)

        assert incr.incr(0, gi.Direct.CCW, None) == 1
        assert incr.incr(1, gi.Direct.CCW, None) == 2
        assert incr.incr(2, gi.Direct.CCW, None) == 3
        assert incr.incr(3, gi.Direct.CCW, None) == 4
        assert incr.incr(4, gi.Direct.CCW, None) == 0


        assert incr.incr(5, gi.Direct.CCW, None) == 6
        assert incr.incr(6, gi.Direct.CCW, None) == 7
        assert incr.incr(7, gi.Direct.CCW, None) == 8
        assert incr.incr(8, gi.Direct.CCW, None) == 9
        assert incr.incr(9, gi.Direct.CCW, None) == 5



class TestSowStore:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                sow_stores=gi.SowStores.OWN,
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
         -1, utils.build_board([1, 2, 3],
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
        # print(game)

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
        assert incr.incr(0, gi.Direct.CW, None) == 11
        assert incr.incr(1, gi.Direct.CW, None) == 0
        assert incr.incr(2, gi.Direct.CW, None) == 1
        assert incr.incr(9, gi.Direct.CW, None) == 2
        assert incr.incr(10, gi.Direct.CW, None) == 9
        assert incr.incr(11, gi.Direct.CW, None) == 10

        # CW, east side
        assert incr.incr(3, gi.Direct.CW, None) == 8
        assert incr.incr(4, gi.Direct.CW, None) == 3
        assert incr.incr(5, gi.Direct.CW, None) == 4
        assert incr.incr(6, gi.Direct.CW, None) == 5
        assert incr.incr(7, gi.Direct.CW, None) == 6
        assert incr.incr(8, gi.Direct.CW, None) == 7

        # CCW, west side
        assert incr.incr(0, gi.Direct.CCW, None) == 1
        assert incr.incr(1, gi.Direct.CCW, None) == 2
        assert incr.incr(2, gi.Direct.CCW, None) == 9
        assert incr.incr(9, gi.Direct.CCW, None) == 10
        assert incr.incr(10, gi.Direct.CCW, None) == 11
        assert incr.incr(11, gi.Direct.CCW, None) == 0

        # CCW, east side
        assert incr.incr(3, gi.Direct.CCW, None) == 4
        assert incr.incr(4, gi.Direct.CCW, None) == 5
        assert incr.incr(5, gi.Direct.CCW, None) == 6
        assert incr.incr(6, gi.Direct.CCW, None) == 7
        assert incr.incr(7, gi.Direct.CCW, None) == 8
        assert incr.incr(8, gi.Direct.CCW, None) == 3


class TestEWClearEnder:
    """The specific ender is no longer needed.
    The normal CLEAR, DEPRIVE and IMMOBILIZE will all work.
    Keeping the test anyway."""

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


class TestEWAllowable:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=gi.Goal.DEPRIVE,
                                capt_on=[4],
                                min_move=2,
                                nbr_holes=game_consts.holes,
                                rules=two_cycle.EastWestCycle.rules)

        return two_cycle.EastWestCycle(game_consts, game_info)


    @pytest.mark.parametrize(
        'board, turn, eresult',
        [([4] * 8,  False, [F, F, T, T, T, T, F, F]),
         ([4] * 8,  True, [T, T, F, F, F, F, T, T]),
         ([1, 2, 3, 0, 0, 1, 2, 3], False, [F, F, T, F, F, F, F, F]),
         ([1, 2, 3, 0, 0, 1, 2, 3], True,  [F, T, F, F, F, F, T, T]),
        ])
    def test_allowables(self, game, board, turn, eresult):

        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult


class TestDisallowEndless:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=gi.Goal.CLEAR,
                                mlaps=gi.LapSower.LAPPER,
                                crosscapt=True,
                                nbr_holes=game_consts.holes,
                                rules=two_cycle.EastWestCycle.rules)

        return two_cycle.EastWestCycle(game_consts, game_info)


    @pytest.mark.parametrize('value', [False, True])
    def test_dlg_disallow_endless(self, game, value, mocker):

        dallow = mocker.patch.object(allowables, 'deco_allowable')
        rep_deco = mocker.patch.object(game.deco, 'replace_deco')

        game.disallow_endless(value)

        dallow.assert_called_once_with(game, no_endless=value)
        rep_deco.assert_called_once()


    def test_disallow_endless(self, game):

        # assert not man_config.CONFIG.get_bool('no_endless'), \
        #     "Test Cond Error: no_endless is set"

        assert 'NoEndlessSows' not in str(game.deco.allow)

        game.disallow_endless(True)
        assert 'NoEndlessSows' in str(game.deco.allow)



class TestEWRules:

    def test_we_rules(self):

        # confirm must share raises an error
        with pytest.raises(gi.GameInfoError):
            gi.GameInfo(goal=gi.Goal.MAX_SEEDS,
                        stores=True,
                        crosscapt=True,
                        nbr_holes=4,
                        mustshare=True,
                        rules=two_cycle.EastWestCycle.rules)

        # build the game info w/o error checking
        no_err_info = gi.GameInfo(goal=gi.Goal.MAX_SEEDS,
                                  stores=True,
                                  crosscapt=True,
                                  nbr_holes=4,
                                  mustshare=True,
                                  rules=lambda ginfo, holes: True)

        # run the error checking but skip the mustshare rule
        #  no error should be reported
        two_cycle.EastWestCycle.rules(no_err_info, 4, {'ns2_no_mshare'})
