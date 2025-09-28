# -*- coding: utf-8 -*-
"""Unit tests for the game class share_one.ShareOne.

Created on Wed Jul  2 16:32:41 2025
@author: Ann"""


import pytest
pytestmark = pytest.mark.unittest

from context import animator
from context import game_constants as gconsts
from context import game_info as gi
from context import share_one



# %%

TEST_COVERS = ['src\\share_one.py']

# %% constants

T = True
F = False
N = None


# %%

class TestAllowables:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on=[3],
                                stores=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                nbr_holes=game_consts.holes,
                                rules=share_one.ShareOne.rules)

        game = share_one.ShareOne(game_consts, game_info)
        return game

    ACASES = [ [False, [1, 2, 2, 0, 0, 0], [N, N, N, N, N, N], [F, T, T]],
               [True,  [0, 0, 0, 1, 2, 1], [N, N, N, N, N, N], [F, T, F]],

                # can't move from children
               [False, [1, 2, 2, 0, 0, 0], [N, N, T, N, N, N], [F, T, F]],
               [True,  [0, 0, 0, 2, 2, 1], [N, N, N, F, N, N], [F, T, F]],

                # use the deco chain  (recall T eresult is reversed)
               [False, [1, 2, 2, 2, 2, 1], [N, N, T, N, N, N], [T, T, F]],
               [True,  [1, 2, 2, 2, 2, 1], [N, N, N, F, N, N], [T, T, F]],

               ]

    @pytest.mark.parametrize('turn, board, child, eresult', ACASES)
    def test_allow(self, game, turn, board, child, eresult):

        game.board = board
        game.child = child
        game.turn = turn

        assert game.get_allowable_holes() == eresult


class TestSowerAnimator:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on=[3],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=share_one.ShareOne.rules)

        game = share_one.ShareOne(game_consts, game_info)
        return game


    @pytest.mark.animator
    def test_animator_fshare(self, mocker, game):

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mocker.patch('animator.one_step')
        mocker.patch('animator.ANIMATOR.change')
        mocker.patch('animator.ANIMATOR.do_flash')
        mobj = mocker.patch('animator.ANIMATOR.do_message')

        game.turn = True
        game.board = [0, 4, 4, 0, 0, 1]
        game.store[0] = game.cts.total_seeds - sum(game.board)
        # print(game)

        # a normal sow to clear True's seeds
        game.move(0)
        assert game.board.copy() == [1, 4, 4, 0, 0, 0]
        # print(game)

        mobj.assert_called_once()

        # test the share one move
        game.move(1)
        assert game.board.copy() == [1, 3, 4, 1, 0, 0]


    def test_tshare(self, mocker, game):

        game.turn = False
        game.board = [0, 0, 1, 0, 4, 4]
        game.store[0] = game.cts.total_seeds - sum(game.board)
        # print(game)

        # a normal sow to clear False's seeds
        game.move(2)
        assert game.board == [0, 0, 0, 1, 4, 4]
        # print(game)

        # test the share one move
        game.move(1)
        assert game.board == [1, 0, 0, 1, 3, 4]
