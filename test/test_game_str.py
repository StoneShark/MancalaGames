# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:49:59 2023

@author: Ann
"""

import pytest
pytestmark = pytest.mark.unittest


import utils

from context import game_constants as gconsts
from context import game_interface as gi
from context import mancala

from game_interface import ChildType
from game_interface import Direct
from game_interface import Goal



TEST_COVERS = ['src\\game_str.py']


class TestGameStr:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_basic_str(self, game):

        assert 'GameString' in str(game.deco.gstr)

        gstr = str(game)
        assert gstr == '  4  4  4  4  4  4   \n  4  4  4  4  4  4  *'

        game.board = utils.build_board([4, 3, 4, 0, 8, 0],
                                       [4, 4, 2, 0, 4, 1])
        game.store = [5, 2]
        gstr = str(game)
        assert gstr == '  4  3  4  0  8  0       2\n  4  4  2  0  4  1  *    5'


    @pytest.fixture
    def bmgame(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(mustpass=True,
                                stores=True,
                                blocks=True,
                                rounds=gi.Rounds.NO_MOVES,
                                moveunlock=True,
                                sow_direct=Direct.CCW,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

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

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                mustpass=True,
                                stores=True,
                                child_type=ChildType.NORMAL,
                                child_cvt=2,
                                sow_direct=Direct.CCW,
                                evens=True,
                                rules=mancala.Mancala.rules
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


    @pytest.fixture
    def cterr_game(self):
        """an odd game goal_param has two differnt purposes."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                mustpass=True,
                                stores=True,
                                child_type=ChildType.NORMAL,
                                child_cvt=3,
                                goal=Goal.TERRITORY,
                                goal_param=5,
                                sow_direct=Direct.CCW,
                                evens=True,
                                rules=mancala.Mancala.rules
                                )

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_child_terr_str(self, cterr_game):

        gstr = str(cterr_game)
        assert gstr == '  2 ↑   2 ↑   2 ↑    \n  2 ↓   2 ↓   2 ↓   *'

        cterr_game.board = utils.build_board([1, 3, 5],
                                             [8, 6, 4])
        cterr_game.child = utils.build_board([False, None, True],
                                             [None,  True, False])
        cterr_game.store = [0, 2]
        gstr = str(cterr_game)
        assert gstr == '  1˅↑   3 ↑   5˄↑        2\n  8 ↓   6˄↓   4˅↓   *'
