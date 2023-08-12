# -*- coding: utf-8 -*-
"""Test the allowables.py file.

Created on Sat Jul 15 14:25:17 2023
@author: Ann
"""


# %%

import sys

import pytest

sys.path.extend(['src'])

import allowables
import game_constants as gc
import game_interface as gi
from game_interface import GameFlags
from game_interface import GrandSlam
import mancala
import utils

# %%   constants

HOLES = 3

FALSES = [False] * (HOLES * 2)
NONES = [None] * (HOLES * 2)

T = True
F = False
N = None


# %%

class TestAllowables:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags())

        game = mancala.Mancala(game_consts, game_info)
        return game


    @pytest.mark.parametrize(
        'turn, board, blocked, child, mustshare, min_move, eresult',
        [(True,  utils.build_board([2, 2, 2], [0, 0, 0]),   # 0
          FALSES, NONES, False, 2, [T, T, T]),
         (True,  utils.build_board([1, 2, 3], [0, 0, 0]),   # 1
          FALSES, NONES, False, 2, [F, T, T]),
         (False, utils.build_board([0, 0, 0], [1, 1, 1]),   # 2
          FALSES, NONES, False, 1,            [T, T, T]),
         (False, utils.build_board([0, 0, 0], [1, 2, 3]),   # 3
           FALSES, NONES, False, 2,           [F, T, T]),

         (True, utils.build_board([2, 2, 0], [1, 0, 0]),    # 4
          FALSES, NONES, True, 2, [T, T, F]),
         (False, utils.build_board([1, 0, 0], [2, 2, 0]),   # 5
          FALSES, NONES, True, 2,             [T, T, F]),
         (True, utils.build_board([2, 1, 0], [0, 0, 0]),    # 6
          FALSES, NONES, True, 1, [T, F, F]),
         (False, utils.build_board([0, 0, 0], [0, 1, 1]),   # 7
          FALSES, NONES, True, 1,             [F, F, T]),

         (True,                                             # 8
          utils.build_board([2, 2, 0], [1, 0, 0]),
          utils.build_board([T, F, T], [T, F, T]), NONES, True, 2,
                            [F, T, F]),
         (True,                                             # 9
          utils.build_board([2, 2, 2], [1, 0, 0]),
          utils.build_board([T, F, F], [T, F, T]),
          utils.build_board([N, T, N], [N, F, T]), True, 2,
                            [F, F, T]),
         (True,                                             # 10
          utils.build_board([2, 2, 0], [1, 0, 0]),
          utils.build_board([F, T, F], [T, F, T]),
          utils.build_board([N, T, N], [N, F, T]), True, 2,
                            [T, F, F]),
        ])
    def test_allowables(self, game, turn, board, blocked, child,
                        mustshare, min_move, eresult):

        game.turn = turn
        game.board = board
        game.blocked = blocked
        game.child = child
        object.__setattr__(game.info, 'min_move', min_move)
        object.__setattr__(game.info.flags, 'mustshare', mustshare)

        allow = allowables.deco_allowable(game)
        assert allow.get_allowable_holes() == eresult


    @pytest.mark.parametrize(
        'turn, board, blocked, child, mustshare, min_move, eresult',
        [(True,  utils.build_board([2, 2, 2], [0, 0, 0]),   # 0
          FALSES, NONES, False, 2, [T, T, T]),
         (True,  utils.build_board([1, 2, 3], [0, 0, 0]),   # 1
          FALSES, NONES, False, 2, [F, T, T]),
         (False, utils.build_board([0, 0, 0], [1, 1, 1]),   # 2
          FALSES, NONES, False, 1,            [T, T, T]),
         (False, utils.build_board([0, 0, 0], [1, 2, 3]),   # 3
           FALSES, NONES, False, 2,           [F, T, T]),

         (True, utils.build_board([2, 2, 0], [1, 0, 0]),    # 4  diff above
          FALSES, NONES, True, 2, [T, F, F]),
         (False, utils.build_board([1, 0, 0], [2, 2, 0]),   # 5
          FALSES, NONES, True, 2,             [T, T, F]),
         (True, utils.build_board([2, 1, 0], [0, 0, 0]),    # 6
          FALSES, NONES, True, 1, [T, F, F]),
         (False, utils.build_board([0, 0, 0], [0, 1, 1]),   # 7
          FALSES, NONES, True, 1,             [F, F, T]),

         (True,                                             # 8 diff above
          utils.build_board([2, 2, 0], [1, 0, 0]),
          utils.build_board([T, F, T], [T, F, T]), NONES, True, 2,
                            [F, F, F]),
         (True,                                             # 9
          utils.build_board([2, 2, 2], [1, 0, 0]),
          utils.build_board([T, F, F], [T, F, T]),
          utils.build_board([N, T, N], [N, F, T]), True, 2,
                            [F, F, T]),
         (True,                                             # 10
          utils.build_board([2, 2, 0], [1, 0, 0]),
          utils.build_board([F, T, F], [T, F, T]),
          utils.build_board([N, T, N], [N, F, T]), True, 2,
                            [T, F, F]),
        ])
    def test_nograndslam(self, game, turn, board, blocked, child,
                        mustshare, min_move, eresult):

        game.turn = turn
        game.board = board
        game.blocked = blocked
        game.child = child
        object.__setattr__(game.info, 'min_move', min_move)
        object.__setattr__(game.info.flags, 'mustshare', mustshare)
        object.__setattr__(game.info.flags, 'grandslam',
                           GrandSlam.NOT_LEGAL)

        allow = allowables.deco_allowable(game)
        assert allow.get_allowable_holes() == eresult
