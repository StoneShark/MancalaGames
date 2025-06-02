# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 13:38:12 2023
@author: Ann"""

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_constants as gconsts
from context import game_interface as gi
from context import mancala
from context import move_data
from context import new_game

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

    game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
    game_info = gi.GameInfo(start_pattern=2,
                            capt_on=[2],
                            stores=True,
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

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
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

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=gi.Rounds.NO_MOVES,
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

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=gi.Rounds.NO_MOVES,
                                stores=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.starter = False
        return game

    @pytest.fixture
    def nbmm_rgame(self):
        """game rounds but no blocks"""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                min_move=2,
                                rounds=gi.Rounds.NO_MOVES,
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

        game.new_game()
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

        rgame.new_game()
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

         # turn is set True if no winner
         (RoundStarter.ALTERNATE, True, None, False),
         (RoundStarter.LOSER, False, None, False),
         (RoundStarter.WINNER, True, None, True),
         (RoundStarter.LAST_MOVER, True, None, False),
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
        rgame.turn = winner if winner is not None else True
        rgame.mdata = move_data.MoveData(rgame, 2)
        rgame.mdata.player = last_player
        rgame.mdata.winner = winner

        rgame.new_game(new_round=True)

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

        rgame.new_game(new_round=True)

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

        nb_rgame.new_game(new_round=True)

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


    EVEN_CASES = [
        # even fill no adjustment
        ('rgame',    [4, 8], [1, 1, 1, 1, 1, 1], [1, 5]),
        ('rgame',    [8, 4], [1, 1, 1, 1, 1, 1], [5, 1]),
        ('nb_rgame', [4, 8], [1, 1, 1, 1, 1, 1], [1, 5]),
        ('nb_rgame', [8, 4], [1, 1, 1, 1, 1, 1], [5, 1]),

        # even will with 0, add two to make playable
        ('rgame',    [2, 10], [2, 0, 0, 2, 0, 0], [0, 8]),
        ('rgame',    [10, 2], [2, 0, 0, 2, 0, 0], [8, 0]),
        ('nb_rgame', [2, 10], [2, 0, 0, 2, 0, 0], [0, 8]),
        ('nb_rgame', [10, 2], [2, 0, 0, 2, 0, 0], [8, 0]),

        # min move set to 2
        ('nbmm_rgame', [4, 8], [2, 1, 1, 2, 1, 1], [0, 4]),
        ('nbmm_rgame', [8, 4], [2, 1, 1, 2, 1, 1], [4, 0]),
        ('nbmm_rgame', [2, 10], [2, 0, 0, 2, 0, 0], [0, 8]),
        ('nbmm_rgame', [10, 2], [2, 0, 0, 2, 0, 0], [8, 0]),
        ('nbmm_rgame', [3, 9], [3, 0, 0, 3, 0, 0], [0, 6]),
        ('nbmm_rgame', [9, 3], [3, 0, 0, 3, 0, 0], [6, 0]),
           ]

    @pytest.mark.parametrize(
        'game_fixt, store, eboard, estore', EVEN_CASES,
        ids=[f'{game_fixt}-{a}-{b}-case{i}'
             for (i, (game_fixt, (a, b), *_)) in enumerate(EVEN_CASES)]
        )
    def test_even_rounds(self, request, game_fixt, store, estore, eboard):

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

        game.new_game(new_round=True)
        # print(game)

        # positive seeds and no loss of seeds
        assert game.store[0] >= 0 and game.store[1] >= 0
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds

        # the resulting game is playable
        game.turn = True
        assert any(game.get_allowable_holes())
        game.turn = False
        assert any(game.get_allowable_holes())

        # test blocks, board and stores
        assert not any(game.blocked)
        assert game.store == estore
        assert game.board == eboard



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

        game.new_game(new_round=True)

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

        game_consts = gconsts.GameConsts(nbr_start=2, holes=nbr_holes)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=gi.Rounds.NO_MOVES,
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

        game.new_game(new_round=True)

        assert game.inhibitor._children == einhibit


class TestRoundTally:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on = [2],
                                stores=True,
                                goal=Goal.RND_WIN_COUNT_MAX,
                                rounds=gi.Rounds.NO_MOVES,
                                goal_param=5,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.mark.parametrize('cond', [WinCond.TIE, WinCond.WIN,
                                      WinCond.ROUND_TIE, WinCond.ROUND_WIN])
    @pytest.mark.parametrize('board',
                             [(0, 0, 0, 0),
                              (1, 2, 3, 4),
                              (8, 8, 8, 8),
                              ])
    def test_restart(self, game, board, cond):

        game.rtally.state = ((1, 1), (2, 3), (5, 8), (3, 0))
        game.board = list(board)
        game.store = (12, 12)

        game.new_game(new_round=cond.is_round_over())

        assert game.board == [3, 3, 3, 3, 3, 3, 3, 3]
        assert game.store == [0, 0]

        if 'ROUND' not in cond.name:
            assert game.rtally.state == ((0, 0), (0, 0), (0, 0), (0, 0))
        else:
            assert game.rtally.state != ((0, 0), (0, 0), (0, 0), (0, 0))


    @pytest.mark.parametrize('cond', [WinCond.TIE, WinCond.WIN,
                                      WinCond.ROUND_TIE, WinCond.ROUND_WIN])
    @pytest.mark.parametrize('start_rule, starter, winner, last, estarter',
                             [
                                 (gi.RoundStarter.ALTERNATE, T, T, T, F),
                                 (gi.RoundStarter.ALTERNATE, T, F, F, F),
                                 (gi.RoundStarter.ALTERNATE, F, T, T, T),
                                 (gi.RoundStarter.ALTERNATE, F, F, F, T),
                                 (gi.RoundStarter.LOSER, T, T, T, F),
                                 (gi.RoundStarter.LOSER, T, T, F, F),
                                 (gi.RoundStarter.LOSER, T, F, T, T),
                                 (gi.RoundStarter.LOSER, T, F, F, T),
                                 (gi.RoundStarter.WINNER, T, T, T, T),
                                 (gi.RoundStarter.WINNER, T, T, F, T),
                                 (gi.RoundStarter.WINNER, T, F, T, F),
                                 (gi.RoundStarter.WINNER, T, F, F, F),
                                 (gi.RoundStarter.LAST_MOVER, T, T, T, T),
                                 (gi.RoundStarter.LAST_MOVER, T, T, F, F),
                                 (gi.RoundStarter.LAST_MOVER, T, F, T, T),
                                 (gi.RoundStarter.LAST_MOVER, T, F, F, F),

                             ])
    def test_new_starter(self, game, cond,
                         start_rule, starter, winner, last, estarter):

        object.__setattr__(game.info, 'round_starter', start_rule)
        game.starter = starter
        game.turn = not winner
        game.mdata = move_data.MoveData(game, 4)
        game.mdata.player = last
        game.mdata.winner = winner

        game.new_game(new_round=cond.is_round_over())

        assert game.starter == estarter
        assert game.turn == estarter


class TestTerritory:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(capt_on = [2],
                                stores=True,
                                goal_param=5,
                                goal=Goal.TERRITORY,
                                rounds=gi.Rounds.NO_MOVES,
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
        game.new_game(new_round=not win)
        assert game.owner == eowners


class TestFixedChildren:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                child_type=gi.ChildType.WEG,
                                child_locs=gi.ChildLocs.FIXED_ONE_RIGHT,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_new_game(self, game):

        game.child = [None] * 3 * 2
        game.new_game()

        assert game.child[2] is False
        assert game.child[5] is True


    def test_move_child(self):
        """Exposing a bug:  The deco chain was built in the wrong
        order: pattern applied before children were made so a
        MOVE_RANDOM could occur from a child.

        There's 50% chance that the random move will be from the
        child due to the allow rule. Do a buch of setups.
        Failed consistently before fix."""

        for _ in range(25):
            game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
            game_info = gi.GameInfo(stores=True,
                                    child_type=gi.ChildType.WEG,
                                    child_locs=gi.ChildLocs.FIXED_ONE_RIGHT,
                                    start_pattern=gi.StartPattern.MOVE_RANDOM,
                                    allow_rule=
                                        gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                    nbr_holes=game_consts.holes,
                                    rules=mancala.Mancala.rules)

            game = mancala.Mancala(game_consts, game_info)
            # new game is now always called in game creation

            assert game.child[2] is False
            assert game.child[5] is True
            assert game.board[2]
            assert game.board[5]




class TestBadEnums:

    def test_bad_round_fill(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'rounds', gi.Rounds.HALF_SEEDS)
        object.__setattr__(game_info, 'round_fill', 25)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)

    def test_bad_round_starter(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'rounds', True)
        object.__setattr__(game_info, 'round_starter', 25)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)
