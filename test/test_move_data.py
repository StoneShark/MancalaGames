# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 06:18:05 2025

@author: Ann
"""

import pytest
pytestmark = pytest.mark.unittest

from context import game_constants as gconsts
from context import game_info as gi
from context import mancala
from context import move_data


TEST_COVERS = ['src\\move_data.py']


class TestMoveData:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=lambda ginfo, holes: True)

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_construct(self, game):

        # this call is needed for copy of MoveData to work
        mdata = move_data.MoveData()
        assert not mdata.player
        assert not mdata.board
        assert not mdata.move

        mdata = move_data.MoveData(game, 5)

        assert mdata.board == tuple(game.board)
        assert mdata.player == game.turn
        assert not mdata.direct

        assert mdata.move == 5

        mstr = str(mdata)
        assert '4, 4, 4, 4' in mstr
        assert 'direct=None' in mstr


    def test_sow_loc_prop(self, game):

        mdata = move_data.MoveData(game, 5)

        # construction settings
        assert mdata.sow_loc == 0
        assert mdata._sow_loc == 0
        assert mdata.cont_sow_loc == 0

        # set sow start and initing cont_sow_loc
        mdata.sow_loc = 3

        assert mdata.sow_loc == 3
        assert mdata._sow_loc == 3
        assert mdata.cont_sow_loc == 3

        # update cont_sow_loc, sow_loc should not change
        mdata.cont_sow_loc = 1

        assert mdata.sow_loc == 3
        assert mdata._sow_loc == 3
        assert mdata.cont_sow_loc == 1


    def test_pass_move(self, game):

        mdata = move_data.MoveData.pass_move(True)
        assert not mdata.board
        assert mdata.player
        assert mdata.move == 'PASS'


    def test_make_move(self, game):

        mdata = move_data.MoveData.make_move(True, 12)
        assert not mdata.board
        assert mdata.player
        assert mdata.move == 12


    def test_state(self, game):

        mdata = move_data.MoveData(game, 22)

        mstate = mdata.state
        assert isinstance(mstate, tuple)
        assert len(mstate) == 19
        assert mstate[2] == 22

        mdata.state = tuple(idx for idx in range(19))
        assert mdata.player == 0
        assert mdata.board == 1
        assert mdata.move == 2
        assert mdata.direct == 3
        assert mdata.seeds == 4
        assert mdata._sow_loc == 5
        assert mdata.cont_sow_loc == 6
        assert mdata.lap_nbr == 7
        assert mdata.capt_loc == 8
        assert mdata.capt_next == 9
        assert mdata.capt_changed == 10
        assert mdata.captured == 11
        assert mdata.repeat_turn == 12
        assert mdata.end_msg == 13
        assert mdata.fmsg == 14
        assert mdata.ended == 15
        assert mdata.win_cond == 16
        assert mdata.winner == 17
        assert mdata.user_end == 18
