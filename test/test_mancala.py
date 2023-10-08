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

import re

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import cfg_keys as ckey
from context import game_constants as gc
from context import game_interface as gi
from context import mancala
from context import minimax

from game_interface import Direct
from game_interface import Goal
from game_interface import WinCond

# %%

TEST_COVERS = ['src\\mancala.py']


# %% constants

T = True
F = False
N = None



# %%


@pytest.mark.filterwarnings("ignore")
class TestConctruction:

    @pytest.fixture
    def min_game_if(self):
        return gi.GameInfo(nbr_holes=6,
                           rules=mancala.Mancala.rules)

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

    def test_min_params(self, min_game_if):

        mancala.Mancala(gc.GameConsts(3, 5), min_game_if)


class TestSetPlayer:

    @pytest.fixture
    def game(self):
        """Game that has access to all of the state data."""

        game_consts = gc.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(nbr_holes = game_consts.holes,
                                capt_on = [2],
                                blocks=True,
                                rounds=True,
                                child=True,
                                convert_cnt=2,
                                moveunlock=True,
                                ai_params={"mm_depth" : [1, 1, 3, 5]},
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        return game

    def test_set_player(self, mocker, game):
        # can't mock/spy the player because we are changing it
        setd = mocker.spy(game, 'set_difficulty')
        game.set_player(minimax.MiniMaxer(game))
        assert setd.call_count == 1

    def test_bad_set_player(self, game):
        with pytest.raises(TypeError):
            game.set_player(5)


class TestGameState:

    @pytest.fixture
    def game(self):
        """Game that has access to all of the state data."""

        game_consts = gc.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(nbr_holes = game_consts.holes,
                                capt_on = [2],
                                blocks=True,
                                rounds=True,
                                child=True,
                                convert_cnt=2,
                                moveunlock=True,
                                ai_params={"mm_depth" : [1, 1, 3, 5]},
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        return game


    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child, ere_one, ere_two',
        [((1, 2, 3, 4), [0, 0], False,
          None, None, None,
          ' *4 +3 *$', ' *1 +2 +\\* *$'),
         ((1, 2, 3, 4), [2, 0], True,
           None, None, None,
           ' *4 +3 +\\* *$', ' *1 +2 +2 *$'),
         ((1, 2, 3, 4), [0, 2], True,
           None, None, None,
           ' *4 +3 +\\* +2 *$', ' *1 +2 *$'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, None,
          ' *4 +3_ +\\* *$', ' *1 +2_ *$'),
         ((1, 2, 3, 4), [0, 0], True,
          None, [T, F, F, T], None,
          ' *x +3 +\\* *$', ' *x +2 *$'),
         ((1, 2, 3, 4), [0, 0], True,
          None, None, [T, F, N, N],
          ' *4 +3 +\\* *$', ' *1˄ +2˅ *$'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, [T, F, N, N],
          ' *4 +3_ +\\* *$', ' *1 ˄ +2_˅ *$'),
         ])
    def test_state_const(self, board, store, turn,
                         unlocked, blocked, child,
                         ere_one, ere_two):

        state = mancala.GameState(board=board,
                                  store=store,
                                  _turn=turn,
                                  unlocked=unlocked,
                                  blocked=blocked,
                                  child=child)
        assert state.board == board
        assert state.store == store
        assert state._turn == turn
        assert state.turn == turn
        assert state.unlocked == unlocked
        assert state.blocked == blocked
        assert state.child == child
        gstrs = str(state).split('\n')
        assert re.match(ere_one, gstrs[0])
        assert re.match(ere_two, gstrs[1])


    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child',
        [((1, 2, 3, 4), (0, 0), False, None, None, None),
         ((1, 2, 3, 4), (2, 0), True,  None, None, None),
         ((1, 2, 3, 4), (0, 2), True,  None, None, None),
         ((1, 2, 3, 4), (0, 0), True,
          (T, F, F, T), None, None),
         ((1, 2, 3, 4), (0, 0), True,
          None, (T, F, F, T), None),
         ((1, 2, 3, 4), (0, 0), True,
          None, None, (T, F, N, N)),
         ((1, 2, 3, 4), (0, 0), True,
          (T, F, F, T), None, (T, F, N, N)),
         ])
    def test_getter(self, game, board, store, turn,
                    unlocked, blocked, child):

        game.board = board
        game.store = store
        game.turn = turn

        if unlocked:
            game.unlocked = unlocked
        else:
            object.__setattr__(game.info,
                               'moveunlock',
                               False)
        if blocked:
            game.blocked = blocked
        else:
            object.__setattr__(game.info,
                               'blocks',
                               False)
        if child:
            game.child = child
        else:
            object.__setattr__(game.info,
                               'child',
                               False)

        state = game.state
        assert state.board == board
        assert state.store == store
        assert state._turn == turn
        assert state.turn == turn
        assert state.unlocked == unlocked
        assert state.blocked == blocked
        assert state.child == child


    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child',
        [((1, 2, 3, 4), (0, 0), False, None, None, None),
         ((1, 2, 3, 4), (2, 0), True,  None, None, None),
         ((1, 2, 3, 4), (0, 2), True,  None, None, None),
         ((1, 2, 3, 4), (0, 0), True,
          (T, F, F, T), None, None),
         ((1, 2, 3, 4), (0, 0), True,
          None, (T, F, F, T), None),
         ((1, 2, 3, 4), (0, 0), True,
          None, None, (T, F, N, N)),
         ((1, 2, 3, 4), (0, 0), True,
          (T, F, F, T), None, (T, F, N, N)),
         ])
    def test_setter(self, game, board, store, turn,
                    unlocked, blocked, child):

        game.state = mancala.GameState(board=board,
                                       store=store,
                                       _turn=turn,
                                       unlocked=unlocked,
                                       blocked=blocked,
                                       child=child)

        assert game.board == list(board)
        assert game.store == list(store)
        assert game.turn == turn

        if unlocked:
            assert game.unlocked == list(unlocked)
        else:
            assert game.unlocked == [F, F, F, F]

        if blocked:
            assert game.blocked == list(blocked)
        else:
            assert game.blocked == [F, F, F, F]

        if child:
            assert game.child == list(child)
        else:
            assert game.child == [N, N, N, N]



class TestBasics:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes = game_consts.holes,
                                capt_on = [2],
                                ai_params={"mm_depth" : [1, 1, 3, 5]},
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.fixture
    def mrgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                mustpass=True,
                                stores=True,
                                blocks=True,
                                moveunlock=True,
                                sow_direct=Direct.CCW,
                                evens=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_get_info(self, game):

        info = game.get_game_info()
        assert isinstance(info, gi.GameInfo)
        assert info.capt_on == [2]
        assert info.sow_direct == Direct.CCW

    def test_set_diff(self, game):

        game.set_difficulty(3)
        assert game.difficulty == 3
        assert game.player.max_depth == 5

        string = game.params_str()
        assert ckey.GAME_CLASS in string
        assert ckey.UDIRECT not in string
        assert 'GameConsts' in string
        assert 'GameInfo' in string


    def test_get_store(self, game):

        game.store = [3, 4]
        # param is row not player
        assert game.get_store(0) == 4
        assert game.get_store(1) == 3

    def test_sides(self, game):

        assert not game.cts.opp_side(game.turn, 0)
        assert game.cts.opp_side(game.turn, 7)

        assert game.cts.my_side(game.turn, 0)
        assert not game.cts.my_side(game.turn, 7)

        game.turn = True

        assert game.cts.opp_side(game.turn, 0)
        assert not game.cts.opp_side(game.turn, 7)

        assert not game.cts.my_side(game.turn, 0)
        assert game.cts.my_side(game.turn, 7)


class TestEndGames:

    @pytest.fixture
    def game(self):

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

    @pytest.mark.parametrize(
        'board, store, econd, eturn',
        [(utils.build_board([1, 0, 0],
                            [0, 0, 1]), [7, 3], WinCond.WIN, False),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [3, 7], WinCond.WIN, True),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [5, 5], WinCond.TIE, False),
         (utils.build_board([1, 0, 0],
                            [0, 0, 1]), [0, 10], WinCond.WIN, True)
         ])
    def test_rounds_end(self, rgame, board, store, econd, eturn):

        rgame.board = board
        rgame.store = store
        assert rgame.end_game() == econd
        assert rgame.turn == eturn


class TestWinMessage:

    @pytest.fixture
    def maxgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def depgame(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=6)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('game_fixt', ['maxgame', 'depgame'])
    @pytest.mark.parametrize('wcond', WinCond)
    @pytest.mark.parametrize('turn', [False, True])
    def test_side_messages(self, request, game_fixt, wcond, turn):

        game = request.getfixturevalue(game_fixt)
        game.turn = turn

        title, message = game.win_message(wcond)

        if 'ROUND' in wcond.name:
            assert 'Round Over' == title
        else:
            assert 'Game Over' == title

        if 'WIN' in wcond.name:
            if turn:
                assert 'Top' in message
            else:
                assert 'Bottom' in message
            assert 'won' in message
            return
        else:
            assert 'Top' not in message
            assert 'Bottom' not in message

        if 'TIE' in wcond.name:
            assert 'tie' in message
            return

        if 'ENDLESS' in wcond.name:
            assert 'No winner' in message
            return

        assert 'Unexpected' in message


    @pytest.mark.parametrize('game_fixt', ['maxgame', 'depgame'])
    @pytest.mark.parametrize('wcond', WinCond)
    def test_goal_messages(self, request, game_fixt, wcond):

        game = request.getfixturevalue(game_fixt)
        game.turn = False

        title, message = game.win_message(wcond)

        print(message)

        if wcond.name in ['WIN', 'ROUND_WIN']:
            if 'max' in game_fixt:
                assert 'most seeds' in message
            elif 'dep' in game_fixt:
                assert 'eliminating' in message
            return

        if 'TIE' in wcond.name:
            if 'max' in game_fixt:
                assert 'ended in a tie' in message
            elif 'dep' in game_fixt:
                assert 'ended with seeds' in message


class TestHoleProp:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'row, pos, eindex',
        [(0, 0, 5),
         (0, 2, 3),
         (1, 0, 0),
         (1, 2, 2)])
    def test_hole_prop(self, game, row, pos, eindex):
        """testing the right pos->loc and array access."""

        game.board = [f'board{i}' for i in range(6)]
        game.unlocked = [f'lock{i}' for i in range(6)]
        game.blocked = [f'block{i}' for i in range(6)]
        game.child = [f'child{i}' for i in range(6)]

        props = game.get_hole_props(row, pos)

        assert props.seeds == 'board' + str(eindex)
        assert props.unlocked == 'lock' + str(eindex)
        assert props.blocked == 'block' + str(eindex)
        assert props.ch_owner == 'child' + str(eindex)




# %% ai interface and scorers

class TestAiIf:

    @pytest.fixture
    def ccw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                sow_direct=Direct.CCW,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def pass_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                min_move=2,
                                mustpass=True,
                                sow_direct=Direct.CCW,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def upass_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                min_move=2,
                                udir_holes=[1],
                                mustpass=True,
                                udirect=True,
                                sow_direct=Direct.SPLIT,
                                rules=mancala.Mancala.rules
                                )

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    def test_ccw_moves(self, ccw_game):

        # false turn
        moves = ccw_game.get_moves()
        assert moves == list(range(4))
        assert ccw_game.move(moves[0]) is None

        # true turn
        moves = ccw_game.get_moves()
        assert moves == list(range(4))
        assert ccw_game.move(moves[-1]) is None

        # false turn 2
        ccw_game.board = utils.build_board([0, 1, 0, 1],
                                           [0, 0, 0, 0])
        assert ccw_game.get_moves() == []

    def test_pass_moves(self, pass_game):

        assert pass_game.turn is False
        pass_game.board = utils.build_board([1, 2, 1, 1],
                                            [0, 3, 1, 2])
        assert pass_game.get_moves() == [1, 3]

        pass_game.board = utils.build_board([1, 2, 1, 1],
                                            [0, 0, 0, 0])
        assert pass_game.get_moves() == [mancala.PASS_TOKEN]

        # this would never get to the get_moves, it's not valid
        # pass_game.board = utils.build_board([0, 1, 0, 1],
        #                                     [0, 0, 0, 0])
        # assert pass_game.get_moves() == []

    def test_upass_moves(self, upass_game):

        # this would never get to the get_moves, it's not valid
        # upass_game.board = utils.build_board([0, 1, 0],
        #                                      [0, 0, 0])
        # assert upass_game.get_moves() == []

        upass_game.board = utils.build_board([2, 1, 0],
                                             [2, 3, 1])
        assert upass_game.get_moves() == [
            (0, None), (1, Direct.CCW), (1, Direct.CW)]

        upass_game.board = utils.build_board([2, 1, 0],
                                             [0, 1, 1])
        assert upass_game.get_moves() == [(mancala.PASS_TOKEN, None)]

    def test_maxer(self, ccw_game):

        assert ccw_game.turn == False
        assert ccw_game.is_max_player() == True

        ccw_game.turn = True
        assert ccw_game.is_max_player() == False

    def test_score_endgame(self, ccw_game):

        assert ccw_game.turn == False
        assert ccw_game.score(WinCond.WIN) == 1000
        assert ccw_game.score(WinCond.TIE) == 5
        assert ccw_game.score(WinCond.ENDLESS) == 0

        ccw_game.turn = True
        assert ccw_game.score(WinCond.WIN) == -1000
        assert ccw_game.score(WinCond.TIE) == -5
        assert ccw_game.score(WinCond.ENDLESS) == 0


class TestScorer:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                scorer=gi.Scorer(easy_rand=0),
                                capt_on=[2],
                                sow_direct=Direct.CCW,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_sc_end_store(self, game):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info.scorer, 'repeat_turn', 10)

        assert game.score(None) == 0
        game.turn = False
        assert game.score(WinCond.END_STORE) == 10
        game.turn = True
        assert game.score(WinCond.END_STORE) == -10


    def test_sc_evens(self, game):

        object.__setattr__(game.info.scorer, 'evens_m', 2)
        object.__setattr__(game.info.scorer, 'stores_m', 0)

        assert game.info.scorer.evens_m == 2
        assert sum(vars(game.info.scorer).values()) == 2

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert game.score(None) == (1 - 2) * 2


    def test_sc_seeds(self, game):

        object.__setattr__(game.info.scorer, 'seeds_m', 3)
        object.__setattr__(game.info.scorer, 'stores_m', 0)

        assert game.info.scorer.seeds_m == 3
        assert sum(vars(game.info.scorer).values()) == 3

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert game.score(None) == (10 - 7) * 3


    def test_sc_empties(self, game):

        object.__setattr__(game.info.scorer, 'empties_m', 2)
        object.__setattr__(game.info.scorer, 'stores_m', 0)

        assert game.info.scorer.empties_m == 2
        assert sum(vars(game.info.scorer).values()) == 2

        game.board = utils.build_board([2, 4, 0, 0],
                                       [0, 5, 4, 1])
        assert game.score(None) == (1 - 2) * 2



    def test_sc_stores(self, game):
        assert game.info.scorer.stores_m == 4
        assert sum(vars(game.info.scorer).values()) == 4

        game.store = [5, 3]
        assert game.score(None) == (5 - 3) * 4


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
    def test_sc_stores_child(self, game, board, store, child, escore):

        object.__setattr__(game.info, 'child', True)

        assert game.info.scorer.stores_m == 4
        assert sum(vars(game.info.scorer).values()) == 4

        game.board = board
        game.store = store
        game.child = child
        assert game.score(None) == escore


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
    def test_sc_child_cnt(self, game, child, escore):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info, 'child', True)
        object.__setattr__(game.info.scorer, 'child_cnt_m', 15)

        game.child = child
        assert game.score(None) == escore


    def test_sc_easy(self, game):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info.scorer, 'easy_rand', 26)

        game.set_difficulty(1)
        assert all(game.score(None) for _ in range(10)) == 0

        game.set_difficulty(0)
        assert any(game.score(None) for _ in range(10)) != 0


    def test_sc_access(self, game):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info.scorer, 'access_m', 10)

        game.set_difficulty(1)
        assert all(game.score(None) for _ in range(10)) == 0

        game.set_difficulty(2)
        game.board = [1, 1, 1, 0, 4, 4, 4, 4]
        assert game.score(None) == -40

        game.board = [4, 4, 4, 4, 1, 1, 1, 0]
        assert game.score(None) == 40

        game.board = [1, 1, 1, 0, 1, 1, 4, 3]
        assert game.score(None) == -10

        object.__setattr__(game.info, 'mlaps', True)
        assert game.score(None) == 0


class TestMove:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                scorer=gi.Scorer(easy_rand=0),
                                capt_on=[2],
                                sow_direct=Direct.CCW,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_move_ifs(self, game, mocker):

        pick_move = mocker.spy(game.player, 'pick_move')
        move_desc = mocker.spy(game.player, 'get_move_desc')

        game.get_ai_move()
        assert pick_move.call_count == 1
        assert move_desc.call_count == 0
        mocker.resetall()

        game.get_ai_move_desc()
        assert pick_move.call_count == 0
        assert move_desc.call_count == 1
