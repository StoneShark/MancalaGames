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


# %%

TEST_COVERS = ['src\\zigzag.py']

# %% constants

T = True
F = False
N = None

CW = gi.Direct.CW
CCW = gi.Direct.CCW


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
