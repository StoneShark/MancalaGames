# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 08:47:26 2023

@author: Ann
"""

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_interface as gi
from context import game_constants as gconsts
from context import mancala

from game_interface import Direct


# %%

TEST_COVERS = ['src\\drawer.py']


# %% constants

HOLES = 3


# %% tests


class TestSowStarter:

    @pytest.mark.parametrize('sow_start, unlock',
                              [(False, False),
                              (False, True),
                              ])
    @pytest.mark.parametrize('pos, turn, eloc, eseeds',
                              [(0, False, 0, 7),
                              (1, False, 1, 8),
                              (2, False, 2, 9),
                              (0, True, 5-0, 4),
                              (1, True, 5-1, 5),
                              (2, True, 5-2, 6)]
                        )
    def test_no_start_loc(self, sow_start, unlock, pos, turn, eloc, eseeds):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(capt_on = [2],
                                sow_start = sow_start,
                                moveunlock = unlock,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 5, 6],
                                       [7, 8, 9])
        game.turn = turn

        sower = game.deco.drawer
        assert sower.draw(pos) == (eloc, eseeds)
        assert game.board[eloc] == 0
        assert game.unlocked[eloc]


    @pytest.mark.parametrize('sow_start, unlock',
                              [(True, False),
                              (True, True),
                              ])
    @pytest.mark.parametrize('pos, turn, eloc, eseeds',
                              [(0, False, 0, 7-1),
                              (1, False, 1, 8-1),
                              (2, False, 2, 9-1),
                              (0, True, 5-0, 4-1),
                              (1, True, 5-1, 5-1),
                              (2, True, 5-2, 6-1)]
                        )
    def test_start_loc(self, sow_start, unlock, pos, turn, eloc, eseeds):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(min_move = 2,
                                capt_on = [2],
                                sow_start = sow_start,
                                moveunlock = unlock,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 5, 6],
                                       [7, 8, 9])
        game.turn = turn

        sower = game.deco.drawer
        assert sower.draw(pos) == (eloc, eseeds)
        assert game.board[eloc] == 1
        assert game.unlocked[eloc]


    @pytest.mark.parametrize('sow_start, unlock',
                              [(False, False),
                              (False, True),
                              ])
    @pytest.mark.parametrize('pos, turn, eloc, eseeds',
                              [(0, False, 0, 7),
                              (1, False, 1, 8),
                              (2, False, 2, 9),
                              (0, True, 5-0, 4),
                              (1, True, 5-1, 5),
                              (2, True, 5-2, 6)]
                        )
    def test_udir(self, sow_start, unlock, pos, turn, eloc, eseeds):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(capt_on = [2],
                                udir_holes=[1],
                                sow_direct=Direct.SPLIT,
                                sow_start = sow_start,
                                moveunlock = unlock,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 5, 6],
                                       [7, 8, 9])
        game.turn = turn

        sower = game.deco.drawer

        # draw doesn't care what the direction is
        assert sower.draw((pos, None)) == (eloc, eseeds)
        assert game.board[eloc] == 0
        assert game.unlocked[eloc]



    @pytest.mark.parametrize('sow_start, unlock',
                              [(False, False),
                              (False, True),
                              ])
    @pytest.mark.parametrize('pos, turn, eloc, eseeds',
                              [(0, False, 0, 7),
                              (1, False, 1, 8),
                              (2, False, 2, 9),
                              (0, True, 5-0, 4),
                              (1, True, 5-1, 5),
                              (2, True, 5-2, 6)]
                        )
    def test_no_sides(self, sow_start, unlock, pos, turn, eloc, eseeds):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(capt_on = [2],
                                udir_holes=[1],
                                sow_direct=Direct.SPLIT,
                                no_sides=True,
                                stores=True,
                                sow_start = sow_start,
                                moveunlock = unlock,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 5, 6],
                                       [7, 8, 9])
        game.turn = turn

        sower = game.deco.drawer

        assert sower.draw((not turn, pos, None)) == (eloc, eseeds)
        assert game.board[eloc] == 0
        assert game.unlocked[eloc]


    @pytest.mark.parametrize('pos, turn, eloc, eseeds, esowed',
                              [(0, False, 0, 6, 1),
                              (1, False, 1, 1, 0),
                              (2, False, 2, 8, 1),
                              (0, True, 5-0, 1, 0),
                              (1, True, 5-1, 4, 1),
                              (2, True, 5-2, 5, 1)]
                        )
    def test_move_one(self, pos, turn, eloc, eseeds, esowed):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(capt_on = [2],
                                udir_holes=[1],
                                sow_direct=Direct.SPLIT,
                                no_sides=True,
                                stores=True,
                                sow_start = True,
                                move_one = True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([1, 5, 6],
                                       [7, 1, 9])
        game.turn = turn

        sower = game.deco.drawer

        assert sower.draw((not turn, pos, None)) == (eloc, eseeds)
        assert game.board[eloc] == esowed
