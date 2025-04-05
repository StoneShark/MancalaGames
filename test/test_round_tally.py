# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:53:31 2024

@author: Ann
"""



# %% imports

import pytest
pytestmark = pytest.mark.unittest

from context import game_interface as gi
from context import round_tally


# %%

TEST_COVERS = ['src\\round_tally.py']


# %%

T = True
F = False
N = None

# %%

class TestRoundTally:

    @pytest.mark.parametrize('goal, idx',
                             [(gi.Goal.RND_WIN_COUNT_MAX, 0),
                              (gi.Goal.RND_SEED_COUNT, 1),
                              (gi.Goal.RND_EXTRA_SEEDS, 2),
                              (gi.Goal.RND_POINTS, 3)])
    def test_const(self, goal, idx):

        rtally = round_tally.RoundTally(goal, 24, 48)
        values = ((1, 2), (3, 4), (5, 6), (7, 8))
        rtally.state = values

        assert rtally.parameter(0) == values[idx][0]
        assert rtally.parameter(1) == values[idx][1]

        assert rtally.msg
        assert rtally.required_win == 24
        assert rtally.skunk_seeds == 36

        vstr = str(rtally)
        assert 'RoundTally' in vstr
        assert all(str(v) in vstr for v in [1, 2, 3, 4, 5, 6, 7, 8])


    def test_bad_enum(self):

        with pytest.raises(gi.GameInfoError):
            round_tally.RoundTally(100, 24, 48)


    def test_state(self):

        rtally = round_tally.RoundTally(gi.Goal.RND_WIN_COUNT_MAX, 12, 24)

        assert rtally.state == ((0, 0), (0, 0), (0, 0), (0, 0))

        rtally.state = ((1, 2), (3, 4), (5, 6), (7, 8))

        assert rtally.round_wins == [1, 2]
        assert rtally.seeds == [3, 4]
        assert rtally.diff_sums == [5, 6]
        assert rtally.score == [7, 8]


    def test_clear(self):

        rtally = round_tally.RoundTally(gi.Goal.RND_EXTRA_SEEDS, 11, 15)
        rtally.state = ((1, 2), (3, 4), (5, 6), (7, 8))
        rtally.clear()
        assert rtally.state == ((0, 0), (0, 0), (0, 0), (0, 0))


    TALLY_CASES = [
        (None, False, (4, 20), ((0, 0), (0, 0), (0, 0), (0, 0))),

        (gi.WinCond.WIN, False, (17, 8), ((1, 0), (17, 8), (9, 0), (1, 0))),
        (gi.WinCond.WIN, False, (18, 8), ((1, 0), (18, 8), (10, 0), (2, 0))),

        (gi.WinCond.WIN, True,  (8, 17), ((0, 1), (8, 17), (0, 9), (0, 1))),
        (gi.WinCond.WIN, True,  (8, 18), ((0, 1), (8, 18), (0, 10), (0, 2))),

        (gi.WinCond.WIN, False, (11, 11), ((1, 0), (11, 11), (0, 0), (0, 0))),
        (gi.WinCond.WIN, True,  (11, 11), ((0, 1), (11, 11), (0, 0), (0, 0))),

        (gi.WinCond.TIE, False, (17, 8), ((0, 0), (17, 8), (0, 0), (0, 0))),
        (gi.WinCond.TIE, False, (18, 8), ((0, 0), (18, 8), (0, 0), (0, 0))),

        (gi.WinCond.TIE, True,  (17, 8), ((0, 0), (17, 8), (0, 0), (0, 0))),
        (gi.WinCond.TIE, True,  (18, 8), ((0, 0), (18, 8), (0, 0), (0, 0))),

        (gi.WinCond.TIE, False, (11, 11), ((0, 0), (11, 11), (0, 0), (0, 0))),
        (gi.WinCond.TIE, True,  (11, 11), ((0, 0), (11, 11), (0, 0), (0, 0))),

        ]

    @pytest.mark.parametrize('goal',
                             [gi.Goal.RND_WIN_COUNT_MAX,
                              gi.Goal.RND_SEED_COUNT,
                              gi.Goal.RND_EXTRA_SEEDS,
                              gi.Goal.RND_POINTS
                              ])
    @pytest.mark.parametrize('cond, winner, seeds, estate',
                             TALLY_CASES)
    def test_tally(self, goal, cond, winner, seeds, estate):

        rtally = round_tally.RoundTally(goal, 12, 24)
        assert rtally.skunk_seeds == 18

        rtally.tally(cond, winner, seeds)

        assert rtally.state == estate


    WIN_CASES = [
        # for these test cases all but the specified cond would result in a win
        (gi.Goal.RND_WIN_COUNT_MAX, ((3, 0), (9, 9), (9, 9), (9, 9)), (None, None)),
        (gi.Goal.RND_WIN_COUNT_MAX, ((0, 3), (9, 9), (9, 9), (9, 9)), (None, None)),
        (gi.Goal.RND_SEED_COUNT, ((9, 9), (3, 0), (9, 9), (9, 9)), (None, None)),
        (gi.Goal.RND_SEED_COUNT, ((9, 9), (0, 3), (9, 9), (9, 9)), (None, None)),
        (gi.Goal.RND_EXTRA_SEEDS, ((9, 9), (9, 9), (3, 0), (9, 9)), (None, None)),
        (gi.Goal.RND_EXTRA_SEEDS, ((9, 9), (9, 9), (0, 3), (9, 9)), (None, None)),
        (gi.Goal.RND_POINTS, ((9, 9), (9, 9), (9, 9), (3, 0)), (None, None)),
        (gi.Goal.RND_POINTS, ((9, 9), (9, 9), (9, 9), (0, 3)), (None, None)),

        # for these test cases only the specified cond will result in the expected cond
        (gi.Goal.RND_WIN_COUNT_MAX, ((8, 8), (4, 4), (4, 4), (4, 4)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_WIN_COUNT_MAX, ((8, 6), (4, 4), (4, 4), (4, 4)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_WIN_COUNT_MAX, ((6, 8), (4, 4), (4, 4), (4, 4)), (gi.WinCond.WIN, True)),
        (gi.Goal.RND_WIN_COUNT_MAX, ((12, 10), (4, 4), (4, 4), (4, 4)), (gi.WinCond.WIN, False)),

        (gi.Goal.RND_SEED_COUNT, ((4, 4), (8, 8), (4, 4), (4, 4)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_SEED_COUNT, ((4, 4), (8, 6), (4, 4), (4, 4)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_SEED_COUNT, ((4, 4), (6, 8), (4, 4), (4, 4)), (gi.WinCond.WIN, True)),

        (gi.Goal.RND_EXTRA_SEEDS, ((4, 4), (4, 4), (8, 8), (4, 4)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_EXTRA_SEEDS, ((4, 4), (4, 4), (8, 6), (4, 4)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_EXTRA_SEEDS, ((4, 4), (4, 4), (6, 8), (4, 4)), (gi.WinCond.WIN, True)),

        (gi.Goal.RND_POINTS, ((4, 4), (4, 4), (4, 4), (8, 8)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_POINTS, ((4, 4), (4, 4), (4, 4), (8, 6)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_POINTS, ((4, 4), (4, 4), (4, 4), (6, 8)), (gi.WinCond.WIN, True)),

        ]

    @pytest.mark.parametrize('goal, state, eresult',
                             WIN_CASES)
    def test_win(self, goal, state, eresult):

        rtally = round_tally.RoundTally(goal, 8, 12)
        rtally.state = state

        assert rtally.win_test() == eresult


    END_CASES = [
        (gi.Goal.RND_WIN_COUNT_MAX, ((7, 7), (0, 4), (0, 4), (0, 4)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_WIN_COUNT_MAX, ((7, 6), (4, 4), (4, 4), (4, 4)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_WIN_COUNT_MAX, ((6, 7), (4, 4), (4, 4), (4, 4)), (gi.WinCond.WIN, True)),

        (gi.Goal.RND_SEED_COUNT, ((4, 0), (7, 7), (0, 4), (0, 4)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_SEED_COUNT, ((4, 4), (7, 6), (4, 4), (4, 4)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_SEED_COUNT, ((4, 4), (6, 7), (4, 4), (4, 4)), (gi.WinCond.WIN, True)),

        (gi.Goal.RND_EXTRA_SEEDS, ((4, 0), (4, 0), (7, 7), (0, 4)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_EXTRA_SEEDS, ((4, 4), (4, 4), (7, 6), (4, 4)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_EXTRA_SEEDS, ((4, 4), (4, 4), (6, 7), (4, 4)), (gi.WinCond.WIN, True)),

        (gi.Goal.RND_POINTS, ((0, 4), (4, 0), (4, 0), (7, 7)), (gi.WinCond.TIE, None)),
        (gi.Goal.RND_POINTS, ((4, 4), (4, 4), (4, 4), (7, 6)), (gi.WinCond.WIN, False)),
        (gi.Goal.RND_POINTS, ((4, 4), (4, 4), (4, 4), (6, 7)), (gi.WinCond.WIN, True)),

        ]

    @pytest.mark.parametrize('goal, state, eresult',
                             END_CASES)
    def test_end(self, goal, state, eresult):

        rtally = round_tally.RoundTally(goal, 8, 12)
        rtally.state = state

        assert rtally.end_it() == eresult
