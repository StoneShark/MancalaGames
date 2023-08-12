# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 08:47:26 2023

@author: Ann
"""

import sys

import pytest

sys.path.extend(['src'])

import game_interface as gi
from game_interface import GameFlags
import game_constants as gc
import mancala
import sow_starter
import utils

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

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                flags=GameFlags(sow_start = sow_start,
                                                moveunlock = unlock))
        game = mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 5, 6],
                                       [7, 8, 9])
        game.turn = turn

        sower = sow_starter.deco_sow_starter(game)
        assert sower.start_sow(pos) == (eloc, eseeds)
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

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                min_move = 2,
                                capt_on = [2],
                                flags=GameFlags(sow_start = sow_start,
                                                moveunlock = unlock))
        game = mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 5, 6],
                                       [7, 8, 9])
        game.turn = turn

        sower = sow_starter.deco_sow_starter(game)
        assert sower.start_sow(pos) == (eloc, eseeds)
        assert game.board[eloc] == 1
        assert game.unlocked[eloc]
