# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 09:48:59 2023
@author: Ann"""

import pytest
pytestmark = pytest.mark.unittest

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import Direct


# %%

TEST_COVERS = ['src\\get_direction.py']


class TestGetDirection:


    @pytest.mark.parametrize('holes, start, direct, exp_dir',
                             [
                              (3, 0, Direct.CW, Direct.CW),
                              (3, 2, Direct.CW, Direct.CW),
                              (3, 3, Direct.CW, Direct.CW),
                              (3, 4, Direct.CW, Direct.CW),
                              (3, 5, Direct.CW, Direct.CW),

                              (4, 0, Direct.CW, Direct.CW),
                              (4, 3, Direct.CW, Direct.CW),
                              (4, 4, Direct.CW, Direct.CW),
                              (4, 5, Direct.CW, Direct.CW),
                              (4, 7, Direct.CW, Direct.CW),

                              (3, 0, Direct.CCW, Direct.CCW),
                              (3, 2, Direct.CCW, Direct.CCW),
                              (3, 3, Direct.CCW, Direct.CCW),
                              (3, 4, Direct.CCW, Direct.CCW),
                              (3, 5, Direct.CCW, Direct.CCW),

                              (4, 0, Direct.CCW, Direct.CCW),
                              (4, 3, Direct.CCW, Direct.CCW),
                              (4, 4, Direct.CCW, Direct.CCW),
                              (4, 5, Direct.CCW, Direct.CCW),
                              (4, 7, Direct.CCW, Direct.CCW),

                              (3, 0, Direct.SPLIT, Direct.CW),
                              (3, 1, Direct.SPLIT, None),  # None stuffed below
                              (3, 2, Direct.SPLIT, Direct.CCW),
                              (3, 3, Direct.SPLIT, Direct.CW),
                              (3, 4, Direct.SPLIT, None),  # None stuffed below
                              (3, 5, Direct.SPLIT, Direct.CCW),

                              (4, 0, Direct.SPLIT, Direct.CW),
                              (4, 1, Direct.SPLIT, Direct.CW),
                              (4, 2, Direct.SPLIT, Direct.CCW),
                              (4, 3, Direct.SPLIT, Direct.CCW),
                              (4, 4, Direct.SPLIT, Direct.CW),
                              (4, 5, Direct.SPLIT, Direct.CW),
                              (4, 6, Direct.SPLIT, Direct.CCW),
                              (4, 7, Direct.SPLIT, Direct.CCW),

                              ])
    def test_common(self, holes, start, direct, exp_dir):
        """Stuff None in for udir moves, it should only be
        used if the hole is in udir_holes."""

        udir_holes = []
        if direct == Direct.SPLIT and holes == 3:
            udir_holes = [1]

        game_consts = gc.GameConsts(nbr_start=4, holes=holes)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=direct,
                                udir_holes=udir_holes,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = start
        if direct == Direct.SPLIT and holes == 3:
            move = (game_consts.loc_to_left_cnt(start), None)

        assert game.deco.get_dir.get_direction(move, start) == exp_dir


    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.parametrize('holes, start, direct, udir_holes, exp_dir',
                             [
                              (4, 0, Direct.CW, [3], Direct.CW),  # 0
                              (4, 3, Direct.CW, [3], None),
                              (4, 4, Direct.CW, [3], Direct.CW),
                              (4, 7, Direct.CW, [3], None),

                              (4, 0, Direct.CCW, [3], Direct.CCW),  # 4
                              (4, 3, Direct.CCW, [3], None),
                              (4, 4, Direct.CCW, [3], Direct.CCW),
                              (4, 7, Direct.CCW, [3], None),

                              (4, 0, Direct.SPLIT, [3], Direct.CW), # 8
                              (4, 3, Direct.SPLIT, [3], None),
                              (4, 4, Direct.SPLIT, [3], Direct.CW),
                              (4, 7, Direct.SPLIT, [3], None),

                              (3, 5, Direct.SPLIT, [0, 1, 2], None),  # 12
                              ],
                             ids= [f'case_{cnbr}' for cnbr in range(13)])
    def test_not_middle(self, holes, start, direct, udir_holes, exp_dir):

        game_consts = gc.GameConsts(nbr_start=4, holes=holes)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=direct,
                                udir_holes=udir_holes,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = (game_consts.loc_to_left_cnt(start), None)
        assert game.deco.get_dir.get_direction(move, start) == exp_dir


    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.parametrize('holes, start, direct, udir_holes, exp_dir',
                             [
                              (4, 0, Direct.CW, [3], Direct.CW),  # 0
                              (4, 3, Direct.CW, [3], None),
                              (4, 4, Direct.CW, [3], Direct.CW),
                              (4, 7, Direct.CW, [3], None),

                              (4, 0, Direct.CCW, [3], Direct.CCW),  # 4
                              (4, 3, Direct.CCW, [3], None),
                              (4, 4, Direct.CCW, [3], Direct.CCW),
                              (4, 7, Direct.CCW, [3], None),

                              (4, 0, Direct.SPLIT, [3], Direct.CW), # 8
                              (4, 3, Direct.SPLIT, [3], None),
                              (4, 4, Direct.SPLIT, [3], Direct.CW),
                              (4, 7, Direct.SPLIT, [3], None),

                              (3, 5, Direct.SPLIT, [0, 1, 2], None),  # 12
                              ],
                             ids= [f'case_{cnbr}' for cnbr in range(13)])
    def test_no_sides(self, holes, start, direct, udir_holes, exp_dir):

        game_consts = gc.GameConsts(nbr_start=4, holes=holes)
        game_info = gi.GameInfo(capt_on=[2],
                                no_sides=True,
                                stores=True,
                                sow_direct=direct,
                                udir_holes=udir_holes,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = (start < holes, game_consts.loc_to_left_cnt(start), None)
        assert game.deco.get_dir.get_direction(move, start) == exp_dir
