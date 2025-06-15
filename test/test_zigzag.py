# -*- coding: utf-8 -*-
"""Test the zigzag game class.

Created on Fri Jun 13 06:58:37 2025
@author: Ann
"""


# %% imports

import pytest
pytestmark = pytest.mark.unittest

from context import game_constants as gconsts
from context import game_info as gi
from context import zigzag


# %% constants

TEST_COVERS = ['src\\zigzag.py']


T = True
F = False
N = None


# %% tests

class TestZigZag:
    """Test for ZigZag."""

    CASES = [
        (4, 4, 0, False, 3, [0, 4, 5, 5, 5, 4, 5, 4]),
        (4, 4, 1, False, 2, [4, 0, 5, 5, 5, 5, 4, 4]),
        (4, 4, 2, False, 1, [5, 5, 0, 4, 4, 4, 5, 5]),
        (4, 4, 3, False, 0, [5, 5, 4, 0, 4, 5, 4, 5]),

        (2, 4, 0, True, 5, [2, 3, 2, 2, 2, 3, 2, 0]),
        (2, 4, 1, True, 4, [2, 2, 3, 2, 3, 2, 0, 2]),
        (2, 4, 2, True, 7, [2, 3, 2, 2, 2, 0, 2, 3]),
        (2, 4, 3, True, 6, [2, 2, 3, 2, 0, 2, 3, 2]),

        (8, 4, 0, False, 0, [1, 9, 9, 9, 9, 9, 9, 9]),

        (3, 5, 0, False, 6, [0, 3, 4, 3, 3, 3, 4, 3, 4, 3]),
        (3, 5, 1, False, 5, [3, 0, 3, 4, 3, 4, 3, 4, 3, 3]),
        (3, 5, 3, False, 9, [3, 4, 3, 0, 3, 3, 3, 4, 3, 4]),
        (3, 5, 4, False, 8, [3, 3, 4, 3, 0, 3, 4, 3, 4, 3]),

        (3, 5, 0, True, 3, [3, 4, 3, 4, 3, 3, 3, 4, 3, 0]),
        (3, 5, 1, True, 4, [3, 3, 4, 3, 4, 3, 4, 3, 0, 3]),
        (3, 5, 3, True, 0, [4, 3, 4, 3, 3, 3, 0, 3, 4, 3]),
        (3, 5, 4, True, 1, [3, 4, 3, 4, 3, 0, 3, 4, 3, 3]),

        ]

    @pytest.mark.parametrize('seeds, holes, pos, turn, eloc, eboard',
                             CASES)
    def test_via_sow(self, seeds, holes, pos, turn, eloc, eboard):
        """exercise get_dir and incr deco by doing a sow operation"""

        udir = [holes // 2] if holes % 2 else []

        game_consts = gconsts.GameConsts(nbr_start=seeds, holes=holes)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                sow_direct=gi.Direct.TOCENTER,
                                udir_holes=udir,
                                nbr_holes=game_consts.holes,
                                rules=zigzag.ZigZag.rules)

        game = zigzag.ZigZag(game_consts, game_info)

        assert 'ZigZagGetDir' in str(game.deco.get_dir)
        assert 'ZigZagIncr' in str(game.deco.incr)

        game.turn = turn

        move = gi.MoveTpl(pos, gi.Direct.CCW) if udir else pos
        mdata = game.do_sow(move)

        assert mdata.capt_loc == eloc
        assert game.board == eboard


    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(stores=True,
                                mlaps=gi.LapSower.LAPPER,
                                sow_direct=gi.Direct.TOCENTER,
                                crosscapt=True,
                                nbr_holes=game_consts.holes,
                                rules=zigzag.ZigZag.rules)

        return zigzag.ZigZag(game_consts, game_info)


    def test_allow_deco_const(self, game):
        """Test the presence of dont undo and the operation of
        disallow_endless wrapper."""

        astr = str(game.deco.allow)
        assert 'zigzag.DontUndoMoveOne' in astr
        assert 'NoEndlessSows' not in astr

        game.disallow_endless(True)

        astr = str(game.deco.allow)
        assert 'zigzag.DontUndoMoveOne' in astr
        assert 'NoEndlessSows' in astr


    def test_odd_board_size(self):
        """DontUndoMoveOne is not included in games that use udir,
        udir is required for games with an odd # holes per side"""

        game_consts = gconsts.GameConsts(nbr_start=3, holes=5)
        game_info = gi.GameInfo(stores=True,
                                mlaps=gi.LapSower.LAPPER,
                                sow_direct=gi.Direct.TOCENTER,
                                udir_holes=[2],
                                crosscapt=True,
                                nbr_holes=game_consts.holes,
                                rules=zigzag.ZigZag.rules)

        game = zigzag.ZigZag(game_consts, game_info)
        astr = str(game.deco.allow)
        assert 'DontUndoMoveOne' not in astr


    ACASES = [
        # first hole is empty from mlap sowing
        ([3, 3, 3, 3, 3, 3, 3, 3], F, 1, [F, T, T, T]),

        # don't allow undo of in 3
        ([4, 1, 0, 5, 1, 0, 0, 2], F, 1, [T, F, F, T]),

        # move of 1 that does a capture so single can be moved back
        ([4, 1, 5, 0, 1, 0, 0, 2], F, 1, [T, F, T, T]),

        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('board, turn, pos, eresult', ACASES)
    def test_allow_results(self, game, board, turn, pos, eresult):
        """Use move for setup so that mdata is completely filled."""

        # print(game.deco.allow)
        game.turn = turn
        game.board = board
        game.store = [game.cts.total_seeds - sum(game.board), 0]

        game.move(pos)
        # print(game.mdata)

        assert game.deco.allow.get_allowable_holes() == eresult
