# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:23:34 2023

@author: Ann
"""

import sys

import pytest

sys.path.extend(['src'])


import man_config
import mancala
from game_interface import GrandSlam


class TestOwareGrandSlam:

    @pytest.fixture
    def game(self):
        return man_config.make_game('./GameProps/Oware.txt')


    def test_false_win(self, game):

        game.turn = True
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 5, 0, 5, 5]
        assert game.store == [1, 0]
        assert cond is None

        # move 3
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 5, 4, 4, 4, 0, 5, 0, 6, 1, 6, 6]
        assert game.store == [1, 0]
        assert cond is None

        # move 4
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 5, 4, 0, 5, 1, 6, 0, 6, 1, 6, 6]
        assert game.store == [2, 0]
        assert cond is None

        # move 5
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 6, 5, 1, 6, 0, 6, 0, 6, 1, 6, 0]
        assert game.store == [2, 2]
        assert cond is None

        # move 6
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 6, 2, 7, 1, 7, 0, 6, 1, 6, 0]
        assert game.store == [3, 2]
        assert cond is None

        # move 7
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 0, 6, 2, 7, 1, 0, 1, 7, 2, 7, 1]
        assert game.store == [3, 3]
        assert cond is None

        # move 8
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 0, 6, 2, 7, 0, 0, 1, 7, 2, 7, 1]
        assert game.store == [4, 3]
        assert cond is None

        # move 9
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 1, 7, 0, 7, 0, 0, 1, 0, 3, 8, 2]
        assert game.store == [4, 6]
        assert cond is None

        # move 10
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 1, 7, 0, 0, 1, 1, 2, 1, 4, 9, 0]
        assert game.store == [7, 6]
        assert cond is None

        # move 11
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 0, 7, 0, 0, 1, 1, 2, 1, 0, 10, 1]
        assert game.store == [7, 8]
        assert cond is None

        # move 12
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 0, 0, 1, 1, 2, 0, 0, 0, 0, 10, 1]
        assert game.store == [15, 8]
        assert cond is None

        # move 13
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 0, 0, 1, 1, 2, 0, 0, 0, 0, 10, 0]
        assert game.store == [15, 8]
        assert cond is None

        # move 14
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [11, 0, 0, 1, 1, 0, 0, 0, 0, 0, 10, 0]
        assert game.store == [17, 8]
        assert cond is None

        # move 15
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [12, 1, 1, 2, 2, 1, 1, 1, 1, 0, 0, 1]
        assert game.store == [17, 8]
        assert cond is None

        # move 16
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [12, 1, 1, 2, 0, 2, 0, 1, 1, 0, 0, 1]
        assert game.store == [19, 8]
        assert cond is None

        # move 17
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [12, 1, 1, 2, 0, 2, 0, 0, 2, 0, 0, 1]
        assert game.store == [19, 8]
        assert cond is None

        # move 18
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [12, 0, 2, 2, 0, 2, 0, 0, 2, 0, 0, 1]
        assert game.store == [19, 8]
        assert cond is None

        # move 19
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [13, 0, 2, 2, 0, 2, 0, 0, 2, 0, 0, 0]
        assert game.store == [19, 8]
        assert cond is None

        # move 20
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [13, 0, 0, 3, 1, 2, 0, 0, 2, 0, 0, 0]
        assert game.store == [19, 8]
        assert cond is None

        # move 21
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [13, 0, 0, 3, 1, 2, 0, 0, 0, 1, 1, 0]
        assert game.store == [19, 8]
        assert cond is None

        # move 22
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [13, 0, 0, 3, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [21, 8]
        assert cond is None

        # move 23
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [13, 0, 0, 3, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [21, 8]
        assert cond is None

        # move 24
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [13, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 0]
        assert game.store == [22, 8]
        assert cond is None

        # move 25
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [14, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [22, 8]
        assert cond is None

        # move 26
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [14, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [23, 8]
        assert cond is None

        # move 27
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [15, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [23, 8]
        assert cond is None

        # move 28
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [15, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [23, 8]
        assert cond is None

        # move 29
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [15, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [23, 8]
        assert cond is None

        # move 30
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [15, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 8]
        assert cond is None

        # move 31
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [15, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 8]
        assert cond is None

        # move 32
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1]
        assert game.store == [24, 8]
        assert cond is None

        # move 33
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 0]
        assert game.store == [24, 9]
        assert cond is None

        # move 34
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [34, 14]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Bottom' in winmsg[1]


    def test_true_win(self, game):

        game.turn = False
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 0, 6, 5, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 0, 1, 6, 6, 0, 6, 5, 5]
        assert game.store == [1, 0]
        assert cond is None

        # move 4
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 6, 5, 5, 0, 1, 6, 6, 0, 6, 5, 0]
        assert game.store == [1, 1]
        assert cond is None

        # move 5
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 6, 5, 0, 1, 2, 7, 7, 0, 6, 5, 0]
        assert game.store == [2, 1]
        assert cond is None

        # move 6
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 7, 6, 0, 1, 2, 7, 7, 0, 0, 6, 1]
        assert game.store == [2, 2]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 7, 0, 1, 2, 3, 8, 8, 0, 0, 6, 1]
        assert game.store == [3, 2]
        assert cond is None

        # move 8
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 8, 0, 0, 0, 3, 8, 8, 0, 0, 0, 2]
        assert game.store == [3, 8]
        assert cond is None

        # move 9
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 1, 1, 1, 4, 9, 9, 0, 0, 0, 2]
        assert game.store == [4, 8]
        assert cond is None

        # move 10
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 10, 0, 0, 0, 4, 9, 0, 1, 1, 1, 3]
        assert game.store == [4, 14]
        assert cond is None

        # move 11
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 5, 10, 1, 2, 2, 2, 4]
        assert game.store == [4, 14]
        assert cond is None

        # move 12
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 5, 0, 2, 3, 3, 3, 5]
        assert game.store == [4, 23]
        assert cond is None

        # move 13
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 3, 4, 4, 4, 5]
        assert game.store == [4, 23]
        assert cond is None

        # move 14
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 3, 0, 5, 5, 6]
        assert game.store == [4, 23]
        assert cond is None

        # move 15
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 3, 0, 5, 5, 6]
        assert game.store == [4, 23]
        assert cond is None

        # move 16
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 1, 1, 1, 3, 0, 5, 5, 0]
        assert game.store == [4, 23]
        assert cond is None

        # move 17
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 2, 1, 1, 3, 0, 5, 5, 0]
        assert game.store == [4, 23]
        assert cond is None

        # move 18
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [7, 41]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


    def test_gs_legal(self, game):

        # get the config vars, change grandslam, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info.flags, 'grandslam', GrandSlam.LEGAL)
        info.__post_init__()
        game = mancala.Mancala(consts, info)

        game.turn = True
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 4, 4, 0, 5, 5, 5, 0, 5, 5, 5, 5]
        assert game.store == [1, 0]
        assert cond is None

        # move 3
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 6]
        assert game.store == [1, 1]
        assert cond is None

        # move 4
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 5, 0, 1, 6, 6, 6, 0, 5, 5, 0, 6]
        assert game.store == [2, 1]
        assert cond is None

        # move 5
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 6, 0, 1, 6, 6, 6, 0, 5, 0, 1, 7]
        assert game.store == [2, 2]
        assert cond is None

        # move 6
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 6, 0, 1, 0, 7, 7, 1, 6, 0, 0, 7]
        assert game.store == [5, 2]
        assert cond is None

        # move 7
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 7, 0, 1, 0, 7, 7, 1, 0, 1, 1, 8]
        assert game.store == [5, 3]
        assert cond is None

        # move 8
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 1, 8, 8, 0, 0, 1, 1, 8]
        assert game.store == [8, 3]
        assert cond is None

        # move 9
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 0, 0, 2, 1, 8, 0, 1, 1, 2, 2, 9]
        assert game.store == [8, 6]
        assert cond is None

        # move 10
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 2, 9, 0, 0, 0, 2, 2, 9]
        assert game.store == [13, 6]
        assert cond is None

        # move 11
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 2, 9, 0, 0, 0, 2, 0, 10]
        assert game.store == [13, 7]
        assert cond is None

        # move 12
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 2, 3, 2, 0, 1, 1, 1, 3, 1, 11]
        assert game.store == [13, 7]
        assert cond is None

        # move 13
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 2, 3, 2, 0, 1, 1, 1, 0, 2, 12]
        assert game.store == [13, 9]
        assert cond is None

        # move 14
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 2, 3, 0, 1, 0, 1, 1, 0, 2, 12]
        assert game.store == [15, 9]
        assert cond is None

        # move 15
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 3, 4, 1, 2, 1, 2, 2, 1, 3, 0]
        assert game.store == [15, 11]
        assert cond is None

        # move 16
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 3, 4, 1, 0, 0, 0, 2, 1, 3, 0]
        assert game.store == [20, 11]
        assert cond is None

        # move 17
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 3, 4, 1, 0, 0, 0, 0, 2, 4, 0]
        assert game.store == [20, 11]
        assert cond is None

        # move 18
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 4, 5, 2, 0, 0, 0, 0, 2, 4, 0]
        assert game.store == [20, 11]
        assert cond is None

        # move 19
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 5, 5, 2, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [20, 11]
        assert cond is None

        # move 20
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 5, 5, 2, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [20, 11]
        assert cond is None

        # move 21
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 5, 5, 2, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [20, 12]
        assert cond is None

        # move 22
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 6, 6, 2, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [20, 12]
        assert cond is None

        # move 23
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 6, 6, 2, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [20, 12]
        assert cond is None

        # move 24
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 7, 3, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [23, 12]
        assert cond is None

        # move 25
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 7, 3, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [23, 13]
        assert cond is None

        # move 26 - a win by grand slam
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [35, 13]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Bottom' in winmsg[1]


    def test_gs_not_legal(self, game):

        # get the config vars, change grandslam, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info.flags, 'grandslam', GrandSlam.NOT_LEGAL)
        info.__post_init__()
        game = mancala.Mancala(consts, info)

        game.turn = True
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 6, 5, 5, 5, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 6, 6, 5, 5, 5, 4, 4, 0, 5, 1, 6]
        assert game.store == [0, 1]
        assert cond is None

        # move 4
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 7, 6, 6, 6, 5, 5, 0, 5, 1, 6]
        assert game.store == [0, 1]
        assert cond is None

        # move 5
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 7, 6, 6, 6, 5, 0, 1, 6, 2, 7]
        assert game.store == [0, 2]
        assert cond is None

        # move 6
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 7, 7, 7, 6, 1, 2, 7, 2, 7]
        assert game.store == [0, 2]
        assert cond is None

        # move 7
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 7, 7, 7, 6, 1, 2, 7, 0, 8]
        assert game.store == [0, 3]
        assert cond is None

        # move 8
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 8, 8, 7, 2, 3, 8, 0, 8]
        assert game.store == [1, 3]
        assert cond is None

        # move 9
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 8, 0, 3, 4, 9, 1, 9]
        assert game.store == [1, 5]
        assert cond is None

        # move 10
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 9, 1, 4, 5, 10, 2, 10]
        assert game.store == [1, 5]
        assert cond is None

        # move 11
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 9, 1, 4, 0, 11, 3, 11]
        assert game.store == [1, 8]
        assert cond is None

        # move 12
        moves = game.get_moves()
        assert moves == [5]

        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 0, 2, 5, 1, 12, 4, 12]
        assert game.store == [1, 8]
        assert cond is None

        # move 13 -   GRANDSLAM: prevented from 10
        moves = game.get_moves()
        assert 10 not in moves

        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 1, 1, 3, 6, 2, 13, 5, 0]
        assert game.store == [1, 11]
        assert cond is None

        # move 14
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 2, 1, 1, 0, 4, 6, 2, 13, 5, 0]
        assert game.store == [1, 11]
        assert cond is None

        # move 15
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 4, 6, 2, 13, 0, 1]
        assert game.store == [1, 20]
        assert cond is None

        # move 16
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 4, 6, 2, 13, 0, 1]
        assert game.store == [1, 20]
        assert cond is None

        # move 17
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 4, 0, 3, 14, 1, 2]
        assert game.store == [1, 22]
        assert cond is None

        # move 18
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 5, 0, 3, 14, 1, 2]
        assert game.store == [1, 22]
        assert cond is None

        # move 19
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [1, 47]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


    def test_no_capt(self, game):

        # get the config vars, change grandslam, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info.flags, 'grandslam', GrandSlam.NO_CAPT)
        info.__post_init__()
        game = mancala.Mancala(consts, info)

        game.turn = True
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 5, 0, 5, 5]
        assert game.store == [1, 0]
        assert cond is None

        # move 3
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [6, 6, 4, 4, 4, 0, 5, 5, 0, 1, 6, 6]
        assert game.store == [1, 0]
        assert cond is None

        # move 4
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 6, 4, 4, 0, 1, 6, 6, 0, 1, 6, 6]
        assert game.store == [2, 0]
        assert cond is None

        # move 5
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 7, 5, 5, 0, 0, 6, 6, 0, 1, 6, 0]
        assert game.store == [2, 3]
        assert cond is None

        # move 6
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 7, 5, 0, 1, 1, 7, 7, 0, 1, 6, 0]
        assert game.store == [3, 3]
        assert cond is None

        # move 7
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 8, 6, 0, 0, 1, 7, 7, 0, 1, 0, 1]
        assert game.store == [3, 6]
        assert cond is None

        # move 8
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 8, 0, 1, 1, 2, 8, 8, 0, 1, 0, 1]
        assert game.store == [4, 6]
        assert cond is None

        # move 9
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [9, 9, 0, 0, 1, 2, 8, 0, 1, 2, 1, 2]
        assert game.store == [4, 9]
        assert cond is None

        # move 10
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [9, 0, 1, 1, 2, 3, 9, 0, 0, 0, 0, 2]
        assert game.store == [12, 9]
        assert cond is None

        # move 11
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 0, 0, 0, 2, 3, 0, 1, 1, 1, 1, 3]
        assert game.store == [12, 14]
        assert cond is None

        # move 12
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 3, 4, 0, 0, 0, 0, 0, 3]
        assert game.store == [21, 14]
        assert cond is None

        # move 13
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 3, 4, 0, 0, 0, 0, 0, 0]
        assert game.store == [21, 19]
        assert cond is None

        # move 14 - GRANDSLAM: no capture
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 3, 0, 1, 1, 1, 1, 0, 0]
        assert game.store == [21, 19]
        assert cond is None

        # move 15
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 3, 0, 1, 1, 0, 2, 0, 0]
        assert game.store == [21, 19]
        assert cond is None

        # move 16
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [27, 21]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Bottom' in winmsg[1]


    @pytest.mark.filterwarnings("ignore")
    def test_gs_opp_get(self, game):

        # get the config vars, change grandslam, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info.flags, 'grandslam', GrandSlam.OPP_GETS_REMAIN)
        info.__post_init__()
        game = mancala.Mancala(consts, info)

        game.turn = False
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 0, 5, 5, 5, 5, 0, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 6, 5, 5, 1, 6, 5, 5, 5, 0, 5]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [6, 0, 6, 5, 5, 1, 6, 5, 0, 6, 1, 6]
        assert game.store == [0, 1]
        assert cond is None

        # move 5
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 0, 6, 5, 5, 0, 7, 5, 0, 6, 1, 6]
        assert game.store == [0, 1]
        assert cond is None

        # move 6
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 0, 6, 5, 5, 0, 0, 6, 1, 7, 2, 7]
        assert game.store == [0, 2]
        assert cond is None

        # move 7
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 0, 0, 6, 6, 1, 1, 7, 0, 7, 2, 7]
        assert game.store == [2, 2]
        assert cond is None

        # move 8
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [8, 0, 0, 6, 6, 1, 1, 0, 1, 8, 3, 8]
        assert game.store == [2, 4]
        assert cond is None

        # move 9
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [8, 0, 0, 6, 0, 2, 2, 1, 2, 9, 4, 8]
        assert game.store == [2, 4]
        assert cond is None

        # move 10
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 0, 0, 6, 0, 2, 2, 1, 2, 9, 0, 9]
        assert game.store == [2, 6]
        assert cond is None

        # move 11
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [9, 0, 0, 0, 1, 3, 3, 2, 3, 10, 0, 9]
        assert game.store == [2, 6]
        assert cond is None

        # move 12
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 0, 0, 0, 1, 3, 3, 2, 0, 11, 1, 10]
        assert game.store == [2, 6]
        assert cond is None

        # move 13
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 2, 4, 4, 3, 1, 12, 1, 10]
        assert game.store == [2, 6]
        assert cond is None

        # move 14
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 2, 4, 4, 3, 1, 12, 0, 11]
        assert game.store == [2, 6]
        assert cond is None

        # move 15
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 2, 0, 5, 4, 2, 13, 0, 11]
        assert game.store == [2, 6]
        assert cond is None

        # move 16
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 2, 0, 0, 5, 3, 14, 1, 12]
        assert game.store == [2, 6]
        assert cond is None

        # move 17
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 1, 0, 5, 3, 14, 1, 12]
        assert game.store == [3, 6]
        assert cond is None

        # move 18
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 2, 2, 1, 2, 1, 6, 4, 15, 2, 0]
        assert game.store == [3, 8]
        assert cond is None

        # move 19
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 3, 2, 2, 1, 6, 4, 15, 2, 0]
        assert game.store == [3, 8]
        assert cond is None

        # move 20
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 2, 2, 1, 0, 5, 16, 3, 1]
        assert game.store == [3, 12]
        assert cond is None

        # move 21
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 3, 0, 0, 5, 16, 3, 1]
        assert game.store == [5, 12]
        assert cond is None

        # move 22
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 4, 4, 1, 1, 6, 0, 5, 3]
        assert game.store == [5, 18]
        assert cond is None

        # move 23
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 5, 2, 2, 7, 0, 5, 3]
        assert game.store == [5, 18]
        assert cond is None

        # move 24
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 5, 2, 2, 0, 1, 6, 4]
        assert game.store == [5, 23]
        assert cond is None

        # move 25
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 3, 3, 1, 2, 7, 4]
        assert game.store == [5, 23]
        assert cond is None

        # move 26 -- GRANDSLAM: opp gets
        # this is the odd behavior warned about with gs Legal and capt on 1s:
        #    true sow starts from pos 0 (loc 6)
        #    3 seeds are sown, all are ones on opp side, e.g. grand slam
        #    false gets true's remaining seeds
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [21, 27]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


    def test_leave_left(self, game):

        # get the config vars, change grandslam, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info.flags, 'grandslam', GrandSlam.LEAVE_LEFT)
        info.__post_init__()
        game = mancala.Mancala(consts, info)

        game.turn = False
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 8, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 0]
        assert game.store == [0, 1]
        assert cond is None

        # move 7
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 8, 7, 6, 5, 5, 5, 5, 5, 0, 0]
        assert game.store == [1, 1]
        assert cond is None

        # move 8
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None

        # move 9
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None

        # move 10
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None

        # move 11
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None

        # move 12
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 0, 1]
        assert game.store == [1, 2]
        assert cond is None

        # move 13
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 2]
        assert game.store == [1, 2]
        assert cond is None

        # move 14
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 0]
        assert game.store == [1, 5]
        assert cond is None

        # move 15
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 1]
        assert game.store == [1, 5]
        assert cond is None

        # move 16
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 0]
        assert game.store == [1, 7]
        assert cond is None

        # move 17
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 8, 0, 8, 8, 8, 3, 3, 1]
        assert game.store == [1, 7]
        assert cond is None

        # move 18
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 0, 8, 8, 8, 3, 3, 0]
        assert game.store == [1, 9]
        assert cond is None

        # move 19
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 9, 9, 9, 4, 4, 1]
        assert game.store == [1, 9]
        assert cond is None

        # move 20 -  GRANDSLAM: keep
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 9, 9, 0, 5, 5, 2]
        assert game.store == [1, 15]
        assert cond is None

        # move 21
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 10, 10, 0, 5, 5, 2]
        assert game.store == [1, 15]
        assert cond is None

        # move 22
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [1, 47]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


    def test_leave_right(self, game):

        # get the config vars, change grandslam, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info.flags, 'grandslam', GrandSlam.LEAVE_RIGHT)
        info.__post_init__()
        game = mancala.Mancala(consts, info)

        game.turn = False
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

        # move 1
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None

        # move 2
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None

        # move 3
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None

        # move 4
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 8, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None

        # move 5
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None

        # move 6
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 0]
        assert game.store == [0, 1]
        assert cond is None

        # move 7
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 8, 7, 6, 5, 5, 5, 5, 5, 0, 0]
        assert game.store == [1, 1]
        assert cond is None

        # move 8
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None

        # move 9
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None

        # move 10
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None

        # move 11
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None

        # move 12
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 0, 1]
        assert game.store == [1, 2]
        assert cond is None

        # move 13
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 2]
        assert game.store == [1, 2]
        assert cond is None

        # move 14
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 0]
        assert game.store == [1, 5]
        assert cond is None

        # move 15
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 1]
        assert game.store == [1, 5]
        assert cond is None

        # move 16
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 0]
        assert game.store == [1, 7]
        assert cond is None

        # move 17
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 8, 8, 8, 8, 3, 3, 1]
        assert game.store == [1, 7]
        assert cond is None

        # move 18
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 8, 8, 8, 8, 3, 3, 0]
        assert game.store == [1, 9]
        assert cond is None

        # move 19
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 9, 9, 9, 4, 4, 1]
        assert game.store == [1, 9]
        assert cond is None

        # move 20
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 9, 9, 9, 4, 4, 0]
        assert game.store == [1, 11]
        assert cond is None

        # move 21
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 9, 9, 9, 4, 4, 0]
        assert game.store == [1, 11]
        assert cond is None

        # move 22 -  GRANDSLAM: keep
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 9, 9, 9, 4, 0, 1]
        assert game.store == [1, 14]
        assert cond is None

        # move 23
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 9, 9, 9, 4, 0, 1]
        assert game.store == [1, 14]
        assert cond is None

        # move 24 -  GRANDSLAM: keep
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 10, 10, 5, 1, 2]
        assert game.store == [1, 18]
        assert cond is None

        # move 25
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 10, 10, 5, 1, 2]
        assert game.store == [1, 18]
        assert cond is None

        # move 26
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 1, 1, 1, 10, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None

        # move 27
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 1, 1, 1, 1, 10, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None

        # move 28
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 3, 1, 1, 1, 1, 0, 11, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None

        # move 29
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 2, 1, 0, 11, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None

        # move 30
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 2, 1, 0, 11, 0, 6, 0, 4]
        assert game.store == [1, 19]
        assert cond is None

        # move 31
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 3, 1, 0, 11, 0, 6, 0, 4]
        assert game.store == [1, 19]
        assert cond is None

        # move 32
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 1, 4, 4, 2, 1, 0, 1, 7, 1, 5]
        assert game.store == [1, 19]
        assert cond is None

        # move 33
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 4, 0, 3, 0, 0, 0, 7, 1, 5]
        assert game.store == [6, 19]
        assert cond is None

        # move 34
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 2, 2, 5, 0, 3, 0, 0, 0, 7, 1, 0]
        assert game.store == [6, 20]
        assert cond is None

        # move 35
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 3, 5, 0, 3, 0, 0, 0, 7, 1, 0]
        assert game.store == [6, 20]
        assert cond is None

        # move 36
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 4, 4, 6, 0, 3, 0, 0, 0, 0, 2, 1]
        assert game.store == [6, 21]
        assert cond is None

        # move 37
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 4, 0, 7, 1, 4, 0, 0, 0, 0, 2, 1]
        assert game.store == [7, 21]
        assert cond is None

        # move 38
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 4, 0, 7, 1, 4, 0, 0, 0, 0, 2, 0]
        assert game.store == [7, 23]
        assert cond is None

        # move 39
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 4, 0, 7, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [11, 23]
        assert cond is None

        # move 40
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 4, 0, 7, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [11, 24]
        assert cond is None

        # move 41
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 4, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [16, 24]
        assert cond is None

        # move 42
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [23, 25]
        assert cond.name == "WIN"

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]
