# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 00:53:49 2023

@author: Ann

Unit test for incrementer.py

"""

# %% imports

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_info as gi
from context import game_constants as gconsts
from context import incrementer as incr
from context import mancala

from game_info import Direct
from incrementer import NOSKIPSTART


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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)

        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def base_incr(self, game):
        object.__setattr__(game.info, 'skip_start', False)
        object.__setattr__(game.info, 'blocks', False)
        return incr.deco_incrementer(game)

    @pytest.fixture
    def start_incr(self, game):
        object.__setattr__(game.info, 'skip_start', True)
        object.__setattr__(game.info, 'blocks', False)
        return incr.deco_incrementer(game)

    @pytest.fixture
    def block_incr(self, game):
        object.__setattr__(game.info, 'skip_start', False)
        object.__setattr__(game.info, 'blocks', True)

        return incr.deco_incrementer(game)

    @pytest.fixture
    def sb_incr(self, game):
        object.__setattr__(game.info, 'skip_start', True)
        object.__setattr__(game.info, 'blocks', True)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)

        game_info = gi.GameInfo(name='my name',
                                capt_on=[2],
                                sow_direct=Direct.CW,
                                skip_start=True,
                                blocks=True,
                                rounds=gi.Rounds.NO_MOVES,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.board =   utils.build_board([8, 7, 6, 5],
                                         [4, 3, 2, 1])
        game.blocked = utils.build_board([T, T, F, F],
                                         [F, T, F, F])

        assert game.deco.incr.incr(2, Direct.CW, start=0) == 5
