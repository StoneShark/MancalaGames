# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 18:15:40 2024
@author: Ann"""


# %% imports

import pytest
pytestmark = pytest.mark.comptest


from context import game_interface as gi
from context import game_constants as gc
from context import mancala


# %% consts

HOLES = 5

T = True
F = False
N = None

CCW = gi.Direct.CCW
CW = gi.Direct.CW

ESTR = [0, 0]
NBLCK = [F] * (2 * HOLES)


# %% setup and cases


GAMECONF = {'basic':
                {'evens': True},   # avoid the no capt warning

            'bs_mlap':    # prescr BASIC with mlaps => no mlap on first
                {'prescribed': gi.SowPrescribed.BASIC_SOWER,
                 'mlaps': True,
                 'evens': True},

            'ms_no_mlap':   # prescr MLAPS without mlaps => mlap on first
                {'prescribed': gi.SowPrescribed.MLAPS_SOWER,
                 'evens': True},

            's1_move1':   # prescr SOW1OPP with move_one, one should be opp
                {'prescribed': gi.SowPrescribed.SOW1OPP,
                 'stores': True,
                 'sow_start': True,
                 'move_one': True,
                 'min_move': 2,
                 'evens': True},

            's1_split':   # prescr SOW1OPP with SPLIT, check both dirs
                {'prescribed': gi.SowPrescribed.SOW1OPP,
                 'stores': True,
                 'sow_direct': gi.Direct.SPLIT,
                 'udir_holes': [2],
                 'evens': True},

            's1_blocks':   # prescr SOW1OPP with blocks, check both dirs
                {'prescribed': gi.SowPrescribed.SOW1OPP,
                 'stores': True,
                 'udir_holes': [0, 1, 2, 3, 4],
                 'blocks': True,
                 'rounds': True,  # only to avoid warning
                 'evens': True},

            'p1m1_udir':   # prescr plus1minus1 with udir, check both dirs
                {'prescribed': gi.SowPrescribed.PLUS1MINUS1,
                 'stores': True,
                 'udir_holes': [0, 1, 2, 3, 4],
                 'evens': True},

            'p1m1_blocks':   # prescr PLUS1MINUS1 with blocks, check both dirs
                {'prescribed': gi.SowPrescribed.PLUS1MINUS1,
                 'stores': True,
                 'udir_holes': [0, 1, 2, 3, 4],
                 'blocks': True,
                 'rounds': True,
                 'evens': True},

            'dep_capta':
                {'goal': gi.Goal.DEPRIVE,
                 'sow_rule': gi.SowRule.OWN_SOW_CAPT_ALL,
                 'mlaps': gi.LapSower.LAPPER,
                 'evens': True},

            'chd_capta':
                {'child_type': gi.ChildType.NORMAL,
                 'child_cvt': 3,
                 'sow_rule': gi.SowRule.OWN_SOW_CAPT_ALL,
                 'mlaps': gi.LapSower.LAPPER,
                 'capt_on': [3]},

            'no2s':         # no prescribed opening
                {'sow_rule': gi.SowRule.NO_SOW_OPP_2S,
                 'capt_on': [3]},

            'no2schd':  # with children, don't stop for child
                {'child_type': gi.ChildType.NORMAL,
                 'child_cvt': 3,
                 'sow_rule': gi.SowRule.NO_SOW_OPP_2S,
                 'stores': True,
                 'capt_on': [3]},

            }

START = {'start':
             mancala.GameState(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                               store=(0, 0),
                               mcount=1,    # mcount is inc'ed at top of move
                               _turn=False,
                               blocked=(F, F, F, F, F, F, F, F, F, F)),
        'second':
             mancala.GameState(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                               store=(0, 0),
                               mcount=2,   # second turn
                               _turn=False,
                               blocked=(F, F, F, F, F, F, F, F, F, F)),

        'ones':
             mancala.GameState(board=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                               store=(5, 5),
                               mcount=1,
                               _turn=False),

        'st_blocks':
             mancala.GameState(board=(2, 2, 2, 2, 0, 0, 2, 2, 2, 2),
                               store=(2, 2),
                               mcount=1,
                               _turn=False,
                               blocked=(F, F, F, F, T, T, F, F, F, F)),

        }

CASES = [('basic', 'start', F, 2,
          4, (2, 2, 0, 3, 3, 2, 2, 2, 2, 2), ESTR, NBLCK),

         ('bs_mlap', 'start', F, 2,
          4, (2, 2, 0, 3, 3, 2, 2, 2, 2, 2), ESTR, NBLCK),
         # stop mlaps for capt
         ('bs_mlap', 'second', F, 2,
          3, (0, 3, 1, 4, 0, 3, 3, 0, 3, 3), ESTR, NBLCK),

         ('ms_no_mlap', 'start', F, 2,
          7, (0, 3, 1, 0, 1, 4, 4, 1, 3, 3), ESTR, NBLCK),
         ('ms_no_mlap', 'second', F, 2,
          4, (2, 2, 0, 3, 3, 2, 2, 2, 2, 2), ESTR, NBLCK),

         ('s1_move1', 'ones', F, 0,
          5, (0, 1, 1, 1, 1, 2, 1, 1, 1, 1), [5, 5], NBLCK),
         ('s1_split', 'start', F, gi.MoveTpl(2, CCW),
          5, (2, 2, 0, 3, 2, 3, 2, 2, 2, 2), ESTR, NBLCK),
         ('s1_split', 'start', F, gi.MoveTpl(2, CW),
          9, (2, 3, 0, 2, 2, 2, 2, 2, 2, 3), ESTR, NBLCK),

         ('s1_blocks', 'st_blocks', F, gi.MoveTpl(1, CCW),
          6, (2, 0, 3, 2, 0, 0, 3, 2, 2, 2), [2, 2],
          (F, F, F, F, T, T, F, F, F, F)),
         ('s1_blocks', 'st_blocks', F, gi.MoveTpl(2, CW),
          9, (2, 3, 0, 2, 0, 0, 2, 2, 2, 3), [2, 2],
          (F, F, F, F, T, T, F, F, F, F)),

         # actual direction doesn't matter
         ('p1m1_udir', 'start', F, gi.MoveTpl(4, CCW),
          5, (3, 1, 3, 1, 2, 2, 3, 1, 3, 1), ESTR, NBLCK),
         ('p1m1_udir', 'start', F, gi.MoveTpl(4, CW),
          5, (3, 1, 3, 1, 2, 2, 3, 1, 3, 1), ESTR, NBLCK),

         ('p1m1_blocks', 'st_blocks', F, gi.MoveTpl(1, CCW),
          8, (1, 2, 1, 3, 0, 0, 1, 3, 2, 3), [2, 2],
          (F, F, F, F, T, T, F, F, F, F)),
         ('p1m1_blocks', 'st_blocks', F, gi.MoveTpl(2, CW),
          7, (3, 1, 2, 1, 0, 0, 3, 2, 3, 1), [2, 2],
          (F, F, F, F, T, T, F, F, F, F)),

         ('dep_capta', 'start', F, 1,
          2, (3, 1, 4, 0, 3, 3, 0, 3, 3, 0), ESTR, NBLCK),

         # capture during sow, stop mlap to make child
         ('chd_capta', 'start', F, 1,
          3, (2, 0, 0, 3, 2, 2, 2, 2, 2, 2), [3, 0], NBLCK),

         ('no2s', 'start', F, 4,
          1, (3, 3, 2, 2, 0, 2, 2, 2, 2, 2), ESTR, NBLCK),
         ('no2schd', 'start', F, 4,
          1, (3, 3, 2, 2, 0, 2, 2, 2, 2, 2), ESTR, NBLCK),

         ]


# %% test_sower

@pytest.mark.parametrize('conf_name, state_name, turn, move,'
                         'eloc, eboard, estore, eblocks',
                         CASES,
                         ids=[f'{case[0]}-{case[1]}-{case[2]}-idx{idx}'
                              for idx, case in enumerate(CASES)])
def test_sower(conf_name, state_name, turn, move,
               eloc, eboard, estore, eblocks):    # expected values
    """Use do_sow from Mancala class. It uses the starter, get_direction,
    and sower."""

    game_consts = gc.GameConsts(nbr_start=2, holes=HOLES)
    game_info = gi.GameInfo(**GAMECONF[conf_name],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game =  mancala.Mancala(game_consts, game_info)

    start_state = START[state_name]
    game.state = start_state
    game.turn = turn

    # check game and state consistency
    assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
        "Test config error: seed count wrong!"
    assert not game.info.blocks or (game.info.blocks and start_state.blocked), \
        "Test config error: game.info.blocks inconsistent with start_state"

    print(GAMECONF[conf_name])
    print(game)
    print(move)
    mdata = game.do_sow(move)
    print(game)

    # check the expected changes
    assert mdata.capt_loc == eloc
    assert game.board == list(eboard)
    assert game.store == estore
    assert game.blocked == list(eblocks)
    if start_state.unlocked:
        assert game.board[mdata.sow_loc].unlocked   # starter does this

    # confirm nothing else changed and board is valid
    assert game.mcount == start_state.mcount
    assert game.turn == turn
    if start_state.child:
        assert game.child == list(start_state.child)
    if start_state.owner:
        assert game.owner == list(start_state.owner)
    # TODO ok to ignore istate?

    assert sum(game.store) + sum(game.board) == game.cts.total_seeds
