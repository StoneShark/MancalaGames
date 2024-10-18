# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 05:31:10 2023

@author: Ann
"""

# %%  imports


import pytest
pytestmark = pytest.mark.unittest

from context import game_constants as gc

# %%

TEST_COVERS = ['src\\game_constants.py']


# %%  test_game_consts


def test_hole_range_one():
    with pytest.raises(gc.GameConstsError):
        gc.GameConsts(0, 5)

def test_hole_range_two():
    with pytest.raises(gc.GameConstsError):
        gc.GameConsts(13, 5)

def test_nbr_start_range_one():
    with pytest.raises(gc.GameConstsError):
        gc.GameConsts(5, 0)

def test_start_range_two():
    with pytest.raises(gc.GameConstsError):
        gc.GameConsts(5, 15)

def test_odd_holes():

    game_consts = gc.GameConsts(6, 5)

    assert game_consts.nbr_start == 6
    assert game_consts.holes == 5

    assert game_consts.dbl_holes == 10
    assert game_consts.half_holes == 2
    assert game_consts.total_seeds == 60

    assert list(game_consts.false_range) == [0, 1, 2, 3, 4]
    assert list(game_consts.true_range) == [9, 8, 7, 6, 5]

    assert list(game_consts.false_fill) == [0, 4, 1, 3, 2]
    assert list(game_consts.true_fill) == [9, 5, 8, 6, 7]

    game_dict = game_consts.get_dict()
    assert 'nbr_start' in game_dict
    assert game_dict['nbr_start'] == 6
    assert 'holes' in game_dict
    assert game_dict['holes'] == 5

    game_consts.adjust_total_seeds(21)
    assert game_consts.total_seeds == 21


def test_even_holes():

    game_consts = gc.GameConsts(3, 6)

    assert game_consts.nbr_start == 3
    assert game_consts.holes == 6

    assert game_consts.dbl_holes == 12
    assert game_consts.half_holes == 3
    assert game_consts.total_seeds == 36

    assert list(game_consts.false_range) == [0, 1, 2, 3, 4, 5]
    assert list(game_consts.true_range) == [11, 10, 9, 8, 7, 6]

    assert list(game_consts.false_fill) == [0, 5, 1, 4, 2, 3]
    assert list(game_consts.true_fill) == [11, 6, 10, 7, 9, 8]

    game_dict = game_consts.get_dict()
    assert 'nbr_start' in game_dict
    assert game_dict['nbr_start'] == 3
    assert 'holes' in game_dict
    assert game_dict['holes'] == 6

    game_consts.adjust_total_seeds(20)
    assert game_consts.total_seeds == 20


def test_print():
    # catch situation where we add to GameConsts but don't update the str
    # -1 : nbr_start and holes are both on the first line of the output
    game_consts = gc.GameConsts(6, 2)
    assert len(str(game_consts).split('\n')) == len(vars(game_consts)) - 1


class TestCtsFuncs:

    @pytest.mark.parametrize(
        'row, pos, eloc',
        [(0, 0, 9),
         (0, 1, 8),
         (0, 4, 5),
         (1, 0, 0),
         (1, 3, 3),
         (1, 4, 4)
         ])
    def test_xlate_pos_loc(self, row, pos, eloc):

        game_consts = gc.GameConsts(6, 5)
        assert game_consts.xlate_pos_loc(row, pos) == eloc


    @pytest.mark.parametrize(
        'loc, cnt',
        [(0, 0),
         (1, 1),
         (2, 2),
         (3, 3),
         (4, 0),
         (5, 1),
         (6, 2),
         (7, 3),
         ])
    def test_loc_to_left_cnt(self, loc, cnt):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        assert game_consts.loc_to_left_cnt(loc) == cnt

    @pytest.mark.parametrize(
        'loc, cross',
        [(0, 7),
         (1, 6),
         (2, 5),
         (3, 4),
         (4, 3),
         (5, 2),
         (6, 1),
         (7, 0),
         ])
    def test_even_cross_from_loc(self, loc, cross):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        assert game_consts.cross_from_loc(loc) == cross

    @pytest.mark.parametrize(
        'loc, cross',
        [(0, 5),
         (1, 4),
         (2, 3),
         (3, 2),
         (4, 1),
         (5, 0),
         ])
    def test_odd_cross_from_loc(self, loc, cross):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        assert game_consts.cross_from_loc(loc) == cross


    @pytest.mark.parametrize('loc, eres',
                             [[0, False],
                              [1, False],
                              [2, False],
                              [3, True],
                              [4, True],
                              [5, True]])
    def test_board_side(self, loc, eres):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        assert game_consts.board_side(loc) == eres


    @pytest.mark.parametrize(
        'turn, loc, eres',
        [(True, 9, False),
         (False, 8, True),
         (True, 5, False),
         (False, 0, False),
         (True, 3, True),
         (False, 4, False)
         ])
    def test_opp_side(self, turn, loc, eres):

        game_consts = gc.GameConsts(6, 5)
        assert game_consts.opp_side(turn, loc) == eres


    @pytest.mark.parametrize(
        'turn, loc, eres',
        [(True, 9, True),
         (False, 8, False),
         (True, 5, True),
         (False, 0, True),
         (True, 3, False),
         (False, 4, True)
         ])
    def test_my_side(self, turn, loc, eres):

        game_consts = gc.GameConsts(6, 5)
        assert game_consts.my_side(turn, loc) == eres


    @pytest.mark.parametrize(
        'turn, erng',
        [(True, [9, 8, 7, 6, 5]),
         (False, [0, 1, 2, 3, 4]),
         ])
    def test_my_range(self, turn, erng):

        game_consts = gc.GameConsts(6, 5)
        assert list(game_consts.get_my_range(turn)) == erng


    @pytest.mark.parametrize(
        'turn, erng',
        [(True, [0, 1, 2, 3, 4]),
         (False, [9, 8, 7, 6, 5]),
         ])
    def test_opp_range(self, turn, erng):

        game_consts = gc.GameConsts(6, 5)
        assert list(game_consts.get_opp_range(turn)) == erng


    @pytest.mark.parametrize(
        'turn, erngs',
        [(True, ([9, 8, 7, 6, 5], [0, 1, 2, 3, 4])),
         (False, ([0, 1, 2, 3, 4], [9, 8, 7, 6, 5])),
         ])
    def test_ranges(self, turn, erngs):

        game_consts = gc.GameConsts(6, 5)
        ranges = game_consts.get_ranges(turn)
        assert list(ranges[0]) == erngs[0]
        assert list(ranges[1]) == erngs[1]
