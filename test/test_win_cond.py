# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 19:21:23 2023
@author: Ann
"""

# %% imports

import pytest
pytestmark = pytest.mark.integtest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import Direct
from game_interface import WinCond


# %%

"""
Not need for coverage but I think this is the only place
test_pass is explicitly tested.

"""

class TestPassWConds:

    # also a few calls to test_pass

    @pytest.fixture
    def pass_game(self):
        game_consts=gc.GameConsts(nbr_start=2, holes=3)
        game_info=gi.GameInfo(nbr_holes=game_consts.holes,
                                sow_direct=Direct.CCW,
                                mustpass=True,
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_nopass_win(self, pass_game):
        # true's turn ended, false has moves
        pass_game.board=utils.build_board([0, 2, 1],
                                            [0, 2, 0])
        pass_game.store=[3, 4]
        pass_game.turn=True

        assert not pass_game.win_conditions()
        assert pass_game.turn
        assert pass_game.board == utils.build_board([0, 2, 1],
                                                    [0, 2, 0])
        assert pass_game.store == [3, 4]

        pass_game.turn=False    # move does this, after win_cond

        assert not pass_game.test_pass()
        assert not pass_game.turn

    def test_t_pass_win(self, pass_game):
        # true's turn ended, false has no moves
        pass_game.board=utils.build_board([2, 2, 1],
                                            [0, 0, 0])
        pass_game.store=[3, 4]
        pass_game.turn=True

        assert not pass_game.win_conditions()
        assert pass_game.turn
        assert pass_game.board == utils.build_board([2, 2, 1],
                                                    [0, 0, 0])
        assert pass_game.store == [3, 4]

        pass_game.turn=False    # move does this, after win_cond

        assert pass_game.test_pass()
        assert pass_game.turn

    def test_f_pass_win2(self, pass_game):
        # false's turn ended, true has no moves
        pass_game.board=utils.build_board([0, 0, 0],
                                            [2, 2, 1])
        pass_game.store=[3, 4]
        pass_game.turn=False

        assert not pass_game.win_conditions()
        assert not pass_game.turn
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [2, 2, 1])
        assert pass_game.store == [3, 4]

        assert pass_game.move(gi.PASS_TOKEN) is None
        assert pass_game.turn

    def test_t_gover_win(self, pass_game):
        pass_game.board=utils.build_board([0, 0, 0],
                                            [0, 0, 0])
        pass_game.store=[4, 8]
        pass_game.turn=True

        assert pass_game.win_conditions() == WinCond.WIN
        assert pass_game.turn
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [0, 0, 0])
        assert pass_game.store == [4, 8]

    def test_f_gover_win(self, pass_game):
        pass_game.board=utils.build_board([0, 0, 0],
                                            [0, 0, 0])
        pass_game.store=[4, 8]
        pass_game.turn=False

        assert pass_game.win_conditions() == WinCond.WIN
        assert pass_game.turn
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [0, 0, 0])
        assert pass_game.store == [4, 8]
