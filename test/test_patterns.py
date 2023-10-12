# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 07:34:54 2023

@author: Ann
"""

import collections

import pytest

import utils

from context import fill_patterns as fp
from context import game_constants as gc
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

    with open('test/fill_patterns.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines[0] = lines[0][1:]

    field_names = lines[0].strip().split(',')[:5]
    Case = collections.namedtuple('Case', field_names)

    CASES = []
    for lcnt in range(1, len(lines), 2):

        line_one = lines[lcnt].strip().split(',')
        line_two = lines[lcnt + 1].strip().split(',')

        board = utils.build_board([cval(val)
                                   for val in line_one[4:4 + int(line_one[1])]],
                                  [cval(val)
                                   for val in line_two[4:4 + int(line_one[1])]])

        CASES += [Case(*([cval(val) for val in line_one[0:4]]), board)]


read_test_cases()


@pytest.fixture(params=CASES)
def case(request):
    return request.param

def test_fill_patterns(case):

    game_consts = gc.GameConsts(nbr_start=4, holes=case.holes)
    game_info = gi.GameInfo(start_pattern=case.pattern,
                            capt_on=[2],
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

    assert fp.SadeqaPatternOne.size_ok(2)
    assert fp.SadeqaPatternOne.size_ok(2)

    assert not fp.SadeqaPatternTwo.size_ok(2)
    assert fp.SadeqaPatternTwo.size_ok(3)

    assert not fp.TapataPattern.size_ok(2)
    assert fp.TapataPattern.size_ok(3)
