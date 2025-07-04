# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 19:21:23 2023
@author: Ann
"""

# %% imports

import pytest
pytestmark = pytest.mark.integtest

import utils

from context import game_constants as gconsts
from context import game_info as gi
from context import mancala

from game_info import Direct
from game_info import WinCond


# %%

"""
Not need for coverage but I think this is the only place
test_pass is explicitly tested.

"""

class TestPassWConds:

    # also a few calls to test_pass

    @pytest.fixture
    def pass_game(self):
        game_consts=gconsts.GameConsts(nbr_start=2, holes=3)
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

        mdata = utils.make_ender_mdata(pass_game, False, False)
        pass_game.win_conditions(mdata)
        assert not mdata.win_cond
        assert mdata.winner is None
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

        mdata = utils.make_ender_mdata(pass_game, False, False)
        pass_game.win_conditions(mdata)
        assert not mdata.win_cond
        assert mdata.winner is None
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

        mdata = utils.make_ender_mdata(pass_game, False, False)
        pass_game.win_conditions(mdata)
        assert not mdata.win_cond
        assert mdata.winner is None
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

        mdata = utils.make_ender_mdata(pass_game, False, False)
        pass_game.win_conditions(mdata)
        assert mdata.win_cond == WinCond.WIN
        assert mdata.winner
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [0, 0, 0])
        assert pass_game.store == [4, 8]

    def test_f_gover_win(self, pass_game):
        pass_game.board=utils.build_board([0, 0, 0],
                                            [0, 0, 0])
        pass_game.store=[4, 8]
        pass_game.turn=False

        mdata = utils.make_ender_mdata(pass_game, False, False)
        pass_game.win_conditions(mdata)
        assert mdata.win_cond == WinCond.WIN
        assert mdata.winner
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [0, 0, 0])
        assert pass_game.store == [4, 8]
