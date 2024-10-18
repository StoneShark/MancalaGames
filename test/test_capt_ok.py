# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:41:35 2023

@author: Ann
"""


# %% imports

import collections

import pytest
pytestmark = pytest.mark.unittest

from context import capt_ok
from context import game_constants as gc
from context import game_interface as gi
from context import mancala



# %%

TEST_COVERS = ['src\\capt_ok.py']


# %%

T = True
F = False
N = None


# %%

class TestSingleClasses:
    """Test each of the classes by instatiating directly
    with a test game fixture."""

    @pytest.fixture
    def game(self):
        """minimum game class"""

        class Info:
            def __init__(self):
                self.capt_on = ()

        class Cts:
           def opp_side(self, turn, loc):
               if turn:
                   return loc in [0, 1]
               return loc in [2, 3]

        class CaptOkTestGame:
            def __init__(self):
                self.turn = False
                self.info = Info()
                self.cts = Cts()
                self.board = [2, 2, 2, 2]
                self.child = [F, F, F, F]
                self.unlocked = [T, T, T, T]

        return CaptOkTestGame()


    @pytest.mark.parametrize('child, seeds, eok',
                              [(False, 0, False),
                               (True, 0, False),
                               (None, 0, False),
                               (False, 3, False),
                               (True, 3, False),
                               (None, 3, True),
                              ])
    def test_needseeds_nochild(self, game, child, seeds, eok):

        loc = 0
        game.board[loc] = seeds
        game.child[loc] = child

        cok = capt_ok.CaptNeedSeedsNotChild(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


    @pytest.mark.parametrize('unlocked, seeds, eok',
                              [(False, 3, False),
                               (True, 3, True),
                              ])
    def test_unlocked(self, game, unlocked, seeds, eok):

        loc = 0
        game.board[loc] = seeds
        game.unlocked[loc] = unlocked

        cok = capt_ok.CaptUnlocked(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


    @pytest.mark.parametrize('turn, loc, eok',
                             [(False, 0, False),
                              (False, 1, False),
                              (False, 2, True),
                              (False, 3, True),
                              (True, 0, True),
                              (True, 1, True),
                              (True, 2, False),
                              (True, 3, False),
                              ])
    def test_oppside(self, game, turn, loc, eok):

        game.turn = turn
        cok = capt_ok.CaptOppSide(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


    @pytest.mark.parametrize('seeds, eok',
                             [# Evens will not see 0 because NeedSeeds
                              (1, False),
                              (2, True),
                              (3, False),
                              (25, False),
                              (26, True)
                              ])
    def test_evens(self, game, seeds, eok):

        loc = 0
        game.board[loc] = seeds
        cok = capt_ok.CaptEvens(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


    @pytest.mark.parametrize('seeds, eok',
                             [(1, True),
                              (2, False),
                              (3, True),
                              (4, True),
                              (5, False),
                              (6, False),
                              ])
    def test_capt_on(self, game, seeds, eok):

        loc = 0
        game.board[loc] = seeds
        game.info.capt_on = [1, 3, 4]
        cok = capt_ok.CaptOn(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


    @pytest.mark.parametrize('seeds, eok',
                             [(1, False),
                              (2, False),
                              (3, True),
                              (4, True),
                              (5, True),
                              ])
    def test_capt_min(self, game, seeds, eok):

        loc = 0
        game.board[loc] = seeds
        game.info.capt_min = 3
        cok = capt_ok.CaptMin(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


    @pytest.mark.parametrize('seeds, eok',
                             [(1, True),
                              (2, True),
                              (3, True),
                              (4, False),
                              (5, False),
                              (5, False),
                              ])
    def test_capt_max(self, game, seeds, eok):

        loc = 0
        game.board[loc] = seeds
        game.info.capt_max = 3
        cok = capt_ok.CaptMax(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


# %%  test cases and methods


CONVERT_DICT = {'None': None,
                'TRUE': True,
                'FALSE': False,
                '': 0,
                }

def convert(val, col, line):

    if val in CONVERT_DICT:
        return CONVERT_DICT[val]

    if all(d in '0123456789' for d in val):
        return int(val)

    if not val:
        return 0

    raise ValueError(f"Unknown value type at line:col {line}/{col}: _{val}_")


def read_test_cases():

    global FIELD_NAMES, CASES

    with open('test/capt_ok_test_cases.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines[0] = lines[0][1:]

    FIELD_NAMES = lines[0].strip().split(',')
    Case = collections.namedtuple('Case', FIELD_NAMES)

    CASES = []
    for lcnt, line in enumerate(lines[3:]):
        CASES += [Case(*(convert(val, col + 1, lcnt + 4)
                       for col, val in enumerate(line.strip().split(','))))]


read_test_cases()


GPARAMS = {'ex_no_flags': {},
           'ex_capt_on_1_3_4': {'capt_on': (1, 3, 4)},
           'ex_evens': {'evens': True},
           'ex_capt_max': {'capt_max': 3},
           'ex_capt_min': {'capt_min': 4},
           'ex_opp_side': {'oppsidecapt': True},
           'ex_unlocked': {'moveunlock': True},
           'ex_evens_opp': {'evens': True,
                            'oppsidecapt': True},
           'ex_capt_on_opp': {'capt_on':(1, 3, 4),
                              'oppsidecapt': True},
           'ex_all_set': {'evens': True,
                          'moveunlock': True,
                          'oppsidecapt': True,
                          'capt_on': (1, 3, 4)}
           }

TEST_METHODS = GPARAMS.keys()



@pytest.mark.filterwarnings("ignore")
class TestCaptOk:

    @pytest.fixture
    def make_game(self):

        def _make_game (turn, seeds, child, unlocked, game_options):

            game_consts = gc.GameConsts(nbr_start=4, holes=2)
            game_info = gi.GameInfo(sow_own_store=True,
                                    stores=True,
                                    **game_options,
                                    nbr_holes=game_consts.holes,
                                    rules=mancala.Mancala.rules)

            game = mancala.Mancala(game_consts, game_info)
            game.turn = turn
            game.board = [seeds] * 4
            game.child = [child] * 4
            game.unlocked = [unlocked] * 4
            return game

        return _make_game


    @pytest.fixture(params=TEST_METHODS)
    def method(self, request):
        return request.param


    @pytest.fixture(params=CASES)
    def case(self, request):
        return request.param


    def test_capt_ok(self, method, case, make_game):

        game = make_game(case.turn, case.seeds, case.child, case.unlocked,
                         GPARAMS[method])
        assert game.deco.capt_ok.capture_ok(case.loc) == getattr(case, method)
