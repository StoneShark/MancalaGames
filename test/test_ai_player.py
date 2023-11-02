# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:30:04 2023

@author: Ann
"""

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import ai_interface
from context import ai_player
from context import cfg_keys as ckey
from context import game_constants as gc
from context import game_interface as gi
from context import mancala
from context import minimax
from context import montecarlo_ts

from game_interface import ChildType
from game_interface import WinCond


TEST_COVERS = ['src\\ai_player.py',
               'src\\ai_interface.py']

# %% constants

T = True
F = False
N = None


# %% ai interface and scorers

# TODO test setup & rules


class TestConstruction:

    def test_default_scorer(self):

        for var in vars(ai_player.ScoreParams):
            if var == 'stores_m':
                assert ai_player.ScoreParams.get_default('stores_m') == 4
            else:
                assert ai_player.ScoreParams.get_default(var) == 0


    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_algorithm(self, game):

        pdict = {'algorithm': 'minimaxer',
                 'scorer': {'stores_m': 8}}
        player = ai_player.AiPlayer(game, pdict)
        assert isinstance(player.algo, minimax.MiniMaxer)
        assert player.sc_params.stores_m == 8
        assert sum(vars(player.sc_params).values()) == 8

        pdict = {'algorithm': 'montecarlo_ts',
                 'scorer': {'easy_rand': 6}}    #st
        player = ai_player.AiPlayer(game, pdict)
        assert isinstance(player.algo, montecarlo_ts.MonteCarloTS)
        assert player.sc_params.easy_rand == 6
        assert sum(vars(player.sc_params).values()) == 10

        pdict = {'algorithm': 'montecarlo_ts',
                 'scorer': {'stores_m': 0,
                            'easy_rand': 6}}
        player = ai_player.AiPlayer(game, pdict)
        assert isinstance(player.algo, montecarlo_ts.MonteCarloTS)
        assert player.sc_params.easy_rand == 6
        assert sum(vars(player.sc_params).values()) == 6

        pdict = {'algorithm': 'minimaxer'}
        player = ai_player.AiPlayer(game, pdict)
        assert player.sc_params.stores_m == 4
        assert sum(vars(player.sc_params).values()) == 4

        pdict = {'scorer': {'stores_m': 8}}
        player = ai_player.AiPlayer(game, pdict)
        assert isinstance(player.algo, minimax.MiniMaxer)
        assert player.sc_params.stores_m == 8
        assert sum(vars(player.sc_params).values()) == 8

        pdict = {'algorithm': 'junky_algo'}
        with pytest.raises(KeyError):
            player = ai_player.AiPlayer(game, pdict)


    def test_difficulty(self, game):

        aid = ai_player.AI_PARAM_DEFAULTS

        pdict = {'algorithm': 'minimaxer'}
        player = ai_player.AiPlayer(game, pdict)
        player.difficulty = 0
        assert player.algo.max_depth == aid[ckey.MM_DEPTH][0]
        player.difficulty = 3
        assert player.algo.max_depth == aid[ckey.MM_DEPTH][3]

        pdict = {'algorithm': 'minimaxer',
                 'ai_params': {'mm_depth': [10, 11, 12, 13]}}
        player = ai_player.AiPlayer(game, pdict)
        player.difficulty = 0
        assert player.algo.max_depth == 10
        player.difficulty = 3
        assert player.algo.max_depth == 13

        pdict = {'algorithm': 'montecarlo_ts'}
        player = ai_player.AiPlayer(game, pdict)
        player.difficulty = 0
        assert player.algo.new_nodes == aid[ckey.MCTS_NODES][0]
        player.difficulty = 3
        assert player.algo.new_nodes == aid[ckey.MCTS_NODES][3]

        pdict = {'algorithm': 'montecarlo_ts',
                 'ai_params': {'mcts_bias': [1, 16, 32, 1000],
                               'mcts_nodes': [10, 20, 30, 40],
                               'mcts_pouts': [1, 4, 8, 16]}}
        player = ai_player.AiPlayer(game, pdict)
        player.difficulty = 0
        val = 1 / 1000
        assert val - 0.001 <= player.algo.bias <= val + 0.001
        assert player.algo.new_nodes == 10
        assert player.algo.nbr_pouts == 1
        player.difficulty = 2
        val = 32 / 1000
        assert val - 0.001 <= player.algo.bias <= val + 0.001
        assert player.algo.new_nodes == 30
        assert player.algo.nbr_pouts == 8

        player.algo = 5
        with pytest.raises(ValueError):
            player.difficulty = 0


    def test_interfaces(self, game, mocker):

        pdict = {'algorithm': 'minimaxer'}
        player = ai_player.AiPlayer(game, pdict)

        m_pick_move = mocker.patch('minimax.MiniMaxer.pick_move')
        player.pick_move()
        m_pick_move.assert_called_once()

        m_get_desc = mocker.patch('minimax.MiniMaxer.get_move_desc')
        player.get_move_desc()
        m_get_desc.assert_called_once()


class TestScorers:


    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def player(self, game):
        return ai_player.AiPlayer(game, {})


    @pytest.fixture
    def nsgame(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                no_sides=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def nsplayer(self, nsgame):
        return ai_player.AiPlayer(nsgame, {})


    def test_score_endgame(self, game, player):

        assert player.difficulty == 1
        assert game.turn == False
        assert player.is_max_player()

        assert player.score(WinCond.WIN) == 1000
        assert player.score(WinCond.TIE) == 5
        assert player.score(WinCond.ENDLESS) == 0

        game.turn = True
        assert not player.is_max_player()
        assert player.score(WinCond.WIN) == -1000
        assert player.score(WinCond.TIE) == -5
        assert player.score(WinCond.ENDLESS) == 0


    def test_sc_end_store(self, game, player):

        player.sc_params.stores_m = 0
        player.sc_params.repeat_turn = 10
        player.collect_scorers()

        assert player.score(None) == 0
        game.turn = False
        assert player.score(WinCond.REPEAT_TURN) == 10
        game.turn = True
        assert player.score(WinCond.REPEAT_TURN) == -10


    def test_sc_diff_evens(self, game, player):

        player.sc_params.evens_m = 2
        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.evens_m == 2
        assert sum(vars(player.sc_params).values()) == 2

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert player.score(None) == (1 - 2) * 2


    def test_sc_cnt_evens(self, nsgame, nsplayer):

        nsplayer.sc_params.evens_m = 2
        nsplayer.sc_params.stores_m = 0
        nsplayer.sc_params.easy_rand = 0
        nsplayer.collect_scorers()

        assert nsplayer.sc_params.evens_m == 2
        assert sum(vars(nsplayer.sc_params).values()) == 2

        nsgame.board = utils.build_board([2, 4, 0, 1],
                                         [0, 5, 4, 1])
        assert nsplayer.score(None) == 3 * 2

        nsgame.turn = True
        assert nsplayer.score(None) == 3 * 2 * -1


    def test_sc_diff_seeds(self, game, player):

        player.sc_params.seeds_m = 3
        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.seeds_m == 3
        assert sum(vars(player.sc_params).values()) == 3

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert player.score(None) == (10 - 7) * 3


    def test_sc_cnt_seeds(self, nsgame, nsplayer):

        nsplayer.sc_params.seeds_m = 3
        nsplayer.sc_params.stores_m = 0
        nsplayer.sc_params.easy_rand = 0
        nsplayer.collect_scorers()

        assert nsplayer.sc_params.seeds_m == 3
        assert sum(vars(nsplayer.sc_params).values()) == 3

        nsgame.board = utils.build_board([2, 4, 0, 1],
                                         [0, 5, 4, 1])
        assert nsplayer.score(None) ==  17 * 3

        nsgame.turn = True
        assert nsplayer.score(None) ==  17 * 3 * -1


    def test_sc_diff_empties(self, game, player):

        player.sc_params.empties_m =  2
        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.empties_m == 2
        assert sum(vars(player.sc_params).values()) == 2

        game.board = utils.build_board([2, 4, 0, 0],
                                       [0, 5, 4, 1])
        assert player.score(None) == (1 - 2) * 2


    def test_sc_cnt_empties(self, nsgame, nsplayer):

        nsplayer.sc_params.empties_m =  2
        nsplayer.sc_params.stores_m = 0
        nsplayer.sc_params.easy_rand = 0
        nsplayer.collect_scorers()

        assert nsplayer.sc_params.empties_m == 2
        assert sum(vars(nsplayer.sc_params).values()) == 2

        nsgame.board = utils.build_board([2, 4, 0, 0],
                                         [0, 5, 4, 1])
        assert nsplayer.score(None) == 3 * 2

        nsgame.turn = True
        assert nsplayer.score(None) == 3 * 2 * -1


    def test_sc_stores(self, game, player):

        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.stores_m == 4
        assert sum(vars(player.sc_params).values()) == 4

        game.store = [5, 3]
        assert player.score(None) == (5 - 3) * 4


    @pytest.mark.parametrize(
        'board, store, child, escore',
        [(utils.build_board([0, 0, 0, 0],
                            [0, 0, 0, 0]), [5, 3],
          utils.build_board([N, N, N, N],
                            [N, N, N, N]), (5 - 3) * 4),

         (utils.build_board([1, 2, 3, 4],
                            [1, 2, 3, 4]), [5, 3],
          utils.build_board([N, F, N, N],
                            [N, N, T, N]), ((5+2) - (3+3)) * 4),

         (utils.build_board([1, 2, 3, 4],
                            [1, 2, 3, 4]), [5, 3],
          utils.build_board([N, F, T, N],
                            [N, N, T, F]), ((5+2+4) - (3+3+3)) * 4),
         ])
    def test_sc_stores_child(self, game, player, board, store, child, escore):

        object.__setattr__(game.info, 'child_type', ChildType.NORMAL)
        object.__setattr__(game.info, 'child_cvt', 4)

        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.stores_m == 4
        assert sum(vars(player.sc_params).values()) == 4

        game.board = board
        game.store = store
        game.child = child
        assert player.score(None) == escore


    @pytest.mark.parametrize(
        'child, escore',
        [(utils.build_board([N, N, N, N],
                            [N, N, N, N]), 0),

         (utils.build_board([N, F, N, N],
                            [N, N, N, N]), 15),

         (utils.build_board([N, T, N, N],
                            [N, N, N, N]), -15),

         (utils.build_board([N, T, F, F],
                            [N, F, N, N]), (3-1) * 15),

         (utils.build_board([N, F, T, T],
                            [N, T, N, N]), (1-3) * 15),

         ])
    def test_sc_child_cnt(self, game, player, child, escore):

        object.__setattr__(game.info, 'child_type', ChildType.NORMAL)
        object.__setattr__(game.info, 'child_cvt', 4)

        player.sc_params.stores_m = 0
        player.sc_params.child_cnt_m = 15
        player.collect_scorers()

        game.child = child
        assert player.score(None) == escore


    def test_sc_easy(self, game, player):

        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 26
        player.collect_scorers()

        player.difficulty = 1
        assert all(player.score(None) == 0 for _ in range(10))

        player.difficulty = 0
        assert any(player.score(None) > 0 for _ in range(10))


    def test_sc_access(self, game, player):

        player.sc_params.stores_m = 0
        player.sc_params.access_m = 10
        player.collect_scorers()

        player.difficulty = 1
        assert player.score(None) == 0

        player.difficulty = 2
        game.board = [1, 1, 1, 0, 4, 4, 4, 4]
        assert player.score(None) == -40

        game.board = [4, 4, 4, 4, 1, 1, 1, 0]
        assert player.score(None) == 40

        game.board = [1, 1, 1, 0, 1, 1, 4, 3]
        assert player.score(None) == -10


class TestAiIf:

    def test_contructors(self):

        class Tplr(ai_interface.AiPlayerIf):

                @property
                def difficulty(self):
                    return 3

                def is_max_player(self):
                    return False

                def score(self, end_cond):
                    return 20

                def pick_move(self):
                    return 34

                def get_move_desc(self):
                    return 'desc'

        with pytest.raises(ValueError):
            Tplr(None, None)

        class Talg(ai_interface.AiAlgorithmIf):
            """A class to enable minimax to pick_moves."""

            def __init__(self, game, player):
                super().__init__(game, player)

            def pick_move(self):
                return False

            def get_move_desc(self):
                return "Move desc"

            def set_params(self, *args):
                pass

        with pytest.raises(ValueError):
            Talg(None, None)

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        with pytest.raises(ValueError):
            Talg(game, None)
