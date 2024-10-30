# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 03:57:49 2023
@author: Ann"""


# %% imports

import collections

import pandas as  pd
import pytest
pytestmark = pytest.mark.unittest

import utils

from context import end_move
from context import game_constants as gc
from context import game_interface as gi
from context import ginfo_rules
from context import mancala

from game_interface import ChildType
from game_interface import Direct
from game_interface import Goal
from game_interface import WinCond


# %%

TEST_COVERS = ['src\\end_move.py']


# %% some constants

N = None
T = True
F = False

REPEAT_TURN = True
ENDED = True

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
    return [int(val.replace('.0', '')) for val in vals]


def read_claimer_cases():

    global TNAMES, CASES

    tfile = 'test/eg_claimers_cases.csv'
    tc_dframe = pd.read_excel('test/eg_claimers_cases.xlsx',
                              header=None)
    with open(tfile, 'w', newline='', encoding='utf-8') as file:
        tc_dframe.to_csv(file, header=False, index=False)


    with open(tfile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines[0] = lines[0][1:]

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
        if tname =='TakeOwnSeeds':
            claimer = tclass(game, game.cts.board_side)
        else:
            claimer = tclass(game)
        seeds = claimer.claim_seeds()

        assert game.board == case.results[tname].board
        assert game.store == case.results[tname].store
        assert seeds == case.results[tname].seeds
        if case.results[tname].error:
            assert sum(game.board) + sum(game.store) != game.cts.total_seeds
        else:
            assert sum(game.board) + sum(game.store) == game.cts.total_seeds





# %%

class TestEndMove:

    @pytest.fixture
    def game(self, request):

        game_props = TestEndMove.GAME_PROPS[request.param]

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        if request.param == 'no_win_game':
            object.__setattr__(game_consts, 'win_count',
                               game_consts.total_seeds)

        game_info = gi.GameInfo(**game_props,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    GAME_PROPS = {
        'game': {'evens': True,
                 'stores': True,
                 },

        'pagame': {'evens': True,
                   'mustpass': True,
                   'stores': True,
                   },

        'rgame': {'rounds': gi.Rounds.HALF_SEEDS,
                  'evens': True,
                  'stores': True,
                  },

        'mmgame': {'min_move': 2,
                   'evens': True,
                   'stores': True,
                   },

        'mmshgame': {'min_move': 2,
                     'mustshare': True,
                     'evens': True,
                     'stores': True,
                     },
        'no_win_game': {'mustshare': True,
                        'evens': True,
                        'stores': True,
                        },

        'rugame': {'rounds': gi.Rounds.HALF_SEEDS,
                   'round_fill': gi.RoundFill.UMOVE,
                   'min_move': 2,
                   'evens': True,
                   'stores': True,
                  },

        'r2game': {'rounds': gi.Rounds.HALF_SEEDS,
                   'gparam_one': 2,   # need two holes to continue (new round)
                   'evens': True,
                   'stores': True,
                  },

        'cogame': {'capt_on': [6],
                   'stores': True,
                  },


        'shgame': {'mustshare': True,
                   'evens': True,
                   'stores': True,
                   'capt_rturn': True,
                  },

    }


    WINCASES = [  # 0: no win
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
                 utils.build_board([2, 0, 0],
                                   [0, 0, 0]), [0, 10], False, WinCond.WIN,
                 utils.build_board([2, 0, 0],
                                   [0, 0, 0]), [0, 10], True),

                # 16: true's turn ended, false has won, true can't continue
                ('rgame', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 2]), [10, 0], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 2]), [10, 0], False),

                # 17: game ended, true has won
                ('game', ENDED, False,
                 utils.build_board([2, 2, 0],
                                   [0, 0, 1]), [3, 4], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [4, 8], True),

                # 18: game ended, false has won
                ('rgame', ENDED, False,
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
                                   [1, 1, 0]), [4, 6], True, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # 25: true has a repeat_turn but no moves, false wins
                ('game', False, REPEAT_TURN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 5]), [3, 4], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [8, 4], False),

                # 26: true's turn ended without moves, false can share and capture
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

                # 29: UMOVE game
                ('rugame', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], True, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], True),

                # 30:  True has just enough seeds to continue
                ('rugame', False, False,
                 utils.build_board([2, 1, 1],
                                   [1, 1, 0]), [5, 0], True, WinCond.ROUND_WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [7, 4], False),

                #31: True does not have enough seeds to continue
                ('rugame', False, False,
                 utils.build_board([2, 1, 0],
                                   [1, 1, 1]), [6, 0], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [9, 3], False),

                # 32: gparam_one with MAX_SEEDS & rounds, e.g. don't need all
                ('r2game', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 6], True, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 6], True),

                # 33: enough seeds to keep playing
                ('r2game', False, False,
                 utils.build_board([2, 2, 0],
                                   [0, 2, 2]), [0, 10], False, WinCond.ROUND_WIN,
                 utils.build_board([2, 2, 0],
                                   [0, 2, 2]), [0, 10], True),

                # 34: not enough seeds to keep playing
                ('r2game', False, False,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 2]), [0, 10], False, WinCond.WIN,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 2]), [0, 10], True),

                # 35: capt_on = 6, can't capt more
                ('cogame', False, False,
                 utils.build_board([2, 0, 0],
                                   [0, 2, 0]), [4, 4], False, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),


                # 36: F moved all but one seed to T, now Ts move
                ('shgame', False, False,
                 utils.build_board([0, 1, 2],
                                   [1, 0, 0]), [5, 5], False, None,
                 utils.build_board([0, 1, 2],
                                   [1, 0, 0]), [5, 5], False),

                # 37: move after 36  Ts move, first move capt all F seeds,
                #     now T repeat turn but can't share,
                #     T still wins on seed collection
                ('shgame', False, REPEAT_TURN,
                 utils.build_board([0, 0, 2],
                                   [0, 0, 0]), [5, 5], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [5, 7], True),

            ]
    @pytest.mark.filterwarnings("ignore")
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize(
        'game, ended, repeat, board, store, turn,'
        ' eres, eboard, estore, eturn',
        WINCASES,
        indirect=['game'],
        ids=[f'case_{c}' for c in range(len(WINCASES))])
    def test_game_ended(self, game, ended,
                        repeat, board, store, turn,
                        eres, eboard, estore, eturn):

        game.board = board
        game.store = store
        game.turn = turn
        cond, winner = game.deco.ender.game_ended(repeat_turn=repeat,
                                                  ended=ended)
        assert cond == eres
        assert game.board == eboard
        assert game.store == estore
        if eturn is not None:
            assert winner == eturn
        assert not game.test_pass()


    @pytest.mark.parametrize(
        'game', ['game'], indirect=['game'])
    def test_str(self, game):
        """Printing the claimer is unique to enders."""
        assert 'ClaimSeeds' in str(game.deco.ender)



class TestEndChildren:


    GAME_PROPS = {
       'game':  {'child_cvt': 2,
                 'child_type': ChildType.NORMAL,
                 'evens': True},

       'rgame': {'rounds': gi.Rounds.HALF_SEEDS,
                 'blocks': True,
                 'child_cvt': 2,
                 'child_type': ChildType.NORMAL,
                 'evens': True},
       }


    @pytest.fixture
    def game(self, request):
        """NOTE: game_info rule checking is turned off."""

        game_props = TestEndChildren.GAME_PROPS[request.param]

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(**game_props,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'game, ended, board, store, turn, '
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
        ], indirect=['game'])
    def test_wincond(self, game, ended,
                     board, store, turn, child,
                     eres, eboard, estore, eturn):

        game.board = board
        game.child = child
        game.store = store
        game.turn = turn

        cond, winner = game.deco.ender.game_ended(False, ended)
        assert cond == eres
        assert game.board == eboard
        assert game.store == estore
        assert winner == eturn
        assert not game.test_pass()


class TestEndDeprive:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                capt_on=[4],
                                min_move=2,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    CASES = [
        # 0: Will be true's turn, but they have no moves
        (False, utils.build_board([0, 0, 0],
                                  [0, 3, 0]),
         WinCond.WIN, False),
        # 1:  Will be false's turn, but they have no moves
        (True, utils.build_board([0, 3, 0],
                                 [0, 0, 0]),
         WinCond.WIN, True),

        # 2: Will be true's turn and they have no moves
        # both have seeds -> a TIE
        (False, utils.build_board([0, 1, 0],
                                  [0, 1, 0]),
         WinCond.TIE, False),

        # 4: Will be false's turn and they have no moves
        # both have seeds -> a TIE
        (False, utils.build_board([0, 1, 0],
                                  [0, 1, 0]),
         WinCond.TIE, False),

        # 4: False gave away all seeds but not their turn
        (False, utils.build_board([0, 3, 0],
                                  [0, 0, 0]),
         None, False),
        # 5: True gave away all seeds but not their turn
        (True, utils.build_board([0, 0, 0],
                                 [0, 3, 0]),
         None, True),

        # 6: False gave away all seeds but true has seeds
        (False, utils.build_board([0, 1, 0],
                                  [0, 0, 0]),
         WinCond.WIN, True),
        # 7: True gave away all seeds but false has seeds
        (True, utils.build_board([0, 0, 0],
                                 [0, 1, 0]),
         WinCond.WIN, False),

        #8: game continues
        (True, utils.build_board([0, 3, 0],
                                 [0, 3, 0]),
         None, None),

        #9: game continues
        (False, utils.build_board([0, 3, 0],
                                  [0, 3, 0]),
         None, None),

    ]

    @pytest.mark.parametrize('turn, board, econd, ewinner',
                             CASES)
    def test_end_game(self, game, turn, board, econd, ewinner):
        game.board = board
        game.turn = turn

        cond, winner = game.deco.ender.game_ended(False, False)
        assert cond == econd
        if ewinner is not None:
            assert winner == ewinner


class TestEndWaldas:

    @pytest.fixture
    def game(self):
        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(child_cvt=4,
                                child_type=ChildType.WALDA,
                                mustpass=True,
                                sow_direct=Direct.SPLIT,
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

        assert game.info.no_sides
        assert len(game.get_allowable_holes()) == 6


class TestQuitter:

    @pytest.fixture
    def game(self, request):

        game_props = TestQuitter.GAME_PROPS[request.param]

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        if request.param == 'no_win_game':
            object.__setattr__(game_consts, 'win_count',
                               game_consts.total_seeds)

        game_info = gi.GameInfo(**game_props,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    GAME_PROPS = {'game': {'evens': True,
                           'stores': True,
                           },

                  'chgame': {'evens': True,
                             'child_type': ChildType.NORMAL,
                             'child_cvt': 2,
                             'stores': True,
                             },

                  'nsgame': {'evens': True,
                             },

                  'chnsgame': {'evens': True,
                               'child_type': ChildType.NORMAL,
                               'child_cvt': 2,
                               },

                  'rgame': {'rounds': gi.Rounds.HALF_SEEDS,
                            'evens': True,
                            'stores': True,
                            },

                  'dipgame': {'evens': True,
                              'goal': gi.Goal.DEPRIVE,
                              },

                  'tergame': {'evens': True,
                              'stores': True,
                              'goal': gi.Goal.TERRITORY,
                              'gparam_one': 4,
                              },

                  'no_win_game': {'evens': True,
                                  'stores': True,
                                  },
                  }


    CASES = \
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

        # 7:  no stores, child - divvy odd
        ('chnsgame',
         utils.build_board([0, 4, 2],
                           [0, 3, 3]), [0, 0], True, WinCond.TIE,
         utils.build_board([N, F, N],
                           [N, T, N]),
         utils.build_board([0, 6, 0],
                           [0, 6, 0]), [0, 0], True),

        # 8:  no stores, child - divvy even
        ('chnsgame',
         utils.build_board([2, 3, 0],
                           [2, 5, 0]), [0, 0], True, WinCond.WIN,
         utils.build_board([N, F, N],
                           [N, T, N]),
         utils.build_board([0, 5, 0],
                           [0, 7, 0]), [0, 0], True),

        # 9:  no stores, True child only
        ('chnsgame',
         utils.build_board([2, 3, 0],
                           [2, 5, 0]), [0, 0], True, WinCond.WIN,
         utils.build_board([N, N, N],
                           [N, T, N]),
         utils.build_board([0, 0, 0],
                           [0, 12, 0]), [0, 0], True),

        # 10:  no stores, False child only
        ('chnsgame',
         utils.build_board([2, 3, 0],
                           [2, 5, 0]), [0, 0], True, WinCond.WIN,
         utils.build_board([N, N, N],
                           [N, F, N]),
         utils.build_board([0, 0, 0],
                           [0, 12, 0]), [0, 0], False),

        # 11:  no stores, child but none
        ('chnsgame',
         utils.build_board([2, 3, 0],
                           [2, 5, 0]), [0, 0], True, WinCond.TIE,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([0, 0, 0],
                           [0, 0, 0]), [0, 0], True),

        # 12: rounds, end game returns definitive result
        ('rgame',
            utils.build_board([0, 2, 1],
                              [0, 2, 0]), [3, 4], True, WinCond.TIE,
            utils.build_board([N, F, N],
                              [N, T, N]),
            utils.build_board([0, 2, 0],
                              [0, 2, 0]), [4, 4], True),

        # 13: rounds, end game returns definitive result
        ('rgame',
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [2, 8], True, WinCond.WIN,
         utils.build_board([F, N, N],
                           [N, N, T]),
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [2, 8], True),

        # 14:
        ('no_win_game',
         utils.build_board([5, 0, 0],
                           [0, 0, 0]), [3, 4], True, WinCond.TIE,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([0, 0, 0],
                           [0, 0, 0]), [6, 6], None),

        #15
        ('dipgame',
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [2, 8], True, WinCond.TIE,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [2, 8], True),

        #16
        ('tergame',
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [5, 5], True, WinCond.TIE,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([0, 0, 0],
                           [0, 0, 0]), [6, 6], True),

        #17
        ('tergame',
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [2, 8], True, WinCond.WIN,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([0, 0, 0],
                           [0, 0, 0]), [3, 9], True),

    ]
    @pytest.mark.parametrize(
        'game, board, store, turn, '
        'eres, child, eboard, estore, eturn',
        CASES,
        indirect=['game'],
        ids=[f'case_{c}' for c in range(len(CASES))])
    def test_ended(self, game, board, store, turn, child,
                   eres, eboard, estore, eturn):

        game.board = board
        game.child = child
        game.store = store
        game.turn = turn

        assert game.end_game() == eres
        assert game.board == eboard
        assert game.store == estore
        if eturn is not None:
            assert game.turn == eturn


class TestTerritory:

    @pytest.fixture
    def rgame(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(capt_on = [1],
                                stores=True,
                                gparam_one=5,
                                goal=Goal.TERRITORY,
                                rounds=gi.Rounds.NO_MOVES,
                                round_fill=gi.RoundFill.UMOVE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(capt_on = [1],
                                stores=True,
                                gparam_one=5,
                                goal=Goal.TERRITORY,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.mark.parametrize('capt_methods, emin_occ',
                             [([('evens', True)], 2),
                              ([('crosscapt', True)], 2),
                              ([('capt_next', True)], 2),
                              ([('capttwoout', True)], 3),
                              ([('capt_on', [3])], 3),
                              ([('capt_min', 2)], 2),

                              ([('capttwoout', True),
                                ('mlaps', True)], 2),

                              ([('capt_on', [4]),
                                ('evens', True)], 4),
                              ([('capt_min', 4),
                                ('evens', True)], 4),
                              ([('child_type', gi.ChildType.NORMAL),
                                ('child_cvt', 3)], 3),
                              ([('child_type', gi.ChildType.NORMAL),
                                ('child_cvt', 3),
                                ('evens', True)], 2),

                              ([('capt_on', [1, 2, 3])], None),
                              ([('min_move', 2),
                                ('evens', True)], None),
                              ([('sow_own_store', True),
                                ('capt_on', [5])], None),
                              ((), None),  # no capture method
                              ])
    def test_min_capture(self, game, capt_methods, emin_occ):
        """Test the minimum capture criteria."""

        object.__setattr__(game.info, 'capt_on', [])
        for cmethod, cvalue in capt_methods:
            object.__setattr__(game.info, cmethod, cvalue)

        deco = end_move.deco_end_move(game)
        while deco and not isinstance(deco, end_move.NoOutcomeChange):
            deco = deco.decorator

        if emin_occ:
            assert deco
            assert deco.min_for_change(game) == emin_occ
        else:
            assert not deco


    @pytest.mark.parametrize(
        'capt_methods, board, child, eresult',
        [([('evens', True)], [1, 0, 1, 0, 1, 0], [N, N, N, N, N, N], False),
         ([('evens', True)], [1, 0, 1, 0, 0, 0], [N, N, N, N, N, N], False),
         ([('evens', True)], [1, 0, 0, 0, 0, 0], [N, N, N, N, N, N], True),

         ([('child_type', gi.ChildType.NORMAL), ('child_cvt', 3)],
          [1, 0, 1, 0, 1, 0], [N, N, N, N, N, N], False), # no child, just enough

         ([('child_type', gi.ChildType.NORMAL), ('child_cvt', 3)],
          [1, 0, 1, 0, 0, 0], [N, N, N, N, N, N], True), # no child, too few

         ([('child_type', gi.ChildType.NORMAL), ('child_cvt', 3)],
          [1, 0, 1, 0, 0, 0], [N, T, N, N, N, N], False),  # too few but child

         ],
        ids=[f'case_{c}' for c in range(6)])
    def test_cant_occ_more(self, game, capt_methods, board, child, eresult):
        """Test the minimum capture criteria."""

        object.__setattr__(game.info, 'capt_on', [])
        for cmethod, cvalue in capt_methods:
            object.__setattr__(game.info, cmethod, cvalue)

        game.board = board
        game.child = child

        deco = end_move.deco_end_move(game)
        while deco and not isinstance(deco, end_move.NoOutcomeChange):
            deco = deco.decorator
        assert deco

        result = deco._too_few_for_change()
        assert result == eresult


    TERR_CASES = [
        (utils.build_board([0, 2, 1],
                           [0, 2, 0]), [6, 7], None, False),
        (utils.build_board([0, 0, 0],
                           [0, 2, 0]), [8, 8], WinCond.ROUND_WIN, False),
        (utils.build_board([0, 0, 0],
                           [0, 0, 0]), [3, 18-3],  WinCond.WIN, True),
        (utils.build_board([0, 0, 0],
                           [0, 0, 0]), [4, 18-4],  WinCond.WIN, True),
        (utils.build_board([0, 0, 0],
                           [0, 0, 0]), [5, 18-5],  WinCond.ROUND_WIN, True),
        (utils.build_board([0, 0, 0],
                           [0, 0, 0]), [18-3, 3],  WinCond.WIN, False),
        (utils.build_board([0, 0, 0],
                           [0, 0, 0]), [18-4, 3],  WinCond.WIN, False),
        (utils.build_board([0, 0, 0],
                           [0, 0, 0]), [18-5, 5],  WinCond.ROUND_WIN, False),
        (utils.build_board([0, 0, 0],
                           [0, 0, 0]), [9, 9],  WinCond.ROUND_TIE, False),
        (utils.build_board([0, 0, 0],
                           [1, 1, 0]), [7, 9], WinCond.ROUND_TIE, False),
        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('board, store, econd, ewinner', TERR_CASES)
    def test_territory(self, rgame, board, store, econd, ewinner):

        rgame.board = board
        rgame.store = store

        cond, winner = rgame.deco.ender.game_ended(False, False)

        assert cond == econd
        assert winner == ewinner


    @pytest.mark.parametrize('board, store, econd, ewinner', TERR_CASES)
    def test_no_rounds_territory(self, game, board, store, econd, ewinner):
        """Same test cases but with a non round territory game."""

        game.board = board
        game.store = store

        cond, winner = game.deco.ender.game_ended(False, False)

        if econd == WinCond.ROUND_WIN:
            assert cond == WinCond.WIN
        elif econd == WinCond.ROUND_TIE:
            assert cond == WinCond.TIE
        else:
            assert cond == econd
        assert winner == ewinner


    @pytest.mark.parametrize(
        'board, store, econd, ewinner',
        [(utils.build_board([0, 0, 0, 0],
                            [2, 2, 0, 2]), [10, 8], None, True),  # can share game continues
         (utils.build_board([0, 0, 0, 0],
                            [2, 2, 0, 0]), [10, 10], WinCond.ROUND_WIN, False),
         (utils.build_board([0, 0, 0, 0],
                            [2, 2, 0, 0]), [2, 18], WinCond.WIN, True),
         ])
    def test_terr_must_share(self, board, store, econd, ewinner):
        """Use the mustshare so the deco chain decides the game is
        over."""

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                gparam_one=6,
                                goal=Goal.TERRITORY,
                                rounds=gi.Rounds.NO_MOVES,
                                mustshare=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        assert game.deco.ender.win_seeds == 23 # one less than all

        game.turn = True
        game.board = board
        game.store = store

        cond, winner = game.deco.ender.game_ended(False, False)
        assert cond == econd
        assert winner == ewinner



class TestWinHoles:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gc.GameConsts(nbr_start=3, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game

    WH_CASES = [((0, 0, 0, 0), [6, 6], (N, N, N, N), True, 2),
                ((0, 0, 0, 0), [3, 3], (N, N, N, N), True, 2),
                ((0, 0, 0, 0), [9, 3], (N, N, N, N), False, 3),
                ((0, 0, 0, 0), [3, 9], (N, N, N, N), True, 3),
                ((0, 0, 0, 0), [3, 8], (N, N, N, N), True, 3),
                ((0, 0, 0, 0), [3, 7], (N, N, N, N), True, 2),
                ((0, 1, 1, 0), [3, 7], (N, T, F, N), True, 3),
                ]

    @pytest.mark.parametrize('board, store, child, fill_start, holes',
                             WH_CASES,
                             ids=[f'case_{cnbr}'
                                  for cnbr in range(len(WH_CASES))])
    def test_win_holes(self, game, board, store, child, fill_start, holes):

        game.board = board
        game.store = store
        game.child = child

        assert game.deco.ender.compute_win_holes() == (fill_start, holes)
