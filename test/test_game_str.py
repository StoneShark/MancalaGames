# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:49:59 2023

@author: Ann
"""

import sys

import pytest

sys.path.extend(['src'])

import game_constants as gc
import game_interface as gi
import mancala
import utils

from game_interface import GameFlags
from game_interface import Direct


class TestGameStr:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=6)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags())

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_basic_str(self, game):

        gstr = str(game)
        assert gstr == '  4   4   4   4   4   4   \n  4   4   4   4   4   4  *'

        game.board = utils.build_board([4, 3, 4, 0, 8, 0],
                                       [4, 4, 2, 0, 4, 1])
        game.store = [5, 2]
        gstr = str(game)
        assert gstr == '  4   3   4   0   8   0       2\n  4   4   2   0   4   1  *    5'


    @pytest.fixture
    def bmgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(mustpass=True,
                                                stores=True,
                                                blocks=True,
                                                moveunlock=True,
                                                sow_direct=Direct.CCW,
                                                evens=True)
                                )

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_blockmarker_str(self, bmgame):

        gstr = str(bmgame)
        assert gstr == '  2_  2_  2_   \n  2_  2_  2_  *'

        bmgame.board = utils.build_board([8, 8, 0],
                                         [8, 0, 0])
        bmgame.blocked = utils.build_board([False, False, False],
                                           [False, True, True])
        bmgame.unlocked = utils.build_board([False, False, True],
                                            [True, False, False])
        bmgame.store = [0, 2]
        gstr = str(bmgame)
        assert gstr == '  8_  8_  0        2\n  8   x_  x_  *'


    @pytest.fixture
    def cgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(mustpass=True,
                                                stores=True,
                                                child=True,
                                                sow_direct=Direct.CCW,
                                                evens=True)
                                )

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_child_str(self, cgame):

        gstr = str(cgame)
        assert gstr == '  2   2   2    \n  2   2   2   *'

        cgame.board = utils.build_board([1, 3, 5],
                                        [8, 6, 4])
        cgame.child = utils.build_board([False, None, True],
                                        [None,  True, False])
        cgame.store = [0, 2]
        gstr = str(cgame)
        assert gstr == '  1˅  3   5˄       2\n  8   6˄  4˅  *'
