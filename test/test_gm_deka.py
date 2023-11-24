# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:23:34 2023

@author: Ann
"""

import pytest
pytestmark = [pytest.mark.integtest]

from context import man_config

@pytest.mark.skip(reason='Test written to allow closing all holes.')
class TestDeka:

    @pytest.fixture
    def game_data(self):
        return man_config.make_game('./GameProps/Deka.txt')


    def test_true_win(self, game_data):

        game = game_data[0]

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
        assert 'eliminating' in winmsg[1]
