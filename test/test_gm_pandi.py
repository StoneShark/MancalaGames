# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 12:29:13 2024
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import man_config


T = True
F = False

class TestPandi:

    @pytest.fixture
    def game_data(self):
        return man_config.make_game('./GameProps/Pandi.txt')


    def test_pandi(self, game_data):

        game, _ = game_data

        game.turn = False
        game.starter = False
        game.board = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        game.blocked = [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        game.store = [0, 0]

        # move 1
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [7, 7, 0, 0, 7, 2, 8, 8, 8, 0, 0, 1, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [8, 0]
        assert cond is None

        # move 2
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 2, 2, 12, 3, 12, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [16, 20]
        assert cond is None

        # move 3
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 1, 2, 0, 1, 14, 0, 0, 1, 1, 1, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [20, 24]
        assert cond is None

        # move 4
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 2, 0, 3, 0, 0, 14, 0, 0, 0, 2, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [20, 25]
        assert cond is None

        # move 5
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 0, 1, 1, 15, 0, 0, 0, 2, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [20, 25]
        assert cond is None

        # move 6
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 1, 0, 1, 1, 15, 0, 0, 0, 0, 1, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [20, 25]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 1, 3, 1, 2, 0, 2, 0, 3, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 29]
        assert cond is None

        # move 8
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 3, 1, 0, 1, 3, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 33]
        assert cond is None

        # move 9
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 0, 2, 1, 2, 0, 1, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 33]
        assert cond is None

        # move 10
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 2, 0, 3, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 36]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [4, 6]

        # move 1
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 6, 6, 6, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [4, 18]
        assert cond is None

        # move 2
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 8, 0, 9, 0, 0, 0, 0, 0, 8, 8, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [12, 18]
        assert cond is None

        # move 3
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 9, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [12, 35]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 10, 1, 1, 0, 0, 0, 0, 0, 8, 0, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [12, 35]
        assert cond is None

        # move 5
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 11, 0, 2, 0, 0, 0, 0, 0, 8, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [12, 35]
        assert cond is None

        # move 6
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 11, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [21, 35]
        assert cond is None

        # move 7
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 11, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [21, 35]
        assert cond is None

        # move 8
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 12, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [21, 35]
        assert cond is None

        # move 9
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [3, 0, 1, 0, 0, 0, 0, 3, 0, 0, 2, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [21, 38]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [0, 10]

        # move 1
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 0, 6, 6, 0, 0, 6, 6, 0, 6, 0, 6, 6]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [12, 10]
        assert cond is None

        # move 2
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [10, 0, 0, 0, 9, 0, 0, 0, 1, 3, 0, 0, 2, 10]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [16, 19]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [3, 0, 1, 0, 13, 0, 0, 0, 0, 2, 0, 3, 1, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [20, 27]
        assert cond is None

        # move 4
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 3, 0, 3, 2, 0, 0, 3, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [20, 35]
        assert cond is None

        # move 5
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 3, 0, 0, 0, 1, 0, 0, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [20, 39]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [1, 9]

        # move 1
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 6, 6, 6, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [1, 21]
        assert cond is None

        # move 2
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 8, 0, 9, 0, 0, 0, 0, 0, 8, 8, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [9, 21]
        assert cond is None

        # move 3
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 9, 1, 10, 1, 0, 0, 0, 0, 8, 0, 2, 3, 3]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [9, 21]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 10, 2, 11, 0, 0, 0, 1, 0, 0, 0, 2, 3, 3]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [17, 21]
        assert cond is None

        # move 5
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 2, 11, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [17, 39]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [0, 5]

        # move 1
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 7, 0, 0, 7, 7, 0, 7, 7, 0, 0, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [2, 5]
        assert cond is None

        # move 2
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [14, 3, 3, 3, 0, 0, 0, 3, 0, 3, 2, 0, 3, 14]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [6, 16]
        assert cond is None

        # move 3
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [14, 0, 0, 0, 1, 0, 0, 0, 0, 3, 2, 0, 3, 14]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [17, 16]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 0, 0, 0, 3, 0, 2, 1, 3, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [25, 26]
        assert cond is None

        # move 5
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 3, 0, 0, 0, 3, 0, 2, 1, 3, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [25, 26]
        assert cond is None

        # move 6
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 0, 0, 3, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [25, 35]
        assert cond is None

        # move 7
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [25, 39]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [4, 6]

        # move 1
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 6, 6, 6, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [4, 18]
        assert cond is None

        # move 2
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 9, 0, 0, 0, 0, 8, 8, 0, 1, 8, 2, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [14, 18]
        assert cond is None

        # move 3
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 3, 12, 0, 0, 0, 0, 0, 1, 0, 3, 2, 1, 3]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [18, 26]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 0, 2, 0, 0, 0, 0, 0, 3, 0, 1, 0, 3, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [24, 34]
        assert cond is None

        # move 5
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.store == [24, 37]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [0, 5]

        # move 1
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 7, 0, 0, 7, 7, 0, 7, 7, 0, 0, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [2, 5]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 2, 11, 0, 11, 0, 0, 0, 0, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [6, 34]
        assert cond is None

        # move 3
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 0, 1, 0, 13, 2, 0, 2, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.store == [8, 38]
        assert cond.name == "ROUND_WIN"

        # New Round Start
        game.new_game(cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, T, T, T, T, T, F, F, F, F, F, F, F]
        assert game.store == [3, 22]

        # move 1
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, T, T, T, T, T, F, F, F, F, F, F, F]
        assert game.store == [3, 67]
        assert cond.name == "WIN"
