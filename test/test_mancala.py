# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 07:32:54 2023

@author: Ann


added these packages:

conda install pytest
conda install coverage
conda install pytest-cov
conda install -c spyder-ide spyder-unittest

To get branch coverage in Anaconda Prompt:

coverage run --branch -m pytest
coverage html

"""


# %% imports

import sys

import pytest

sys.path.extend(['src'])

import game_constants as gc
import game_interface as gi
from game_interface import GameFlags
from game_interface import Direct
from game_interface import WinCond
import mancala
import new_game
import utils


# %%


class TestConctruction:

    @pytest.fixture
    def min_game_if(self):
        return gi.GameInfo(nbr_holes=6,
                           flags=GameFlags(),
                           rules=mancala.Mancala.rules)

    @pytest.mark.filterwarnings("ignore")
    def test_bad_params(self, min_game_if):

        with pytest.raises(TypeError):
            mancala.Mancala()

        with pytest.raises(TypeError):
            mancala.Mancala(None, None)

        with pytest.raises(TypeError):
            mancala.Mancala(gc.GameConsts(3, 5), None)

        with pytest.raises(TypeError):
            mancala.Mancala(None, min_game_if)

        with pytest.raises(TypeError):
            mancala.Mancala(gc.GameConsts(3, 5), min_game_if, 5)

    @pytest.mark.filterwarnings("ignore")
    def test_min_params(self, min_game_if):

        mancala.Mancala(gc.GameConsts(3, 5), min_game_if)


class TestBasics:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes = game_consts.holes,
                                capt_on = [2],
                                flags=GameFlags(),
                                ai_params={"mm_depth" : [1, 1, 3, 5]},
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.fixture
    def mrgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(mustpass=True,
                                                stores=True,
                                                blocks=True,
                                                moveunlock=True,
                                                sow_direct=Direct.CCW,
                                                evens=True),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_get_info(self, game):

        info = game.get_game_info()
        assert isinstance(info, gi.GameInfo)
        assert info.nbr_holes == 6
        assert info.flags.sow_direct == Direct.CCW

    def test_set_diff(self, game):

        game.set_difficulty(3)
        assert game.difficulty == 3
        assert game.player.max_depth == 5

    def test_get_store(self, game):

        game.store = [3, 4]
        # param is row not player
        assert game.get_store(0) == 4
        assert game.get_store(1) == 3

    def test_sides(self, game):

        assert game.cts.opp_side(game.turn, 0) == False
        assert game.cts.opp_side(game.turn, 7) == True

        assert game.cts.my_side(game.turn, 0) == True
        assert game.cts.my_side(game.turn, 7) == False

        game.turn = True

        assert game.cts.opp_side(game.turn, 0) == True
        assert game.cts.opp_side(game.turn, 7) == False

        assert game.cts.my_side(game.turn, 0) == False
        assert game.cts.my_side(game.turn, 7) == True


class TestNewEndGames:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                flags=GameFlags(stores=True),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def rgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                flags=GameFlags(rounds=True,
                                                blocks=True,
                                                stores=True),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.starter = False
        return game

    def test_no_rounds_start(self, game):

        assert isinstance(game.deco.new_game, new_game.NewGame)

        game.unlocked = [False, True, True] * 2
        game.blocked = [True, False, True] * 2
        game.board = utils.build_board([1, 0, 0],
                                       [0, 0, 1])
        game.store = [7, 3]

        game.new_game()
        assert game.board == [2] * 6
        assert game.store == [0, 0]
        assert game.turn in [False, True]
        assert game.starter == game.turn
        assert game.unlocked == [True] * 6
        assert game.blocked == [False] * 6

    @pytest.mark.parametrize(
        'board, store, econd, eturn',
        [(utils.build_board([1, 0, 0],
                            [0, 0, 1]), [7, 3], WinCond.WIN, False),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [3, 7], WinCond.WIN, True),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [5, 5], WinCond.TIE, False),
         ])
    def test_no_rounds_end(self, game, board, store, econd, eturn):

        game.board = board
        game.store = store
        assert game.end_game() == econd
        assert game.turn == eturn


    def test_rounds_start_force(self, rgame):

        assert isinstance(rgame.deco.new_game, new_game.NewRound)
        assert isinstance(rgame.deco.new_game.decorator, new_game.NewGame)

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [8, 4]

        rgame.new_game()
        assert rgame.board == [2] * 6
        assert rgame.store == [0, 0]
        assert rgame.turn in [False, True]
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * 6
        assert rgame.blocked == [False] * 6

    def test_rounds_start(self, rgame):

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [8, 4]
        starter = rgame.turn

        rgame.new_game(win_cond=WinCond.ROUND_WIN,
                       new_round_ok=True)
        assert rgame.board == utils.build_board([2, 0, 2],
                                                [2, 2, 2])
        assert rgame.store == [2, 0]
        assert rgame.turn == (not starter)
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * rgame.cts.dbl_holes
        assert rgame.blocked == utils.build_board([False, True, False],
                                                  [False, False, False])

    def test_rounds_start_nat(self, rgame):

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [11, 1]

        rgame.new_game(new_round_ok=True)
        assert rgame.board == [2] * 6
        assert rgame.store == [0, 0]
        assert rgame.turn in [False, True]
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * 6
        assert rgame.blocked == [False] * 6

    @pytest.mark.parametrize(
        'board, store, econd, eturn',
        [(utils.build_board([1, 0, 0],
                            [0, 0, 1]), [7, 3], WinCond.ROUND_WIN, False),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [3, 7], WinCond.ROUND_WIN, True),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [5, 5], WinCond.ROUND_TIE, False),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [0, 10], WinCond.WIN, True)
         ])
    def test_rounds_end(self, rgame, board, store, econd, eturn):

        rgame.board = board
        rgame.store = store
        assert rgame.end_game() == econd
        assert rgame.turn == eturn
