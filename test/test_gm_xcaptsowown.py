# -*- coding: utf-8 -*-
"""Test the xcaptsowown game.
Tests sow stores and cross capture with pick own.

Created on Thu Aug 17 06:42:25 2023
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest


from context import man_config

class TestXCaptSowOwn:

    @pytest.fixture
    def game_data(self):
        return man_config.make_game('./GameProps/XCaptSowOwn.txt')

    def test_tie(self, game_data):

        game = game_data[0]
        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 4, 0, 5, 5, 5, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [1, 0]
        assert cond.name == "REPEAT_TURN"

        # move 2
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 0, 5, 5, 5, 5, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 0]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 1, 5, 5, 0, 5, 5, 5, 5, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 1]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 2, 6, 6, 0, 0, 5, 5, 5, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [8, 1]
        assert cond is None

        # move 5
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 6, 2, 6, 6, 0, 0, 0, 6, 6, 5, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [8, 2]
        assert cond.name == "REPEAT_TURN"

        # move 6
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 2, 6, 6, 0, 0, 0, 6, 6, 5, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [8, 3]
        assert cond.name == "REPEAT_TURN"

        # move 7
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 7, 2, 6, 6, 0, 0, 0, 0, 7, 6, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [8, 4]
        assert cond is None

        # move 8
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 7, 2, 6, 0, 1, 1, 1, 1, 8, 6, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [9, 4]
        assert cond is None

        # move 9
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 7, 2, 6, 0, 1, 1, 1, 1, 8, 6, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [9, 5]
        assert cond.name == "REPEAT_TURN"

        # move 10
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 8, 3, 7, 0, 1, 1, 1, 1, 8, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [9, 6]
        assert cond is None

        # move 11
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 8, 3, 7, 0, 0, 1, 1, 1, 8, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [10, 6]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 8, 0, 8, 1, 0, 0, 1, 1, 8, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [12, 6]
        assert cond is None

        # move 13
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 8, 0, 8, 1, 0, 0, 0, 2, 8, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [12, 6]
        assert cond is None

        # move 14
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 8, 0, 0, 2, 1, 1, 1, 3, 9, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [13, 6]
        assert cond is None

        # move 15
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 8, 0, 0, 2, 1, 1, 1, 3, 9, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [13, 7]
        assert cond.name == "REPEAT_TURN"

        # move 16
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 2, 1, 1, 1, 0, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [13, 10]
        assert cond is None

        # move 17
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 2, 0, 1, 1, 0, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [14, 10]
        assert cond.name == "REPEAT_TURN"

        # move 18
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 0, 1, 1, 1, 0, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [15, 10]
        assert cond.name == "REPEAT_TURN"

        # move 19
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 0, 0, 1, 1, 0, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [16, 10]
        assert cond.name == "REPEAT_TURN"

        # move 20
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 2, 2, 1, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [17, 10]
        assert cond is None

        # move 21
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 1, 0, 3, 2, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [17, 10]
        assert cond is None

        # move 22
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 3, 2, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [18, 10]
        assert cond.name == "REPEAT_TURN"

        # move 23
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 3, 2, 10, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [18, 10]
        assert cond is None

        # move 24
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 3, 2, 10, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [18, 11]
        assert cond.name == "REPEAT_TURN"

        # move 25
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 3, 11, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [18, 11]
        assert cond is None

        # move 26
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 3, 11, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 11]
        assert cond.name == "REPEAT_TURN"

        # move 27
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 3, 11, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [20, 11]
        assert cond.name == "REPEAT_TURN"

        # move 28
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 11]
        assert cond is None

        # move 29
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 24]
        assert cond.name == "TIE"


    def test_win(self, game_data):

        game = game_data[0]

        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 4, 0, 5, 5, 5, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [1, 0]
        assert cond.name == "REPEAT_TURN"

        # move 2
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 0, 5, 5, 5, 5, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 0]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 1, 5, 5, 0, 5, 5, 5, 5, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 1]
        assert cond is None

        # move 4
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 0, 2, 6, 6, 1, 5, 5, 5, 5, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [3, 1]
        assert cond.name == "REPEAT_TURN"

        # move 5
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 0, 2, 6, 6, 0, 5, 5, 5, 5, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 1]
        assert cond.name == "REPEAT_TURN"

        # move 6
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 7, 7, 0, 0, 5, 5, 5, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [10, 1]
        assert cond is None

        # move 7
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 3, 7, 7, 0, 0, 0, 6, 6, 5, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [10, 2]
        assert cond.name == "REPEAT_TURN"

        # move 8
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 7, 7, 0, 0, 0, 6, 6, 5, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [10, 3]
        assert cond.name == "REPEAT_TURN"

        # move 9
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 4, 7, 7, 0, 0, 0, 6, 0, 6, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [10, 4]
        assert cond is None

        # move 10
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 0, 8, 8, 1, 0, 0, 6, 0, 6, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [11, 4]
        assert cond.name == "REPEAT_TURN"

        # move 11
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 0, 8, 8, 0, 0, 0, 6, 0, 6, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [12, 4]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 0, 8, 8, 0, 0, 0, 6, 0, 6, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [12, 4]
        assert cond is None

        # move 13
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 4, 0, 8, 8, 0, 0, 0, 0, 1, 7, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [12, 5]
        assert cond is None

        # move 14
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 9, 9, 1, 0, 0, 0, 1, 7, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [12, 5]
        assert cond is None

        # move 15
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 2, 10, 10, 1, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [12, 6]
        assert cond is None

        # move 16
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 2, 10, 10, 0, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [13, 6]
        assert cond.name == "REPEAT_TURN"

        # move 17
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 2, 2, 10, 0, 1, 1, 1, 1, 2, 1, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [14, 6]
        assert cond is None

        # move 18
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 2, 2, 10, 0, 1, 1, 1, 0, 3, 1, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [14, 6]
        assert cond is None

        # move 19
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 2, 2, 10, 0, 0, 1, 1, 0, 3, 1, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [15, 6]
        assert cond.name == "REPEAT_TURN"

        # move 20
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 2, 0, 11, 0, 0, 1, 0, 0, 3, 1, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [17, 6]
        assert cond is None

        # move 21
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 3, 1, 11, 0, 0, 1, 0, 0, 3, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [17, 7]
        assert cond is None

        # move 22
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 1, 1, 2, 1, 1, 4, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [18, 7]
        assert cond is None

        # move 23
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 4, 1, 0, 1, 1, 2, 1, 0, 5, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [18, 7]
        assert cond is None

        # move 24
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 4, 1, 0, 1, 0, 2, 1, 0, 5, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [19, 7]
        assert cond.name == "REPEAT_TURN"

        # move 25
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [22, 7]
        assert cond is None

        # move 26
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [22, 8]
        assert cond.name == "REPEAT_TURN"

        # move 27
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [22, 9]
        assert cond.name == "REPEAT_TURN"

        # move 28
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [22, 10]
        assert cond.name == "REPEAT_TURN"

        # move 29
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 0, 1, 5, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [22, 10]
        assert cond is None

        # move 30
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 4, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 10]
        assert cond is None

        # move 31
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [24, 11]
        assert cond is None

        # move 32
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 6, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [25, 11]
        assert cond.name == "WIN"
