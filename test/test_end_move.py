# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 03:57:49 2023
@author: Ann"""


# %% imports

import collections

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import end_move
from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import Direct
from game_interface import Goal
from game_interface import WinCond


# %%

TEST_COVERS = ['src\\end_move.py']


# %% some constants

N = None
T = True
F = False




# %%

SBOARD = slice(0, 4)
SCHILD = slice(4, 8)
STORE = 8

OSTORE = 4
OSEEDS = 5
OERROR = 6


CONVERT_DICT = {'N': None,
                'T': True,
                'F': False,
                '': None}

def make_ints(vals):
    return [int(val) for val in vals]


def read_claimer_cases():

    global TNAMES, CASES

    with open('test/eg_claimers_cases.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    tnames = lines[0].split(',')
    TNAMES = [name for name in tnames[:-1] if name]

    Case = collections.namedtuple('Case',
                                  ['board', 'child', 'store', 'results'])
    Result = collections.namedtuple('Result',
                                    ['board', 'store', 'seeds', 'error'])

    CASES = []
    for lcnt in range(3, len(lines), 2):

        line_one = lines[lcnt].split(',')
        line_two = lines[lcnt + 1].split(',')

        case = Case(
            make_ints(utils.build_board(line_one[SBOARD], line_two[SBOARD])),
            [CONVERT_DICT[val] for val in
                 utils.build_board(line_one[SCHILD], line_two[SCHILD])],
            make_ints([line_two[STORE], line_one[STORE]]),
            {})

        CASES += [case]

        start = STORE + 1
        for name in TNAMES:

            case.results[name] = Result(
                make_ints(utils.build_board(
                    line_one[(start):(start + 4)],
                    line_two[(start):(start + 4)])),
                make_ints([line_two[start + OSTORE],
                           line_one[start + OSTORE]]),
                make_ints([line_two[start + OSEEDS],
                           line_one[start + OSEEDS]]),
                CONVERT_DICT[line_one[start + OERROR]])

            start += OERROR + 1

read_claimer_cases()


# %%

class TestClaimers:

    @pytest.fixture
    def game(self):
        """minimum game class for claimers"""

        class ClaimerTestGame:
            def __init__(self):
                self.cts = gc.GameConsts(nbr_start=2, holes=4)
                self.board = [2, 2, 2, 2]
                self.child = [F, F, F, F]
                self.store = [0, 0]

        return ClaimerTestGame()


    @pytest.mark.parametrize('tname', TNAMES)
    @pytest.mark.parametrize('case', CASES)
    def test_claimer(self, game, tname, case):

        game.board = case.board.copy()
        game.child = case.child.copy()
        game.store = case.store.copy()

        assert sum(game.board) + sum(game.store) == game.cts.total_seeds, \
            "Game setup error."

        tclass = getattr(end_move, tname)
        claimer = tclass(game)
        seeds = claimer.claim_seeds()

        assert seeds == case.results[tname].seeds
        assert game.board == case.results[tname].board
        assert game.store == case.results[tname].store
        if case.results[tname].error:
            assert sum(game.board) + sum(game.store) != game.cts.total_seeds
        else:
            assert sum(game.board) + sum(game.store) == game.cts.total_seeds





# %%

class TestEndMove:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def pagame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                evens=True,
                                mustpass=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def rgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                rounds=True,
                                blocks=True,  # req with rounds
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def mmgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                min_move=2,
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def mmshgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                min_move=2,
                                mustshare=True,
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def no_win_game(self):
        """win_count is patched so that the Winner class will not
        declare a winner; that is no one has winner_cnt seeds.
        The Winner class should collect seeds and return GAME_OVER. """

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        object.__setattr__(game_consts, 'win_count', game_consts.total_seeds)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                mustshare=True,
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'fixture, ended, repeat, board, store, turn,'
        ' eres, eboard, estore, eturn',
        [  # 0: no win
            ('game', False, False,
             utils.build_board([0, 2, 1],
                               [0, 2, 0]), [3, 4], True, None,
             utils.build_board([0, 2, 1],
                               [0, 2, 0]), [3, 4], True),

            # 1: true win on true turn, playable
            ('game', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True, WinCond.WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True),

            # 2: true win on false turn, playable
            ('game', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], False, WinCond.WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True),

            # 3: false win on false turn, playable
            ('game', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False, WinCond.WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False),

            # 4: false win on true turn, playable
            ('game', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], True, WinCond.WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False),

            # 5: tie on false turn, playable
            ('game', False, False,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], False, WinCond.TIE,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], False),

            # 6: tie on true turn, playable
            ('game', False, False,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], True, WinCond.TIE,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], True),

            # 7: true's turn ended, false has no moves
            ('game', False, False,
             utils.build_board([5, 0, 0],
                               [0, 0, 0]), [3, 4], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [3, 9], True),

            # 8: false's turn ended, true has no moves
            ('game', False, False,
             utils.build_board([0, 0, 0],
                               [0, 0, 5]), [3, 4], False, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [8, 4], False),

            # 9: true win on true turn, playable
            ('rgame', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True, WinCond.ROUND_WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True),

            # 10: test_ft_win
            ('rgame', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], False, WinCond.ROUND_WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True),

            # 11: test_ff_win
            ('rgame', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False, WinCond.ROUND_WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False),

            # 12: test_tf_win
            ('rgame', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], True, WinCond.ROUND_WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False),

            # 13: test_f_tie_win
            ('rgame', False, False,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], False, WinCond.ROUND_TIE,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], False),

            # 14: test_t_tie_win
            ('rgame', False, False,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], True, WinCond.ROUND_TIE,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], True),

            # 15: false's turn ended, true has won, doesn't have seeds
            ('rgame', False, False,
             utils.build_board([1, 0, 0],
                               [0, 0, 0]), [0, 11], False, WinCond.WIN,
             utils.build_board([1, 0, 0],
                               [0, 0, 0]), [0, 11], True),

            # 16: true's turn ended, false has won, true can't continue
            ('rgame', False, False,
             utils.build_board([0, 0, 0],
                               [0, 0, 1]), [11, 0], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 1]), [11, 0], False),

            # 17: game ended, true has won
            ('game', True, False,
             utils.build_board([2, 2, 0],
                               [0, 0, 1]), [3, 4], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [4, 8], True),

            # 18: game ended, false has won
            ('rgame', True, False,
             utils.build_board([1, 0, 0],
                               [0, 2, 2]), [4, 3], False, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [8, 4], False),

            # 19: false's turn ended, no valid moves, true wins
            ('mmgame', False, False,
             utils.build_board([1, 1, 0],
                               [0, 1, 1]), [3, 5], False, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [5, 7], True),

            # 20: true's turn ended, no valid moves, false wins
            ('mmgame', False, False,
             utils.build_board([1, 1, 0],
                               [0, 1, 1]), [5, 3], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [7, 5], False),

            # 21: true's turn ended, no valid moves, false wins
            ('mmshgame', False, False,
             utils.build_board([1, 1, 0],
                               [0, 1, 1]), [5, 3], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [7, 5], False),

            # 22: true's turn ended, false has no moves, no pass
            ('no_win_game', False, False,
             utils.build_board([5, 0, 0],
                               [0, 0, 0]), [3, 4], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [3, 9], True),

            # 23: true's turn ended without seeds, false can't share
            ('no_win_game', False, False,
             utils.build_board([0, 0, 0],
                               [1, 1, 0]), [5, 5], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [7, 5], False),

            # 24: true's turn ended without seeds, false can't share
            ('no_win_game', False, False,
             utils.build_board([0, 0, 0],
                               [1, 1, 0]), [3, 5], True, WinCond.TIE,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [5, 5], None),

            # 25: true has a repeat_turn but no moves, false wins
            ('game', False, True,
             utils.build_board([0, 0, 0],
                               [0, 0, 5]), [3, 4], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [8, 4], False),

            # 26: true's turn ended without moves, false can share
            ('mmshgame', False, False,
             utils.build_board([1, 1, 0],
                               [0, 1, 3]), [3, 3], True, None,
             utils.build_board([1, 1, 0],
                               [0, 1, 3]), [3, 3], True),

            # 27: true has no moves but has a repeat turn, false can share
            ('mmshgame', False, True,
             utils.build_board([1, 1, 0],
                               [0, 1, 3]), [3, 3], True, WinCond.WIN,
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [7, 5], False),

            # 28: true's turn ended, false has no moves, pass
            ('pagame', False, False,
             utils.build_board([5, 0, 0],
                               [0, 0, 0]), [3, 4], True, None,
             utils.build_board([5, 0, 0],
                               [0, 0, 0]), [3, 4], True),

        ])
    def test_wincond(self, request, fixture, ended,
                     repeat, board, store, turn,
                     eres, eboard, estore, eturn):

        game = request.getfixturevalue(fixture)
        game.board = board
        game.store = store
        game.turn = turn

        assert game.win_conditions(repeat_turn=repeat, ended=ended) == eres
        assert game.board == eboard
        assert game.store == estore
        assert game.turn == eturn
        assert not game.test_pass()


class TestEndChildren:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                child=True,
                                convert_cnt=2,
                                evens=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def rgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                rounds=True,
                                blocks=True,  # req with rounds
                                child=True,
                                convert_cnt=2,
                                evens=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'fixture, ended, board, store, turn, '
        'eres, child, eboard, estore, eturn',
        [  # 0: collect seeds and count children to determine win
            ('game', False,
             utils.build_board([0, 2, 1],
                               [0, 2, 0]), [3, 4], True, WinCond.WIN,
             utils.build_board([N, F, N],
                               [N, T, N]),
             utils.build_board([0, 2, 0],
                               [0, 2, 0]), [3, 5], True),

            # 1: false has won with children
            ('game', False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False, WinCond.WIN,
             utils.build_board([F, N, N],
                               [N, N, T]),
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [8, 2], False),

            # 2: collect seeds and count children to determine win, rounds
            ('rgame', False,
                utils.build_board([0, 2, 1],
                                  [0, 2, 0]), [3, 4], True, WinCond.ROUND_WIN,
                utils.build_board([N, F, N],
                                  [N, T, N]),
                utils.build_board([0, 2, 0],
                                  [0, 2, 0]), [3, 5], True),

            # 3: true has won with children, rounds
            ('rgame', False,
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True, WinCond.ROUND_WIN,
             utils.build_board([F, N, N],
                               [N, N, T]),
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True),
        ])
    def test_wincond(self, request, fixture, ended,
                     board, store, turn, child,
                     eres, eboard, estore, eturn):

        game = request.getfixturevalue(fixture)
        game.board = board
        game.child = child
        game.store = store
        game.turn = turn

        assert game.win_conditions(ended=ended) == eres
        assert game.board == eboard
        assert game.store == estore
        assert game.turn == eturn
        assert not game.test_pass()

class TestEndDeprive:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.mark.parametrize('turn, board, econd, ewinner',
                             [(False, utils.build_board([0, 0, 0],
                                                        [0, 3, 0]),
                               WinCond.WIN, False),
                              (True, utils.build_board([0, 0, 0],
                                                       [0, 3, 0]),
                                WinCond.WIN, False),

                              (False, utils.build_board([0, 3, 0],
                                                        [0, 0, 0]),
                               WinCond.WIN, True),
                              (True, utils.build_board([0, 3, 0],
                                                        [0, 0, 0]),
                               WinCond.WIN, True),
                              (True, utils.build_board([0, 3, 0],
                                                       [0, 3, 0]),
                                None, None),
                              (False, utils.build_board([0, 3, 0],
                                                        [0, 3, 0]),
                               None, None),

                              ])
    def test_end_game(self, game, turn, board, econd, ewinner):

        game.board = board
        game.turn = turn

        cond, winner = game.deco.ender.game_ended(False, False)
        assert cond == econd
        assert winner == ewinner


class TestEndWaldas:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(child=True,
                                convert_cnt=4,
                                mustpass=True,
                                sow_direct=Direct.SPLIT,
                                waldas=True,
                                capt_on=[4],
                                skip_start=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('turn, board, child, eboard',
                             [(True,
                               [0, 0, 0, 0, 10, 12, 2, 1, 1, 0, 4, 18],
                               [None, None, None, None, True, True,
                                None, None, None, None, None, False],
                               [0, 0, 0, 0, 18, 12, 0, 0, 0, 0, 0, 18]),
                              (True,
                               [0, 0, 0, 0, 10, 12, 2, 1, 1, 0, 4, 18],
                               [None, None, None, None, True, True,
                                None, None, None, None, None, None],
                               [0, 0, 0, 0, 36, 12, 0, 0, 0, 0, 0, 0]),
                              (False,
                               [2, 1, 1, 0, 4, 40, 0, 0, 0, 0, 0, 0],
                               [None, None, None, None, None, None,
                                None, None, None, None, None, False],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48]),
                              (False,
                               [2, 1, 1, 0, 4, 40, 0, 0, 0, 0, 0, 0],
                               [None, None, None, None, None, None,
                                None, None, None, None, None, None],
                               [48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                              (True,
                                [0, 0, 0, 0, 18, 12, 0, 0, 0, 0, 0, 18],
                                [None, None, None, None, True, True,
                                 None, None, None, None, None, False],
                                [0, 0, 0, 0, 18, 12, 0, 0, 0, 0, 0, 18],
                                ),
                              ],
                             ids=[f'case_{c}' for c in range(5)])
    def test_no_pass(self, game, turn, board, child, eboard):

        # get the config vars, change mustpass, build new game
        consts = game.cts
        info = game.info
        object.__setattr__(info, 'mustpass', False)
        info.__post_init__(nbr_holes=game.cts.holes,
                           rules=mancala.Mancala.rules)
        game = mancala.Mancala(consts, info)

        game.turn = turn
        game.board = board
        game.child = child
        game.store = [0, 0]

        cond = game.move(3)
        assert cond.name == 'WIN'
        assert game.board == eboard


    def test_end_game_no_walda(self, game):

        cond = game.end_game()

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'tie' in winmsg[1]


    def test_end_game_t_walda(self, game):

        game.turn = False
        game.board = [8, 0, 2, 1, 8, 6, 4, 0, 8, 8, 2, 1]
        game.child = [None, None, None, None, None, True,
                      None, None, None, None, None, None]
        game.store = [0, 0]

        cond = game.end_game()
        assert game.board == [0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0]

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


    def test_end_game_f_walda(self, game):

        game.turn = False
        game.board = [8, 0, 2, 1, 8, 6, 4, 0, 8, 8, 2, 1]
        game.child = [False, None, None, None, None, None,
                      None, None, None, None, None, None]
        game.store = [0, 0]

        cond = game.end_game()
        assert game.board == [48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Bottom' in winmsg[1]


    def test_end_game_both_walda(self, game):

        game.turn = False
        game.board = [8, 0, 2, 1, 8, 6, 4, 0, 8, 8, 2, 1]
        game.child = [True, None, None, None, None, False,
                      None, None, None, None, None, None]
        game.store = [0, 0]

        cond = game.end_game()
        assert game.board == [25, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0]

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert 'Top' in winmsg[1]


class TestNoSides:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(no_sides=True,
                                stores=True,
                                capt_on=[3],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_no_sides(self, game):
        """Everything except construction is already tested."""

        pass


class TestQuitter:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def chgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                evens=True,
                                child=True,
                                convert_cnt=2,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def nsgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                evens=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def chnsgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                evens=True,
                                child=True,
                                convert_cnt=2,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def rgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                rounds=True,
                                blocks=True,  # req with rounds
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def no_win_game(self):
        """win_count is patched so that the Winner class will not
        declare a winner.  The Winner class should collect seeds
        and return GAME_OVER. Expectation is that a derived
        game dynamics class will wrap the deco chain and do the
        right thing with GAME_OVER--none of the rest of code
        is designed to handle it.

        GAME_OVER is only return if something in the deco chain
        decides that the game is over (e.g. MUSTSHARE, NOPASS)."""
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        object.__setattr__(game_consts, 'win_count', game_consts.total_seeds)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                evens=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'fixture, board, store, turn, '
        'eres, child, eboard, estore, eturn',
        [   # 0:  stores, no child - divvy odd, true gets extra
            ('game',
             utils.build_board([2, 2, 1],
                               [0, 0, 0]), [3, 4], True, WinCond.TIE,
             utils.build_board([N, N, N],
                               [N, N, N]),
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], True),

            # 1:  stores, no child - divvy odd, false gets extra
            ('game',
             utils.build_board([2, 2, 1],
                               [0, 0, 0]), [4, 3], True, WinCond.TIE,
             utils.build_board([N, N, N],
                               [N, N, N]),
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], True),

            # 2:  stores, no child - divvy even
            ('game',
             utils.build_board([0, 0, 0],
                               [2, 2, 0]), [3, 5], True, WinCond.WIN,
             utils.build_board([N, N, N],
                               [N, N, N]),
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [5, 7], True),

            # 3:  stores, child - divvy odd
            ('chgame',
             utils.build_board([0, 2, 1],
                               [0, 2, 0]), [3, 4], True, WinCond.TIE,
             utils.build_board([N, F, N],
                               [N, T, N]),
             utils.build_board([0, 2, 0],
                               [0, 2, 0]), [4, 4], True),

            # 4:  stores, child - divvy even
            ('chgame',
             utils.build_board([1, 2, 1],
                               [0, 3, 0]), [2, 3], True, WinCond.WIN,
             utils.build_board([N, F, N],
                               [N, T, N]),
             utils.build_board([0, 2, 0],
                               [0, 3, 0]), [3, 4], True),

            # 5: no store, no children
            ('nsgame',
             utils.build_board([2, 2, 1],
                               [4, 0, 3]), [0, 0], True, WinCond.TIE,
             utils.build_board([N, N, N],
                               [N, N, N]),
             utils.build_board([2, 2, 1],
                               [4, 0, 3]), [0, 0], True),

            # 6:  no stores, child - divvy odd
            ('chnsgame',
             utils.build_board([0, 3, 2],
                               [0, 4, 3]), [0, 0], True, WinCond.TIE,
             utils.build_board([N, F, N],
                               [N, T, N]),
             utils.build_board([0, 6, 0],
                               [0, 6, 0]), [0, 0], True),

            # 6b:  no stores, child - divvy odd
            ('chnsgame',
             utils.build_board([0, 4, 2],
                               [0, 3, 3]), [0, 0], True, WinCond.TIE,
             utils.build_board([N, F, N],
                               [N, T, N]),
             utils.build_board([0, 6, 0],
                               [0, 6, 0]), [0, 0], True),

            # 7:  no stores, child - divvy even
            ('chnsgame',
             utils.build_board([2, 3, 0],
                               [2, 5, 0]), [0, 0], True, WinCond.WIN,
             utils.build_board([N, F, N],
                               [N, T, N]),
             utils.build_board([0, 5, 0],
                               [0, 7, 0]), [0, 0], True),

            # 8:  no stores, True child only
            ('chnsgame',
             utils.build_board([2, 3, 0],
                               [2, 5, 0]), [0, 0], True, WinCond.WIN,
             utils.build_board([N, N, N],
                               [N, T, N]),
             utils.build_board([0, 0, 0],
                               [0, 12, 0]), [0, 0], True),

            # 9:  no stores, False child only
            ('chnsgame',
             utils.build_board([2, 3, 0],
                               [2, 5, 0]), [0, 0], True, WinCond.WIN,
             utils.build_board([N, N, N],
                               [N, F, N]),
             utils.build_board([0, 0, 0],
                               [0, 12, 0]), [0, 0], False),

            # 10:  no stores, child but none
            ('chnsgame',
             utils.build_board([2, 3, 0],
                               [2, 5, 0]), [0, 0], True, WinCond.TIE,
             utils.build_board([N, N, N],
                               [N, N, N]),
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [0, 0], True),

            # 11: rounds, end game returns definitive result
            ('rgame',
                utils.build_board([0, 2, 1],
                                  [0, 2, 0]), [3, 4], True, WinCond.TIE,
                utils.build_board([N, F, N],
                                  [N, T, N]),
                utils.build_board([0, 2, 0],
                                  [0, 2, 0]), [4, 4], True),

            # 12: rounds, end game returns definitive result
            ('rgame',
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True, WinCond.WIN,
             utils.build_board([F, N, N],
                               [N, N, T]),
             utils.build_board([1, 0, 0],
                               [0, 0, 1]), [2, 8], True),

            # 13:
            ('no_win_game',
             utils.build_board([5, 0, 0],
                               [0, 0, 0]), [3, 4], True, WinCond.GAME_OVER,
             utils.build_board([N, N, N],
                               [N, N, N]),
             utils.build_board([0, 0, 0],
                               [0, 0, 0]), [6, 6], None),

        ])
    def test_ended(self, request, fixture,
                   board, store, turn, child,
                   eres, eboard, estore, eturn):

        game = request.getfixturevalue(fixture)
        game.board = board
        game.child = child
        game.store = store
        game.turn = turn

        assert game.end_game() == eres
        assert game.board == eboard
        assert game.store == estore
        assert game.turn == eturn
