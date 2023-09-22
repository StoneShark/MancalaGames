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


# %% minimum game class for capt_ok


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



# %%

class TestSingleClasses:


    @pytest.mark.parametrize('child, seeds, eok',
                              [(False, 0, False),
                               (True, 0, False),
                               (None, 0, False),
                               (False, 3, False),
                               (True, 3, False),
                               (None, 3, True),
                              ])
    def test_needseeds_nochild(self, child, seeds, eok):

        game = CaptOkTestGame()

        loc = 0
        game.board[loc] = seeds
        game.child[loc] = child

        cok = capt_ok.CaptNeedSeedsNotChild(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


    @pytest.mark.parametrize('unlocked, seeds, eok',
                              [(False, 3, False),
                               (True, 3, True),
                              ])
    def test_unlocked(self, unlocked, seeds, eok):

        game = CaptOkTestGame()

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
    def test_oppside(self, turn, loc, eok):

        game = CaptOkTestGame()
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
    def test_evens(self, seeds, eok):

        game = CaptOkTestGame()
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
    def test_capt_on(self, seeds, eok):

        game = CaptOkTestGame()
        loc = 0
        game.board[loc] = seeds
        game.info.capt_on = [1, 3, 4]
        cok = capt_ok.CaptOn(game, capt_ok.CaptTrue(game))

        assert cok.capture_ok(loc) == eok


# %%  test cases

"""Build one array of all the test cases along with the
expected values given a different combination of game flags.

The table was created with a spreadsheet 'capt_ok_test_cases.ods'
"""

FIELD_NAMES = ['seeds', 'child', 'unlocked', 'loc', 'turn',
               'ex_no_flags', 'ex_capt_on_1_3_4', 'ex_evens', 'ex_opp_side',
               'ex_unlocked', 'ex_evens_opp', 'ex_capt_on_opp', 'ex_all_set']

TCase = collections.namedtuple('TCase', FIELD_NAMES)

#              test case   <-|-> expected results
CASES = [TCase( 0, N, T, 0, F, F, F, F, F, F, F, F, F),
         TCase( 1, T, T, 0, F, F, F, F, F, F, F, F, F),
         TCase( 1, N, T, 0, F, T, T, F, F, T, F, F, F),
         TCase( 1, N, F, 0, F, T, T, F, F, F, F, F, F),
         TCase( 1, N, T, 0, F, T, T, F, F, T, F, F, F),
         TCase( 2, N, T, 0, F, T, F, T, F, T, F, F, F),
         TCase( 2, N, T, 2, F, T, F, T, T, T, T, F, F),
         TCase( 2, N, T, 1, T, T, F, T, T, T, T, F, F),
         TCase( 2, N, T, 3, T, T, F, T, F, T, F, F, F),
         TCase( 3, N, T, 1, T, T, T, F, T, T, F, T, F),
         TCase( 4, N, T, 1, T, T, T, T, T, T, T, T, T),
         TCase( 5, N, T, 1, T, T, F, F, T, T, F, F, F),
         TCase( 6, N, T, 1, T, T, F, T, T, T, T, F, F),
         TCase(25, N, T, 1, T, T, F, F, T, T, F, F, F),
         TCase(26, N, T, 1, T, T, F, T, T, T, T, F, F),
         ]
NBR_CASES = len(CASES)

def get_fnames(eres_name):
    """return a list of the test case field names with the result name."""
    return FIELD_NAMES[:5] + [eres_name]

def get_cases(eres_name):
    """return a tuple of the test case with the choosen result."""
    return [case[:5] + tuple([getattr(case, eres_name)]) for case in CASES]


# %%

@pytest.mark.filterwarnings("ignore")
class TestCaptures:

    @pytest.fixture
    def make_game(self):

        def _make_game (turn, seeds, child, unlocked,
                        evens=False, oppsidecapt=False,
                        moveunlock=False, capt_on=()):

            game_consts = gc.GameConsts(nbr_start=4, holes=2)
            game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                    capt_on=capt_on,
                                    flags=gi.GameFlags(evens=evens,
                                                       oppsidecapt=oppsidecapt,
                                                       moveunlock=moveunlock),
                                    rules=mancala.Mancala.rules)

            game = mancala.Mancala(game_consts, game_info)
            game.turn = turn
            game.board = [seeds] * 4
            game.child = [child] * 4
            game.unlocked = [unlocked] * 4
            return game

        return _make_game



    @pytest.mark.parametrize(get_fnames('ex_no_flags'),
                              get_cases('ex_no_flags'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_no_flags(self, make_game,
                      seeds, child, unlocked, loc, turn, ex_no_flags):
        """This is fantasy because the capturer doesn't call capt_ok,
        if none of the flags are set."""

        game = make_game(turn, seeds, child, unlocked)
        assert game.deco.capt_ok.capture_ok(loc) == ex_no_flags



    @pytest.mark.parametrize(get_fnames('ex_capt_on_1_3_4'),
                              get_cases('ex_capt_on_1_3_4'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_capt_on(self, make_game,
                     seeds, child, unlocked, loc, turn, ex_capt_on_1_3_4):

        game = make_game(turn, seeds, child, unlocked, capt_on=(1, 3, 4))

        assert game.deco.capt_ok.capture_ok(loc) == ex_capt_on_1_3_4



    @pytest.mark.parametrize(get_fnames('ex_evens'),
                              get_cases('ex_evens'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_evens(self, make_game,
                   seeds, child, unlocked, loc, turn,  ex_evens):

        game = make_game(turn, seeds, child, unlocked, evens=True)
        assert game.deco.capt_ok.capture_ok(loc) == ex_evens



    @pytest.mark.parametrize(get_fnames('ex_opp_side'),
                              get_cases('ex_opp_side'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_opp_side(self, make_game,
                      seeds, child, unlocked, loc, turn, ex_opp_side):

        game = make_game(turn, seeds, child, unlocked, oppsidecapt=True)
        assert game.deco.capt_ok.capture_ok(loc) == ex_opp_side



    @pytest.mark.parametrize(get_fnames('ex_unlocked'),
                              get_cases('ex_unlocked'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_unlocked(self, make_game,
                      seeds, child, unlocked, loc, turn, ex_unlocked):

        game = make_game(turn, seeds, child, unlocked, moveunlock=True)
        assert game.deco.capt_ok.capture_ok(loc) == ex_unlocked



    @pytest.mark.parametrize(get_fnames('ex_evens_opp'),
                              get_cases('ex_evens_opp'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_even_opp(self, make_game,
                      seeds, child, unlocked, loc, turn, ex_evens_opp):

        game = make_game(turn, seeds, child, unlocked,
                         evens=True, oppsidecapt=True)
        assert game.deco.capt_ok.capture_ok(loc) == ex_evens_opp



    @pytest.mark.parametrize(get_fnames('ex_capt_on_opp'),
                              get_cases('ex_capt_on_opp'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_capt_on_opp(self, make_game,
                         seeds, child, unlocked, loc, turn, ex_capt_on_opp):

        game = make_game(turn, seeds, child, unlocked,
                         capt_on=(1, 3, 4), oppsidecapt=True)
        assert game.deco.capt_ok.capture_ok(loc) == ex_capt_on_opp



    @pytest.mark.parametrize(get_fnames('ex_all_set'),
                              get_cases('ex_all_set'),
                              ids=[f'case_{n}' for n in range(NBR_CASES)])
    def test_all_flags(self, make_game,
                       seeds, child, unlocked, loc, turn, ex_all_set):

        game = make_game(turn, seeds, child, unlocked,
                         evens=True, moveunlock=True, oppsidecapt=True,
                         capt_on=(1, 3, 4))
        assert game.deco.capt_ok.capture_ok(loc) == ex_all_set


# %%

"""
pytest.main(['test_capt_ok.py'])
"""
