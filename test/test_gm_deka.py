# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:23:34 2023

@author: Ann
"""

import sys

import pytest
pytestmark = [pytest.mark.unittest, pytest.mark.integtest]

sys.path.extend(['src'])

import deka
import man_config

from game_interface import WinCond


class TestDeka:

    @pytest.fixture
    def game(self):
        return man_config.make_game('./GameProps/Deka.txt')


    def test_true_win(self, game):

        game.turn = False
        assert game.turn is False
        assert game.board == [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 4, 0, 1, 5, 5, 1, 4, 4, 4, 0, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 1, 0, 6, 0, 2, 5, 5, 5, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 6, 2, 1, 1, 2, 0, 7, 7, 7, 1, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 7, 3, 0, 2, 0, 1, 8, 1, 8, 2, 3]
        assert game.blocked == [False, False, False, False, False, True, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 8, 4, 1, 1, 0, 2, 0, 2, 9, 3, 4]
        assert game.blocked == [False, False, False, False, False, True, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 0, 5, 2, 2, 0, 3, 1, 3, 10, 1, 5]
        assert game.blocked == [False, False, False, False, False, True, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [1, 0]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 0, 1, 7, 3, 0, 1, 5, 3, 2, 1, 9]
        assert game.blocked == [False, False, False, False, False, True, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [1, 0]
        assert cond is None

        # move 8
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 3, 0, 0, 3, 2, 6, 0, 13]
        assert game.blocked == [False, False, False, False, False, True, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [5, 0]
        assert cond is None

        # move 9
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 7, 1, 0, 1, 0, 0, 2, 0, 1, 5, 0]
        assert game.blocked == [False, False, False, False, False, True, True, False, True, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [13, 0]
        assert cond is None

        # move 10
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 5, 0, 3, 0, 0, 3, 0, 0, 4, 1]
        assert game.blocked == [False, False, False, False, False, True, True, False, True, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [17, 0]
        assert cond is None

        # move 11
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 4, 0, 0, 4, 0, 0, 4, 1]
        assert game.blocked == [False, False, False, False, False, True, True, False, True, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 0]
        assert cond is None

        # move 12
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 5, 0, 0, 0, 0, 1, 5, 2]
        assert game.blocked == [True, False, False, False, False, True, True, False, True, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [20, 0]
        assert cond is None

        # move 13
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 2, 1, 1, 0, 0, 1, 0, 2, 0, 3]
        assert game.blocked == [True, False, False, False, False, True, True, False, True, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [23, 0]
        assert cond is None

        # move 14
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 4, 0, 2, 2, 0, 0, 1, 0, 2, 0, 0]
        assert game.blocked == [True, False, True, False, False, True, True, False, True, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [25, 0]
        assert cond is None

        # move 15
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 1, 0, 0, 1, 0, 0, 1, 1]
        assert game.blocked == [True, False, True, False, False, True, True, False, True, True, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [29, 0]
        assert cond is None

        # move 16
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.blocked == [True, False, True, False, False, True, True, False, True, True, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [30, 0]
        assert cond is None

        # move 17
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [True, False, True, False, False, True, True, False, True, True, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [33, 0]
        assert cond is None

        # move 18
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [True, False, True, False, False, True, True, False, True, True, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [33, 0]
        assert cond is None

        # move 19
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.blocked == [True, False, True, False, False, True, True, False, True, True, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [34, 0]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


    def test_no_mlap(self, game):

        # get the config vars, change mlaps, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info.flags, 'mlaps', False)
        info.__post_init__(rules=deka.Deka.rules)
        game = deka.Deka(consts, info)

        game.turn = True
        game.board = [0, 0, 2, 0, 0, 2, 1, 1, 12, 9, 6, 3]

        assert game.move(5) is None
        assert not game.turn
        assert not any(game.blocked[l] for l in range(game.cts.dbl_holes))
        assert game.board == [0, 0, 2, 0, 0, 2, 0, 2, 12, 9, 6, 3]
        assert game.store[0] == 0 and game.store[1] == 0

        assert game.move(5) is None
        assert game.turn
        assert game.blocked[7]
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 0, 12, 9, 6, 3]
        assert game.store[0] == 3 and game.store[1] == 0


    def test_end_game_tie(self, game):

        cond = game.end_game()

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Both players' in winmsg[1]


    @pytest.mark.parametrize('turn', range(2))
    def test_wincond_t_win(self, game, turn):

        game.board = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        game.store == [34, 0]
        game.turn = turn

        cond = game.win_conditions()

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


    @pytest.mark.parametrize('turn', range(2))
    def test_wincond_f_win(self, game, turn):

        game.board = [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        game.store == [34, 0]
        game.turn = turn

        cond = game.win_conditions()

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Bottom' in winmsg[1]


    def test_win_message(self, game):

        winmsg = game.win_message(42)
        assert 'Game Over' in winmsg[0]
        assert 'Unexpected' in winmsg[1]

        winmsg = game.win_message(WinCond.ENDLESS)
        assert 'Game Over' in winmsg[0]
        assert 'stuck' in winmsg[1]


    def test_endless(self, game):

        game.turn = False
        game.board = [0, 1, 0, 1, 2, 0, 1, 0, 4, 3, 2, 1]
        game.store = [21, 0]
        assert game.move(4) == WinCond.ENDLESS
