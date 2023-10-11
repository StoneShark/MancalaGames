# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 16:59:31 2023

@author: Ann
"""

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import Direct


HOLES = 3

FALSES = [False] * (HOLES * 2)
NONES = [None] * (HOLES * 2)

T = True
F = False
N = None


TEST_COVERS = ['src\\get_moves.py']


class TestGetMove:

    @pytest.mark.parametrize(
        'turn, board, blocked, child, mustshare, mustpass, min_move, eresult',
        [
            (True,  utils.build_board([2, 2, 2], [0, 0, 0]),   # 0
              FALSES, NONES, False, False, 2, [0, 1, 2]),
            (True,  utils.build_board([1, 2, 3], [0, 0, 0]),   # 1
              FALSES, NONES, False, False, 2, [1, 2]),
            (True, utils.build_board([3, 1, 0], [0, 0, 0]),    # 2
              FALSES, NONES, True, False, 1, [0]),
            (True, utils.build_board([2, 3, 2], [0, 0, 0]),    # 3
              FALSES, NONES, True, False, 2, [0, 1]),
            (True,  utils.build_board([2, 2, 2], [0, 0, 0]),   # 4
              FALSES, NONES, False, True, 2, [0, 1, 2]),
            (True, utils.build_board([3, 1, 0], [0, 0, 0]),    # 5
              FALSES, NONES, True, True, 1, [0]),

            (False,  utils.build_board([1, 2, 3], [0, 0, 0]),   # 6
              FALSES, NONES, False, True, 2, [gi.PASS_TOKEN]),

            (True,                                             # 7
             utils.build_board([2, 2, 0], [1, 0, 0]),
             utils.build_board([T, F, T], [T, F, T]), NONES,
             True, False, 2, [1]),
            (True,                                             # 8
             utils.build_board([2, 2, 2], [1, 0, 0]),
             utils.build_board([T, F, F], [T, F, T]),
             utils.build_board([N, T, N], [N, F, T]),
             True, True, 2, [2]),
        ],
        ids=[f'case_{cnt}' for cnt in range(9)])
    def test_basic_moves(self, turn, board, blocked, child,
                    mustshare, mustpass, min_move, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                min_move=min_move,
                                mustshare=mustshare,
                                mustpass=mustpass,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board
        game.blocked = blocked
        game.child = child
        assert game.deco.moves.get_moves() == eresult


    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.parametrize(
        'turn, board, udir, mustpass, eresult',
        [
            (True, utils.build_board([2, 2, 2], [1, 0, 0]),   # 0
             [1], False,
             [(0, None), (1, Direct.CCW), (1, Direct.CW), (2, None)]),

            (False, utils.build_board([2, 2, 2], [1, 0, 0]),   # 1
             [0], False,
             [(0, Direct.CCW), (0, Direct.CW)]),
            (True, utils.build_board([2, 2, 2], [1, 0, 0]),   # 2
             [0], False,
             [(0, None), (1, None), (2, Direct.CCW), (2, Direct.CW)]),

            (True, utils.build_board([2, 0, 2], [1, 0, 0]),  # 3
             [0], False,
             [(2, Direct.CCW), (2, Direct.CW), (0, None)]),
            (True, utils.build_board([2, 2, 0], [1, 0, 0]),   # 4
             [0], False,
             [(0, None), (1, None)]),

            (False, utils.build_board([2, 0, 2], [0, 0, 0]),   # 5
             [0], True,
             [(gi.PASS_TOKEN, None)]),
            (True, utils.build_board([2, 0, 2], [1, 0, 0]),    # 6
             [0], True,
             [(2, Direct.CCW), (2, Direct.CW), (0, None)]),

        ],
        ids=[f'case_{cnt}' for cnt in range(7)])
    def test_udir_moves(self, turn, board, udir, mustpass, eresult):
        """
        blocked, child, mustshare, min_move are all handled by
        allowables, don't bother with further testing."""

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                mustpass=mustpass,
                                udir_holes=udir,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board
        assert set(game.deco.moves.get_moves()) == set(eresult)


class TestNoSidesMoves:

    @pytest.mark.parametrize('turn', [False, True])
    @pytest.mark.parametrize(
        'board, min_move, eresult',
        [([2, 2, 2, 0, 0, 0], 2,   # 0
          {(1, 0, None),
           (1, 1, Direct.CCW), (1, 1, Direct.CW),
           (1, 2, None)}),

         ([1, 2, 3, 0, 0, 0], 2,   # 1
          {(1, 1, Direct.CCW), (1, 1, Direct.CW),
           (1, 2, None)}),

         ([0, 0, 0, 1, 1, 1], 1,   # 2
          {(0, 0, None),
           (0, 1, Direct.CCW), (0, 1, Direct.CW),
           (0, 2, None)}),
        ])

    def test_get_moves(self, turn, board, min_move, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                no_sides=True,
                                stores=True,
                                min_move=min_move,
                                udir_holes = [1],
                                sow_direct=Direct.SPLIT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert set(game.deco.moves.get_moves()) == eresult
