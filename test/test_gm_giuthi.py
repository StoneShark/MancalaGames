# -*- coding: utf-8 -*-
"""Test giuthi

Created on Thu Jul 11 17:56:04 2024
@author: Ann"""

import pytest
pytestmark = pytest.mark.integtest

from context import game_interface as gi
from context import man_config


CW = gi.Direct.CW
CCW = gi.Direct.CCW



class TestGiuthi:

    @pytest.fixture
    def game_data(self):
        return man_config.make_game('./GameProps/Giuthi.txt')


    def test_t_win(self, game_data):

        game, _ = game_data
        game.turn = True
        game.starter = True
        game.board = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        game.blocked = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        game.unlocked = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        game.child = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        game.owner = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        game.store = [0, 0]

        # move 1
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 6, 6, 6, 6, 6, 6, 0, 2, 9, 9, 9, 9, 9, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond.name == "REPEAT_TURN"

        # move 2
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [9, 9, 9, 9, 1, 7, 7, 0, 0, 2, 9, 0, 10, 0, 12, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 8]
        assert cond is None

        # move 3
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [11, 11, 11, 11, 3, 1, 8, 1, 1, 3, 10, 1, 10, 0, 0, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 8]
        assert cond is None

        # move 4
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [11, 11, 11, 11, 3, 1, 8, 1, 1, 0, 12, 0, 14, 1, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 8]
        assert cond.name == "REPEAT_TURN"

        # move 5
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 12, 12, 12, 1, 0, 0, 0, 6, 0, 0, 4, 18, 1, 2, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 23]
        assert cond is None

        # move 6
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 12, 12, 1, 0, 1, 1, 7, 1, 0, 5, 19, 2, 3, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 23]
        assert cond is None

        # move 7
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [2, 0, 12, 12, 1, 0, 1, 1, 7, 1, 1, 6, 20, 3, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 23]
        assert cond.name == "REPEAT_TURN"

        # move 8
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 12, 1, 0, 1, 1, 7, 1, 1, 6, 20, 0, 6, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 36]
        assert cond is None

        # move 9
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [3, 3, 3, 0, 0, 3, 1, 4, 1, 1, 1, 0, 25, 1, 11, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 36]
        assert cond is None

        # move 10
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 1, 7, 1, 1, 1, 1, 6, 3, 7, 2, 7, 0, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [2, 47]
        assert cond is None

        # move 11
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [5, 2, 3, 0, 3, 0, 4, 0, 0, 6, 3, 7, 2, 0, 2, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 47]
        assert cond is None

        # move 12
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [5, 2, 3, 0, 3, 0, 4, 0, 0, 6, 0, 8, 3, 1, 2, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 47]
        assert cond.name == "REPEAT_TURN"

        # move 13
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 6, 3, 0, 1, 1, 3, 3, 9, 3, 0, 1, 3, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond is None

        # move 14
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 2, 7, 0, 0, 1, 1, 3, 3, 9, 3, 0, 1, 3, 4, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 15
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [2, 3, 0, 0, 0, 1, 1, 3, 3, 9, 3, 1, 2, 4, 5, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond is None

        # move 16
        cond = game.move((7, CW))
        assert game.turn is False
        assert game.board == [2, 3, 1, 1, 1, 1, 4, 0, 0, 9, 3, 1, 2, 4, 5, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond is None

        # move 17
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 9, 3, 1, 2, 4, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond is None

        # move 18
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 9, 0, 3, 1, 5, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 19
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 12, 0, 0, 1, 5, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 20
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 2, 0, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 21
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 0, 2, 3, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 22
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 0, 2, 1, 3, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 23
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 3, 2, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 24
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 3, 1, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"

        # move 25
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [2, 5, 1, 1, 4, 0, 0, 2, 2, 0, 0, 2, 4, 2, 3, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 63]
        assert cond is None

        # move 26
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 2, 2, 0, 0, 2, 4, 2, 3, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 63]
        assert cond.name == "REPEAT_TURN"

        # move 27
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 0, 3, 1, 0, 2, 4, 2, 3, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 63]
        assert cond is None

        # move 28
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 2, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 63]
        assert cond.name == "REPEAT_TURN"

        # move 29
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 1, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 63]
        assert cond.name == "REPEAT_TURN"

        # move 30
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 4, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 1, 0, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 72]
        assert cond is None

        # move 31
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 1, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 72]
        assert cond is None

        # move 32
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 4, 2, 2, 2, 0, 1, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 72]
        assert cond is None

        # move 33
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 4, 2, 2, 2, 0, 1, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 72]
        assert cond is None

        # move 34
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 0, 1, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 74]
        assert cond is None

        # move 35
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 0, 1, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 74]
        assert cond is None

        # move 36
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 74]
        assert cond.name == "REPEAT_TURN"

        # move 37
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 38
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 39
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 40
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 41
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 2, 4, 1, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"

        # move 42
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 2, 0, 2, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 43
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 2, 0, 2, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 44
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 1, 1, 2, 0, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"

        # move 45
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 3, 1, 0, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"

        # move 46
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 2, 1, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"

        # move 47
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 1, 3, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"

        # move 48
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 1, 0, 0, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 49
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 1, 0, 0, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 50
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 2, 1, 1, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"

        # move 51
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 4, 0, 3, 2, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"

        # move 52
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 3, 2, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 53
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 3, 2, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 76]
        assert cond is None

        # move 54
        cond = game.move((7, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 80]
        assert cond is None

        # move 55
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 80]
        assert cond is None

        # move 56
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 0, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 82]
        assert cond is None

        # move 57
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 0, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 82]
        assert cond is None

        # move 58
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1, 4, 2, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 82]
        assert cond.name == "REPEAT_TURN"

        # move 59
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 6, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 82]
        assert cond.name == "REPEAT_TURN"

        # move 60
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 82]
        assert cond is None

        # move 61
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 82]
        assert cond is None

        # move 62
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [4, 82]
        assert cond.name == "REPEAT_TURN"

        # move 63
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [9, 87]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 78]

        # move 1
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 78]
        assert cond.name == "REPEAT_TURN"

        # move 2
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 78]
        assert cond.name == "REPEAT_TURN"

        # move 3
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 80]
        assert cond is None

        # move 4
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 80]
        assert cond is None

        # move 5
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond is None

        # move 6
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond is None

        # move 7
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond is None

        # move 8
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [4, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond is None

        # move 9
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [4, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond.name == "REPEAT_TURN"

        # move 10
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [4, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond is None

        # move 11
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 2, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond is None

        # move 12
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 83]
        assert cond.name == "REPEAT_TURN"

        # move 13
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [6, 90]
        assert cond.name == "WIN"


    def test_f_win(self, game_data):

        game, _ = game_data
        game.turn = False
        game.starter = False
        game.board = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        game.blocked = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        game.unlocked = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        game.child = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        game.owner = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        game.store = [0, 0]

        # move 1
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [1, 9, 9, 9, 9, 9, 2, 0, 6, 6, 6, 6, 6, 6, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond.name == "REPEAT_TURN"

        # move 2
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [4, 12, 0, 10, 0, 9, 2, 0, 0, 7, 7, 1, 9, 9, 9, 9]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [8, 0]
        assert cond is None

        # move 3
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [5, 13, 1, 11, 1, 10, 3, 1, 0, 7, 7, 1, 9, 9, 0, 10]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [8, 0]
        assert cond is None

        # move 4
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [6, 0, 2, 12, 1, 13, 0, 2, 1, 8, 8, 2, 10, 10, 0, 11]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [10, 0]
        assert cond is None

        # move 5
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [5, 1, 7, 19, 8, 2, 9, 3, 0, 15, 3, 8, 3, 1, 0, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [10, 0]
        assert cond is None

        # move 6
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [10, 6, 12, 5, 14, 0, 0, 4, 1, 0, 0, 0, 6, 4, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [31, 0]
        assert cond is None

        # move 7
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [10, 6, 12, 5, 14, 0, 1, 5, 2, 1, 1, 1, 0, 4, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [31, 0]
        assert cond is None

        # move 8
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [10, 1, 14, 7, 16, 2, 3, 0, 2, 1, 1, 1, 0, 4, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [31, 0]
        assert cond.name == "REPEAT_TURN"

        # move 9
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [10, 1, 14, 7, 16, 0, 4, 1, 2, 1, 1, 1, 0, 4, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [31, 0]
        assert cond.name == "REPEAT_TURN"

        # move 10
        cond = game.move((6, CW))
        assert game.turn is True
        assert game.board == [13, 0, 0, 9, 18, 2, 1, 2, 3, 2, 2, 2, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [41, 0]
        assert cond is None

        # move 11
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [13, 0, 0, 9, 18, 2, 1, 2, 0, 4, 0, 5, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [41, 0]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 10, 19, 3, 2, 3, 1, 5, 1, 1, 3, 2, 2, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [41, 0]
        assert cond is None

        # move 13
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [2, 1, 5, 0, 1, 4, 0, 7, 5, 0, 0, 3, 5, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [51, 0]
        assert cond is None

        # move 14
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [2, 1, 5, 0, 1, 4, 0, 7, 5, 0, 0, 0, 7, 6, 6, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [51, 0]
        assert cond.name == "REPEAT_TURN"

        # move 15
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 5, 0, 1, 4, 0, 0, 7, 2, 2, 2, 9, 0, 9, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [51, 3]
        assert cond is None

        # move 16
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 1, 8, 0, 2, 0, 0, 0, 7, 2, 2, 2, 9, 0, 9, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [51, 3]
        assert cond.name == "REPEAT_TURN"

        # move 17
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 2, 1, 1, 1, 1, 0, 5, 5, 1, 10, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [63, 3]
        assert cond is None

        # move 18
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 3, 2, 2, 2, 2, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [63, 3]
        assert cond is None

        # move 19
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 3, 1, 5, 2, 0, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"

        # move 20
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 1, 0, 2, 0, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"

        # move 21
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 0, 2, 1, 0, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"

        # move 22
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 0, 0, 2, 1, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"

        # move 23
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 5, 7, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond is None

        # move 24
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond is None

        # move 25
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 3, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond is None

        # move 26
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 3, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond is None

        # move 27
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 4, 0, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 28
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 7, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 29
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond is None

        # move 30
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [1, 1, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond is None

        # move 31
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 3, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 32
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 33
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 3, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 34
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 35
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 3, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 36
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"

        # move 37
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [85, 11]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [74, 0]

        # move 1
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [77, 0]
        assert cond is None

        # move 2
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [77, 0]
        assert cond is None

        # move 3
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond is None

        # move 4
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond is None

        # move 5
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond is None

        # move 6
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond is None

        # move 7
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 3, 4, 4, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond is None

        # move 8
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 3, 4, 4, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond is None

        # move 9
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 4, 4, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"

        # move 10
        cond = game.move((7, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 4, 0, 5, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"

        # move 11
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"

        # move 13
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond is None

        # move 14
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [3, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond is None

        # move 15
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond is None

        # move 16
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond is None

        # move 17
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [3, 0, 1, 3, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond is None

        # move 18
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [3, 0, 1, 3, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond is None

        # move 19
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 2, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond.name == "REPEAT_TURN"

        # move 20
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 0, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [81, 0]
        assert cond.name == "REPEAT_TURN"

        # move 21
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 1, 0, 1, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [84, 0]
        assert cond is None

        # move 22
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [84, 0]
        assert cond is None

        # move 23
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 1, 1, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [84, 0]
        assert cond.name == "REPEAT_TURN"

        # move 24
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 0, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [84, 0]
        assert cond.name == "REPEAT_TURN"

        # move 25
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [84, 0]
        assert cond is None

        # move 26
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [84, 0]
        assert cond is None

        # move 27
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.owner == [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        assert game.store == [89, 7]
        assert cond.name == "WIN"
