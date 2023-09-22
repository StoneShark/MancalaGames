# -*- coding: utf-8 -*-
"""Test bechi

Tests blocks, multi capture with capt same direction, capt evens,
move unlocks, must pass, rounds, split sow, and sow start.
AI pass and player pass.

Created on Thu Aug 17 07:27:20 2023
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import man_config

class TestBechi:

    @pytest.fixture
    def game(self):
        return man_config.make_game('./GameProps/bechi.txt')


    def test_round_1(self, game):

        game.turn = False
        game.starter = game.turn
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 4, 4, 1, 5, 5, 5, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 1, 5, 5, 1, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 5, 5, 1, 6, 6, 2, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 4 - opp side capture
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 6, 6, 2, 7, 1, 2, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, False, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None

        # move 5
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 6, 6, 1, 8, 1, 2, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, False, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None

        # move 6 - same side capture
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 7, 7, 2, 1, 0, 3, 7]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None

        # move 7
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 7, 7, 1, 0, 0, 3, 7]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [2, 4]
        assert cond is None

        # move 8
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 7, 7, 1, 0, 0, 1, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [2, 6]
        assert cond is None

        # move 9
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 7, 0, 1, 1, 2, 9]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 6]
        assert cond is None

        # move 10 - multi capture across sides
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 8, 1, 2, 2, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 12]
        assert cond is None

        # move 11
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 1, 2, 3, 3, 4, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 12]
        assert cond is None

        # move 12
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 3, 1, 3, 4, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 14]
        assert cond is None

        # move 13
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 2, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 14]
        assert cond is None

        # move 14
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [14, 18]
        assert cond.name == "ROUND_WIN"

        winmsg = game.win_message(cond)
        assert 'Round' in winmsg[0]
        assert 'Top' in winmsg[1]

        game.new_game(win_cond=cond, new_round_ok=True)
        assert game.turn == True
        assert game.board == [4, 4, 0, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [2, 2]


    def test_round_2(self, game):

        # start condition is not the same as after new game above
        # because seeds were moved via the UI

        # blocked hole on bottom
        game.turn = True
        game.starter = game.turn
        game.board = [4, 4, 4, 0, 4, 4, 4, 4]
        game.blocked = [False, False, False, True, False, False, False, False]
        game.unlocked = [False, False, False, False, False, False, False, False]
        game.child = [None, None, None, None, None, None, None, None]
        game.store = [2, 2]

        # move 1
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 5, 5, 0, 1, 4, 4, 4]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [False, False, False, False, True, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [2, 2]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 5, 5, 0, 0, 5, 5, 5]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, False, False, False, True, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 2]
        assert cond is None

        # move 3
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 6, 6, 0, 1, 1, 5, 5]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, False, False, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 4]
        assert cond is None

        # move 4  -- same dir capture but lock stops
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 6, 0, 0, 2, 6, 6]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, False, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [6, 4]
        assert cond is None

        # move 5
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 6, 0, 1, 1, 6, 6]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, False, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [6, 4]
        assert cond is None

        # move 6
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 2, 2, 7, 7]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 4]
        assert cond is None

        # move 7
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 2, 7, 7]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 6]
        assert cond is None

        # move 8 - bottom passes
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 2, 7, 7]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 6]
        assert cond is None

        # move 9
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 7, 7]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 8]
        assert cond is None

        # move 10 - bottom passes
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 7, 7]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 8]
        assert cond is None

        # move 11
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 1, 0, 1, 8]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 10]
        assert cond is None

        # move 12
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 1, 8]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [10, 10]
        assert cond is None

        # move 13
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 2, 0, 2, 1, 2, 0]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [10, 12]
        assert cond is None

        # move 14
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 2, 1, 2, 0]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 12]
        assert cond is None

        # move 15
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 1, 1, 2, 0]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 12]
        assert cond is None

        # move 16
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 2, 0, 0, 0]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [16, 12]
        assert cond is None

        # move 17
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, True, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [17, 15]
        assert cond.name == "ROUND_WIN"

        winmsg = game.win_message(cond)
        assert 'Round' in winmsg[0]
        assert 'Bottom' in winmsg[1]

        game.new_game(win_cond=cond, new_round_ok=True)
        assert game.turn == False
        assert game.board == [4, 4, 4, 4, 4, 0, 4, 4]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 3]


    def test_round_3(self, game):

        # blocked hole on top
        game.turn = False
        game.starter = game.turn
        game.board = [4, 4, 4, 4, 4, 0, 4, 4]
        game.blocked = [False, False, False, False, False, True, False, False]
        game.unlocked = [False, False, False, False, False, False, False, False]
        game.child = [None, None, None, None, None, None, None, None]
        game.store = [1, 3]

        # move 1
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 4, 4, 1, 5, 0, 5, 5]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [False, False, False, True, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 3]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 5, 0, 5, 0, 5, 1]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [False, False, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 5]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 5, 5, 1, 6, 0, 6, 2]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 5]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 5, 5, 1, 6, 0, 6, 1]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 7]
        assert cond is None

        # move 5
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 5, 1, 7, 0, 7, 2]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 7]
        assert cond is None

        # move 6
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 5, 1, 7, 0, 7, 1]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 9]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 8, 0, 8, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 9]
        assert cond is None

        # move 8
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 2, 3, 9, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 11]
        assert cond is None

        # move 9
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 2, 3, 9, 0, 0, 1]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [5, 11]
        assert cond is None

        # move 10
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 3, 5, 2, 0, 1, 2]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [5, 11]
        assert cond is None

        # move 11
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 3, 5, 2, 0, 1, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [9, 11]
        assert cond is None

        # move 12
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 1, 0, 1, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [9, 17]
        assert cond.name == "ROUND_WIN"

        winmsg = game.win_message(cond)
        assert 'Round' in winmsg[0]
        assert 'Top' in winmsg[1]

        game.new_game(win_cond=cond, new_round_ok=True)
        assert game.turn == True
        assert game.board == [4, 4, 0, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 3]


    def test_round_4_tie(self, game):

        game.turn = True
        game.starter = game.turn
        game.board = [4, 4, 0, 4, 4, 4, 4, 4]
        game.blocked = [False, False, True, False, False, False, False, False]
        game.unlocked = [False, False, False, False, False, False, False, False]
        game.child = [None, None, None, None, None, None, None, None]
        game.store = [1, 3]

        # move 1
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 0, 5, 4, 4, 4, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 3]
        assert cond is None

        # move 2
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 0, 1, 5, 5, 5, 0]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 3]
        assert cond is None

        # move 3
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 6, 0, 0, 5, 5, 1, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None

        # move 4
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 1, 0, 0, 6, 6, 2, 2]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [False, True, False, True, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None

        # move 5
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 1, 0, 0, 6, 6, 2, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [False, True, False, True, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None

        # move 6
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 7, 7, 3, 0]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [7, 5]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 3, 0, 2, 8, 1, 0, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, False, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [7, 9]
        assert cond is None

        # move 8
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 0, 2, 8, 1, 0, 0]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, False, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [9, 9]
        assert cond is None

        # move 9
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 2, 0, 3, 0, 2, 1, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [9, 11]
        assert cond is None

        # move 10
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 0, 3, 0, 2, 1, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [13, 11]
        assert cond is None

        # move 11
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 3, 1, 1, 1, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [13, 11]
        assert cond is None

        # move 12
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 2, 0, 1, 1]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [15, 11]
        assert cond is None

        # move 13
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, True, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [16, 16]
        assert cond.name == "ROUND_TIE"

        winmsg = game.win_message(cond)
        assert 'Round Over' in winmsg[0]
        assert 'tie' in winmsg[1]

        game.new_game(win_cond=cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]


    def test_round_5(self, game):

        game.turn = False
        game.starter = game.turn
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 4, 4, 1, 5, 5, 5, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 1, 5, 5, 1, 5]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 5, 5, 1, 6, 6, 2, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 6, 6, 2, 7, 1, 2, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, False, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None

        # move 5
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 6, 2, 8, 2, 3, 7]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, False, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None

        # move 6
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 6, 2, 8, 2, 1, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, False, True, False, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 9, 3, 2, 9]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, False, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None

        # move 8
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 4, 3, 10]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 14]
        assert cond is None

        # move 9
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 4, 3, 10]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 14]
        assert cond is None

        # move 10
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 4, 1, 11]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 16]
        assert cond is None

        # move 11
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 4, 1, 11]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 16]
        assert cond is None

        # move 12
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 1, 5, 2, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 18]
        assert cond.name == "ROUND_WIN"

        winmsg = game.win_message(cond)
        assert 'Round' in winmsg[0]
        assert 'Top' in winmsg[1]

        game.new_game(win_cond=cond, new_round_ok=True)
        assert game.turn == True
        assert game.board == [4, 0, 0, 0, 4, 4, 4, 4]
        assert game.blocked == [False, True, True, True, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 12]


    def test_round_6_game_win(self, game):

        game.turn = True
        game.starter = game.turn
        game.board = [4, 0, 0, 0, 4, 4, 4, 4]
        game.blocked = [False, True, True, True, False, False, False, False]
        game.unlocked = [False, False, False, False, False, False, False, False]
        game.child = [None, None, None, None, None, None, None, None]
        game.store = [0, 12]

        # move 1
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 0, 0, 0, 5, 5, 4, 1]
        assert game.blocked == [False, True, True, True, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 12]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 6, 6, 5, 2]
        assert game.blocked == [False, True, True, True, False, False, False, False]
        assert game.unlocked == [True, False, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 12]
        assert cond is None

        # move 3
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 7, 6, 3]
        assert game.blocked == [False, True, True, True, False, False, False, False]
        assert game.unlocked == [True, False, False, False, True, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 16]
        assert cond is None

        # move 4
        cond = game.move(65535)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 7, 6, 3]
        assert game.blocked == [False, True, True, True, False, False, False, False]
        assert game.unlocked == [True, False, False, False, True, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 16]
        assert cond is None

        # move 5
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 8, 0, 0]
        assert game.blocked == [False, True, True, True, False, False, False, False]
        assert game.unlocked == [True, False, False, False, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 22]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert winmsg[0] == 'Game Over'
        assert 'Top' in winmsg[1]

        game.new_game(win_cond=cond, new_round_ok=True)
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
