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
from context import game_interface as gi
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


class TestRandom:

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
