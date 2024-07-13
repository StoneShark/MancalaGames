# -*- coding: utf-8 -*-
"""Integration test of weg:
    4 rounds, round wins by both players
    start turns alternate
    wegs made on both sides of the board by owner (not side)
    captures by both players
    move passes
    game winner at 10 holes owned

Created on Fri Jun 28 08:00:54 2024
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest


from context import man_config

T = True
F = False
N = None


class TestWeg:

    @pytest.fixture
    def game_data(self):
        return man_config.make_game('./GameProps/Weg.txt')

    def test_it(self, game_data):

        game = game_data[0]

        game.turn = False
        game.starter = False

        # move 1
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [6, 0, 1, 6, 6, 2, 7, 1, 6, 1, 6, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [7, 1, 1, 6, 6, 2, 0, 2, 7, 2, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [8, 1, 1, 8, 1, 4, 2, 4, 8, 3, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, F, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [0, 2, 2, 9, 2, 5, 3, 5, 9, 1, 9, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, F, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 2, 0, 10, 0, 6, 4, 6, 9, 1, 9, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, F, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [2, 4, 2, 12, 2, 8, 2, 7, 0, 3, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, F, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 2]
        assert cond.name == "REPEAT_TURN"

        # move 7
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [1, 6, 4, 1, 4, 9, 3, 8, 1, 1, 3, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 2]
        assert cond is None

        # move 8
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [0, 0, 5, 2, 5, 10, 4, 9, 0, 2, 4, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 2]
        assert cond is None

        # move 9
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [2, 2, 7, 4, 7, 0, 5, 10, 1, 1, 6, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 2]
        assert cond is None

        # move 10
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [2, 2, 7, 0, 8, 1, 6, 11, 1, 1, 6, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 2]
        assert cond is None

        # move 11
        cond = game.move((0, 2, None))
        assert game.turn is True
        assert game.board == [2, 2, 7, 0, 8, 1, 6, 11, 1, 0, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 4]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [0, 3, 8, 1, 8, 1, 6, 11, 1, 0, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None

        # move 13
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [0, 3, 8, 0, 7, 1, 6, 11, 1, 0, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 4]
        assert cond.name == "REPEAT_TURN"

        # move 14
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [0, 0, 9, 1, 6, 1, 6, 11, 1, 0, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond.name == "REPEAT_TURN"

        # move 15
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 7, 2, 7, 12, 2, 1, 6, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 16
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 7, 2, 0, 13, 3, 2, 7, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 17
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [1, 0, 1, 2, 7, 2, 0, 13, 3, 2, 7, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 18
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 3, 8, 2, 0, 13, 0, 3, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 19
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [0, 2, 1, 3, 8, 2, 0, 13, 0, 3, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 20
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [1, 2, 1, 3, 8, 2, 0, 13, 0, 0, 9, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 21
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 9, 3, 1, 14, 0, 0, 9, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 22
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [0, 3, 1, 0, 9, 3, 1, 14, 0, 0, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 23
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 9, 3, 1, 14, 0, 0, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 24
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 9, 3, 0, 13, 0, 0, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond.name == "REPEAT_TURN"

        # move 25
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 9, 3, 0, 13, 0, 0, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 26
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 8, 3, 0, 13, 0, 0, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 6]
        assert cond.name == "REPEAT_TURN"

        # move 27
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 8, 0, 1, 14, 1, 0, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 6]
        assert cond is None

        # move 28
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 8, 0, 0, 13, 1, 0, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 8]
        assert cond.name == "REPEAT_TURN"

        # move 29
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 8, 0, 0, 13, 0, 1, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 8]
        assert cond is None

        # move 30
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 7, 0, 0, 13, 0, 1, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 8]
        assert cond.name == "REPEAT_TURN"

        # move 31
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 6, 0, 0, 13, 0, 1, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 8]
        assert cond.name == "REPEAT_TURN"

        # move 32
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 6, 0, 0, 13, 0, 1, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 8]
        assert cond is None

        # move 33
        cond = game.move((0, 2, None))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 6, 0, 0, 13, 0, 0, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 10]
        assert cond.name == "REPEAT_TURN"

        # move 34
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 6, 0, 0, 13, 0, 0, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 10]
        assert cond is None

        # move 35
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 5, 0, 0, 13, 0, 0, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, F, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 10]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]

        # move 1
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [1, 6, 1, 6, 6, 6, 0, 1, 6, 6, 2, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [5, 1, 3, 0, 1, 10, 0, 5, 2, 10, 0, 11]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [7, 0, 5, 2, 0, 12, 2, 1, 3, 1, 2, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [3, 1, 8, 5, 0, 15, 5, 0, 6, 0, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [6, 1, 1, 7, 0, 17, 0, 2, 2, 3, 8, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [7, 0, 1, 1, 1, 18, 1, 3, 3, 4, 9, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 7
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [8, 1, 1, 1, 1, 18, 1, 3, 3, 0, 10, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 8
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [8, 1, 1, 0, 0, 19, 0, 4, 4, 0, 10, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 9
        cond = game.move((0, 1, None))
        assert game.turn is True
        assert game.board == [9, 2, 2, 1, 1, 20, 1, 5, 3, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 2]
        assert cond.name == "REPEAT_TURN"

        # move 10
        cond = game.move((0, 0, None))
        assert game.turn is True
        assert game.board == [10, 0, 3, 2, 0, 21, 0, 6, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 4]
        assert cond.name == "REPEAT_TURN"

        # move 11
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [10, 0, 3, 2, 0, 21, 0, 6, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None

        # move 12
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [13, 3, 6, 1, 0, 1, 4, 1, 6, 3, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None

        # move 13
        # weg created by True on True side of board
        # but it's right because False is hole owner
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [2, 6, 1, 4, 0, 4, 7, 4, 8, 2, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None

        # move 14
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [0, 7, 2, 0, 1, 1, 9, 6, 10, 0, 1, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None

        # move 15
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [2, 9, 4, 2, 0, 3, 1, 8, 11, 1, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None

        # move 16
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [3, 1, 5, 3, 1, 4, 2, 9, 12, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None

        # move 17
        cond = game.move((0, 2, None))
        assert game.turn is True
        assert game.board == [4, 2, 0, 4, 2, 5, 3, 10, 11, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 6]
        assert cond.name == "REPEAT_TURN"

        # move 18
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [4, 2, 0, 4, 2, 5, 3, 10, 11, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 6]
        assert cond is None

        # move 19
        # False capture from True's weg on True side of board (correct)
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [4, 2, 0, 0, 3, 6, 4, 9, 11, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond.name == "REPEAT_TURN"

        # move 20
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [4, 0, 1, 1, 3, 6, 4, 9, 11, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 21
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 1, 2, 2, 4, 0, 5, 10, 12, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 22
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 5, 1, 5, 10, 12, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 23
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 6, 0, 6, 11, 12, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 24
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [1, 2, 0, 1, 6, 0, 0, 12, 13, 2, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 25
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [0, 3, 1, 1, 6, 0, 0, 12, 13, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 26
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [0, 3, 1, 1, 0, 1, 1, 13, 14, 3, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 27
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 4, 1, 1, 0, 1, 1, 13, 14, 3, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 28
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [1, 4, 1, 0, 1, 1, 1, 13, 14, 3, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 6]
        assert cond is None

        # move 29
        cond = game.move((0, 2, None))
        assert game.turn is True
        assert game.board == [0, 5, 0, 1, 0, 2, 0, 14, 13, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond.name == "REPEAT_TURN"

        # move 30
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [1, 5, 0, 1, 0, 2, 0, 14, 13, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond is None

        # move 31
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [1, 5, 0, 0, 1, 2, 0, 14, 13, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond is None

        # move 32
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [2, 6, 0, 0, 1, 2, 0, 14, 13, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond is None

        # move 33
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [2, 6, 0, 0, 0, 0, 1, 15, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond is None

        # move 34
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [2, 6, 0, 0, 0, 0, 1, 15, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond is None

        # move 35
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [0, 7, 1, 0, 0, 0, 1, 15, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond is None

        # move 36
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 7, 1, 0, 0, 0, 1, 15, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [2, 8]
        assert cond is None

        # move 37
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [0, 7, 1, 0, 0, 0, 0, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond.name == "REPEAT_TURN"

        # move 38
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 7, 0, 1, 0, 0, 0, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 39
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 7, 0, 1, 0, 0, 0, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 40
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [0, 7, 0, 0, 1, 0, 0, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 41
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 7, 0, 0, 1, 0, 0, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 42
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [0, 7, 0, 0, 0, 1, 0, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 43
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 7, 0, 0, 0, 1, 0, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 44
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [0, 7, 0, 0, 0, 0, 1, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 45
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 7, 0, 0, 0, 0, 1, 14, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 46
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [0, 7, 0, 0, 0, 0, 0, 13, 14, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, T, F, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [6, 8]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

        # move 1
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [6, 2, 7, 1, 6, 1, 6, 6, 6, 0, 1, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move((1, 0, None))
        assert game.turn is False
        assert game.board == [1, 4, 8, 2, 7, 2, 0, 7, 7, 1, 2, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [3, 4, 9, 1, 0, 1, 2, 9, 1, 3, 4, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond.name == "REPEAT_TURN"

        # move 4
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [3, 4, 9, 1, 0, 0, 0, 10, 2, 4, 4, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 5
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [1, 7, 2, 4, 3, 1, 3, 1, 4, 6, 2, 12]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 6
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [1, 7, 2, 4, 0, 2, 4, 0, 5, 7, 2, 12]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 7
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [2, 8, 2, 4, 0, 2, 0, 1, 6, 8, 0, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 8
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [2, 8, 2, 4, 0, 0, 1, 0, 7, 9, 0, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 9
        cond = game.move((1, 0, None))
        assert game.turn is False
        assert game.board == [0, 9, 0, 5, 1, 1, 1, 0, 7, 9, 0, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 10
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [0, 9, 0, 5, 0, 0, 2, 1, 7, 9, 0, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 11
        cond = game.move((0, 3, None))
        assert game.turn is True
        assert game.board == [1, 10, 1, 0, 1, 1, 3, 2, 1, 9, 1, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [4, 13, 0, 2, 3, 0, 5, 4, 0, 11, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 13
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [4, 13, 0, 0, 4, 1, 5, 4, 0, 11, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 14
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [1, 14, 1, 1, 5, 0, 6, 0, 1, 12, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 15
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [1, 14, 1, 1, 0, 1, 7, 1, 2, 13, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 16
        cond = game.move((1, 0, None))
        assert game.turn is False
        assert game.board == [0, 15, 1, 1, 0, 1, 7, 1, 2, 13, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 17
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [0, 15, 1, 0, 1, 1, 7, 1, 2, 13, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 18
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [2, 17, 1, 1, 0, 2, 0, 2, 3, 14, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 19
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [2, 17, 1, 0, 1, 2, 0, 2, 3, 14, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 20
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [0, 18, 2, 1, 1, 2, 0, 2, 3, 14, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 21
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 18, 0, 2, 0, 3, 1, 2, 3, 14, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 22
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [1, 18, 0, 2, 0, 3, 0, 0, 4, 15, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 2]
        assert cond is None

        # move 23
        cond = game.move((1, 5, None))
        assert game.turn is False
        assert game.board == [2, 17, 0, 2, 0, 0, 1, 1, 0, 16, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 2]
        assert cond.name == "REPEAT_TURN"

        # move 24
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [2, 17, 0, 0, 1, 1, 1, 1, 0, 16, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 2]
        assert cond is None

        # move 25
        cond = game.move((0, 4, None))
        assert game.turn is False
        assert game.board == [2, 17, 0, 0, 1, 1, 1, 0, 1, 16, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 2]
        assert cond is None

        # move 26
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [2, 17, 0, 0, 0, 0, 2, 1, 1, 16, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 2]
        assert cond is None

        # move 27
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [3, 18, 0, 0, 0, 0, 2, 1, 1, 16, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 2]
        assert cond is None

        # move 28
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [3, 18, 0, 0, 0, 0, 2, 1, 1, 16, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 2]
        assert cond is None

        # move 29
        cond = game.move((0, 3, None))
        assert game.turn is True
        assert game.board == [3, 18, 0, 0, 0, 0, 2, 1, 0, 15, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond.name == "REPEAT_TURN"

        # move 30
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [3, 18, 0, 0, 0, 0, 0, 2, 1, 15, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 31
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [3, 18, 0, 0, 0, 0, 0, 2, 1, 15, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 4]
        assert cond is None

        # move 32
        cond = game.move((0, 3, None))
        assert game.turn is True
        assert game.board == [3, 18, 0, 0, 0, 0, 0, 2, 0, 14, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond.name == "REPEAT_TURN"

        # move 33
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [3, 18, 0, 0, 0, 0, 0, 2, 0, 14, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 34
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [3, 18, 0, 0, 0, 0, 0, 2, 0, 14, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 35
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [0, 19, 1, 1, 1, 0, 0, 2, 0, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 36
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [0, 19, 1, 0, 0, 1, 1, 2, 0, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 37
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [0, 19, 1, 0, 0, 1, 0, 0, 1, 15, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 38
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [0, 19, 1, 0, 0, 0, 1, 0, 1, 15, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 39
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [0, 19, 1, 0, 0, 0, 1, 0, 1, 15, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 40
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 19, 0, 1, 0, 0, 1, 0, 1, 15, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 41
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 19, 0, 1, 0, 0, 1, 0, 1, 15, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 42
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [1, 19, 0, 0, 1, 0, 1, 0, 1, 15, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 6]
        assert cond is None

        # move 43
        cond = game.move((0, 3, None))
        assert game.turn is True
        assert game.board == [1, 19, 0, 0, 1, 0, 1, 0, 0, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond.name == "REPEAT_TURN"

        # move 44
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [1, 19, 0, 0, 1, 0, 0, 1, 0, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 45
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [1, 19, 0, 0, 0, 1, 0, 1, 0, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 46
        cond = game.move((0, 4, None))
        assert game.turn is False
        assert game.board == [1, 19, 0, 0, 0, 1, 0, 0, 1, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 47
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [1, 19, 0, 0, 0, 0, 1, 0, 1, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None

        # move 48
        cond = game.move((0, 3, None))
        assert game.turn is True
        assert game.board == [1, 19, 0, 0, 0, 0, 1, 0, 0, 13, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 10]
        assert cond.name == "REPEAT_TURN"

        # move 49
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [1, 19, 0, 0, 0, 0, 0, 1, 0, 13, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 10]
        assert cond is None

        # move 50
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 19, 0, 0, 0, 0, 0, 1, 0, 13, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 10]
        assert cond is None

        # move 51
        cond = game.move((0, 4, None))
        assert game.turn is False
        assert game.board == [1, 19, 0, 0, 0, 0, 0, 0, 1, 13, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 10]
        assert cond is None

        # move 52
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 19, 0, 0, 0, 0, 0, 0, 1, 13, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 10]
        assert cond is None

        # move 53
        cond = game.move((1, 0, None))
        assert game.turn is False
        assert game.board == [0, 20, 0, 0, 0, 0, 0, 0, 1, 13, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 10]
        assert cond is None

        # move 54
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 20, 0, 0, 0, 0, 0, 0, 1, 13, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 10]
        assert cond is None

        # move 55
        cond = game.move((0, 3, None))
        assert game.turn is True
        assert game.board == [0, 20, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, T, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 12]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

        # move 1
        cond = game.move((0, 4, None))
        assert game.turn is False
        assert game.board == [6, 6, 6, 0, 1, 6, 6, 2, 7, 1, 6, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [0, 4, 1, 4, 5, 2, 11, 2, 3, 1, 11, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [0, 6, 0, 1, 7, 4, 12, 3, 0, 2, 12, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [4, 6, 3, 0, 1, 12, 3, 4, 5, 9, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [5, 0, 4, 1, 2, 13, 4, 5, 1, 10, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [6, 1, 1, 2, 3, 14, 0, 6, 2, 11, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 7
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [8, 0, 3, 4, 0, 16, 2, 8, 1, 0, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 8
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [8, 0, 3, 0, 1, 17, 3, 9, 1, 0, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 9
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [8, 0, 3, 0, 1, 17, 3, 9, 0, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 10
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [8, 0, 3, 0, 0, 16, 3, 9, 0, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond.name == "REPEAT_TURN"

        # move 11
        cond = game.move((1, 2, None))
        assert game.turn is False
        assert game.board == [8, 0, 0, 1, 1, 15, 3, 9, 0, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 0]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [8, 0, 0, 1, 0, 14, 3, 9, 0, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 0]
        assert cond.name == "REPEAT_TURN"

        # move 13
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [8, 0, 0, 0, 1, 14, 3, 9, 0, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 0]
        assert cond is None

        # move 14
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [9, 1, 0, 0, 1, 14, 0, 10, 1, 0, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 0]
        assert cond is None

        # move 15
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [9, 1, 0, 0, 0, 13, 0, 10, 1, 0, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 0]
        assert cond.name == "REPEAT_TURN"

        # move 16
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [9, 1, 0, 0, 0, 13, 0, 10, 1, 0, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 17
        cond = game.move((1, 0, None))
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 1, 14, 1, 11, 2, 1, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 18
        cond = game.move((1, 2, None))
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 2, 13, 1, 11, 2, 1, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 0]
        assert cond.name == "REPEAT_TURN"

        # move 19
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 14, 0, 12, 0, 2, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 0]
        assert cond is None

        # move 20
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [1, 3, 1, 1, 1, 15, 0, 12, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 0]
        assert cond is None

        # move 21
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [1, 3, 1, 1, 0, 14, 0, 12, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond.name == "REPEAT_TURN"

        # move 22
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [1, 3, 1, 0, 1, 14, 0, 12, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 23
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 0, 15, 1, 12, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 24
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 1, 15, 1, 12, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 25
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [2, 1, 1, 2, 1, 15, 1, 12, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 26
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [2, 1, 1, 2, 0, 14, 1, 12, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [14, 0]
        assert cond.name == "REPEAT_TURN"

        # move 27
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 1, 15, 0, 13, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [14, 0]
        assert cond is None

        # move 28
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 1, 15, 0, 13, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [14, 0]
        assert cond is None

        # move 29
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 0, 14, 0, 13, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond.name == "REPEAT_TURN"

        # move 30
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 0, 14, 0, 13, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 31
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 0, 14, 0, 13, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 32
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 0, 14, 0, 13, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 33
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 0, 14, 0, 13, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 34
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 0, 14, 0, 13, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 35
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 0, 14, 0, 13, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 36
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 0, 14, 0, 13, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 37
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 15, 0, 13, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond is None

        # move 38
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 14, 0, 13, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [18, 0]
        assert cond.name == "REPEAT_TURN"

        # move 39
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 14, 0, 13, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [18, 0]
        assert cond is None

        # move 40
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 14, 0, 13, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [18, 0]
        assert cond is None

        # move 41
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 14, 0, 13, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [18, 0]
        assert cond is None

        # move 42
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 14, 0, 13, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [18, 0]
        assert cond is None

        # move 43
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 13, 0, 13, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond.name == "REPEAT_TURN"

        # move 44
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 13, 0, 13, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 45
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 13, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 46
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 13, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 47
        cond = game.move((1, 0, None))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 13, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 48
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 12, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond.name == "REPEAT_TURN"

        # move 49
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 12, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 50
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 12, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 51
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 12, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 52
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 12, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 53
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 12, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 54
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 12, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 55
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 11, 0, 13, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, F, N, N, N, N]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 0]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]

        # move 1
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [6, 6, 2, 7, 1, 6, 1, 6, 6, 6, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [8, 8, 4, 0, 2, 7, 2, 7, 7, 1, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [10, 10, 6, 2, 1, 8, 1, 0, 1, 3, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 1, 8, 4, 3, 10, 3, 2, 3, 5, 6, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [3, 3, 10, 2, 6, 1, 5, 1, 5, 7, 1, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [4, 4, 11, 3, 0, 2, 6, 2, 6, 8, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 7
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [0, 5, 12, 4, 1, 1, 7, 0, 7, 9, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 8
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [2, 7, 14, 5, 2, 2, 0, 1, 8, 1, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 9
        cond = game.move((1, 0, None))
        assert game.turn is False
        assert game.board == [0, 8, 13, 5, 2, 2, 0, 1, 8, 1, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond.name == "REPEAT_TURN"

        # move 10
        cond = game.move((0, 4, None))
        assert game.turn is True
        assert game.board == [1, 9, 14, 6, 3, 0, 1, 1, 1, 2, 3, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 11
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [2, 10, 15, 7, 4, 0, 1, 1, 1, 2, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 12
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [2, 0, 16, 8, 5, 1, 2, 2, 2, 3, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 13
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 1, 17, 0, 6, 2, 3, 3, 3, 4, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 14
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [0, 0, 18, 1, 6, 2, 3, 3, 3, 4, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 15
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [1, 1, 18, 1, 6, 2, 3, 3, 3, 0, 6, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 16
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [1, 0, 19, 0, 7, 0, 4, 4, 0, 1, 7, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 17
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [2, 1, 20, 1, 8, 1, 4, 4, 0, 1, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 18
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [2, 1, 20, 1, 8, 1, 0, 5, 1, 2, 1, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 19
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [3, 2, 21, 2, 9, 1, 0, 5, 1, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 20
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [3, 2, 21, 2, 9, 0, 1, 5, 1, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 21
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [4, 2, 21, 2, 9, 0, 1, 5, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 22
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [4, 2, 21, 0, 10, 1, 1, 5, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 23
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [5, 2, 21, 0, 10, 1, 1, 5, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 24
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [5, 0, 22, 1, 10, 1, 1, 5, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 25
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [5, 0, 22, 1, 10, 1, 1, 5, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [2, 0]
        assert cond is None

        # move 26
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [5, 0, 22, 0, 9, 1, 1, 5, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [4, 0]
        assert cond.name == "REPEAT_TURN"

        # move 27
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [6, 1, 22, 0, 9, 1, 0, 0, 2, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [4, 0]
        assert cond is None

        # move 28
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [7, 1, 22, 0, 9, 1, 0, 0, 2, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [4, 0]
        assert cond is None

        # move 29
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [7, 0, 21, 0, 9, 1, 0, 0, 2, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [6, 0]
        assert cond.name == "REPEAT_TURN"

        # move 30
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [6, 0, 21, 0, 9, 1, 0, 0, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond.name == "REPEAT_TURN"

        # move 31
        cond = game.move((1, 5, None))
        assert game.turn is True
        assert game.board == [6, 0, 21, 0, 9, 0, 1, 0, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 32
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [7, 0, 21, 0, 9, 0, 1, 0, 0, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 33
        cond = game.move((0, 5, None))
        assert game.turn is True
        assert game.board == [7, 0, 21, 0, 9, 0, 0, 1, 0, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 34
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [7, 0, 21, 0, 9, 0, 0, 1, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 35
        cond = game.move((0, 4, None))
        assert game.turn is True
        assert game.board == [7, 0, 21, 0, 9, 0, 0, 0, 1, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 36
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [8, 0, 21, 0, 9, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 37
        cond = game.move((0, 3, None))
        assert game.turn is True
        assert game.board == [8, 0, 21, 0, 9, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 38
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [8, 0, 21, 0, 9, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 39
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [8, 0, 21, 0, 9, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 40
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [9, 0, 21, 0, 9, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 41
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [9, 0, 21, 0, 9, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 42
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [9, 0, 21, 0, 9, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 43
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [9, 0, 21, 0, 9, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 44
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [9, 0, 21, 0, 9, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 45
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [9, 0, 21, 0, 9, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond is None

        # move 46
        cond = game.move((0, 0, None))
        assert game.turn is True
        assert game.board == [10, 0, 21, 0, 9, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, T, N, T, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 0]
        assert cond.name == "WIN"



    def test_with_single_capt(self, game_data):
        """This game includes captures of only one seed
        (i.e. weg has no seeds to begin with)
        Look for stores with odd number of seeds."""

        game = game_data[0]

        game.turn = False
        game.starter = False
        game.board = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        game.blocked = [F, F, F, F, F, F, F, F, F, F, F, F]
        game.unlocked = [T, T, T, T, T, T, T, T, T, T, T, T]
        game.child = [N, N, N, N, N, N, N, N, N, N, N, N]
        game.owner = [F, F, F, F, F, F, T, T, T, T, T, T]
        game.store = [0, 0]

        # move 1
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [2, 7, 1, 6, 1, 6, 6, 6, 0, 1, 6, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move((0, 1, None))
        assert game.turn is False
        assert game.board == [2, 3, 1, 11, 4, 0, 4, 1, 4, 5, 2, 11]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move((1, 4, None))
        assert game.turn is True
        assert game.board == [3, 0, 2, 12, 1, 0, 6, 0, 1, 7, 4, 12]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [4, 1, 3, 13, 2, 1, 7, 1, 2, 8, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [7, 4, 3, 1, 6, 3, 2, 0, 6, 3, 9, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [8, 5, 4, 0, 7, 4, 0, 1, 0, 4, 10, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None

        # move 7
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [9, 6, 5, 1, 1, 4, 1, 2, 1, 5, 11, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [2, 0]
        assert cond.name == "REPEAT_TURN"

        # move 8
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [9, 6, 5, 1, 0, 3, 1, 2, 1, 5, 11, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 0]
        assert cond.name == "REPEAT_TURN"

        # move 9
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [9, 6, 0, 2, 1, 4, 2, 0, 2, 6, 12, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 0]
        assert cond is None

        # move 10
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [9, 6, 0, 2, 1, 4, 0, 1, 0, 7, 13, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 0]
        assert cond is None

        # move 11
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [9, 6, 0, 0, 2, 3, 0, 1, 0, 7, 13, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [6, 0]
        assert cond.name == "REPEAT_TURN"

        # move 12
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [10, 1, 2, 2, 4, 3, 1, 0, 1, 0, 14, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 0]
        assert cond.name == "REPEAT_TURN"

        # move 13
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [10, 1, 2, 0, 5, 2, 1, 0, 1, 0, 14, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [10, 0]
        assert cond.name == "REPEAT_TURN"

        # move 14
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [10, 0, 0, 1, 6, 1, 1, 0, 1, 0, 14, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond.name == "REPEAT_TURN"

        # move 15
        cond = game.move((1, 3, None))
        assert game.turn is True
        assert game.board == [11, 1, 1, 0, 0, 2, 2, 1, 2, 1, 15, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 16
        cond = game.move((0, 5, None))
        assert game.turn is False
        assert game.board == [11, 1, 1, 0, 0, 2, 0, 2, 0, 2, 16, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 17
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [1, 0, 3, 2, 0, 4, 0, 4, 0, 4, 18, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 18
        cond = game.move((0, 4, None))
        assert game.turn is False
        assert game.board == [1, 0, 3, 2, 0, 4, 0, 0, 1, 5, 19, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None

        # move 19
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 1, 3, 0, 0, 1, 5, 19, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [14, 0]
        assert cond.name == "REPEAT_TURN"

        # move 20
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 0, 2, 0, 0, 1, 5, 19, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 0]
        assert cond.name == "REPEAT_TURN"

        # move 21
        cond = game.move((1, 2, None))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 1, 0, 0, 1, 5, 19, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [18, 0]
        assert cond.name == "REPEAT_TURN"

        # move 22
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 1, 5, 19, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond.name == "REPEAT_TURN"

        # move 23
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 1, 5, 19, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 24
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 0, 1, 5, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 25
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 0, 1, 5, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 26
        cond = game.move((0, 2, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 2, 1, 0, 0, 0, 1, 0, 20, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 0]
        assert cond is None

        # move 27
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 2, 0, 0, 0, 0, 1, 0, 20, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [21, 0]
        assert cond.name == "REPEAT_TURN"

        # move 28
        cond = game.move((1, 3, None))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 1, 0, 0, 0, 1, 0, 20, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond.name == "REPEAT_TURN"

        # move 29
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 1, 0, 0, 0, 1, 0, 20, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 30
        cond = game.move((0, 3, None))
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 1, 0, 0, 0, 0, 1, 20, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [22, 0]
        assert cond is None

        # move 31
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 20, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [23, 0]
        assert cond.name == "REPEAT_TURN"

        # move 32
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 0, 0, 1, 20, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [23, 0]
        assert cond is None

        # move 33
        cond = game.move((0, 2, None))
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 19, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [23, 2]
        assert cond.name == "REPEAT_TURN"

        # move 34
        cond = game.move((0, 0, None))
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [23, 2]
        assert cond is None

        # move 35
        cond = game.move((1, 1, None))
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 2]
        assert cond.name == "REPEAT_TURN"

        # move 36
        cond = game.move((1, 0, None))
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 2]
        assert cond is None

        # move 37
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 2]
        assert cond is None

        # move 38
        cond = game.move((1, 2, None))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 2]
        assert cond is None

        # move 39
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 2]
        assert cond is None

        # move 40
        cond = game.move((1, 1, None))
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 2]
        assert cond is None

        # move 41
        cond = game.move(65535)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 2]
        assert cond is None

        # move 42
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [25, 2]
        assert cond.name == "REPEAT_TURN"

        # move 43
        cond = game.move((1, 2, None))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [26, 2]
        assert cond.name == "REPEAT_TURN"

        # move 44
        cond = game.move((1, 4, None))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, F, N]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [27, 2]
        assert cond.name == "WIN"
