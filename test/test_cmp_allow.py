# -*- coding: utf-8 -*-
"""The goal of this testing to exercise the allowables deco
chain in unique ways.
Created on Thu Sep 19 07:49:19 2024
@author: Ann"""


# %% imports

import pytest
pytestmark = pytest.mark.comptest


from context import game_info as gi
from context import game_constants as gconsts
from context import mancala


# %% consts

HOLES = 5

T = True
F = False
N = None

CCW = gi.Direct.CCW
CW = gi.Direct.CW

# %% setup and cases


GAMECONF = {'basic':
                {'evens': True,
                 'stores': True},   # not inputs, but avoid capt warnings

            'msh_all2':
                {'evens': True,
                 'stores': True,
                 'mustshare': True,
                 'allow_rule': gi.AllowRule.TWO_ONLY_ALL},

            'msh_1_0':
                {'evens': True,
                 'stores': True,
                 'mustshare': True,
                 'allow_rule': gi.AllowRule.SINGLE_TO_ZERO},

            'rght2_all':
                {'evens': True,
                 'stores': True,
                 'start_pattern': gi.StartPattern.ALTERNATES,
                 'allow_rule': gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO},

            'first2rgt':
                {'evens': True,
                 'stores': True,
                 'start_pattern': gi.StartPattern.ALTERNATES,
                 'allow_rule': gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO},

            'no2s_right':
                {'evens': True,
                 'stores': True,
                 'start_pattern': gi.StartPattern.ALTERNATES,
                 'allow_rule': gi.AllowRule.TWO_ONLY_ALL_RIGHT},

            'mshare_sowo':
                {'evens': True,
                 'stores': True,
                 'mustshare': True,
                 'sow_stores': gi.SowStores.OWN},

            'gsnot_pick2s':
                {'capt_on': [2, 3],
                 'stores': True,
                 'capt_side': 1,
                 'grandslam': gi.GrandSlam.NOT_LEGAL,
                 'pickextra': gi.CaptExtraPick.PICKOPPBASIC},

            # game configs with mlength = 3
            'ter':
                {'evens': True,
                 'stores': True,
                 'goal': gi.Goal.TERRITORY,
                 'goal_param': 2 * HOLES},

            'ter1_0':
                {'evens': True,
                 'stores': True,
                 'goal': gi.Goal.TERRITORY,
                 'goal_param': 2 * HOLES,
                 'allow_rule': gi.AllowRule.SINGLE_TO_ZERO},

            'ter1all':
                {'evens': True,
                 'stores': True,
                 'goal': gi.Goal.TERRITORY,
                 'goal_param': 2 * HOLES,
                 'allow_rule': gi.AllowRule.SINGLE_ONLY_ALL},


            }

START = {
    'start':
         mancala.GameState(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                           store=(0, 0),
                           mcount=1,    # mcount is inc'ed at top of move
                           _turn=False),

    'altpatt':
         mancala.GameState(board=(0, 2, 0, 2, 0, 2, 0, 2, 0, 2),
                           store=(0, 0),
                           mcount=0,
                           _turn=False),

    'one_to':
         mancala.GameState(board=(1, 0, 1, 2, 3, 1, 0, 1, 2, 3),
                           store=(3, 3),
                           mcount=4,
                           _turn=False),

    'fshare':
         mancala.GameState(board=(1, 0, 1, 3, 2, 0, 0, 0, 0, 0),
                           store=(7, 6),
                           mcount=15,
                           _turn=False),

    'tshare':
         mancala.GameState(board=(0, 0, 0, 0, 0, 1, 0, 1, 3, 2),
                           store=(7, 6),
                           mcount=15,
                           _turn=False),

    'onefshare':
         mancala.GameState(board=(1, 1, 1, 1, 1, 0, 0, 0, 0, 0),
                           store=(15, 0),
                           mcount=4,
                           _turn=False),
    'onetshare':
         mancala.GameState(board=(0, 0, 0, 0, 0, 1, 1, 1, 1, 1),
                           store=(15, 0),
                           mcount=4,
                           _turn=False),

        }

CASES = [('basic', 'start', [T, T, T, T, T], [T, T, T, T, T]),

         ('msh_all2', 'fshare', [F, F, F, T, F], [F, F, F, F, F]),
         ('msh_all2', 'tshare', [F, F, F, F, F], [F, T, F, F, F]),
         ('msh_1_0', 'onefshare', [F, F, F, F, T], [F, F, F, F, F]),
         ('msh_1_0', 'onetshare', [F, F, F, F, F], [T, F, F, F, F]),

         # start pattern has empty first hole
         ('rght2_all', 'altpatt', [F, T, F, T, F], [T, F, T, F, F]),
         ('first2rgt', 'altpatt', [F, T, F, T, F], [T, F, T, F, F]),
         ('no2s_right', 'altpatt', [F, F, F, T, F], [T, F, F, F, F]),

         # can't move any seeds to opp because they don't reach
         ('mshare_sowo', 'onefshare', [F, F, F, F, F], [F, F, F, F, F]),
         ('mshare_sowo', 'onetshare', [F, F, F, F, F], [F, F, F, F, F]),

         # game config can pick all opps seeds on start moves
         ('gsnot_pick2s', 'start', [T, T, T, F, F], [F, F, T, T, T]),

         ('ter', 'start',
          [T, T, T, T, T, F, F, F, F, F],
          [F, F, F, F, F, T, T, T, T, T]),

         ('ter1_0', 'start',
          [T, T, T, T, T, F, F, F, F, F],
          [F, F, F, F, F, T, T, T, T, T]),

         ('ter1_0', 'one_to',
          [T, F, F, T, T, F, F, F, F, F],
          [F, F, F, F, F, T, F, F, T, T]),

         ('ter1all', 'start',
          [T, T, T, T, T, F, F, F, F, F],
          [F, F, F, F, F, T, T, T, T, T]),

         ]

CIDS = [f'{case[0]}-{case[1]}-idx{idx}' for idx, case in enumerate(CASES)]

# @pytest.mark.usefixtures("logger")
@pytest.mark.parametrize('conf_name, state_name,e_f_allow, e_t_allow',
                         CASES, ids=CIDS)
def test_allowables(conf_name, state_name,
                    e_t_allow, e_f_allow):    # expected values
    """Check allowables for both True and False in each test case."""

    game_consts = gconsts.GameConsts(nbr_start=2, holes=HOLES)
    game_info = gi.GameInfo(**GAMECONF[conf_name],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game =  mancala.Mancala(game_consts, game_info)

    start_state = START[state_name]
    game.state = start_state

    # print(GAMECONF[conf_name])
    # print(game)
    # print(game.deco.allow)

    # check game consistency
    assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
        "Test error: seed count wrong!"

    game.turn = False
    allowables = game.deco.allow.get_allowable_holes()
    # print(allowables)
    assert allowables == e_f_allow

    game.turn = True
    allowables = game.deco.allow.get_allowable_holes()
    # print(allowables)
    assert allowables == e_t_allow

    # confirm game state unchanged (don't check things that weren't set)
    game_state = game.state
    assert game_state.board == start_state.board
    assert game_state.store == start_state.store
    assert game_state.mcount == start_state.mcount
    if start_state.child:
        assert game_state.child == start_state.child
    if start_state.owner:
        assert game_state.owner == start_state.owner
    if start_state.blocked:
        assert game_state.blocked == start_state.blocked



# %% invalid configs

BAD_CONFIGS = {

    'opp_empty':
        {'evens': True,
         'stores': True,
         'goal': gi.Goal.TERRITORY,
         'goal_param': 2 * HOLES,
         'allow_rule': gi.AllowRule.OPP_OR_EMPTY},

    'two_or_right':
        {'evens': True,
         'stores': True,
         'goal': gi.Goal.TERRITORY,
         'goal_param': 2 * HOLES,
         'allow_rule': gi.AllowRule.TWO_ONLY_ALL_RIGHT},

    'right_two':
        {'evens': True,
         'stores': True,
         'goal': gi.Goal.TERRITORY,
         'goal_param': 2 * HOLES,
         'allow_rule': gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO},

    'right21all':
        {'evens': True,
         'stores': True,
         'no_sides': True,
         'allow_rule': gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO},

    'ns_opp_empty':
        {'evens': True,
         'stores': True,
         'no_sides': True,
         'allow_rule': gi.AllowRule.OPP_OR_EMPTY},

    'ns_two_or_right':
        {'evens': True,
         'stores': True,
         'no_sides': True,
         'allow_rule': gi.AllowRule.TWO_ONLY_ALL_RIGHT},

    'ns_right_two':
        {'evens': True,
         'stores': True,
         'no_sides': True,
         'allow_rule': gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO},


    'ns_right21all':
        {'evens': True,
         'stores': True,
         'no_sides': True,
         'allow_rule': gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO},

    }

@pytest.mark.parametrize('conf_dict',
                         BAD_CONFIGS.values(),
                         ids=BAD_CONFIGS.keys())
def test_bad_config(conf_dict):
    """ginfo_rules prevents these games so they are not tested.
    if ginfo_rules is changed to allow them,
    report an error so tests are written."""

    with pytest.raises(gi.GameInfoError):
        gi.GameInfo(**conf_dict,
                    nbr_holes=HOLES,
                    rules=mancala.Mancala.rules)
