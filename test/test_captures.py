# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:31:23 2023
@author: Ann"""

import collections
import re

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import GrandSlam


# %%

TEST_COVERS = ['src\\capturer.py']


# %% read test cases

SKEEP = slice(0, 42)
SBOARD = slice(0, 4)
SCHILD = slice(4, 8)
SLOCKS = slice(8, 12)
SSTORE = slice(12, 14)
SINDIV = slice(14, 31)
SEBOARD = slice(31, 35)
SECHILD = slice(35, 39)
SESTORE = slice(39, 41)

CAPT_ON = 18
RESULT = 41

CONVERT_DICT = {'N': None,
                'T': True,
                'TRUE': True,
                'F': False,
                'FALSE': False,
                '': 0,

                'CCW': Direct.CCW,
                'CW': Direct.CW,
                'SPLIT': Direct.SPLIT,

                'PICKCAPT': CrossCaptOwn.PICK_ON_CAPT,
                'ALWAYS': CrossCaptOwn.ALWAYS_PICK,

                'LEGAL': GrandSlam.LEGAL,    # the default
                'NO_CAPT': GrandSlam.NO_CAPT,
                'OPP_GETS': GrandSlam.OPP_GETS_REMAIN,
                'KLEFT': GrandSlam.LEAVE_LEFT,
                'KRIGHT': GrandSlam.LEAVE_RIGHT,

                }

def convert(val, col, line):

    if col == CAPT_ON:
        capts = []
        if val:
            for ival in val.split(' '):
                if re.match('[0-9]+$', ival):
                    capts += [int(ival)]
                else:
                    raise ValueError(f"Non-integer found for capt {line}.")
        return capts

    if (SCHILD.start <= col < SCHILD.stop
        or SECHILD.start <= col < SECHILD.stop) and not val:
        return None

    if SLOCKS.start <= col < SLOCKS.stop and not val:
        return True

    if val in CONVERT_DICT:
        return CONVERT_DICT[val]

    if re.match('[0-9]+$', val):
        return int(val)

    if not val:
        return 0

    raise ValueError(f"Unknown value type at col/line {col}/{line}: {val}")


def read_test_cases():

    global FIELD_NAMES, CASES

    with open('test/capture_test_data.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    field_names = lines[2].split(',')
    FIELD_NAMES = [fname for fname in field_names[:-1] if fname]

    Case = collections.namedtuple('Case', FIELD_NAMES)

    CASES = []
    for lcnt in range(4, len(lines), 2):

        line_one = [convert(val, col, lcnt + 1)
                    for col, val in enumerate(lines[lcnt].split(',')[SKEEP])]
        line_two = [convert(val, col, lcnt + 2)
                    for col, val in enumerate(lines[lcnt + 1].split(',')[SKEEP])]

        board = utils.build_board(line_one[SBOARD], line_two[SBOARD])
        child = utils.build_board(line_one[SCHILD], line_two[SCHILD])
        locks = utils.build_board(line_one[SLOCKS], line_two[SLOCKS])
        store = line_one[SSTORE]

        eboard = utils.build_board(line_one[SEBOARD], line_two[SEBOARD])
        echild = utils.build_board(line_one[SECHILD], line_two[SECHILD])
        estore = line_one[SESTORE]

        CASES += [Case(board, child, locks, store,
                       *(line_one[SINDIV]),
                       eboard, echild, estore, line_one[RESULT])]


read_test_cases()


# %%  the tests


@pytest.mark.filterwarnings("ignore")
def test_no_capturer():
    game_consts = gc.GameConsts(nbr_start=3, holes=4)
    game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                            flags=gi.GameFlags(),
                            rules=mancala.Mancala.rules)
    game = mancala.Mancala(game_consts, game_info)
    assert not game.deco.capturer.do_captures(5, Direct.CCW)


def make_game(case):

    game_consts = gc.GameConsts(nbr_start=3, holes=4)
    game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                            capt_on=case.capt_on,
                            flags=gi.GameFlags(skip_start=case.skip_start,
                                               evens=case.evens,
                                               oppsidecapt=case.oppside,
                                               multicapt=case.multicapt,
                                               moveunlock=case.moveunlock,
                                               capsamedir=case.capsamedir,
                                               child=case.child,
                                               convert_cnt=case.convert_cnt,
                                               crosscapt=case.xcapt,
                                               xcpickown=case.xcapt_pick_own,
                                               grandslam=case.gslam),
                            rules=mancala.Mancala.rules)

    game = mancala.Mancala(game_consts, game_info)

    game.turn = case.turn
    game.board = case.board.copy()
    game.child = case.children.copy()
    game.unlocked = case.unlocked.copy()
    game.store = case.store.copy()

    return game


@pytest.fixture(params=CASES)
def case(request):
    return request.param


def test_capturer(case):

    game = make_game(case)
    print(game)
    assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
        f"Game setup error: board={sum(game.board)} stores={sum(game.store)}"

    captures = game.deco.capturer.do_captures(case.loc, case.direct)
    print(game)

    assert sum(game.store) + sum(game.board) == game.cts.total_seeds
    assert bool(captures) == getattr(case, 'erval')
    assert game.board == getattr(case, 'eboard')
    assert game.store == getattr(case, 'estore')
    assert game.child == getattr(case, 'echild')


# %%

"""
pytest.main(['test_captures_new.py'])
"""
