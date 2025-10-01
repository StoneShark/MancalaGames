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
N = None


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
        assert start_incr.incr(loc, Direct.CCW, None, start) == expected


    @pytest.mark.parametrize('loc, start, expected',
                             [(0, 5, 4), (0, 3, 5), (1, 0, 5), (2, 2, 1)])
    def test_start_cw(self, start_incr, loc, start, expected):
        assert start_incr.incr(loc, Direct.CW, None, start) == expected


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

        assert sb_incr.incr(loc, Direct.CCW, None, start) == expected


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

        assert sb_incr.incr(loc, Direct.CW, None, start) == expected


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

        assert game.deco.incr.incr(2, Direct.CW, None, start=0) == 5


    def test_map_incr(self, game):

        mapi = incr.MapIncrement(game)

        assert 'cw' in str(mapi)
        assert 'ccw' in str(mapi)

        assert len(mapi.ccw_map) == game.cts.dbl_holes
        assert len(mapi.cw_map) == game.cts.dbl_holes

        assert mapi.incr(4, Direct.CW, None) == 2
        assert mapi.incr(3, Direct.CCW, None) == 5


    def test_map_cycle(self, game):

        mapi = incr.MapIncrement(game)
        mapi.build_maps_from_cycle([0, 5, 4, 1, 2, 3])

        assert mapi.ccw_map == [5, 2, 3, 0, 1, 4]
        assert mapi.cw_map == [3, 4, 1, 2, 5, 0]



    def test_map_two_cycle(self, game):

        mapi = incr.MapStoresIncr(game)
        mapi.build_maps_from_cycles([0, 4, 2], [3, 1, 5])

        #                                         -2 -1  0  1  2  3  4  5
        assert mapi.map[False][gi.Direct.CCW] ==  [N, N, 4, N, 0, N, 2, N]
        assert mapi.map[False][gi.Direct.CW] ==   [N, N, 2, N, 4, N, 0, N]

        assert mapi.map[True][gi.Direct.CCW] == [N, N, N, 5, N, 1, N, 3]
        assert mapi.map[True][gi.Direct.CW] ==  [N, N, N, 3, N, 5, N, 1]

        assert mapi.incr(gi.T_STORE, gi.Direct.CCW, False) == N
        assert mapi.incr(gi.F_STORE, gi.Direct.CCW, False) == N
        assert mapi.incr(0, gi.Direct.CCW, False) == 4
        assert mapi.incr(1, gi.Direct.CCW, False) == N
        assert mapi.incr(2, gi.Direct.CCW, False) == 0
        assert mapi.incr(3, gi.Direct.CCW, False) == N
        assert mapi.incr(4, gi.Direct.CCW, False) == 2
        assert mapi.incr(5, gi.Direct.CCW, False) == N

        assert mapi.incr(gi.T_STORE, gi.Direct.CW, False) == N
        assert mapi.incr(gi.F_STORE, gi.Direct.CW, False) == N
        assert mapi.incr(0, gi.Direct.CW, False) == 2
        assert mapi.incr(1, gi.Direct.CW, False) == N
        assert mapi.incr(2, gi.Direct.CW, False) == 4
        assert mapi.incr(3, gi.Direct.CW, False) == N
        assert mapi.incr(4, gi.Direct.CW, False) == 0
        assert mapi.incr(5, gi.Direct.CW, False) == N

        assert mapi.incr(gi.T_STORE, gi.Direct.CCW, True) == N
        assert mapi.incr(gi.F_STORE, gi.Direct.CCW, True) == N
        assert mapi.incr(0, gi.Direct.CCW, True) == N
        assert mapi.incr(1, gi.Direct.CCW, True) == 5
        assert mapi.incr(2, gi.Direct.CCW, True) == N
        assert mapi.incr(3, gi.Direct.CCW, True) == 1
        assert mapi.incr(4, gi.Direct.CCW, True) == N
        assert mapi.incr(5, gi.Direct.CCW, True) == 3

        assert mapi.incr(gi.T_STORE, gi.Direct.CW, True) == N
        assert mapi.incr(gi.F_STORE, gi.Direct.CW, True) == N
        assert mapi.incr(0, gi.Direct.CW, True) == N
        assert mapi.incr(1, gi.Direct.CW, True) == 3
        assert mapi.incr(2, gi.Direct.CW, True) == N
        assert mapi.incr(3, gi.Direct.CW, True) == 5
        assert mapi.incr(4, gi.Direct.CW, True) == N
        assert mapi.incr(5, gi.Direct.CW, True) == 1

        mstr = str(mapi)
        assert '4, None, 0' in mstr
        assert '5, None, 1' in mstr


    def test_sow_own_store(self, game):

        mapi = incr.IncOwnStores(game)

        assert mapi.incr(gi.T_STORE, gi.Direct.CCW, False) == N
        assert mapi.incr(gi.F_STORE, gi.Direct.CCW, False) == 3
        assert mapi.incr(0, gi.Direct.CCW, False) == 1
        assert mapi.incr(1, gi.Direct.CCW, False) == 2
        assert mapi.incr(2, gi.Direct.CCW, False) == gi.F_STORE
        assert mapi.incr(3, gi.Direct.CCW, False) == 4
        assert mapi.incr(4, gi.Direct.CCW, False) == 5
        assert mapi.incr(5, gi.Direct.CCW, False) == 0

        assert mapi.incr(gi.T_STORE, gi.Direct.CW, False) == N
        assert mapi.incr(gi.F_STORE, gi.Direct.CW, False) == 2
        assert mapi.incr(0, gi.Direct.CW, False) == 5
        assert mapi.incr(1, gi.Direct.CW, False) == 0
        assert mapi.incr(2, gi.Direct.CW, False) == 1
        assert mapi.incr(3, gi.Direct.CW, False) == gi.F_STORE
        assert mapi.incr(4, gi.Direct.CW, False) == 3
        assert mapi.incr(5, gi.Direct.CW, False) == 4

        assert mapi.incr(gi.T_STORE, gi.Direct.CCW, True) == 0
        assert mapi.incr(gi.F_STORE, gi.Direct.CCW, True) == N
        assert mapi.incr(0, gi.Direct.CCW, True) == 1
        assert mapi.incr(1, gi.Direct.CCW, True) == 2
        assert mapi.incr(2, gi.Direct.CCW, True) == 3
        assert mapi.incr(3, gi.Direct.CCW, True) == 4
        assert mapi.incr(4, gi.Direct.CCW, True) == 5
        assert mapi.incr(5, gi.Direct.CCW, True) == gi.T_STORE

        assert mapi.incr(gi.T_STORE, gi.Direct.CW, True) == 5
        assert mapi.incr(gi.F_STORE, gi.Direct.CW, True) == N
        assert mapi.incr(0, gi.Direct.CW, True) == gi.T_STORE
        assert mapi.incr(1, gi.Direct.CW, True) == 0
        assert mapi.incr(2, gi.Direct.CW, True) == 1
        assert mapi.incr(3, gi.Direct.CW, True) == 2
        assert mapi.incr(4, gi.Direct.CW, True) == 3
        assert mapi.incr(5, gi.Direct.CW, True) == 4


    def test_sow_both_stores(self, game):

        mapi = incr.IncBothStores(game)

        for turn in (False, True):
            assert mapi.incr(gi.T_STORE, gi.Direct.CCW, turn) == 0
            assert mapi.incr(0, gi.Direct.CCW, turn) == 1
            assert mapi.incr(1, gi.Direct.CCW, turn) == 2
            assert mapi.incr(2, gi.Direct.CCW, turn) == gi.F_STORE
            assert mapi.incr(gi.F_STORE, gi.Direct.CCW, turn) == 3
            assert mapi.incr(3, gi.Direct.CCW, turn) == 4
            assert mapi.incr(4, gi.Direct.CCW, turn) == 5
            assert mapi.incr(5, gi.Direct.CCW, turn) == gi.T_STORE

            assert mapi.incr(gi.T_STORE, gi.Direct.CW, turn) == 5
            assert mapi.incr(0, gi.Direct.CW, turn) == gi.T_STORE
            assert mapi.incr(1, gi.Direct.CW, turn) == 0
            assert mapi.incr(2, gi.Direct.CW, turn) == 1
            assert mapi.incr(gi.F_STORE, gi.Direct.CW, turn) == 2
            assert mapi.incr(3, gi.Direct.CW, turn) == gi.F_STORE
            assert mapi.incr(4, gi.Direct.CW, turn) == 3
            assert mapi.incr(5, gi.Direct.CW, turn) == 4


    def test_sow_from_stores(self, game):

        mapi = incr.IncFromStores(game)

        for turn in (False, True):
            assert mapi.incr(gi.T_STORE, gi.Direct.CCW, turn) == 0
            assert mapi.incr(gi.F_STORE, gi.Direct.CCW, turn) == 3
            assert mapi.incr(0, gi.Direct.CCW, turn) == 1
            assert mapi.incr(1, gi.Direct.CCW, turn) == 2
            assert mapi.incr(2, gi.Direct.CCW, turn) == 3
            assert mapi.incr(3, gi.Direct.CCW, turn) == 4
            assert mapi.incr(4, gi.Direct.CCW, turn) == 5
            assert mapi.incr(5, gi.Direct.CCW, turn) == 0

            assert mapi.incr(gi.T_STORE, gi.Direct.CW, turn) == 5
            assert mapi.incr(gi.F_STORE, gi.Direct.CW, turn) == 2
            assert mapi.incr(0, gi.Direct.CW, turn) == 5
            assert mapi.incr(1, gi.Direct.CW, turn) == 0
            assert mapi.incr(2, gi.Direct.CW, turn) == 1
            assert mapi.incr(4, gi.Direct.CW, turn) == 3
            assert mapi.incr(5, gi.Direct.CW, turn) == 4


    DCASES = [
        (gi.SowStores.NEITHER, gi.PlayLocs.BOARD_ONLY, incr.Increment),
        (gi.SowStores.OWN, gi.PlayLocs.BOARD_ONLY, incr.IncOwnStores),
        (gi.SowStores.BOTH, gi.PlayLocs.BOARD_ONLY, incr.IncBothStores),

        (gi.SowStores.NEITHER, gi.PlayLocs.BRD_OWN_STR_ALL, incr.IncFromStores),
        (gi.SowStores.OWN, gi.PlayLocs.BRD_OWN_STR_ALL, incr.IncOwnStores),
        (gi.SowStores.BOTH, gi.PlayLocs.BRD_OWN_STR_ALL, incr.IncBothStores),

        (gi.SowStores.NEITHER, gi.PlayLocs.BRD_OWN_STR_CHS, incr.IncFromStores),
        (gi.SowStores.OWN, gi.PlayLocs.BRD_OWN_STR_CHS, incr.IncOwnStores),
        (gi.SowStores.BOTH, gi.PlayLocs.BRD_OWN_STR_CHS, incr.IncBothStores),
        ]

    @pytest.mark.parametrize('sow_stores, play_locs, incr_class',
                             DCASES)
    def test_deco_build(self, sow_stores, play_locs, incr_class):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                sow_stores=sow_stores,
                                play_locs=play_locs,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert isinstance(game.deco.incr, incr_class)
