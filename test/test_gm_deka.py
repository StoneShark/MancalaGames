# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:23:34 2023
@author: Ann"""

import pytest
pytestmark = [pytest.mark.integtest]

from context import man_config


N = None
T = True
F = False

class TestDeka:

    @pytest.fixture
    def game_data(self):

        return man_config.make_game('./GameProps/Deka.txt')


    def test_deka_1(self, game_data):

        game, _ = game_data

        game.turn = False
        game.starter = False
        game.board = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        game.blocked = [F, F, F, F, F, F, F, F, F, F, F, F]
        game.unlocked = [T, T, T, T, T, T, T, T, T, T, T, T]
        game.child = [N, N, N, N, N, N, N, N, N, N, N, N]
        game.owner = [N, N, N, N, N, N, N, N, N, N, N, N]
        game.store = [0, 0]

        # move 1
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 0, 3, 3, 0, 1, 4, 1, 3, 3, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 0, 3, 3, 0, 1, 0, 2, 4, 4, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 6, 1, 1, 0, 0, 0, 6, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 3, 1, 7, 0, 2, 1, 0, 0, 6, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None

        # move 5
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 2, 8, 1, 2, 1, 0, 0, 6, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None

        # move 6
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 0, 2, 8, 1, 2, 1, 0, 0, 6, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 0, 0, 9, 0, 3, 0, 0, 1, 6, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None

        # move 8
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 1, 2, 1, 0, 1, 0, 4, 1, 3, 3]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None

        # move 9
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 1, 2, 0, 1, 1, 0, 4, 1, 3, 3]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None

        # move 10
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 1, 2, 0, 1, 1, 0, 0, 2, 4, 4]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [6, 0]
        assert cond is None

        # move 11
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 1, 2, 0, 0, 0, 0, 1, 2, 4, 4]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [7, 0]
        assert cond is None

        # move 12
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 4, 2, 3, 1, 0, 0, 0, 1, 0, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None

        # move 13
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 4, 2, 3, 0, 1, 0, 0, 1, 0, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None

        # move 14
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 4, 2, 3, 0, 1, 0, 0, 0, 1, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None

        # move 15
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 4, 2, 0, 1, 2, 1, 0, 0, 1, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None

        # move 16
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 4, 2, 0, 1, 2, 0, 0, 1, 1, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None

        # move 17
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 4, 2, 3, 1, 1, 0, 0, 2, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None

        # move 18
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 5, 0, 4, 2, 0, 0, 1, 1, 1, 0]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 0]
        assert cond is None

        # move 19
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 5, 3, 1, 0, 0, 2, 0, 1]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [11, 0]
        assert cond is None

        # move 20
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 5, 3, 1, 0, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [13, 0]
        assert cond is None

        # move 21
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 4, 2, 0, 1, 1, 1, 0]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 0]
        assert cond is None

        # move 22
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 4, 2, 0, 0, 0, 2, 1]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 0]
        assert cond is None

        # move 23
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 4, 2, 0, 0, 0, 2, 1]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 0]
        assert cond is None

        # move 24
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 4, 2, 0, 0, 0, 0, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [15, 0]
        assert cond is None

        # move 25
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 3, 0, 1, 1, 0, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 0]
        assert cond is None

        # move 26
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 1, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 0]
        assert cond is None

        # move 27
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 3, 0, 1, 0, 1, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 0]
        assert cond is None

        # move 28
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 3]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [17, 0]
        assert cond is None

        # move 29
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 3]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [17, 0]
        assert cond is None

        # move 30
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 3]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [17, 0]
        assert cond.name == "WIN"


    def test_deka_2(self, game_data):

        game, _ = game_data

        game.turn = False
        game.starter = False
        game.board = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        game.blocked = [F, F, F, F, F, F, F, F, F, F, F, F]
        game.unlocked = [T, T, T, T, T, T, T, T, T, T, T, T]
        game.child = [N, N, N, N, N, N, N, N, N, N, N, N]
        game.owner = [N, N, N, N, N, N, N, N, N, N, N, N]
        game.store = [0, 0]

        # move 1
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 0, 3, 3, 0, 1, 4, 1, 3, 3, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 4, 4, 1, 1, 4, 1, 3, 0, 1, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 0, 2, 7, 1, 3, 1, 0, 5, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [4, 0, 4, 1, 2, 4, 1, 0, 1, 4, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 0, 0, 2, 3, 5, 0, 0, 0, 5, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None

        # move 6
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 1, 1, 2, 3, 5, 0, 0, 0, 5, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 1, 0, 0, 4, 6, 1, 0, 0, 5, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None

        # move 8
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 2, 1, 1, 4, 6, 1, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None

        # move 9
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 3, 1, 6, 1, 3, 0, 1, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None

        # move 10
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 7, 2, 1, 0, 2, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None

        # move 11
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 8, 3, 0, 0, 0, 3, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [7, 0]
        assert cond is None

        # move 12
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 2, 1, 4, 1, 0, 0, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [7, 0]
        assert cond is None

        # move 13
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 5, 0, 0, 0, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None

        # move 14
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 3, 1, 0, 2, 5, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None

        # move 15
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 3, 1, 0, 0, 6, 1, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None

        # move 16
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 3, 0, 2, 1, 2, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None

        # move 17
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 0, 4, 1, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 0]
        assert cond.name == "WIN"
