# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 00:53:49 2023

@author: Ann

Unit test for incrementer.py

"""

# %% imports

import sys

import pytest
pytestmark = pytest.mark.unittest

sys.path.extend(['src'])

import game_interface as gi
from game_interface import GameFlags
from game_interface import Direct
import game_constants as gc
import incrementer as incr
from incrementer import NOSKIPSTART
import mancala
import utils


# %%

TEST_COVERS = ['src\\incrementer.py']


# %% consts

HOLES = 3

T = True
F = False


# %%

class TestIncr:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=HOLES)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags(),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def base_incr(self, game):
        object.__setattr__(game.info.flags, 'skip_start', False)
        object.__setattr__(game.info.flags, 'blocks', False)
        return incr.deco_incrementer(game)

    @pytest.fixture
    def start_incr(self, game):
        object.__setattr__(game.info.flags, 'skip_start', True)
        object.__setattr__(game.info.flags, 'blocks', False)
        return incr.deco_incrementer(game)

    @pytest.fixture
    def block_incr(self, game):
        object.__setattr__(game.info.flags, 'skip_start', False)
        object.__setattr__(game.info.flags, 'blocks', True)

        return incr.deco_incrementer(game)

    @pytest.fixture
    def sb_incr(self, game):
        object.__setattr__(game.info.flags, 'skip_start', True)
        object.__setattr__(game.info.flags, 'blocks', True)
        return incr.deco_incrementer(game)


    def test_deco_base(self, base_incr):
        assert isinstance(base_incr, incr.Increment)


    @pytest.mark.parametrize('loc, expected',
                             [(0, 1), (2, 3), (5, 0)])
    def test_base_ccw(self, base_incr, loc, expected):
        assert base_incr.incr(loc, Direct.CCW, None) == expected


    @pytest.mark.parametrize('loc, expected',
                             [(0, 5), (2, 1), (5, 4)])
    def test_base_cw(self, base_incr, loc, expected):
        assert base_incr.incr(loc, Direct.CW, None) == expected


    @pytest.mark.parametrize('loc, start, expected',
                             [(0, 1, 2), (0, 3, 1), (4, 5, 0),
                              (5, 0, 1), (0, 0, 1),
                              (5, NOSKIPSTART, 0),
                              (0, NOSKIPSTART, 1)])
    def test_start_ccw(self, start_incr, loc, start, expected):
        assert start_incr.incr(loc, Direct.CCW, start) == expected


    @pytest.mark.parametrize('loc, start, expected',
                             [(0, 5, 4), (0, 3, 5), (1, 0, 5), (2, 2, 1)])
    def test_start_cw(self, start_incr, loc, start, expected):
        assert start_incr.incr(loc, Direct.CW, start) == expected


    @pytest.mark.parametrize('loc, blocks, expected',
                             [(1, [2], 3),
                              (4, [5], 0),
                              (5, [0], 1),
                              (3, [0, 1, 3, 4], 5),
                              (3, [0, 1, 4, 5], 2)])
    def test_block_ccw(self, block_incr, game, loc, blocks, expected):
        game.blocked = [False] * (HOLES * 2)
        for bloc in blocks:
            game.blocked[bloc] = True

        assert block_incr.incr(loc, Direct.CCW, None) == expected

    @pytest.mark.parametrize('loc, blocks, expected',
                             [(1, [0], 5),
                              (0, [5], 4),
                              (2, [0], 1),
                              (5, [0, 1, 3, 4], 2),
                              (2, [0, 1, 4, 5], 3)])
    def test_block_cw(self, block_incr, game, loc, blocks, expected):

        game.blocked = [False] * (HOLES * 2)
        for bloc in blocks:
            game.blocked[bloc] = True

        assert block_incr.incr(loc, Direct.CW, None) == expected


    @pytest.mark.parametrize('loc, blocks, start, expected',
                             [(5, [0, 1], 2, 3),
                              (5, [1, 2], 0, 3),
                              (5, [0, 2], 1, 3),
                              (4, [5, 0], 1, 2),
                              (4, [0, 1], 5, 2),
                              (4, [5, 1], 0, 2)])
    def test_sb_ccw(self, sb_incr, game, loc, blocks, start, expected):

        game.blocked = [False] * (HOLES * 2)
        for bloc in blocks:
            game.blocked[bloc] = True

        assert sb_incr.incr(loc, Direct.CCW, start) == expected


    @pytest.mark.parametrize('loc, blocks, start, expected',
                             [(3, [0, 1], 2, 5),
                              (3, [1, 2], 0, 5),
                              (3, [0, 2], 1, 5),
                              (2, [5, 0], 1, 4),
                              (2, [0, 1], 5, 4),
                              (2, [5, 1], 0, 4)])
    def test_sb_cw(self, sb_incr, game, loc, blocks, start, expected):

        game.blocked = [False] * (HOLES * 2)
        for bloc in blocks:
            game.blocked[bloc] = True

        assert sb_incr.incr(loc, Direct.CW, start) == expected


    def test_blk_start_blk(self):
        """Test the incrementer inc'ing past a start hole
        surrounded by blocked holes."""

        game_consts = gc.GameConsts(nbr_start=4, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CW,
                                                skip_start=True,
                                                blocks=True,
                                                rounds=True),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.board =   utils.build_board([8, 7, 6, 5],
                                         [4, 3, 2, 1])
        game.blocked = utils.build_board([T, T, F, F],
                                         [F, T, F, F])

        assert game.deco.incr.incr(2, Direct.CW, start=0) == 5
