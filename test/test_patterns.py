# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 07:34:54 2023

@author: Ann
"""

import collections

import pandas as pd
import pytest
pytestmark = pytest.mark.unittest

import utils

from context import fill_patterns as fp
from context import game_constants as gconsts
from context import game_info as gi
from context import mancala


TEST_COVERS = ['src\\fill_patterns.py']


CONVERT_DICT = {'TRUE': True,
                'FALSE': False,
                '': 0}

def cval(value):

    if value in CONVERT_DICT:
        return CONVERT_DICT[value]
    return int(value)


def read_test_cases():

    global CASES

    cases_df = pd.read_excel('test/fill_patterns.xlsx')

    field_names = cases_df.columns[:5]
    Case = collections.namedtuple('Case', field_names)

    CASES = []
    first = True
    for _, row in cases_df.iterrows():

        if first:
            pattern = int(row.pattern)
            holes = int(row.holes)
            starter = bool(row.starter)
            seeds = int(row.seeds)

            row1 = [int(row.iloc[i]) for i in range(4, 4 + holes)]

        else:
            row2 = [int(row.iloc[i]) for i in range(4, 4 + holes)]

            board = utils.build_board(row1, row2)
            CASES += [Case(pattern, holes, starter, seeds, board)]

        first = not first


read_test_cases()


@pytest.fixture(params=CASES)
def case(request):
    return request.param

def test_fill_patterns(case):

    game_consts = gconsts.GameConsts(nbr_start=4, holes=case.holes)
    game_info = gi.GameInfo(start_pattern=case.pattern,
                            capt_on=[2],
                            stores=True,
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)

    game = mancala.Mancala(game_consts, game_info)
    game.turn = case.starter
    fp.PCLASSES[game.info.start_pattern].fill_seeds(game)

    assert fp.PCLASSES[case.pattern].nbr_seeds(case.holes, 4) == case.seeds
    assert game.board == case.board



def test_rules():

    assert not fp.GamachaPattern.size_ok(2)
    assert fp.GamachaPattern.size_ok(3)

    assert fp.AlternatesPattern.size_ok(2)
    assert fp.AlternatesPattern.size_ok(3)

    assert not fp.AltsWithOnePattern.size_ok(2)
    assert fp.AltsWithOnePattern.size_ok(3)

    assert not fp.ClippedTriplesPattern.size_ok(2)
    assert fp.ClippedTriplesPattern.size_ok(3)

    assert not fp.TwoEmptyPattern.size_ok(2)
    assert not fp.TwoEmptyPattern.size_ok(3)
    assert fp.TwoEmptyPattern.size_ok(4)

    assert fp.RandomPattern.size_ok(2)
    assert fp.RandomPattern.size_ok(3)

    assert fp.AltsThenSplitPattern.size_ok(2)
    assert not fp.AltsThenSplitPattern.size_ok(3)


class TestRandomFill:

    @pytest.fixture
    def game(self, request):

        (holes, start) = request.param
        game_consts = gconsts.GameConsts(nbr_start=start, holes=holes)
        game_info = gi.GameInfo(start_pattern=gi.StartPattern.RANDOM,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('game, etot',
                             [((2, 28), 28),
                              ((2, 36), 36),
                              ((6, 68), 68),
                              ((6, 12), 12),
                              ], indirect=['game'])
    def test_totals(self, game, etot):

        assert game.cts.total_seeds == etot


    @pytest.mark.no_seed
    @pytest.mark.parametrize('game',
                             [(2, 28),
                              (2, 36),
                              (6, 68),
                              (6, 12),
                              ], indirect=['game'])
    def test_patterns(self, game):
        """Fill the game pattern a bunch of times, confirming
        the total number of seeds and that they are all
        0 or positive."""

        for _ in range(50):
            fp.PCLASSES[game.info.start_pattern].fill_seeds(game)

            assert len(game.board) == game.cts.dbl_holes
            assert sum(game.board) == game.cts.total_seeds
            assert all(s >= 0 for s in game.board)


class TestRandomEmptiesFill:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=64, holes=6)
        game_info = gi.GameInfo(start_pattern=gi.StartPattern.RANDOM_ZEROS,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    CASES = [
        [0] + [0.1] * 9 + [0],
        [0.001, 0.2, 0.1, 0.4, 0.099, 0.001, 0.5, 0.8, 0.2, 0.0, 0.0],

        [0.101, 0.922, 0.714, 0.936, 0.657, 0.489, 0.393, 0.797,
         0.530, 0.622, 0.645],

        # error < 0
        [0.02710652393737345, 0.09076916608405483, 0.11674709460519095,
         0.2243833998672179, 0.4118584098180995, 0.640342222421666,
         0.6981872817074174, 0.7539198581760017, 0.8605283491917431,
         0.9424585220363698, 0.9537550771416434]
        ]

    @pytest.mark.parametrize('rvalues', CASES)
    def test_patterns(self, mocker, game, rvalues):
        """Fill the game pattern a bunch of times, confirming
        the total number of seeds and that they are all
        0 or positive."""

        mrand = mocker.patch('random.random')
        mrand.side_effect = rvalues

        fp.PCLASSES[game.info.start_pattern].fill_seeds(game)

        assert len(game.board) == game.cts.dbl_holes
        assert sum(game.board) == game.cts.total_seeds
        assert all(s >= 0 for s in game.board)


    @pytest.mark.no_seed
    def test_many(self, game):
        """Fill the game pattern a bunch of times, confirming
        the total number of seeds and that they are all
        0 or positive."""

        for _ in range(50):
            fp.PCLASSES[game.info.start_pattern].fill_seeds(game)

            assert len(game.board) == game.cts.dbl_holes
            assert sum(game.board) == game.cts.total_seeds
            assert all(s >= 0 for s in game.board)


class TestMoveRightmost:

    def test_simple_game(case):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(start_pattern=gi.StartPattern.MOVE_RIGHTMOST,
                                capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = True
        game.new_game()

        assert game.board == [2, 2, 2, 0, 3, 3, 2, 2]


    def test_mlaps_game(case):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(start_pattern=gi.StartPattern.MOVE_RIGHTMOST,
                                sow_direct=gi.Direct.CW,
                                mlaps=gi.LapSower.LAPPER,
                                crosscapt=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.new_game()

        assert game.board == [3, 0, 3, 1, 0, 3, 0, 3]
        assert game.store == [3, 0]


class TestRandomMove:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(start_pattern=gi.StartPattern.MOVE_RANDOM,
                                evens=True,
                                stores=True,
                                sow_stores=gi.SowStores.OWN,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.no_seed
    def test_patterns(self, game):
        """Fill the game pattern a bunch of times."""

        for _ in range(100):

            game.new_game()

            store = game.store
            board = game.board

            assert len(board) == 12
            assert all(cnt >= 0 for cnt in board + store)
            assert sum(store) + sum(board) == game.cts.total_seeds
            assert not all(board[loc] == 6 for loc in range(12))


    def test_repeat_turn(self, mocker, game):
        """Force a repeat turn by mocking random.choice.
        It should be ignored and the turn changed to the non-starter."""

        mrand = mocker.patch('random.choice')
        mrand.return_value = 2

        game.starter = True       # need False to start the next game

        game.new_game()

        assert game.mdata
        assert game.mdata.repeat_turn == True
        assert game.turn != game.starter



class TestNoRepeat:


    def test_bad_size(self):

        with pytest.raises(gi.GameInfoError):
            gi.GameInfo(start_pattern=gi.StartPattern.NO_REPEAT_SOW_OWN,
                        evens=True,
                        stores=True,
                        sow_stores=gi.SowStores.OWN,
                        nbr_holes=2,
                        rules=mancala.Mancala.rules)

    # tested them all but don't need these 200+ tests in the test suite
    # @pytest.mark.parametrize('holes', range(3, gconsts.MAX_HOLES))
    # @pytest.mark.parametrize('seeds', range(1, 21))

    @pytest.mark.parametrize('holes', [3, 5, 6, 7, gconsts.MAX_HOLES])
    @pytest.mark.parametrize('seeds', [1, 2, 3, 4, 5, 8, 10, 20])
    def test_no_repeat(self, holes, seeds):

        game_consts = gconsts.GameConsts(holes=holes, nbr_start=seeds)
        game_info = gi.GameInfo(start_pattern=gi.StartPattern.NO_REPEAT_SOW_OWN,
                                evens=True,
                                stores=True,
                                sow_stores=gi.SowStores.OWN,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        print()
        print(game)

        for pos in range(holes):
            with game.save_restore_state():
                mdata = game.do_sow(pos)
                assert mdata.capt_loc != gi.WinCond.REPEAT_TURN
