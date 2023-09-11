# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 05:31:10 2023

@author: Ann
"""

# %%  imports

import sys

import pytest

sys.path.extend(['src'])

import game_constants as gc


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
    assert game_consts.win_count == 30

    assert list(game_consts.false_range) == [0, 1, 2, 3, 4]
    assert list(game_consts.true_range) == [9, 8, 7, 6, 5]

    assert list(game_consts.false_fill) == [0, 4, 1, 3, 2]
    assert list(game_consts.true_fill) == [9, 5, 8, 6, 7]

    game_dict = game_consts.get_dict()
    assert 'nbr_start' in game_dict
    assert game_dict['nbr_start'] == 6
    assert 'holes' in game_dict
    assert game_dict['holes'] == 5

def test_even_holes():

    game_consts = gc.GameConsts(3, 6)

    assert game_consts.nbr_start == 3
    assert game_consts.holes == 6

    assert game_consts.dbl_holes == 12
    assert game_consts.half_holes == 3
    assert game_consts.total_seeds == 36
    assert game_consts.win_count == 18

    assert list(game_consts.false_range) == [0, 1, 2, 3, 4, 5]
    assert list(game_consts.true_range) == [11, 10, 9, 8, 7, 6]

    assert list(game_consts.false_fill) == [0, 5, 1, 4, 2, 3]
    assert list(game_consts.true_fill) == [11, 6, 10, 7, 9, 8]

    game_dict = game_consts.get_dict()
    assert 'nbr_start' in game_dict
    assert game_dict['nbr_start'] == 3
    assert 'holes' in game_dict
    assert game_dict['holes'] == 6


def test_print():
    # catch situation where we add to GameConsts but don't update the str
    # -1 : nbr_start and holes are both on the first line of the output
    game_consts = gc.GameConsts(6, 2)
    assert len(str(game_consts).split('\n')) == len(vars(game_consts)) - 1
