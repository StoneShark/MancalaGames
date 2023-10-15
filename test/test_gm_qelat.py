# -*- coding: utf-8 -*-
"""Test the qelat game.

Created on Thu Aug 17 06:42:25 2023
@author: Ann"""


import pytest
pytestmark = [pytest.mark.integtest]

from context import man_config


class TestQelat:

    @pytest.fixture
    def game_data(self):
        return man_config.make_game('./GameProps/Qelat.txt')

    def test_win(self, game_data):

        game = game_data[0]

        game.turn = True
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 5, 4, 4, 0, 5, 5, 5, 5, 0, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 6, 6, 5, 5, 1, 0, 5, 5, 5, 0, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 7, 0, 5, 5, 1, 0, 5, 6, 6, 1, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 7, 1, 6, 6, 2, 1, 0, 6, 6, 1, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 7, 1, 0, 7, 3, 2, 1, 7, 7, 1, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 7
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 8, 2, 1, 8, 4, 2, 1, 7, 7, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 8
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [8, 0, 2, 1, 8, 5, 3, 2, 8, 8, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 9
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [8, 0, 2, 1, 8, 6, 4, 0, 8, 8, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 10
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 0, 2, 1, 0, 7, 5, 1, 9, 9, 3, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 11
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 1, 3, 2, 1, 8, 6, 1, 9, 0, 4, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 12
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 2, 0, 2, 1, 8, 6, 1, 9, 0, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 13
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [11, 2, 0, 2, 1, 8, 7, 0, 9, 0, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 14
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 3, 2, 9, 8, 1, 10, 1, 5, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 15
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 4, 2, 4, 3, 10, 0, 1, 10, 1, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 16
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 5, 0, 4, 3, 10, 0, 1, 10, 1, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 17
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 6, 1, 5, 4, 10, 0, 1, 10, 1, 0, 7]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 18
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 1, 5, 4, 10, 0, 2, 11, 2, 1, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 19
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 0, 1, 5, 4, 10, 0, 2, 11, 0, 2, 9]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 20
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 5, 4, 10, 0, 2, 12, 1, 3, 10]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 21
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 2, 6, 9, 11, 1, 0, 0, 2, 4, 11]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 22
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 2, 0, 6, 9, 11, 1, 0, 0, 2, 4, 11]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 23
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 3, 1, 6, 9, 11, 1, 0, 0, 2, 0, 12]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 24
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 0, 0, 6, 9, 11, 1, 0, 0, 2, 0, 16]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 25
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 0, 0, 6, 9, 11, 1, 0, 0, 0, 1, 17]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 26
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 6, 9, 11, 1, 0, 0, 1, 2, 18]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 27
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 6, 9, 11, 1, 0, 0, 0, 3, 18]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 28
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 10, 12, 2, 1, 1, 1, 3, 18]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond is None

        # move 29
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 14, 12, 2, 1, 1, 0, 0, 18]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, True, True, None, None, None, None, None, False]
        assert game.store == [0, 0]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]
