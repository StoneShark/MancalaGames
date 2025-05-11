"""
Created on Fri Sep 15 03:57:49 2023
@author: Ann"""


# %% imports

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import animator
from context import end_move
from context import end_move_decos as emd
from context import end_move_rounds as emr
from context import game_constants as gconsts
from context import game_interface as gi
from context import ginfo_rules
from context import mancala

from game_interface import ChildType
from game_interface import Direct
from game_interface import Goal
from game_interface import WinCond


# %%

TEST_COVERS = ['src\\end_move.py',
               'src\\end_move_decos.py',
               'src\\end_move_rounds.py']


# %% some constants

N = None
T = True
F = False

DONT_CARE = None
REPEAT_TURN = True
ENDED = True


# %%

class TestEndMove:

    @pytest.fixture
    def game(self, request):

        game_props = TestEndMove.GAME_PROPS[request.param]

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
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
                   'goal_param': 2,   # need two holes to continue (new round)
                   'evens': True,
                   'stores': True,
                  },

        'rnmgame': {'rounds': gi.Rounds.NO_MOVES,
                   'goal_param': 2,   # need two holes to continue (new round)
                   'evens': True,
                   'stores': True,
                  },

        'rnm2game': {'rounds': gi.Rounds.NO_MOVES,
                   'goal_param': 0,
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

        'dont_score': {'evens': True,
                       'stores': True,
                       'unclaimed': gi.EndGameSeeds.DONT_SCORE},

        'unfed_player': {'evens': True,
                         'stores': True,
                         'capt_rturn': True,
                         'mustshare': True,
                         'unclaimed': gi.EndGameSeeds.UNFED_PLAYER},

        'hole_owner': {'evens': True,
                       'stores': True,
                       'unclaimed': gi.EndGameSeeds.HOLE_OWNER},

        'last_mover': {'evens': True,
                       'stores': True,
                       'capt_rturn': True,
                       'min_move': 2,
                       'unclaimed': gi.EndGameSeeds.LAST_MOVER},

        'divvied': {'evens': True,
                    'stores': True,
                    'mustshare': True,
                    'unclaimed': gi.EndGameSeeds.DIVVIED},

        'st_game': {'evens': True,
                    'stores': True,
                    'rounds': gi.Rounds.END_S_SEEDS,
                    'goal_param': 2,   # need two holes to continue
                    },

        'st2_game': {'evens': True,
                     'stores': True,
                     'rounds': gi.Rounds.END_2S_SEEDS,
                     'goal_param': 2,   # need two holes to continue
                     },

        'pp_game': {'evens': True,
                    'stores': True,
                    'sow_direct': gi.Direct.SPLIT,
                    'udir_holes': [1],
                    'mustpass': True,
                    'unclaimed': gi.EndGameSeeds.DONT_SCORE,
                     },

        'ef_game': {'evens': True,
                    'stores': True,
                    'rounds': gi.Rounds.NO_MOVES,
                    'round_fill': gi.RoundFill.EVEN_FILL,
                    'min_move': 2}

    }


    WINCASES = [  # no win
                ('0', 'game', False, False,
                 utils.build_board([0, 2, 1],
                                   [0, 2, 0]), [3, 4], True, None,
                 utils.build_board([0, 2, 1],
                                   [0, 2, 0]), [3, 4], None),

                # true win on true turn, playable
                ('1', 'game', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], True, WinCond.WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], True),

                # true win on false turn, playable
                ('2', 'game', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], False, WinCond.WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], True),

                # false win on false turn, playable
                ('3', 'game', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], False, WinCond.WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], False),

                # false win on true turn, playable
                ('4', 'game', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], True, WinCond.WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], False),

                # tie on false turn, playable
                ('5', 'game', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], False, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # tie on true turn, playable
                ('6', 'game', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], True, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # true's turn ended, false has no moves
                ('7', 'game', False, False,
                 utils.build_board([5, 0, 0],
                                   [0, 0, 0]), [3, 4], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [3, 9], True),

                # false's turn ended, true has no moves
                ('8', 'game', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 5]), [3, 4], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [8, 4], False),

                # true win on true turn, playable
                ('9', 'rgame', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], True, WinCond.ROUND_WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], True),

                # test_ft_win
                ('10', 'rgame', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], False, WinCond.ROUND_WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [2, 8], True),

                # test_ff_win
                ('11', 'rgame', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], False, WinCond.ROUND_WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], False),

                # test_tf_win
                ('12', 'rgame', False, False,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], True, WinCond.ROUND_WIN,
                 utils.build_board([1, 0, 0],
                                   [0, 0, 1]), [8, 2], False),

                # test_f_tie_win
                ('13', 'rgame', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], False, WinCond.ROUND_TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # test_t_tie_win
                ('14', 'rgame', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], True, WinCond.ROUND_TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # false's turn ended, true has won, doesn't have seeds
                ('15', 'rgame', False, False,
                 utils.build_board([2, 0, 0],
                                   [0, 0, 0]), [0, 10], False, WinCond.WIN,
                 utils.build_board([2, 0, 0],
                                   [0, 0, 0]), [0, 10], True),

                # true's turn ended, false has won, true can't continue
                ('16', 'rgame', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 2]), [10, 0], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 2]), [10, 0], False),

                # game ended, true has won
                ('17', 'game', ENDED, False,
                 utils.build_board([2, 2, 0],
                                   [0, 0, 1]), [3, 4], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [4, 8], True),

                # game ended, false has won
                ('18', 'rgame', ENDED, False,
                 utils.build_board([1, 0, 0],
                                   [0, 2, 2]), [4, 3], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [8, 4], False),

                # false's turn ended, no valid moves, true wins
                ('19', 'mmgame', False, False,
                 utils.build_board([1, 1, 0],
                                   [0, 1, 1]), [3, 5], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [5, 7], True),

                # true's turn ended, no valid moves, false wins
                ('20', 'mmgame', False, False,
                 utils.build_board([1, 1, 0],
                                   [0, 1, 1]), [5, 3], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [7, 5], False),

                # true's turn ended, no valid moves, false wins
                ('21', 'mmshgame', False, False,
                 utils.build_board([1, 1, 0],
                                   [0, 1, 1]), [5, 3], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [7, 5], False),

                # true's turn ended, false has no moves, no pass
                ('22', 'no_win_game', False, False,
                 utils.build_board([5, 0, 0],
                                   [0, 0, 0]), [3, 4], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [3, 9], True),

                # true's turn ended without seeds, false can't share
                ('23', 'no_win_game', False, False,
                 utils.build_board([0, 0, 0],
                                   [1, 1, 0]), [5, 5], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [7, 5], False),

                # true's turn ended without seeds, false can't share
                ('24', 'no_win_game', False, False,
                 utils.build_board([0, 0, 0],
                                   [1, 1, 0]), [4, 6], True, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # true has a repeat_turn but no moves, false wins
                ('25', 'game', False, REPEAT_TURN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 5]), [3, 4], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [8, 4], False),

                # true's turn ended without moves, false can share and capture
                ('26', 'mmshgame', False, False,
                 utils.build_board([1, 1, 0],
                                   [0, 1, 3]), [3, 3], True, None,
                 utils.build_board([1, 1, 0],
                                   [0, 1, 3]), [3, 3], None),

                # true has no moves but has a repeat turn, false can share
                ('27', 'mmshgame', False, True,
                 utils.build_board([1, 1, 0],
                                   [0, 1, 3]), [3, 3], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [7, 5], False),

                # true's turn ended, false has no moves, pass
                ('28', 'pagame', False, False,
                 utils.build_board([5, 0, 0],
                                   [0, 0, 0]), [3, 4], True, None,
                 utils.build_board([5, 0, 0],
                                   [0, 0, 0]), [3, 4], None),

                # UMOVE game
                ('29', 'rugame', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], True, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], None),

                #  True has just enough seeds to continue
                ('30', 'rugame', False, False,
                 utils.build_board([2, 1, 1],
                                   [1, 1, 0]), [5, 0], True, WinCond.ROUND_WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [7, 4], False),

                #31: True does not have enough seeds to continue
                ('31', 'rugame', False, False,
                 utils.build_board([2, 1, 0],
                                   [1, 1, 1]), [6, 0], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [9, 3], False),

                # goal_param with MAX_SEEDS & rounds, e.g. don't need all
                ('32', 'r2game', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 6], True, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 6], None),

                # enough seeds to keep playing
                ('33', 'r2game', False, False,
                 utils.build_board([2, 2, 0],
                                   [0, 2, 2]), [0, 10], False, WinCond.ROUND_WIN,
                 utils.build_board([2, 2, 0],
                                   [0, 2, 2]), [0, 10], True),

                # not enough seeds to keep playing
                ('34', 'r2game', False, False,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 2]), [0, 10], False, WinCond.WIN,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 2]), [0, 10], True),

                # goal_param with MAX_SEEDS & rounds, e.g. don't need all
                ('32_nm', 'rnmgame', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 6], True, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 6], None),

                # enough seeds to keep playing
                ('33_nm', 'rnmgame', False, False,
                 utils.build_board([2, 2, 0],
                                   [0, 2, 2]), [0, 10], False, WinCond.ROUND_WIN,
                 utils.build_board([2, 2, 0],
                                   [0, 2, 2]), [0, 10], True),

                # not enough seeds to keep playing
                ('34_nm', 'rnmgame', False, False,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 2]), [0, 10], False, WinCond.WIN,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 2]), [0, 10], True),

                # not enough seeds to keep playing
                ('34_nm_2', 'rnm2game', False, False,
                 utils.build_board([0, 1, 0],
                                   [0, 1, 0]), [0, 14], False, WinCond.WIN,
                 utils.build_board([0, 1, 0],
                                   [0, 1, 0]), [0, 14], True),

                # capt_on = 6, can't capt more
                ('35', 'cogame', False, False,
                 utils.build_board([2, 0, 0],
                                   [0, 2, 0]), [4, 4], False, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # F moved all but one seed to T, now Ts move
                ('36', 'shgame', False, False,
                 utils.build_board([0, 1, 2],
                                   [1, 0, 0]), [5, 5], False, None,
                 utils.build_board([0, 1, 2],
                                   [1, 0, 0]), [5, 5], None),

                # move after 36  Ts move, first move capt all F seeds,
                #     now T repeat turn but can't share,
                #     T still wins on seed collection
                ('37', 'shgame', False, REPEAT_TURN,
                 utils.build_board([0, 0, 2],
                                   [0, 0, 0]), [5, 5], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [5, 7], True),

                # ended dont score
                ('end_ds_base', 'game', ENDED, False,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 3]), [2, 3], False, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                ('end_ds', 'dont_score', ENDED, False,
                 utils.build_board([2, 1, 0],
                                   [0, 1, 3]), [2, 3], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [2, 3], True),

                # ended divvy
                ('end_div_base', 'game', ENDED, False,
                 utils.build_board([2, 1, 0],
                                   [0, 2, 3]), [2, 2], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [7, 5], False),
                ('end_div', 'divvied', ENDED, False,
                 utils.build_board([2, 1, 0],
                                   [0, 2, 3]), [2, 2], False, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                # RoundEndLimit tests
                ('rnd_not_send', 'st_game', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], False, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], None),

                ('rnd_send_3', 'st_game', False, False,
                 utils.build_board([0, 1, 1],
                                   [0, 1, 0]), [5, 4], False, None,
                 utils.build_board([0, 1, 1],
                                   [0, 1, 0]), [5, 4], None),

                ('rnd_send_tie', 'st_game', False, False,
                 utils.build_board([0, 1, 0],
                                   [0, 1, 0]), [5, 5], False, WinCond.ROUND_TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 6], None),

                ('rnd_send_win', 'st_game', False, False,
                 utils.build_board([0, 1, 1],
                                   [0, 0, 0]), [4, 6], False, WinCond.ROUND_WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [4, 8], DONT_CARE),

                ('rnd_send_win', 'st_game', False, False,
                 utils.build_board([0, 1, 1],
                                   [0, 0, 0]), [2, 8], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [2, 10], DONT_CARE),

                ('rnd_not_s2end', 'st2_game', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], False, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], None),

                ('rnd_s2end_win', 'st2_game', False, False,
                 utils.build_board([1, 1, 1],
                                   [0, 1, 0]), [4, 6], False, WinCond.ROUND_WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [5, 9], DONT_CARE),

                ('pp_normal', 'pp_game', False, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], False, None,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], None),

                ('pp_ended', 'pp_game', True, False,
                 utils.build_board([2, 2, 2],
                                   [2, 2, 2]), [0, 0], False, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [0, 0], None),

                ('pp_p1none', 'pp_game', False, False,
                 utils.build_board([2, 2, 2],
                                   [0, 0, 0]), [0, 0], False, None,
                 utils.build_board([2, 2, 2],
                                   [0, 0, 0]), [0, 0], None),

                ('case_ef_1', 'ef_game', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [3, 9], False, WinCond.ROUND_WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [3, 9], True),

                ('case_ef_2', 'ef_game', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [2, 10], False, WinCond.ROUND_WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [2, 10], True),

                ('case_ef_3', 'ef_game', False, False,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [1, 11], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [1, 11], True),

            ]
    @pytest.mark.filterwarnings("ignore")
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize(
        'case, game, ended, repeat, board, store, turn,'
        ' eres, eboard, estore, ewinner',
        WINCASES,
        indirect=['game'],
        ids=[f'{case[0]}_idx_{idx}' for idx, case in enumerate(WINCASES)])
    def test_game_ended(self, case, game, ended,
                        repeat, board, store, turn,
                        eres, eboard, estore, ewinner):

        game.board = board
        game.store = store
        game.turn = turn
        # print(game)
        # print(game.deco.ender)

        mdata = utils.make_ender_mdata(game, repeat, ended)
        mdata.end_msg = 'first part'
        game.deco.ender.game_ended(mdata)

        # print('after:', game, sep='\n')
        # print(mdata.win_cond, mdata.winner)

        assert mdata.win_cond == eres
        assert game.board == eboard
        assert game.store == estore
        if ewinner != DONT_CARE:
            assert mdata.winner == ewinner
        if 'pp' not in case:
            assert not game.test_pass()


    PPCASES = [

                ('pp_none_twin', 'pp_game', False, False,
                 utils.build_board([0, 0, 0],
                                   [1, 0, 0]), [4, 6], False, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [4, 6], True),

                ('pp_none_fwin', 'pp_game', False, False,
                 utils.build_board([0, 1, 1],
                                   [1, 1, 0]), [6, 4], True, WinCond.WIN,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [6, 4], False),

                ('pp_none_tie', 'pp_game', False, False,
                 utils.build_board([0, 1, 1],
                                   [1, 1, 0]), [4, 4], False, WinCond.TIE,
                 utils.build_board([0, 0, 0],
                                   [0, 0, 0]), [4, 4], DONT_CARE),

            ]
    @pytest.mark.filterwarnings("ignore")
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize(
        'case, game, ended, repeat, board, store, turn,'
        ' eres, eboard, estore, eturn',
        PPCASES,
        indirect=['game'],
        ids=[f'{case[0]}_idx_{idx}' for idx, case in enumerate(PPCASES)])
    def test_game_ended_pp(self, mocker, case, game, ended,
                           repeat, board, store, turn,
                           eres, eboard, estore, eturn):
        """Test the cases were there are no moves for either player,
        force it by patching get_allowable_holes.
        Creating this condition would require doing moves to setup
        DontUndoMoveOne to prevent a move."""

        mobj = mocker.patch('mancala.Mancala.get_allowable_holes')
        mobj.return_value = []

        game.board = board
        game.store = store
        game.turn = turn
        # print(game)
        # print(game.deco.ender)

        mdata = utils.make_ender_mdata(game, repeat, ended)
        game.deco.ender.game_ended(mdata)

        # print('after:', game, sep='\n')
        # print(mdata.win_cond, mdata.winner)
        assert mdata.win_cond == eres
        assert game.board == eboard
        assert game.store == estore
        if eturn != DONT_CARE:
            assert mdata.winner == eturn


    @pytest.mark.parametrize('game', ['game'], indirect=['game'])
    def test_str(self, game):
        """Printing the claimer is unique to enders."""
        assert 'ClaimSeeds' in str(game.deco.ender)


    def test_bad_ucl(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        mancala.Mancala(game_consts, game_info)

        object.__setattr__(game_info, 'unclaimed', 12)
        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    MOVECASES = [
        # give away final seed, no repeat turn, F can't share
        ('give', 'unfed_player',
         utils.make_state(board=(0, 0, 0, 0, 0, 1),
                          store=(6, 5),
                          turn=True),
         0, [0, 0, 0, 0, 0, 0], [6, 6], N, WinCond.TIE),

        # capture Fs last seed, T repeat turn but can't share
        ('capt_rturn', 'unfed_player',
         utils.make_state(board=(1, 0, 0, 1, 0, 1),
                          store=(5, 4),
                          turn=True),
         0, [0, 0, 0, 0, 0, 0], [6, 6], N, WinCond.TIE),

        # capture all ops, repeat turn, but can't share
        ('cr_flose', 'unfed_player',
         utils.make_state(board=(1, 0, 0, 2, 0, 1),
                          store=(5, 3),
                          turn=True),
         0, [0, 0, 0, 0, 0, 0], [7, 5], F, WinCond.WIN),

        # same as above, but reflected
        ('cr_tlose', 'unfed_player',
         utils.make_state(board=(2, 0, 1, 1, 0, 0,),
                          store=(3, 5),
                          turn=False),
         2, [0, 0, 0, 0, 0, 0], [5, 7], T, WinCond.WIN),

        # capture, all ops, repeat turn, but can share
        ('cr_cont', 'unfed_player',
         utils.make_state(board=(1, 0, 0, 3, 0, 1),
                          store=(4, 3),
                          turn=True),
         0, [0, 0, 0, 3, 0, 0], [4, 5], N, WinCond.REPEAT_TURN),


        # capture 0 (now tie) repeat turn, but no moves, T gets remaining and wins
        ('lm_crturn', 'last_mover',
         utils.make_state(board=(1, 1, 0, 0, 2, 0),
                          store=(5, 3),
                          turn=True),
         1, [0, 0, 0, 0, 0, 0], [5, 7], T, WinCond.WIN),

        # T moves, F has no moves, T gets remaining and wins
        ('no_capt', 'last_mover',
         utils.make_state(board=(0, 1, 0, 0, 2, 0),
                          store=(5, 4),
                          turn=True),
         1, [0, 0, 0, 0, 0, 0], [5, 7], T, WinCond.WIN),
        ]

    @pytest.mark.filterwarnings("ignore")
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize(
        'case, game, state, move, eboard, estore, ewin, econd',
        MOVECASES,
        indirect=['game'],
        ids=[f'{case[0]}_idx_{idx}' for idx, case in enumerate(MOVECASES)])
    def test_end_w_moves(self, case, game, state, move,
                         eboard, estore, ewin, econd):
        """These tests require that an actual move be made
        before end_game is called (at the end of move)."""

        game.state = state
        # print(game)
        # print(game.deco.ender)

        wcond = game.move(move)
        # print(game)

        assert wcond == econd
        assert game.mdata.winner == ewin
        assert game.board == eboard
        assert game.store == estore


class TestEndChildren:


    GAME_PROPS = {
       'game':  {'child_cvt': 2,
                 'child_type': ChildType.NORMAL,
                 'stores': True,
                 'evens': True},

       'rgame': {'rounds': gi.Rounds.HALF_SEEDS,
                 'blocks': True,
                 'stores': True,
                 'child_cvt': 2,
                 'child_type': ChildType.NORMAL,
                 'evens': True},

       's2game': {'rounds': gi.Rounds.END_2S_SEEDS,
                  'stores': True,
                  'child_cvt': 2,
                  'child_type': ChildType.NORMAL,
                  'evens': True},

       }


    @pytest.fixture
    def game(self, request):
        """NOTE: game_info rule checking is turned off."""

        game_props = TestEndChildren.GAME_PROPS[request.param]

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(**game_props,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        return mancala.Mancala(game_consts, game_info)


    WCOND_CASES = [
        # 0: collect seeds and count children to determine win
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

        # 4:  RoundEndLimit finds no new seeds, win decided by clear winner
        ('s2game', False,
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [2, 8], True, WinCond.ROUND_WIN,
         utils.build_board([F, N, N],
                           [N, N, T]),
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [2, 8], True),

        ]

    @pytest.mark.parametrize(
        'game, ended, board, store, turn, '
        'eres, child, eboard, estore, eturn',
        WCOND_CASES, indirect=['game'])
    def test_wincond(self, game, ended,
                     board, store, turn, child,
                     eres, eboard, estore, eturn):

        game.board = board
        game.child = child
        game.store = store
        game.turn = turn

        mdata = utils.make_ender_mdata(game, False, ended)
        game.deco.ender.game_ended(mdata)

        assert mdata.win_cond == eres
        assert game.board == eboard
        assert game.store == estore
        assert mdata.winner == eturn
        assert not game.test_pass()


class TestEndDeprive:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                capt_on=[4],
                                allow_rule=gi.AllowRule.NOT_XFROM_1S,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def rndgame(self):
        """Outcomes should be exactly the sames as for game.
        Round ender is tested elsewhere."""
        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.RND_WIN_COUNT_DEP,
                                goal_param=1,
                                capt_on=[4],
                                rounds=gi.Rounds.NO_MOVES,
                                allow_rule=gi.AllowRule.NOT_XFROM_1S,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def mm2game(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                capt_on=[4],
                                min_move=2,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    CASES = [
        # 0: Will be true's turn, but they have no moves
        #     game rturn: current player has another move
        (False, utils.build_board([0, 0, 0],
                                  [0, 3, 0]),
         (WinCond.WIN, False), (WinCond.WIN, False),
         (None, None)),

        # 1:  Will be false's turn, but they have no moves
        #     game rturn: current player has another move
        (True, utils.build_board([0, 3, 0],
                                 [0, 0, 0]),
         (WinCond.WIN, True), (WinCond.WIN, True),
         (None, None)),

        # 2: False gave away all seeds
        #     game: F loses no seeds, mm2: T has a move
        #     game rturn: F has no seeds for repeat turn, T wins
        (False, utils.build_board([0, 3, 0],
                                  [0, 0, 0]),
         (WinCond.WIN, True), (None, None),
         (WinCond.WIN, True)),

        # 3: True gave away all seeds
        #     game: T loses no seeds, mm2: F has a move
        (True, utils.build_board([0, 0, 0],
                                 [0, 3, 0]),
         (WinCond.WIN, False), (None, None),
         (WinCond.WIN, False)),

        # 4: False gave away all seeds
        #   game: F has no seeds, mm2: T can't move; F was the last mover
        #   game rturn: F has no seeds for repeat turn, T wins
        (False, utils.build_board([0, 1, 0],
                                  [0, 0, 0]),
         (WinCond.WIN, True), (WinCond.WIN, False),
         (WinCond.WIN, True)),

        # 5: True gave away all seeds
        #   game: T has no seeds, mm2: F can't move; T was the last mover
        (True, utils.build_board([0, 0, 0],
                                 [0, 1, 0]),
         (WinCond.WIN, False), (WinCond.WIN, True),
         (WinCond.WIN, False)),

        # 6: game continues
        (True, utils.build_board([0, 3, 0],
                                 [0, 3, 0]),
         (None, None), (None, None), (None, None)),

        # 7: game continues
        (False, utils.build_board([0, 3, 0],
                                  [0, 3, 0]),
         (None, None), (None, None), (None, None)),

        # 8: Will be true's turn and they have no moves
        #     both: next player no moves
        #     game: opp immobilized  mm2: last mover (current player) wins
        #     game rturn: F does not have a move for repeat turn
        (False, utils.build_board([0, 1, 0],
                                  [0, 1, 0]),
         (WinCond.WIN, False), (WinCond.WIN, False),
         (WinCond.WIN, True)),

        # 9: Will be false's turn and they have no moves
        #     both: next player no moves
        #     game: opp immobilized  mm2: last mover (current player) wins
        (True, utils.build_board([0, 1, 0],
                                 [0, 1, 0]),
         (WinCond.WIN, True), (WinCond.WIN, True),
         (WinCond.WIN, False)),
        ]

    @pytest.mark.parametrize('game_fixt, repeat_turn',
                             [('game', True),
                              ('game', False),
                              ('rndgame', False),
                              ('mm2game', False)])
    @pytest.mark.parametrize('turn, board, eresg, eresmm2, eresg_rturn',
                             CASES,
                             ids=[f'case{idx}' for idx, _ in enumerate(CASES)])
    def test_end_game(self, request,
                      game_fixt, repeat_turn,
                      turn, board,
                      eresg, eresmm2, eresg_rturn):

        game = request.getfixturevalue(game_fixt)
        if repeat_turn:
            econd, ewinner = eresg_rturn
        else:
            if game_fixt in ('game', 'rndgame'):
                econd, ewinner = eresg
            else:
                econd, ewinner = eresmm2

        game.board = board
        game.turn = turn

        mdata = utils.make_ender_mdata(game, repeat_turn, False)
        game.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        if ewinner is not None:
            assert mdata.winner == ewinner


    def test_rnd_end_game(self, game, rndgame):
        """was the tallier added to the deco chain."""

        assert not isinstance(game.deco.ender,
                              emr.RoundTallyWinner)

        assert isinstance(rndgame.deco.ender,
                          emr.RoundTallyWinner)


class TestEndClear:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.CLEAR,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.fixture
    def rndgame(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.RND_WIN_COUNT_CLR,
                                goal_param=1,
                                rounds=gi.Rounds.NO_MOVES,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    CASES = [
        # 0: Will be true's turn, but they have no moves
        (False, utils.build_board([0, 0, 0],
                                  [0, 3, 0]),
         WinCond.WIN, True),

        # 1: Will be false's turn, but they have no moves
        (True, utils.build_board([0, 3, 0],
                                 [0, 0, 0]),
         WinCond.WIN, False),

        # 2: False gave away all seeds but not their turn
        (False, utils.build_board([0, 3, 0],
                                  [0, 0, 0]),
         WinCond.WIN, False),

        # 3: True gave away all seeds but not their turn
        (True, utils.build_board([0, 0, 0],
                                 [0, 3, 0]),
         WinCond.WIN, True),

        # 4: False gave away all seeds but true has seeds
        (False, utils.build_board([0, 1, 0],
                                  [0, 0, 0]),
         WinCond.WIN, False),

        # 5: True gave away all seeds but false has seeds
        (True, utils.build_board([0, 0, 0],
                                 [0, 1, 0]),
         WinCond.WIN, True),

        # 6: game continues
        (True, utils.build_board([0, 3, 0],
                                 [0, 3, 0]),
         None, None),

        # 7: game continues
        (False, utils.build_board([0, 3, 0],
                                  [0, 3, 0]),
         None, None),

    ]

    @pytest.mark.parametrize('game_fixt', ['game', 'rndgame'])
    @pytest.mark.parametrize('turn, board, econd, ewinner',
                             CASES)
    def test_end_game(self, request, game_fixt, turn, board, econd, ewinner):

        game = request.getfixturevalue(game_fixt)

        game.board = board
        game.turn = turn

        mdata = utils.make_ender_mdata(game, False, False)
        game.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        if ewinner is not None:
            assert mdata.winner == ewinner


    def test_rnd_end_game(self, game, rndgame):
        """was the tallier added to the deco chain."""

        assert not isinstance(game.deco.ender,
                              emr.RoundTallyWinner)

        assert isinstance(rndgame.deco.ender,
                          emr.RoundTallyWinner)


class TestEndWaldas:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(child_cvt=4,
                                child_type=ChildType.NORMAL,
                                child_locs=gi.ChildLocs.ENDS_PLUS_ONE_OPP,
                                mustpass=True,
                                sow_direct=Direct.SPLIT,
                                capt_on=[4],
                                skip_start=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    WALDA_CASES = [(True,
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
                ]

    @pytest.mark.parametrize('turn, board, child, eboard',
                             WALDA_CASES,
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


        game.mdata = utils.make_ender_mdata(game, False, False)
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

        game.mdata = utils.make_ender_mdata(game, False, False)
        cond = game.end_game()
        assert game.board == [0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0]

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[True] in winmsg[1]


    def test_end_game_f_walda(self, game):

        game.turn = False
        game.board = [8, 0, 2, 1, 8, 6, 4, 0, 8, 8, 2, 1]
        game.child = [False, None, None, None, None, None,
                      None, None, None, None, None, None]
        game.store = [0, 0]

        game.mdata = utils.make_ender_mdata(game, False, False)
        cond = game.end_game()
        assert game.board == [48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[False] in winmsg[1]


    def test_end_game_both_walda(self, game):

        game.turn = False
        game.board = [8, 0, 2, 1, 8, 6, 4, 0, 8, 8, 2, 1]
        game.child = [True, None, None, None, None, False,
                      None, None, None, None, None, None]
        game.store = [0, 0]

        game.mdata = utils.make_ender_mdata(game, False, False)
        cond = game.end_game()
        assert game.board == [25, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0]

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[True] in winmsg[1]



class TestNoSides:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
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

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
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
                              'goal_param': 4,
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
                           [0, 0, 0]), [6, 6], None),

        # 1:  stores, no child - divvy odd, false gets extra
        ('game',
         utils.build_board([2, 2, 1],
                           [0, 0, 0]), [4, 3], True, WinCond.TIE,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([0, 0, 0],
                           [0, 0, 0]), [6, 6], None),

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
                           [0, 2, 0]), [4, 4], None),

        # 4:  stores, child - divvy even
        ('chgame',
         utils.build_board([1, 2, 1],
                           [0, 3, 0]), [2, 3], True, WinCond.WIN,
         utils.build_board([N, F, N],
                           [N, T, N]),
         utils.build_board([0, 2, 0],
                           [0, 3, 0]), [3, 4], True),

        # 5: no store, no children
        pytest.param('nsgame',
         utils.build_board([2, 2, 1],
                           [4, 0, 3]), [0, 0], True, WinCond.TIE,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([2, 2, 1],
                           [4, 0, 3]), [0, 0], None,
         marks=pytest.mark.filterwarnings("ignore")),

        # 6:  no stores, child - divvy odd
        ('chnsgame',
         utils.build_board([0, 3, 2],
                           [0, 4, 3]), [0, 0], True, WinCond.TIE,
         utils.build_board([N, F, N],
                           [N, T, N]),
         utils.build_board([0, 6, 0],
                           [0, 6, 0]), [0, 0], None),

        # 7:  no stores, child - divvy odd
        ('chnsgame',
         utils.build_board([0, 4, 2],
                           [0, 3, 3]), [0, 0], True, WinCond.TIE,
         utils.build_board([N, F, N],
                           [N, T, N]),
         utils.build_board([0, 6, 0],
                           [0, 6, 0]), [0, 0], None),

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
                           [0, 0, 0]), [0, 0], None),

        # 12: rounds, end game returns definitive result
        ('rgame',
            utils.build_board([0, 2, 1],
                              [0, 2, 0]), [3, 4], True, WinCond.TIE,
            utils.build_board([N, F, N],
                              [N, T, N]),
            utils.build_board([0, 2, 0],
                              [0, 2, 0]), [4, 4], None),

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
                           [0, 0, 1]), [2, 8], None),

        #16
        ('tergame',
         utils.build_board([1, 0, 0],
                           [0, 0, 1]), [5, 5], True, WinCond.TIE,
         utils.build_board([N, N, N],
                           [N, N, N]),
         utils.build_board([0, 0, 0],
                           [0, 0, 0]), [6, 6], None),

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
        'eres, child, eboard, estore, ewin',
        CASES,
        indirect=['game'],
        ids=[f'case_{c}' for c in range(len(CASES))])
    def test_ended(self, game, board, store, turn, child,
                   eres, eboard, estore, ewin):

        game.board = board
        game.child = child
        game.store = store
        game.turn = turn

        game.mdata = utils.make_ender_mdata(game, False, False)
        assert game.end_game() == eres
        assert game.board == eboard
        assert game.store == estore
        assert game.mdata.winner == ewin


class TestTerritory:

    @pytest.fixture
    def rgame(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(capt_on = [1],
                                stores=True,
                                goal_param=5,
                                goal=Goal.TERRITORY,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(capt_on = [1],
                                stores=True,
                                goal_param=5,
                                goal=Goal.TERRITORY,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.mark.parametrize('capt_methods, emin_occ',
                             [([('evens', True)], 2),
                              ([('crosscapt', True)], 2),
                              ([('capt_type', gi.CaptType.NEXT)], 2),
                              ([('capt_type', gi.CaptType.TWO_OUT)], 3),
                              ([('capt_on', [3])], 3),
                              ([('capt_min', 2)], 2),

                              ([('capt_type', gi.CaptType.TWO_OUT),
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
        while deco and not isinstance(deco, emd.NoOutcomeChange):
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
        while deco and not isinstance(deco, emd.NoOutcomeChange):
            deco = deco.decorator
        assert deco

        result = deco._too_few_for_change()
        assert result == eresult


    TERR_CASES = [
        (utils.build_board([0, 2, 1],
                           [0, 2, 0]), [6, 7], None, None),
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
                           [0, 0, 0]), [9, 9],  WinCond.ROUND_TIE, None),
        (utils.build_board([0, 0, 0],
                           [1, 1, 0]), [7, 9], WinCond.ROUND_TIE, None),
        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('board, store, econd, ewinner', TERR_CASES)
    def test_territory(self, rgame, board, store, econd, ewinner):

        rgame.board = board
        rgame.store = store

        mdata = utils.make_ender_mdata(rgame, False, False)
        rgame.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        assert mdata.winner == ewinner

        assert 'req_seeds' in str(rgame.deco.ender)


    @pytest.mark.parametrize('board, store, econd, ewinner', TERR_CASES)
    def test_no_rounds_territory(self, game, board, store, econd, ewinner):
        """Same test cases but with a non round territory game."""

        game.board = board
        game.store = store

        mdata = utils.make_ender_mdata(game, False, False)
        game.deco.ender.game_ended(mdata)

        if econd == WinCond.ROUND_WIN:
            assert mdata.win_cond == WinCond.WIN
        elif econd == WinCond.ROUND_TIE:
            assert mdata.win_cond == WinCond.TIE
        else:
            assert mdata.win_cond == econd
        assert mdata.winner == ewinner


    @pytest.mark.parametrize(
        'board, store, econd, ewinner',
        [(utils.build_board([0, 0, 0, 0],
                            [2, 2, 0, 2]), [10, 8], None, None),  # can share game continues
         (utils.build_board([0, 0, 0, 0],
                            [2, 2, 0, 0]), [10, 10], WinCond.ROUND_WIN, False),
         (utils.build_board([0, 0, 0, 0],
                            [2, 2, 0, 0]), [2, 18], WinCond.WIN, True),
         ])
    def test_terr_must_share(self, board, store, econd, ewinner):
        """Use the mustshare so the deco chain decides the game is
        over."""

        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal_param=6,
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

        mdata = utils.make_ender_mdata(game, False, False)
        game.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        assert mdata.winner == ewinner



class TestWinHoles:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gconsts.GameConsts(nbr_start=3, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game

    @pytest.fixture
    def pat_game(self):
        """fewer seeds will use self.equalize,
        start seeds doubled so same test cases can be used"""

        game_consts = gconsts.GameConsts(nbr_start=6, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                start_pattern=gi.StartPattern.ALTERNATES,
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

    @pytest.mark.parametrize('game_fixt', ['game', 'pat_game'])
    @pytest.mark.parametrize('board, store, child, fill_start, holes',
                             WH_CASES,
                             ids=[f'case_{cnbr}'
                                  for cnbr in range(len(WH_CASES))])
    def test_win_holes(self, request, game_fixt,
                       board, store, child, fill_start, holes):

        game = request.getfixturevalue(game_fixt)
        assert game.deco.ender.equalized == (game_fixt == 'pat_game')

        game.board = board
        game.store = store
        game.child = child

        assert game.deco.ender.compute_win_holes() == (fill_start, holes)


class TestRoundTally:

    # TODO RoundTally games with children are not tested

    @pytest.fixture
    def game(self):
        """round tally game"""

        game_consts = gconsts.GameConsts(nbr_start=3, holes=2)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                goal=gi.Goal.RND_POINTS,
                                goal_param=5,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game

    CASES = [
        # 0: start game, not over
        (False, [3, 3, 3, 3], [0, 0], (0, 0), None, None, (0, 0)),

        # 1: round over (no moves), no points yet
        (True, [0, 0, 2, 0], [4, 6], (0, 0), WinCond.ROUND_WIN, True, (0, 1)),
        # 2: round over (no moves), points still low
        (True, [0, 0, 2, 0], [4, 6], (0, 3), WinCond.ROUND_WIN, True, (0, 4)),
        # 3: round over (no moves), points just enough
        (True, [0, 0, 2, 0], [4, 6], (0, 4), WinCond.WIN, True, (0, 5)),

        # 4: round over (two few), no points yet
        (False, [0, 0, 1, 0], [7, 4], (0, 0), WinCond.ROUND_WIN, False, (1, 0)),
        # 5: round over (two few), points still low
        (False, [0, 0, 1, 0], [7, 4], (3, 0), WinCond.ROUND_WIN, False, (4, 0)),
        # 6: round over (two few), points just enough
        (False, [0, 0, 1, 0], [7, 4], (4, 0), WinCond.WIN, False, (5, 0)),

        # 7: round over, skunk so win
        (False, [0, 0, 1, 0], [9, 2], (3, 0), WinCond.WIN, False, (5, 0)),
        # 8: round over, points just enough
        (False, [0, 0, 1, 0], [9, 2], (4, 0), WinCond.WIN, False, (6, 0)),

        # 9: round over (no moves), no points yet
        (True, [0, 0, 2, 0], [6, 4], (0, 0), WinCond.ROUND_TIE, None, (0, 0)),
        # 10: round over (no moves), points still low
        (True, [0, 0, 2, 0], [6, 4], (0, 4), WinCond.ROUND_TIE, None, (0, 4)),

        # 11: round over (no moves), points just enough
        # an odd case because the game should have ended on the last round
        # seeds might have been a better test case
        (True, [0, 0, 2, 0], [6, 4], (5, 5), WinCond.TIE, None, (5, 5)),

        # 12: both over threshhold, higher player should win
        # an odd case because the game should have ended on the last round
        # points not awarded because this game ends in a TIE
        (True, [0, 0, 2, 0], [6, 4], (6, 8), WinCond.WIN, True, (6, 8)),

        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('turn, board, store, ptally, econd, ewinner, etally',
                             CASES,
                             ids=[f"case_{idx}" for idx in range(len(CASES))])
    def test_round_tally(self, game, turn, board, store, ptally, etally,
                         econd, ewinner):

        game.turn = turn
        game.board = board
        game.store = store
        game.rtally.state = ((0, 0), (0, 0), (0, 0), ptally)
        # print(game.deco.ender)

        mdata = utils.make_ender_mdata(game, False, False)
        game.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        assert mdata.winner == ewinner
        assert game.rtally.parameter(0) == etally[0]
        assert game.rtally.parameter(1) == etally[1]


    RND_CASES = [
        # 0: start game
        (False, [3, 3, 3, 3], [0, 0], (0, 0), WinCond.ROUND_TIE, None, (0, 0)),

        # 1:  ending round
        (False, [2, 0, 2, 1], [3, 4], (0, 0), WinCond.ROUND_WIN, True, (0, 1)),

        # 2:  ending round should be a skunk
        (False, [2, 0, 2, 1], [7, 0], (0, 0), WinCond.ROUND_WIN, False, (2, 0)),

        # 3: ending round, T win round
        (True, [2, 0, 2, 0], [3, 5], (0, 3), WinCond.ROUND_WIN, True, (0, 4)),

        # 4: even though ending the round the game ends
        (True, [2, 0, 2, 0], [3, 5], (0, 4), WinCond.WIN, True, (0, 5)),

        # 5:  ending round from even points
        (False, [2, 0, 2, 1], [3, 4], (4, 4), WinCond.WIN, True, (4, 5)),

        # 6:  ending round from even points
        (False, [2, 1, 2, 1], [3, 3], (4, 4), WinCond.ROUND_TIE, None, (4, 4)),

        # 7: round over (no moves), points just enough
        # an odd case because the game should have ended on the last round
        # seeds might have been a better test case
        (True, [0, 0, 2, 0], [6, 4], (5, 5), WinCond.TIE, None, (5, 5)),

        ]
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('turn, board, store, ptally, econd, ewinner, etally',
                             RND_CASES,
                             ids=[f"case_{idx}" for idx in range(len(RND_CASES))])
    def test_rend_tally(self, game, turn, board, store, ptally,
                         econd, ewinner, etally):
        """Test the use round end command"""

        game.turn = turn
        game.board = board
        game.store = store
        game.rtally.state = ((0, 0), (0, 0), (0, 0), ptally)

        mdata = utils.make_ender_mdata(game, False, "round")
        game.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        assert mdata.winner == ewinner

        assert game.rtally.parameter(0) == etally[0]
        assert game.rtally.parameter(1) == etally[1]


    END_CASES = [
        # 0: current game tie, result tie
        (False, [3, 3, 3, 3], [0, 0], (0, 0), WinCond.TIE, None),

        # 1: current game goes to T, T wins
        (True, [0, 0, 2, 0], [4, 6], (0, 0), WinCond.WIN, True),

        # 2: current game goes to F, F wins
        (False, [0, 2, 0, 0], [6, 4], (0, 0), WinCond.WIN, False),

        # 3: current game goes to T, T wins
        (True, [0, 0, 2, 0], [4, 6], (4, 4), WinCond.WIN, True),

        # 4: current game goes to F, F wins
        (False, [0, 2, 0, 0], [6, 4], (4, 4), WinCond.WIN, False),
        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('turn, board, store, ptally, econd, ewinner',
                             END_CASES,
                             ids=[f"case_{idx}" for idx in range(len(END_CASES))])
    def test_end_round_tally(self, game, turn, board, store, ptally,
                             econd, ewinner):

        game.turn = turn
        game.board = board
        game.store = store
        game.rtally.state = ((0, 0), (0, 0), (0, 0), ptally)

        mdata = utils.make_ender_mdata(game, False, True)
        game.deco.ender.game_ended(mdata)

        assert mdata.win_cond == econd
        assert mdata.winner == ewinner


    QUIT_CASES = [
        # 0: current game tie, result tie
        (False, [3, 3, 3, 3], [0, 0], (0, 0), WinCond.TIE, None),

        # 1: divvy to 5, 7, T wins
        (True, [0, 0, 2, 0], [4, 6], (0, 0), WinCond.WIN, True),

        # 2: diffy to 7, 5, F wins
        (False, [0, 2, 0, 0], [6, 4], (0, 0), WinCond.WIN, False),

        # 3: divvy to 5, 7, T wins
        (True, [0, 0, 1, 0], [4, 7], (4, 4), WinCond.WIN, True),

        # 4: divvy to 7, 5, F wins
        (False, [0, 1, 0, 0], [7, 4], (4, 4), WinCond.WIN, False),
        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('turn, board, store, ptally, econd, ewinner',
                             QUIT_CASES,
                             ids=[f"case_{idx}"
                                  for idx in range(len(QUIT_CASES))])
    def test_quit_round_tally(self, game, turn, board, store, ptally,
                             econd, ewinner):

        game.turn = turn
        game.board = board
        game.store = store
        game.rtally.state = ((0, 0), (0, 0), (0, 0), ptally)
        # print(game)

        mdata = utils.make_ender_mdata(game, False, True)
        game.deco.quitter.game_ended(mdata)
        # print(game)

        assert mdata.win_cond == econd
        assert mdata.winner == ewinner


class TestAnimator:

    @pytest.mark.animator
    def test_animator(self, mocker):

        assert animator.ENABLED
        animator.make_animator(None)
        animator.set_active(True)

        mocker.patch('animator.animator.change')
        mobj = mocker.patch('animator.one_step')

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        assert animator.ENABLED
        game = mancala.Mancala(game_consts, game_info)

        assert isinstance(game.deco.ender, emd.AnimateEndMove)
        assert isinstance(game.deco.quitter, emd.AnimateEndMove)

        mdata = utils.make_ender_mdata(game, False, True)
        game.deco.ender.game_ended(mdata)

        mobj.assert_called_once()


    def test_no_animator(self, mocker):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        assert not animator.ENABLED
        game = mancala.Mancala(game_consts, game_info)

        assert not isinstance(game.deco.ender, emd.AnimateEndMove)
        assert not isinstance(game.deco.quitter, emd.AnimateEndMove)
