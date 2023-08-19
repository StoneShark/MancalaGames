# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:23:34 2023

@author: Ann
"""

import sys

import pytest

sys.path.extend(['src'])

import man_config

class TestDeka:

    @pytest.fixture
    def game(self):
        return man_config.make_game('./GameProps/Oware.txt')


    def test_false_win(self, game):

        game.turn = True
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 5, 0, 5, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [1, 0]
        assert cond is None

        # move 3
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 5, 4, 4, 4, 0, 5, 0, 6, 1, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [1, 0]
        assert cond is None

        # move 4
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 5, 4, 0, 5, 1, 6, 0, 6, 1, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 0]
        assert cond is None

        # move 5
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 6, 5, 1, 6, 0, 6, 0, 6, 1, 6, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 2]
        assert cond is None

        # move 6
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 6, 2, 7, 1, 7, 0, 6, 1, 6, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [3, 2]
        assert cond is None

        # move 7
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 0, 6, 2, 7, 1, 0, 1, 7, 2, 7, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [3, 3]
        assert cond is None

        # move 8
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 0, 6, 2, 7, 0, 0, 1, 7, 2, 7, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 3]
        assert cond is None

        # move 9
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 1, 7, 0, 7, 0, 0, 1, 0, 3, 8, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 6]
        assert cond is None

        # move 10
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 1, 7, 0, 0, 1, 1, 2, 1, 4, 9, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [7, 6]
        assert cond is None

        # move 11
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 0, 7, 0, 0, 1, 1, 2, 1, 0, 10, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [7, 8]
        assert cond is None

        # move 12
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 0, 0, 1, 1, 2, 0, 0, 0, 0, 10, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [15, 8]
        assert cond is None

        # move 13
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 0, 0, 1, 1, 2, 0, 0, 0, 0, 10, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [15, 8]
        assert cond is None

        # move 14
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [11, 0, 0, 1, 1, 0, 0, 0, 0, 0, 10, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [17, 8]
        assert cond is None

        # move 15
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [12, 1, 1, 2, 2, 1, 1, 1, 1, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [17, 8]
        assert cond is None

        # move 16
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [12, 1, 1, 2, 0, 2, 0, 1, 1, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 8]
        assert cond is None

        # move 17
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [12, 1, 1, 2, 0, 2, 0, 0, 2, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 8]
        assert cond is None

        # move 18
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [12, 0, 2, 2, 0, 2, 0, 0, 2, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 8]
        assert cond is None

        # move 19
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [13, 0, 2, 2, 0, 2, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 8]
        assert cond is None

        # move 20
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [13, 0, 0, 3, 1, 2, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 8]
        assert cond is None

        # move 21
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [13, 0, 0, 3, 1, 2, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 8]
        assert cond is None

        # move 22
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [13, 0, 0, 3, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [21, 8]
        assert cond is None

        # move 23
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [13, 0, 0, 3, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [21, 8]
        assert cond is None

        # move 24
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [13, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [22, 8]
        assert cond is None

        # move 25
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [14, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [22, 8]
        assert cond is None

        # move 26
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [14, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [23, 8]
        assert cond is None

        # move 27
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [15, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [23, 8]
        assert cond is None

        # move 28
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [15, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [23, 8]
        assert cond is None

        # move 29
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [15, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [23, 8]
        assert cond is None

        # move 30
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [15, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 8]
        assert cond is None

        # move 31
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [15, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 8]
        assert cond is None

        # move 32
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 8]
        assert cond is None

        # move 33
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 9]
        assert cond is None

        # move 34
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [34, 14]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Bottom' in winmsg[1]
