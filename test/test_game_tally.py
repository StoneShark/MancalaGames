# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 08:33:21 2024

@author: Ann
"""


# %% imports


import pytest
pytestmark = pytest.mark.unittest

from context import game_interface as gi
from context import game_tally

from game_interface import WinCond


# %%

TEST_COVERS = ['src\\gtally.py']



# %%

class MyStrVar:

    def __init__(self, *args, **kwargs):
        self.value = '1999'

    def grid(self, *args, **kwargs):
        print('grided')

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


def mint(value):
    """make an int from the string value"""

    return int(value.strip())

# %%

class TestGameTally:

    @pytest.fixture
    def gtally(self, mocker):

        mocker.patch('tkinter.StringVar', MyStrVar)
        mocker.patch('tkinter.Label', mocker.MagicMock())
        return game_tally.GameTally(None)


    TCASES = [(True,  WinCond.WIN,            1, 0, 1, 0, 0, 0, 0, 0),
              (False, WinCond.WIN,            1, 1, 0, 0, 0, 0, 0, 0),
              (True,  WinCond.TIE,            1, 0, 0, 1, 0, 0, 0, 0),
              (False, WinCond.TIE,            1, 0, 0, 1, 0, 0, 0, 0),
              (True,  WinCond.ROUND_WIN,      0, 0, 0, 0, 1, 0, 1, 0),
              (False, WinCond.ROUND_WIN,      0, 0, 0, 0, 1, 1, 0, 0),
              (True,  WinCond.ROUND_TIE,      0, 0, 0, 0, 1, 0, 0, 1),
              (False, WinCond.ROUND_TIE,      0, 0, 0, 0, 1, 0, 0, 1),
              (True,  WinCond.GAME_OVER,      0, 0, 0, 0, 0, 0, 0, 0),
              (False, WinCond.GAME_OVER,      0, 0, 0, 0, 0, 0, 0, 0),
              (True,  WinCond.ENDLESS,        0, 0, 0, 0, 0, 0, 0, 0),
              (False, WinCond.ENDLESS,        0, 0, 0, 0, 0, 0, 0, 0),
              (True,  WinCond.REPEAT_TURN,    0, 0, 0, 0, 0, 0, 0, 0),
              (False, WinCond.REPEAT_TURN,    0, 0, 0, 0, 0, 0, 0, 0),
              ]

    @pytest.mark.parametrize('winner, cond, '
                             'gcnt, gwsf, gwst, gties, '
                             'rcnt, rwsf, rwst, rties',
                             TCASES)
    def test_gtally(self, gtally, winner, cond,
                        gcnt, gwsf, gwst, gties, rcnt, rwsf, rwst, rties):

        gtally.tally_game(winner, cond)

        assert gtally.games == gcnt
        assert gtally.game_wins == [gwsf, gwst]
        assert gtally.game_ties == gties
        assert gtally.rounds == rcnt
        assert gtally.round_wins == [rwsf, rwst]
        assert gtally.round_ties == rties

        assert mint(gtally.games_str.get()) == gtally.games
        assert mint(gtally.gtwins_str.get()) == gtally.game_wins[1]
        assert mint(gtally.gfwins_str.get()) == gtally.game_wins[0]
        assert mint(gtally.gties_str.get()) == gtally.game_ties

        assert mint(gtally.rounds_str.get()) == gtally.rounds
        assert mint(gtally.rtwins_str.get()) == gtally.round_wins[1]
        assert mint(gtally.rfwins_str.get()) == gtally.round_wins[0]
        assert mint(gtally.rties_str.get()) == gtally.round_ties


    def test_gt_sums(self, gtally):

        gtally.tally_game(True, WinCond.WIN)
        gtally.tally_game(True, WinCond.WIN)
        gtally.tally_game(True, WinCond.TIE)
        gtally.tally_game(False, WinCond.WIN)

        assert gtally.games == 4
        assert gtally.game_wins == [1, 2]
        assert gtally.game_ties == 1

        gtally.tally_game(False, WinCond.ROUND_WIN)
        gtally.tally_game(False, WinCond.ROUND_TIE)
        gtally.tally_game(False, WinCond.ROUND_WIN)
        gtally.tally_game(True, WinCond.ROUND_WIN)
        gtally.tally_game(True, WinCond.ROUND_TIE)
        gtally.tally_game(True, WinCond.ROUND_TIE)

        assert gtally.games == 4
        assert gtally.game_wins == [1, 2]
        assert gtally.game_ties == 1

        assert gtally.rounds == 6
        assert gtally.round_wins == [2, 1]
        assert gtally.round_ties == 3

        assert mint(gtally.games_str.get()) == gtally.games
        assert mint(gtally.gtwins_str.get()) == gtally.game_wins[1]
        assert mint(gtally.gfwins_str.get()) == gtally.game_wins[0]
        assert mint(gtally.gties_str.get()) == gtally.game_ties

        assert mint(gtally.rounds_str.get()) == gtally.rounds
        assert mint(gtally.rtwins_str.get()) == gtally.round_wins[1]
        assert mint(gtally.rfwins_str.get()) == gtally.round_wins[0]
        assert mint(gtally.rties_str.get()) == gtally.round_ties

        # game win should reset round counts
        gtally.tally_game(False, WinCond.WIN)

        assert gtally.games == 5
        assert gtally.game_wins == [2, 2]
        assert gtally.game_ties == 1

        assert gtally.rounds == 0
        assert gtally.round_wins == [0, 0]
        assert gtally.round_ties == 0
