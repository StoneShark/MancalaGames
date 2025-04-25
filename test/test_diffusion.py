# -*- coding: utf-8 -*-
"""Test the diffusion game class.

Created on Mon Nov  4 09:30:32 2024
@author: Ann"""

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import end_move_decos as emd
from context import game_constants as gconsts
from context import game_interface as gi
from context import diffusion
from context import mancala
from context import move_data
from context import two_cycle

import utils

# %%

TEST_COVERS = ['src\\diffusion.py']

# %% constants

T = True
F = False
N = None


# %%

class TestDiffusion:

    @pytest.fixture
    def diff(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=gi.Goal.CLEAR,
                                no_sides=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=diffusion.Diffusion.rules)

        return diffusion.Diffusion(game_consts, game_info)


    @pytest.fixture
    def diff_v2(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=gi.Goal.CLEAR,
                                no_sides=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=diffusion.DiffusionV2.rules)

        return diffusion.DiffusionV2(game_consts, game_info)


    def test_deco_overrides(self, diff):

        assert isinstance(diff.deco.sower, diffusion.DiffusionSower)
        assert isinstance(diff.deco.quitter, emd.QuitToTie)


    def test_deco_v2_overrides(self, diff_v2):

        assert isinstance(diff_v2.deco.sower, diffusion.DiffusionSower)
        assert isinstance(diff_v2.deco.quitter, emd.QuitToTie)


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
    def test_end_game(self, diff, turn, board, econd, ewinner):
        diff.board = board
        diff.turn = turn

        mdata = utils.make_ender_mdata(diff, False, False)
        diff.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        assert mdata.winner == ewinner


    # these boards do not need to be valid game board
    # i.e. too few/many seeds is ok
    #  eooplay: is new seeds that are out of play

    SOW_CASES = [
        [0, 0, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([0, 4, 4, 4],
                           [5, 5, 4, 4]), 2],

        [0, 1, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([5, 0, 4, 4],
                           [5, 5, 5, 4]), 0],

        [0, 2, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([4, 5, 0, 4],
                           [4, 5, 5, 5]), 0],

        [0, 3, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([4, 4, 5, 0],
                           [4, 4, 5, 5]), 1],

        [1, 0, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([5, 5, 4, 4],
                           [0, 5, 4, 4]), 1],

        [1, 1, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([5, 5, 5, 4],
                           [4, 0, 5, 4]), 0],

        [1, 2, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([4, 5, 5, 5],
                           [4, 4, 0, 5]), 0],

        [1, 3, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 4]),
         utils.build_board([4, 4, 5, 5],
                           [4, 4, 4, 0]), 2],

        #  8: only one seed to sow in store
        [1, 3, utils.build_board([4, 4, 4, 4],
                                 [4, 4, 4, 1]),
         utils.build_board([4, 4, 4, 4],
                           [4, 4, 4, 0]), 1],

        # 9: mix of divert and sow
        [1, 2, utils.build_board([5, 5, 5, 4],
                                 [4, 0, 5, 4]),
         utils.build_board([5, 5, 5, 5],
                           [4, 1, 0, 5]), 2],

        # 10: mix of divert, store and sow
        [1, 3, utils.build_board([4, 4, 4, 5],
                                 [4, 4, 4, 5]),
         utils.build_board([4, 4, 5, 5],
                           [4, 4, 5, 0]), 3],
    ]

    # @pytest.mark.usefixtures('logger')
    @pytest.mark.parametrize('row, pos, board, eboard, eooplay',
                             SOW_CASES,
                             ids=[f"case_{i}" for i in range(len(SOW_CASES))])
    def test_base_sower(self, diff,
                        row, pos, board, eboard, eooplay):

        diff.board = board
        # print(diff)
        move = gi.MoveTpl(row, pos, None)

        mdata = move_data.MoveData(diff, move)
        mdata.sow_loc, mdata.seeds = diff.deco.drawer.draw(move)
        diff.deco.sower.sow_seeds(mdata)

        # print(diff)

        assert diff.board == eboard
        assert sum(diff.store) == eooplay


    def test_win_message_v1(self, diff):

        diff.mdata = utils.make_win_mdata(diff, gi.WinCond.WIN, True)
        _, message = diff.win_message(gi.WinCond.WIN)
        assert 'Left' in message

        diff.mdata = utils.make_win_mdata(diff, gi.WinCond.WIN, False)
        _, message = diff.win_message(gi.WinCond.WIN)
        assert 'Right' in message

    def test_win_message_v2(self, diff_v2):

        diff_v2.mdata = utils.make_win_mdata(diff_v2, gi.WinCond.WIN, True)
        _, message = diff_v2.win_message(gi.WinCond.WIN)
        assert 'Top' in message

        diff_v2.mdata = utils.make_win_mdata(diff_v2, gi.WinCond.WIN, False)
        _, message = diff_v2.win_message(gi.WinCond.WIN)
        assert 'Bottom' in message
