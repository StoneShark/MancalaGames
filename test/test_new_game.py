# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 13:38:12 2023
@author: Ann"""

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import ChildType
from game_interface import Goal
from game_interface import RoundFill
from game_interface import RoundStarter
from game_interface import WinCond


TEST_COVERS = ['src\\new_game.py']

T = True
F = False
N = None


def test_patterns():
    """test_patterns.py does most of the testing,
    here create a game that uses new_game and a start pattern"""

    game_consts = gc.GameConsts(nbr_start=4, holes=4)
    game_info = gi.GameInfo(start_pattern=2,
                            capt_on=[2],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)

    game = mancala.Mancala(game_consts, game_info)
    game.turn = False

    assert game.board == [0, 4] * 4

    # check for override of __str__
    assert 'AlternatesPattern' in str(game.deco.new_game)



class TestNewGame:

    @pytest.fixture
    def game(self):
        """generic simple game"""

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                stores=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def rgame(self):
        """game with rounds"""

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=True,
                                blocks=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.starter = False
        return game

    @pytest.fixture
    def nb_rgame(self):
        """game rounds but no blocks"""

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.starter = False
        return game


    def test_no_rounds_start(self, game):

        game.unlocked = [False, True, True] * 2
        game.blocked = [True, False, True] * 2
        game.board = utils.build_board([1, 0, 0],
                                       [0, 0, 1])
        game.store = [7, 3]

        assert game.new_game()
        assert game.board == [2] * 6
        assert game.store == [0, 0]
        assert game.turn in [False, True]   # random
        assert game.starter == game.turn
        assert game.unlocked == [True] * 6
        assert game.blocked == [False] * 6


    @pytest.mark.parametrize('round_fill',
                             [RoundFill.LEFT_FILL, RoundFill.EVEN_FILL])
    def test_rounds_start_force(self, rgame, round_fill):
        """Tell new game that it cannot start a new round,
        e.g. force a new game.
        Test for both NewRound and NewRoundEven"""

        object.__setattr__(rgame.info, 'round_fill', round_fill)
        rgame.deco = mancala.ManDeco(rgame)

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [8, 4]

        assert rgame.new_game()
        assert rgame.board == [2] * 6
        assert rgame.store == [0, 0]
        assert rgame.turn in [False, True]   # random
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * 6
        assert rgame.blocked == [False] * 6


    @pytest.mark.parametrize('last_player', (True, False))
    @pytest.mark.parametrize(
        'start_method, starter, winner, estarter',
        [(RoundStarter.ALTERNATE, True, False, False),
         (RoundStarter.ALTERNATE, True, True, False),
         (RoundStarter.ALTERNATE, False, False, True),
         (RoundStarter.ALTERNATE, False, True, True),
         (RoundStarter.LOSER, True, False, True),
         (RoundStarter.LOSER, False, True, False),
         (RoundStarter.WINNER, True, False, False),
         (RoundStarter.WINNER, True, True, True),
         (RoundStarter.LAST_MOVER, True, False, False),
         (RoundStarter.LAST_MOVER, True, True, True),
          ])
    def test_rounds_start(self, rgame, last_player,
                          start_method, starter, winner, estarter):

        object.__setattr__(rgame.info, 'round_starter', start_method)

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.starter = starter
        if winner:
            rgame.store = [4, 8]
        else:
            rgame.store = [8, 4]
        rgame.turn = winner
        rgame.last_mdata = mancala.MoveData(rgame, 2)
        rgame.last_mdata.player = last_player

        assert not rgame.new_game(win_cond=WinCond.ROUND_WIN,
                                  new_round_ok=True)

        if start_method == RoundStarter.LAST_MOVER:
            assert rgame.turn == last_player
        else:
            assert rgame.turn == estarter
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * rgame.cts.dbl_holes
        if winner:
            assert rgame.board == utils.build_board([2, 2, 2],
                                                    [2, 0, 2])
            assert rgame.store == [0, 2]
            assert rgame.blocked == utils.build_board([False, False, False],
                                                      [False, True, False])
        else:
            assert rgame.board == utils.build_board([2, 0, 2],
                                                    [2, 2, 2])
            assert rgame.store == [2, 0]
            assert rgame.blocked == utils.build_board([False, True, False],
                                                      [False, False, False])


    def get_fill_pat_ans(self, case, pattern):
        """The answer for the fill pattern is the holes that
        are blocked."""

        answers = {

            RoundFill.LEFT_FILL:
                [utils.build_board([False, False, False],
                                   [False, False, True]),
                 utils.build_board([True, False, False],
                                   [False, False, False]),
                 utils.build_board([False, False, False],
                                   [False, True, True]),
                 utils.build_board([True, True, False],
                                   [False, False, False])],

             RoundFill.RIGHT_FILL:
                 [utils.build_board([False, False, False],
                                    [True, False, False]),
                  utils.build_board([False, False, True],
                                    [False, False, False]),
                  utils.build_board([False, False, False],
                                    [True, True, False]),
                  utils.build_board([False, True, True],
                                    [False, False, False])],

            RoundFill.OUTSIDE_FILL:
                [utils.build_board([False, False, False],
                                   [False, True, False]),
                 utils.build_board([False, True, False],
                                   [False, False, False]),
                 utils.build_board([False, False, False],
                                   [False, True, True]),
                 utils.build_board([False, True, True],
                                   [False, False, False])],

             RoundFill.SHORTEN:
                 [utils.build_board([False, False, True],
                                    [False, False, True]),
                  utils.build_board([False, False, True],
                                    [False, False, True]),
                  utils.build_board([False, True, True],
                                    [False, True, True]),
                  utils.build_board([False, True, True],
                                    [False, True, True])],
         }
        return answers[pattern][case]


    @pytest.mark.parametrize(
        'case, store, estore',
        [(0, [4, 8], [0, 2]),
         (1, [8, 4], [2, 0]),
         (2, [2, 10], [0, 4]),
         (3, [10, 2], [4, 0])])
    @pytest.mark.parametrize('round_fill',
                             [RoundFill.LEFT_FILL, RoundFill.RIGHT_FILL,
                              RoundFill.OUTSIDE_FILL, RoundFill.SHORTEN])
    def test_fill_patterns(self, rgame, case, store, estore, round_fill):
        """Test basic fill patterns. For UMOVE and UCHOOSE, the fill
        pattern doesn't really matter."""

        object.__setattr__(rgame.info, 'round_fill', round_fill)
        rgame.deco = mancala.ManDeco(rgame)

        # choose some random board setup
        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2

        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = store.copy()
        # set turn to winner
        winner = store[0] < store[1]
        rgame.turn = winner

        assert not rgame.new_game(win_cond=WinCond.ROUND_WIN,
                                  new_round_ok=True)

        # no loss of seeds
        assert sum(rgame.store) + sum(rgame.board) == rgame.cts.total_seeds

        # no locks and check blocks
        assert rgame.unlocked == [True] * rgame.cts.dbl_holes
        assert rgame.blocked == self.get_fill_pat_ans(case, round_fill)

        # test board and blocks
        assert all(rgame.blocked[loc]
                   or rgame.board[loc] == 2
                       for loc in range(rgame.cts.dbl_holes))

        # test stores
        if round_fill == RoundFill.SHORTEN:
            assert rgame.store == [s * 2 for s in estore]
        else:
            assert rgame.store == estore


    @pytest.mark.parametrize(
        'store, estore',
        [([4, 8], [0, 2]),
         ([8, 4], [2, 0]),
         ([2, 10], [0, 4]),
         ([10, 2], [4, 0]),
       ])
    @pytest.mark.parametrize('round_fill',
                             [RoundFill.LEFT_FILL, RoundFill.RIGHT_FILL,
                              RoundFill.OUTSIDE_FILL, RoundFill.SHORTEN])
    def test_no_blocks(self, nb_rgame, round_fill, store, estore):

        object.__setattr__(nb_rgame.info, 'round_fill', round_fill)
        nb_rgame.deco = mancala.ManDeco(nb_rgame)

        nb_rgame.blocked = [True, False, True] * 2
        nb_rgame.board = utils.build_board([0, 0, 0],
                                           [0, 0, 0])
        nb_rgame.store = store.copy()
        # set turn to winner
        winner = store[0] < store[1]
        nb_rgame.turn = winner

        assert not nb_rgame.new_game(win_cond=WinCond.ROUND_WIN,
                                     new_round_ok=True)

        # no loss of seeds
        assert (sum(nb_rgame.store) + sum(nb_rgame.board)
                == nb_rgame.cts.total_seeds)

        # test board and blocks
        assert not any(nb_rgame.blocked)
        assert all(nb_rgame.board[loc] in (0, 2)
                   for loc in range(nb_rgame.cts.dbl_holes))

        # test the stores
        if round_fill == RoundFill.SHORTEN:
            assert nb_rgame.store == [s * 2 for s in estore]
        else:
            assert nb_rgame.store == estore



    @pytest.mark.parametrize('game_fixt', ['rgame', 'nb_rgame'])
    @pytest.mark.parametrize(
        'store, estore, even_ok',
        [([4, 8], [1, 5], True),
         ([8, 4], [5, 1], True),
         ([2, 10], [0, 8], False),
         ([10, 2], [8, 0], False),
       ])
    def test_even_rounds(self, request, game_fixt, store, estore, even_ok):
        """The test is somewhat dependent on the test cases.
        even_ok == False, with different game parameters (e.g. min_move)
        could yield a different result."""

        game = request.getfixturevalue(game_fixt)
        object.__setattr__(game.info, 'round_fill', RoundFill.EVEN_FILL)
        game.deco = mancala.ManDeco(game)

        game.blocked = [True, False, True] * 2
        game.board = utils.build_board([0, 0, 0],
                                       [0, 0, 0])
        game.store = store.copy()
        # set turn to winner
        winner = store[0] < store[1]
        game.turn = winner

        assert not game.new_game(win_cond=WinCond.ROUND_WIN,
                                 new_round_ok=True)

        # positive seeds and no loss of seeds
        assert game.store[0] >= 0 and game.store[1] >= 0
        assert (sum(game.store) + sum(game.board) == game.cts.total_seeds)

        # test blocks, board and stores
        assert not any(game.blocked)
        assert game.store == estore
        if even_ok:
            assert all(game.board[0] == game.board[loc]
                           for loc in range(game.cts.dbl_holes))
        else:
            assert (game.board[0] == 2 and game.board[3] == 2 and
                        all(game.board[loc] == 0 for loc in [1, 2, 4, 5]))


    @pytest.mark.parametrize('game_fixt', ['rgame', 'nb_rgame'])
    @pytest.mark.parametrize(
        'store, estore_choose, estore_move',
        [([4, 8], [0, 2], [1, 5]),
         ([8, 4], [2, 0], [5, 1]),
         ([2, 10], [0, 4], [0, 8]),
         ([10, 2], [4, 0], [8, 0]),
       ])
    @pytest.mark.parametrize('round_fill',
                             [RoundFill.UMOVE, RoundFill.UCHOOSE])
    def test_user_fill(self, request, game_fixt, round_fill, store,
                       estore_choose, estore_move):
        """Do a reasonableness check on the  user choose fills."""

        game = request.getfixturevalue(game_fixt)
        object.__setattr__(game.info, 'round_fill', round_fill)
        game.deco = mancala.ManDeco(game)

        game.blocked = [True, False, True] * 2
        game.board = utils.build_board([0, 0, 0],
                                       [0, 0, 0])
        game.store = store.copy()
        # set turn to winner
        winner = store[0] < store[1]
        game.turn = winner

        assert not game.new_game(win_cond=WinCond.ROUND_WIN,
                                 new_round_ok=True)

        if round_fill == RoundFill.UMOVE:
            assert game.store == estore_move
        else:
            assert game.store == estore_choose
        assert (sum(game.store) + sum(game.board) == game.cts.total_seeds)



    @pytest.mark.parametrize('nbr_holes, fseeds, einhibit',
                             [(2, 2, False),
                              (2, 3, False),
                              (3, 2, False),
                              (3, 4, False),
                              (6, 4, True),
                              (6, 10, False)])
    def test_shorten_inhibit(self, nbr_holes, fseeds, einhibit):
        """The inhibitor is only set when the board size is REDUCED
        to 3 or fewer; if it starts <= 3 then the inhibitor is
        never set."""

        game_consts = gc.GameConsts(nbr_start=2, holes=nbr_holes)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=True,
                                blocks=True,
                                stores=True,
                                child_type=ChildType.NORMAL,
                                child_cvt=2,
                                round_fill=RoundFill.SHORTEN,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.starter = False

        # setup end game conditions
        game.board = [0] * (2 * nbr_holes)
        game.store = [fseeds, game.cts.total_seeds - fseeds]
        assert not game.inhibitor._children

        assert not game.new_game(win_cond=WinCond.ROUND_WIN,
                                 new_round_ok=True)

        assert game.inhibitor._children == einhibit



class TestTerritory:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(capt_on = [2],
                                stores=True,
                                gparam_one=5,
                                goal=Goal.TERRITORY,
                                rounds=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.mark.parametrize('fseeds, win, eowners',
                             [(15, T, [F, F, F, T, T, T]),
                              (14, T, [F, F, F, T, T, T]),
                              (13, F, [F, F, F, F, T, T]),
                              (12, F, [F, F, F, F, T, T]),
                              (11, F, [F, F, F, F, T, T]),
                              (10, F, [F, F, F, T, T, T]),
                              ( 9, F, [F, F, F, T, T, T]),
                              ( 6, F, [T, F, F, T, T, T]),
                              ( 5, F, [T, F, F, T, T, T]),
                              ( 4, F, [T, T, F, T, T, T]),
                              ( 4, T, [F, F, F, T, T, T]),
                              ( 3, T, [F, F, F, T, T, T]),

                              ])
    def test_territory(self, game, fseeds, win, eowners):

        game.board = [0] * game.cts.dbl_holes
        game.store = [fseeds, game.cts.total_seeds - fseeds]

        cond = WinCond.WIN if win else WinCond.ROUND_WIN
        game.new_game(cond, new_round_ok=True)
        assert game.owner == eowners
