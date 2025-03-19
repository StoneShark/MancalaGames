# -*- coding: utf-8 -*-
"""The goal of this testing to exercise the sower deco
chain in unique ways.

Created on Sat Aug 10 18:15:40 2024
@author: Ann"""


# %% imports

import pytest
pytestmark = pytest.mark.comptest


from context import game_interface as gi
from context import game_constants as gconsts
from context import mancala


# %% consts

HOLES = 5

T = True
F = False
N = None

CCW = gi.Direct.CCW
CW = gi.Direct.CW

NBLCK = [F] * (2 * HOLES)

NSTR = 1967  # no change in the store expected


# %% setup and cases


GAMECONF = {'basic':
                {'evens': True,
                 'stores': True},   # avoid the capt warnings

            'bs_mlap':    # prescr BASIC with mlaps => no mlap on first
                {'prescribed': gi.SowPrescribed.BASIC_SOWER,
                 'mlaps': True,
                 'evens': True,
                 'stores': True},

            'ms_no_mlap':   # prescr MLAPS without mlaps => mlap on first
                {'prescribed': gi.SowPrescribed.MLAPS_SOWER,
                 'evens': True,
                 'stores': True},

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

            'sbd_udir':   # sow block div with udir but no mlaps, check both dirs
                {'goal': gi.Goal.DEPRIVE,
                 'sow_rule': gi.SowRule.SOW_BLKD_DIV,
                 'goal_param': 3,
                 'blocks': True,
                 'udir_holes': [0, 1, 2, 3, 4]},

            'dep_capta':
                {'goal': gi.Goal.DEPRIVE,
                 'sow_rule': gi.SowRule.OWN_SOW_CAPT_ALL,
                 'mlaps': gi.LapSower.LAPPER,
                 'evens': True,
                 'stores': True},

            'chd_capta':
                {'child_type': gi.ChildType.NORMAL,
                 'child_cvt': 3,
                 'sow_rule': gi.SowRule.OWN_SOW_CAPT_ALL,
                 'mlaps': gi.LapSower.LAPPER,
                 'capt_on': [3],
                  'stores': True},

            'no2s':         # no prescribed opening
                {'sow_rule': gi.SowRule.NO_SOW_OPP_NS,
                 'sow_param': 2,
                 'capt_on': [3],
                  'stores': True},

            'no2schd':  # with children, don't stop for child
                {'child_type': gi.ChildType.NORMAL,
                 'child_cvt': 3,
                 'sow_rule': gi.SowRule.NO_SOW_OPP_NS,
                 'sow_param': 2,
                 'stores': True,
                 'capt_on': [3]},

            'mlvisopd':  # mlap, visit opp, change dir
                {'mlaps': gi.LapSower.LAPPER,
                 'sow_rule': gi.SowRule.CHANGE_DIR_LAP,
                 'visit_opp': True,
                 'stores': True,
                 'crosscapt': True},

            'mlaps_cnt':
                {'mlaps': gi.LapSower.LAPPER,
                 'child_type': gi.ChildType.NORMAL,
                 'child_cvt': 3,
                 'visit_opp': True,
                 'sow_own_store': True,
                 'stores': True,
                 'capt_on': [2]},

            's_own_rnds':
                {"blocks": True,
                 "crosscapt": True,
                 "mustpass": True,
                 "rounds": True,
                 "sow_own_store": True,
                 "stores": True,
                 },

            's_own_rnds_lap':
                {"blocks": True,
                 "mlaps": True,
                 "crosscapt": True,
                 "mustpass": True,
                 "rounds": True,
                 "sow_own_store": True,
                 "stores": True,
                 },

            'mlaps_walda':
                {'mlaps': gi.LapSower.LAPPER,
                 'child_type': gi.ChildType.NORMAL,
                 'child_locs': gi.ChildLocs.ENDS_PLUS_ONE_OPP,
                 'child_cvt': 3},

            }

START = {'start':
             mancala.GameState(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                               store=(0, 0),
                               mcount=1,    # mcount is inc'ed at top of move
                               _turn=False,
                               blocked=(F, F, F, F, F, F, F, F, F, F),
                               child=(N, N, N, N, N, N, N, N, N, N)),
        'second':
             mancala.GameState(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                               store=(0, 0),
                               mcount=2,   # second turn
                               _turn=False,
                               blocked=(F, F, F, F, F, F, F, F, F, F),
                               child=(N, N, N, N, N, N, N, N, N, N)),

        'ones':
             mancala.GameState(board=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                               store=(5, 5),
                               mcount=1,
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N)),

        'st_blocks':
             mancala.GameState(board=(2, 2, 2, 2, 0, 0, 2, 2, 2, 2),
                               store=(2, 2),
                               mcount=1,
                               _turn=False,
                               blocked=(F, F, F, F, T, T, F, F, F, F)),

        'wchild':
            mancala.GameState(board=(1, 1, 1, 3, 3, 3, 4, 2, 1, 0),
                              child=(N, N, N, N, N, F, N, N, N, N),
                              store=(0, 1),
                              mcount=1,
                              _turn=False,
                              blocked=(F, F, F, F, F, F, F, F, F, F)),

        'wochild':
            mancala.GameState(board=(1, 1, 1, 3, 1, 3, 0, 0, 0, 0),
                              child=(N, N, N, N, N, N, N, N, N, N),
                              store=(5, 5),
                              mcount=1,
                              _turn=False,
                              blocked=(F, F, F, F, F, F, F, F, F, F)),

        '2ndround':
             mancala.GameState(board=(2, 4, 2, 0, 3, 0, 0, 0, 0, 0),
                               store=(0, 9),
                               mcount=5,
                               _turn=False,
                               blocked=(F, F, F, F, F, T, F, F, F, F)),

        '2ndround2b':
             mancala.GameState(board=(2, 4, 2, 2, 0, 0, 0, 0, 0, 0),
                               store=(0, 10),
                               mcount=5,
                               _turn=False,
                               blocked=(F, F, F, F, T, T, F, F, F, F)),

        'walda_nostop':
             mancala.GameState(board=(0, 2, 3, 0, 0, 1, 1, 2, 0, 4),
                               store=(3, 4),
                               mcount=5,
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N)),

        }

CASES = [('basic', 'start', F, 2,
          4, (2, 2, 0, 3, 3, 2, 2, 2, 2, 2), NSTR, NBLCK),

         ('bs_mlap', 'start', F, 2,
          4, (2, 2, 0, 3, 3, 2, 2, 2, 2, 2), NSTR, NBLCK),
         # stop mlaps for capt
         ('bs_mlap', 'second', F, 2,
          3, (0, 3, 1, 4, 0, 3, 3, 0, 3, 3), NSTR, NBLCK),

         ('ms_no_mlap', 'start', F, 2,
          7, (0, 3, 1, 0, 1, 4, 4, 1, 3, 3), NSTR, NBLCK),
         ('ms_no_mlap', 'second', F, 2,
          4, (2, 2, 0, 3, 3, 2, 2, 2, 2, 2), NSTR, NBLCK),

         ('s1_move1', 'ones', F, 0,
          5, (0, 1, 1, 1, 1, 2, 1, 1, 1, 1), NSTR, NBLCK),
         ('s1_split', 'start', F, gi.MoveTpl(2, CCW),
          5, (2, 2, 0, 3, 2, 3, 2, 2, 2, 2), NSTR, NBLCK),
         ('s1_split', 'start', F, gi.MoveTpl(2, CW),
          9, (2, 3, 0, 2, 2, 2, 2, 2, 2, 3), NSTR, NBLCK),

         ('s1_blocks', 'st_blocks', F, gi.MoveTpl(1, CCW),
          6, (2, 0, 3, 2, 0, 0, 3, 2, 2, 2), NSTR,
          (F, F, F, F, T, T, F, F, F, F)),
         ('s1_blocks', 'st_blocks', F, gi.MoveTpl(2, CW),
          9, (2, 3, 0, 2, 0, 0, 2, 2, 2, 3), NSTR,
          (F, F, F, F, T, T, F, F, F, F)),

         # actual direction doesn't matter
         ('p1m1_udir', 'start', F, gi.MoveTpl(4, CCW),
          5, (3, 1, 3, 1, 2, 2, 3, 1, 3, 1), NSTR, NBLCK),
         ('p1m1_udir', 'start', F, gi.MoveTpl(4, CW),
          5, (3, 1, 3, 1, 2, 2, 3, 1, 3, 1), NSTR, NBLCK),

         ('p1m1_blocks', 'st_blocks', F, gi.MoveTpl(1, CCW),
          8, (1, 2, 1, 3, 0, 0, 1, 3, 2, 3), NSTR,
          (F, F, F, F, T, T, F, F, F, F)),
         ('p1m1_blocks', 'st_blocks', F, gi.MoveTpl(2, CW),
          7, (3, 1, 2, 1, 0, 0, 3, 2, 3, 1), NSTR,
          (F, F, F, F, T, T, F, F, F, F)),

         ('sbd_udir', 'start', F, gi.MoveTpl(4, CCW),
          6, (2, 2, 2, 2, 0, 3, 0, 2, 2, 2), [3, 0],
             (F, F, F, F, F, F, T, F, F, F)),
         ('sbd_udir', 'start', T, gi.MoveTpl(1, CW),
          6, (2, 2, 2, 2, 2, 2, 3, 3, 0, 2), NSTR, NBLCK),
         ('sbd_udir', 'st_blocks', F, gi.MoveTpl(3, CCW),
          6, (2, 2, 2, 0, 0, 0, 0, 2, 2, 2), [6, 2],
             (F, F, F, F, T, T, T, F, F, F)),

         ('dep_capta', 'start', F, 1,
          2, (3, 1, 4, 0, 3, 3, 0, 3, 3, 0), NSTR, NBLCK),

         # capture during sow, stop mlap to make child
         ('chd_capta', 'start', F, 1,
          3, (2, 0, 0, 3, 2, 2, 2, 2, 2, 2), [3, 0], NBLCK),

         ('no2s', 'start', F, 4,
          1, (3, 3, 2, 2, 0, 2, 2, 2, 2, 2), NSTR, NBLCK),
         ('no2schd', 'start', F, 4,
          1, (3, 3, 2, 2, 0, 2, 2, 2, 2, 2), NSTR, NBLCK),

         # ops with visit
         ('mlvisopd', 'start', T, 2,  # didn't reach
          9, (2, 2, 2, 2, 2, 2, 2, 0, 3, 3), NSTR, NBLCK),
         ('mlvisopd', 'start', T, 1,  # does reach, dir change after 1st lap
          0, (1, 2, 2, 2, 2, 2, 2, 0, 2, 5), NSTR, NBLCK),

         # mlap continuer
         ('mlaps_cnt', 'ones', F, 1, # stop no visit
          2, (1, 0, 2, 1, 1, 1, 1, 1, 1, 1), NSTR, NBLCK),
         ('mlaps_cnt', 'start', F, 1, # stop no visit (1st) &  make child
          3, (2, 0, 3, 3, 2, 2, 2, 2, 2, 2), NSTR, NBLCK),
         ('mlaps_cnt', 'start', F, 4, # stop make child
          5, (2, 2, 2, 2, 0, 3, 2, 2, 2, 2), [1, 0], NBLCK),
         ('mlaps_cnt', 'wchild', F, 3, # stop in child
          5, (1, 1, 1, 0, 4, 4, 4, 2, 1, 0), [1, 1], NBLCK),
         ('mlaps_cnt', 'start', F, 3, # repeat turn (end in store)
          gi.WinCond.REPEAT_TURN,
          (2, 2, 2, 0, 3, 2, 2, 2, 2, 2), [1, 0], NBLCK),
         ('mlaps_cnt', 'wchild', F, 4, # do mlaps, then capt
          1, (2, 2, 1, 3, 0, 4, 0, 3, 2, 1), [1, 1], NBLCK),
          ('mlaps_cnt', 'wochild', F, 3, # do mlaps, then stop
           9, (1, 1, 1, 0, 2, 0, 1, 1, 1, 1), [6, 5], NBLCK),

          # sow own err with block/rounds
          ('s_own_rnds', '2ndround', F, 1,
           gi.WinCond.REPEAT_TURN,
           (2, 0, 3, 1, 4, 0, 0, 0, 0, 0), [1, 9],
           (F, F, F, F, F, T, F, F, F, F)),
          ('s_own_rnds', '2ndround2b', F, 2,
           gi.WinCond.REPEAT_TURN,
           (2, 4, 0, 3, 0, 0, 0, 0, 0, 0), [1, 10],
           (F, F, F, F, T, T, F, F, F, F)),
          ('s_own_rnds', '2ndround2b', F, 3,   # don't sow on own side, 1st is in store
           6,
           (2, 4, 2, 0, 0, 0, 1, 0, 0, 0), [1, 10],
           (F, F, F, F, T, T, F, F, F, F)),

          ('s_own_rnds_lap', '2ndround', F, 0,
           gi.WinCond.REPEAT_TURN,
           (0, 5, 0, 1, 4, 0, 0, 0, 0, 0), [1, 9],
           (F, F, F, F, F, T, F, F, F, F)),

          ('mlaps_walda', 'walda_nostop', F, 2,
           0, (1, 2, 0, 1, 1, 0, 2, 0, 1, 5), NSTR, NBLCK),

         ]

CIDS = [f'{case[0]}-{case[1]}-{case[2]}-idx{idx}' for idx, case in enumerate(CASES)]


BAD_INHIBITOR_TESTS = [

    # cannot have blocked holes on the first move of a deprive game
    'test_inhibit_sower[sbd_udir-st_blocks-False-idx16-1]',
    ]


# %% test_sower

@pytest.mark.usefixtures('logger')
@pytest.mark.parametrize('conf_name, state_name, turn, move,'
                         'eloc, eboard, estore, eblocks',
                         CASES, ids=CIDS)
def test_sower(conf_name, state_name, turn, move,
               eloc, eboard, estore, eblocks):    # expected values
    """Use do_sow from Mancala class. It uses the starter, get_direction,
    and sower."""

    game_consts = gconsts.GameConsts(nbr_start=2, holes=HOLES)
    game_info = gi.GameInfo(**GAMECONF[conf_name],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game =  mancala.Mancala(game_consts, game_info)

    start_state = START[state_name]
    game.state = start_state
    game.turn = turn

    # check game and state consistency
    assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
        "Test error: seed count wrong!"
    assert not game.info.blocks or (game.info.blocks and start_state.blocked), \
        "Test error: game.info.blocks inconsistent with start_state"
    assert not game.info.child_type or (game.info.child_type and start_state.child), \
        "Test error: game.info.child_type inconsistent with start_state"

    print(GAMECONF[conf_name])
    print(game)
    print('move:', move)
    mdata = game.do_sow(move)

    # check the expected changes
    assert mdata.capt_loc == eloc
    assert game.board == list(eboard)
    if estore == NSTR:
        assert tuple(game.store) == start_state.store
    else:
        assert game.store == estore
        assert tuple(game.store) != start_state.store, \
            "Test error: use NSTR when store expected to be unchanged"
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
    assert game.inhibitor.get_state() == start_state.istate

    assert sum(game.store) + sum(game.board) == game.cts.total_seeds


# @pytest.mark.usefixtures('logger')
@pytest.mark.parametrize('mcount', (1, 2))
@pytest.mark.parametrize('conf_name, state_name, turn, move,'
                         'eloc, eboard, estore, eblocks',
                         CASES, ids=CIDS)
def test_inhibit_sower(request,
                       mcount, conf_name, state_name, turn, move,
                       eloc, eboard, estore, eblocks):    # expected values
    """Use the same test cases for both first and second move of the game,
    but set nocaptmoves for all. If there's error in building game_info,
    skip the test."""

    if request.node.name in BAD_INHIBITOR_TESTS:
        return

    game_consts = gconsts.GameConsts(nbr_start=2, holes=HOLES)
    try:
        game_info = gi.GameInfo(**GAMECONF[conf_name],
                                nocaptmoves=1,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
    except gi.GameInfoError as error:
        if 'sow_own_nocapt' in repr(error):
            pytest.skip('nocaptmoves incomp with sow_own_store')
        else:
            pytest.fail('nocaptmoves conflict for unkown reason')
    game =  mancala.Mancala(game_consts, game_info)

    # save istate and put it back after copying in test state
    istate = game.inhibitor.get_state()
    start_state = START[state_name]
    game.state = start_state
    game.inhibitor.set_state(istate)

    game.turn = turn

    # clear_if is called at end of move, but we want to simulate
    # it being called for the previous turn
    game.mcount = mcount - 1
    game.inhibitor.clear_if(game, None)  # mdata isn't used in this inhibitor
    game.mcount = mcount

    # confirm inhibitor config
    assert game.inhibitor.stop_me_capt(turn) == (not bool(mcount - 1))

    game.do_sow(move)

    if mcount == 1 or estore == NSTR:
        # blocks & stores should be unchanged
        if game.info.blocks:
            assert tuple(game.blocked) == start_state.blocked
        assert tuple(game.store) == start_state.store
    else:
        # blocks and stores changed as expected
        assert game.blocked == list(eblocks)
        assert game.store == estore

    assert sum(game.store) + sum(game.board) == game.cts.total_seeds
