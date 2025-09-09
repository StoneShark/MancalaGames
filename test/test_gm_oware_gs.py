# -*- coding: utf-8 -*-
"""Test Oware and Oware configured with each of the grand slam methods.

Created on Thu Aug 17 15:23:34 2023
@author: Ann"""

import pytest
pytestmark = pytest.mark.integtest

from context import cfg_keys as ckey
from context import game_info as gi
from context import man_config
from context import man_path
from context import mancala

from game_info import GrandSlam


class GameTestData:
    """allow passing move-end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class.

    Oware was changed to match traditional definition, but tests
    were written when 1 was included in the capt_on."""

    game_dict = man_config.read_game(man_path.GAMEPATH + 'Oware.txt')
    game_dict[ckey.GAME_INFO][ckey.CAPT_ON] = [1, 2, 3]
    game = man_config.game_from_config(game_dict)
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestFalseWin:

    def test_setup(self, gstate):
        game = gstate.game
        game.turn = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 5, 0, 5, 5]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 5, 4, 4, 4, 0, 5, 0, 6, 1, 6, 6]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 5, 4, 0, 5, 1, 6, 0, 6, 1, 6, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 6, 5, 1, 6, 0, 6, 0, 6, 1, 6, 0]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 6, 2, 7, 1, 7, 0, 6, 1, 6, 0]
        assert game.store == [3, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 0, 6, 2, 7, 1, 0, 1, 7, 2, 7, 1]
        assert game.store == [3, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 0, 6, 2, 7, 0, 0, 1, 7, 2, 7, 1]
        assert game.store == [4, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 1, 7, 0, 7, 0, 0, 1, 0, 3, 8, 2]
        assert game.store == [4, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 1, 7, 0, 0, 1, 1, 2, 1, 4, 9, 0]
        assert game.store == [7, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 0, 7, 0, 0, 1, 1, 2, 1, 0, 10, 1]
        assert game.store == [7, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 0, 0, 1, 1, 2, 0, 0, 0, 0, 10, 1]
        assert game.store == [15, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 0, 0, 1, 1, 2, 0, 0, 0, 0, 10, 0]
        assert game.store == [15, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [11, 0, 0, 1, 1, 0, 0, 0, 0, 0, 10, 0]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [12, 1, 1, 2, 2, 1, 1, 1, 1, 0, 0, 1]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [12, 1, 1, 2, 0, 2, 0, 1, 1, 0, 0, 1]
        assert game.store == [19, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [12, 1, 1, 2, 0, 2, 0, 0, 2, 0, 0, 1]
        assert game.store == [19, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [12, 0, 2, 2, 0, 2, 0, 0, 2, 0, 0, 1]
        assert game.store == [19, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [13, 0, 2, 2, 0, 2, 0, 0, 2, 0, 0, 0]
        assert game.store == [19, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [13, 0, 0, 3, 1, 2, 0, 0, 2, 0, 0, 0]
        assert game.store == [19, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [13, 0, 0, 3, 1, 2, 0, 0, 0, 1, 1, 0]
        assert game.store == [19, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [13, 0, 0, 3, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [21, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [13, 0, 0, 3, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [21, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [13, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 0]
        assert game.store == [22, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [14, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [22, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [14, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [23, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [15, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [23, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [40, 8]
        assert cond.name == "WIN"
        gstate.cond = cond
        assert game.mdata.winner is False     # manual change
        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[False] in winmsg[1]


@pytest.mark.incremental
class TestTrueWin:

    def test_setup(self, gstate):
        game = gstate.game
        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 0, 6, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 0, 1, 6, 6, 0, 6, 5, 5]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 6, 5, 5, 0, 1, 6, 6, 0, 6, 5, 0]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 6, 5, 0, 1, 2, 7, 7, 0, 6, 5, 0]
        assert game.store == [2, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 7, 6, 0, 1, 2, 7, 7, 0, 0, 6, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 7, 0, 1, 2, 3, 8, 8, 0, 0, 6, 1]
        assert game.store == [3, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 8, 0, 0, 0, 3, 8, 8, 0, 0, 0, 2]
        assert game.store == [3, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 1, 1, 1, 4, 9, 9, 0, 0, 0, 2]
        assert game.store == [4, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 10, 0, 0, 0, 4, 9, 0, 1, 1, 1, 3]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 5, 10, 1, 2, 2, 2, 4]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 5, 0, 2, 3, 3, 3, 5]
        assert game.store == [4, 23]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [4, 44]
        assert cond.name == "WIN"
        gstate.cond = cond
        assert game.mdata.winner is True     # manual change
        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[True] in winmsg[1]


@pytest.mark.incremental
class TestGSLegal:

    def test_setup(self, gstate):

        # get the config vars, change grandslam, build new game
        consts = gstate.game.cts
        info = gstate.game.info
        object.__setattr__(info, 'grandslam', GrandSlam.LEGAL)
        info.__post_init__(nbr_holes=gstate.game.cts.holes,
                           rules=mancala.Mancala.rules)
        gstate.game = mancala.Mancala(consts, info)
        game = gstate.game

        game.turn = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 4, 4, 0, 5, 5, 5, 0, 5, 5, 5, 5]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 6]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 5, 0, 1, 6, 6, 6, 0, 5, 5, 0, 6]
        assert game.store == [2, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 6, 0, 1, 6, 6, 6, 0, 5, 0, 1, 7]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 6, 0, 1, 0, 7, 7, 1, 6, 0, 0, 7]
        assert game.store == [5, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 7, 0, 1, 0, 7, 7, 1, 0, 1, 1, 8]
        assert game.store == [5, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 1, 8, 8, 0, 0, 1, 1, 8]
        assert game.store == [8, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 0, 0, 2, 1, 8, 0, 1, 1, 2, 2, 9]
        assert game.store == [8, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 2, 9, 0, 0, 0, 2, 2, 9]
        assert game.store == [13, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 2, 9, 0, 0, 0, 2, 0, 10]
        assert game.store == [13, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 2, 3, 2, 0, 1, 1, 1, 3, 1, 11]
        assert game.store == [13, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 2, 3, 2, 0, 1, 1, 1, 0, 2, 12]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 2, 3, 0, 1, 0, 1, 1, 0, 2, 12]
        assert game.store == [15, 9]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 3, 4, 1, 2, 1, 2, 2, 1, 3, 0]
        assert game.store == [15, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 3, 4, 1, 0, 0, 0, 2, 1, 3, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 3, 4, 1, 0, 0, 0, 0, 2, 4, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 4, 5, 2, 0, 0, 0, 0, 2, 4, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 5, 5, 2, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 5, 5, 2, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 5, 5, 2, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [20, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 6, 6, 2, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [20, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 6, 6, 2, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [20, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 7, 3, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 7, 3, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        """a win by grand slam"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 4, 2, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 13]
        assert cond.name == "WIN"
        gstate.cond = cond

        assert game.mdata.winner is False     # manual change
        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[False] in winmsg[1]


@pytest.mark.incremental
class TestGSNotLegal:

    def test_setup(self, gstate):

        # get the config vars, change grandslam, build new game
        consts = gstate.game.cts
        info = gstate.game.info
        object.__setattr__(info, 'grandslam', GrandSlam.NOT_LEGAL)
        info.__post_init__(nbr_holes=gstate.game.cts.holes,
                           rules=mancala.Mancala.rules)
        gstate.game = mancala.Mancala(consts, info)
        game = gstate.game

        game.turn = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 6, 5, 5, 5, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 6, 6, 5, 5, 5, 4, 4, 0, 5, 1, 6]
        assert game.store == [0, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 7, 6, 6, 6, 5, 5, 0, 5, 1, 6]
        assert game.store == [0, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 7, 6, 6, 6, 5, 0, 1, 6, 2, 7]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 7, 7, 7, 6, 1, 2, 7, 2, 7]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 7, 7, 7, 6, 1, 2, 7, 0, 8]
        assert game.store == [0, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 8, 8, 7, 2, 3, 8, 0, 8]
        assert game.store == [1, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 8, 0, 3, 4, 9, 1, 9]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 9, 1, 4, 5, 10, 2, 10]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 9, 1, 4, 0, 11, 3, 11]
        assert game.store == [1, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        moves = game.get_moves()
        assert moves == [5]

        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 0, 2, 5, 1, 12, 4, 12]
        assert game.store == [1, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        """GRANDSLAM: prevented from 10"""
        game = gstate.game
        moves = game.get_moves()
        assert 10 not in moves

        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 1, 1, 3, 6, 2, 13, 5, 0]
        assert game.store == [1, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 2, 1, 1, 0, 4, 6, 2, 13, 5, 0]
        assert game.store == [1, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 4, 6, 2, 13, 0, 1]
        assert game.store == [1, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 4, 6, 2, 13, 0, 1]
        assert game.store == [1, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 4, 0, 3, 14, 1, 2]
        assert game.store == [1, 22]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 5, 0, 3, 14, 1, 2]
        assert game.store == [1, 22]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [1, 47]
        assert cond.name == "WIN"
        gstate.cond = cond

        assert game.mdata.winner is True     # manual change
        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[True] in winmsg[1]


@pytest.mark.incremental
class TestGSNoCapt:

    def test_setup(self, gstate):

        # get the config vars, change grandslam, build new game
        consts = gstate.game.cts
        info = gstate.game.info
        object.__setattr__(info, 'grandslam', GrandSlam.NO_CAPT)
        info.__post_init__(nbr_holes=gstate.game.cts.holes,
                           rules=mancala.Mancala.rules)
        gstate.game = mancala.Mancala(consts, info)
        game = gstate.game

        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 0, 5, 5, 5, 5, 4, 4, 4, 0, 5]
        assert game.store == [0, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 0, 5, 5, 0, 6, 5, 5, 5, 0, 5]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 6, 0, 5, 5, 0, 6, 5, 5, 0, 1, 6]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 1, 6, 6, 1, 7, 6, 5, 0, 1, 6]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 0, 1, 6, 6, 1, 7, 6, 0, 1, 2, 7]
        assert game.store == [1, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 0, 0, 7, 6, 1, 7, 6, 0, 1, 2, 7]
        assert game.store == [1, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 1, 1, 8, 7, 2, 8, 6, 0, 1, 2, 0]
        assert game.store == [1, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [8, 1, 1, 8, 0, 3, 9, 7, 0, 0, 0, 0]
        assert game.store == [8, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [9, 0, 0, 8, 0, 3, 9, 0, 1, 1, 1, 1]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [9, 0, 0, 8, 0, 0, 10, 0, 0, 1, 1, 1]
        assert game.store == [11, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 1, 1, 9, 0, 0, 0, 1, 1, 2, 2, 2]
        assert game.store == [11, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 1, 0, 10, 0, 0, 0, 1, 1, 2, 2, 2]
        assert game.store == [11, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 0, 0, 10, 0, 0, 0, 1, 1, 2, 2, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        """GRANDSLAM: no capture"""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 11, 1, 1, 1, 2, 2, 3, 3, 1]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 1, 11, 1, 1, 1, 2, 2, 3, 3, 0]
        assert game.store == [11, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 12, 1, 1, 1, 2, 2, 3, 3, 0]
        assert game.store == [11, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 12, 1, 1, 1, 2, 2, 0, 4, 1]
        assert game.store == [11, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 12, 1, 0, 0, 2, 2, 0, 4, 1]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 12, 1, 0, 0, 0, 3, 1, 4, 1]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 12, 0, 1, 0, 0, 3, 1, 4, 1]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 0, 12, 0, 1, 0, 0, 3, 1, 4, 0]
        assert game.store == [13, 13]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 12, 0, 0, 0, 0, 3, 1, 4, 0]
        assert game.store == [14, 13]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 12, 0, 0, 0, 0, 3, 1, 0, 1]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 2, 1, 1, 1, 4, 2, 1, 2]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 2, 1, 1, 1, 4, 0, 2, 3]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 2, 0, 0, 1, 4, 0, 2, 3]
        assert game.store == [16, 17]
        assert cond is None
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 2, 0, 0, 1, 4, 0, 0, 4]
        assert game.store == [16, 19]
        assert cond is None
        gstate.cond = cond

    def test_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 1, 4, 0, 0, 4]
        assert game.store == [17, 19]
        assert cond is None
        gstate.cond = cond

    def test_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 5]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 5]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 5]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 5]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 0, 2, 1, 5]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 2, 0, 0, 0, 2, 1, 5]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 6]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_37(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 2, 6]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_38(self, gstate):
        """GRANDSLAM: no capture"""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 1, 3, 0, 0, 0, 0, 2, 0]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [20, 22]
        assert cond is None
        gstate.cond = cond

    def test_move_41(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [20, 22]
        assert cond is None
        gstate.cond = cond

        # False can't share, True won't be able to move -> Game Over

    def test_move_42(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 23]
        assert cond.name == "WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond


@pytest.mark.incremental
class TestGSOppGet:

    def test_setup(self, gstate):

        # get the config vars, change grandslam, build new game
        consts = gstate.game.cts
        info = gstate.game.info
        object.__setattr__(info, 'grandslam', GrandSlam.OPP_GETS_REMAIN)
        info.__post_init__(nbr_holes=gstate.game.cts.holes,
                           rules=mancala.Mancala.rules)
        gstate.game = mancala.Mancala(consts, info)
        game = gstate.game

        game.turn = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 6, 6, 5, 5, 4, 4, 0, 5, 0, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 6, 5, 5, 4, 4, 0, 5, 0, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 8, 7, 6, 6, 5, 4, 0, 5, 0, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 8, 7, 7, 6, 5, 1, 6, 0, 6, 0]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 8, 7, 7, 6, 5, 0, 7, 0, 6, 0]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 8, 7, 7, 0, 6, 1, 8, 1, 7, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 8, 7, 7, 0, 6, 1, 8, 0, 8, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 8, 0, 8, 1, 7, 2, 9, 1, 9, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 9, 1, 9, 2, 8, 3, 9, 1, 0, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 9, 0, 10, 2, 8, 3, 9, 1, 0, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 2, 10, 1, 11, 0, 8, 3, 0, 2, 1, 2]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 2, 10, 0, 12, 0, 8, 3, 0, 2, 1, 2]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 2, 10, 0, 12, 0, 8, 3, 0, 2, 0, 3]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 3, 11, 1, 0, 2, 9, 4, 1, 3, 1, 4]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 4, 12, 0, 0, 2, 0, 5, 2, 4, 2, 5]
        assert game.store == [2, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 5, 0, 2, 1, 3, 1, 6, 3, 5, 3, 6]
        assert game.store == [2, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 6, 0, 2, 1, 3, 1, 6, 3, 0, 4, 7]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [7, 6, 0, 2, 1, 0, 2, 7, 4, 0, 4, 7]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 7, 1, 3, 2, 1, 3, 7, 4, 0, 4, 0]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 8, 2, 4, 3, 2, 4, 8, 5, 0, 4, 0]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 9, 2, 4, 3, 2, 4, 8, 0, 1, 5, 1]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 10, 2, 4, 3, 2, 4, 8, 0, 1, 5, 1]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 10, 2, 4, 3, 2, 4, 8, 0, 0, 6, 1]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 10, 2, 4, 3, 0, 5, 9, 0, 0, 6, 1]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 11, 3, 5, 4, 0, 5, 9, 0, 0, 0, 2]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 4, 6, 5, 1, 6, 10, 1, 1, 1, 3]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 1, 5, 6, 5, 1, 6, 10, 1, 1, 1, 0]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 1, 5, 6, 5, 0, 7, 10, 1, 1, 1, 0]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 2, 6, 7, 6, 0, 7, 0, 2, 2, 2, 1]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 7, 8, 7, 0, 7, 0, 2, 2, 2, 1]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 7, 8, 7, 0, 7, 0, 2, 2, 2, 0]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_34(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 7, 8, 0, 1, 8, 0, 0, 0, 0, 0]
        assert game.store == [13, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 4, 8, 8, 0, 1, 0, 1, 1, 1, 1, 1]
        assert game.store == [13, 8]
        assert cond is None
        gstate.cond = cond

    def test_move_36(self, gstate):
        """GRANDSLAM: opp gets"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [24, 24]
        assert cond.name == "TIE"
        assert game.mdata.winner is None
        gstate.cond = cond


@pytest.mark.incremental
class TestGSLeftLeft:

    def test_setup(self, gstate):

        # get the config vars, change grandslam, build new game
        consts = gstate.game.cts
        info = gstate.game.info
        object.__setattr__(info, 'grandslam', GrandSlam.LEAVE_LEFT)
        info.__post_init__(nbr_holes=gstate.game.cts.holes,
                           rules=mancala.Mancala.rules)
        gstate.game = mancala.Mancala(consts, info)
        game = gstate.game

        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 8, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 0]
        assert game.store == [0, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 8, 7, 6, 5, 5, 5, 5, 5, 0, 0]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 0, 1]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 2]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 0]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 1]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 0]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 8, 0, 8, 8, 8, 3, 3, 1]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 0, 8, 8, 8, 3, 3, 0]
        assert game.store == [1, 9]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 9, 9, 9, 4, 4, 1]
        assert game.store == [1, 9]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        """GRANDSLAM: keep"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 9, 9, 0, 5, 5, 2]
        assert game.store == [1, 15]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [1, 47]
        assert cond.name == "WIN"
        gstate.cond = cond

        assert game.mdata.winner is True     # manual change
        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[True] in winmsg[1]


@pytest.mark.incremental
class TestGSLeaveRight:

    def test_setup(self, gstate):

        # get the config vars, change grandslam, build new game
        consts = gstate.game.cts
        info = gstate.game.info
        object.__setattr__(info, 'grandslam', GrandSlam.LEAVE_RIGHT)
        info.__post_init__(nbr_holes=gstate.game.cts.holes,
                           rules=mancala.Mancala.rules)
        gstate.game = mancala.Mancala(consts, info)
        game = gstate.game

        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 8, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 9, 7, 6, 5, 4, 4, 4, 4, 4, 0, 0]
        assert game.store == [0, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 8, 7, 6, 5, 5, 5, 5, 5, 0, 0]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 1]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 9, 7, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 1, 0]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 10, 8, 6, 5, 5, 5, 5, 0, 0, 1]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 2]
        assert game.store == [1, 2]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 9, 7, 6, 6, 6, 6, 1, 1, 0]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 1]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 7, 7, 7, 7, 2, 2, 0]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 8, 8, 8, 8, 3, 3, 1]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 8, 8, 8, 8, 3, 3, 0]
        assert game.store == [1, 9]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 9, 9, 9, 4, 4, 1]
        assert game.store == [1, 9]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 9, 9, 9, 4, 4, 0]
        assert game.store == [1, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 9, 9, 9, 4, 4, 0]
        assert game.store == [1, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        """GRANDSLAM: keep"""
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 9, 9, 9, 4, 0, 1]
        assert game.store == [1, 14]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 9, 9, 9, 4, 0, 1]
        assert game.store == [1, 14]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        """GRANDSLAM: keep"""
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 10, 10, 5, 1, 2]
        assert game.store == [1, 18]
        assert cond is None
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 10, 10, 5, 1, 2]
        assert game.store == [1, 18]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 1, 1, 1, 10, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 1, 1, 1, 1, 10, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 3, 1, 1, 1, 1, 0, 11, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None
        gstate.cond = cond

    def test_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 2, 1, 0, 11, 0, 6, 2, 3]
        assert game.store == [1, 18]
        assert cond is None
        gstate.cond = cond

    def test_move_30(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 2, 1, 0, 11, 0, 6, 0, 4]
        assert game.store == [1, 19]
        assert cond is None
        gstate.cond = cond

    def test_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 3, 1, 0, 11, 0, 6, 0, 4]
        assert game.store == [1, 19]
        assert cond is None
        gstate.cond = cond

    def test_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 1, 4, 4, 2, 1, 0, 1, 7, 1, 5]
        assert game.store == [1, 19]
        assert cond is None
        gstate.cond = cond

    def test_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 4, 0, 3, 0, 0, 0, 7, 1, 5]
        assert game.store == [6, 19]
        assert cond is None
        gstate.cond = cond

    def test_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 2, 2, 5, 0, 3, 0, 0, 0, 7, 1, 0]
        assert game.store == [6, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 3, 5, 0, 3, 0, 0, 0, 7, 1, 0]
        assert game.store == [6, 20]
        assert cond is None
        gstate.cond = cond

    def test_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 4, 4, 6, 0, 3, 0, 0, 0, 0, 2, 1]
        assert game.store == [6, 21]
        assert cond is None
        gstate.cond = cond

    def test_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 4, 0, 7, 1, 4, 0, 0, 0, 0, 2, 1]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 4, 0, 7, 1, 4, 0, 0, 0, 0, 2, 0]
        assert game.store == [7, 23]
        assert cond is None
        gstate.cond = cond

    def test_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 4, 0, 7, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [11, 23]
        assert cond is None
        gstate.cond = cond

    def test_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 4, 0, 7, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [11, 24]
        assert cond is None
        gstate.cond = cond

    def test_move_41(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 4, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_move_42(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 4, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [16, 25]
        assert cond.name == "WIN"
        gstate.cond = cond

        assert game.mdata.winner is True     # manual change
        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[True] in winmsg[1]
