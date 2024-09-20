# -*- coding: utf-8 -*-
"""The goal of this testing to exercise the capturer deco
chain in unique ways.

Created on Wed Sep 18 10:42:11 2024
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

NCHILD = [N] * (2 * HOLES)
ESTR = [0, 0]

# %% setup and cases


GAMECONF = {'basic':
                {'evens': True},

            }

START = {'start':
             mancala.GameState(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                               store=(0, 0),
                               mcount=1,    # mcount is inc'ed at top of move
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N)),

        }

CASES = [('basic', 'start', F, 2,
          2, (2, 2, 0, 2, 2, 2, 2, 2, 2, 2), (2, 0), NCHILD, F, T),

         ]

# %debug doesn't work if this is spread across lines
CIDS = [f'{case[0]}-{case[1]}-{case[2]}-idx{idx}' for idx, case in enumerate(CASES)]



# %% test_capturer

@pytest.mark.parametrize('conf_name, state_name, turn, capt_loc,'
                         'eloc, eboard, estore, echild, ecchg, ecapt',
                         CASES, ids=CIDS)
def test_capturer(logger, conf_name, state_name, turn, capt_loc,
                  eloc, eboard, estore, echild, ecchg, ecapt):    # expected values
    """Run the capturer."""

    game_consts = gc.GameConsts(nbr_start=2, holes=HOLES)
    game_info = gi.GameInfo(**GAMECONF[conf_name],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game =  mancala.Mancala(game_consts, game_info)

    start_state = START[state_name]
    game.state = start_state
    game.turn = turn

    # check game and state consistency
    assert game.info.sow_direct in (CW, CCW), \
        "Test error: use only concrete sow dirs"
    assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
        "Test error: seed count wrong!"
    assert not game.info.child_type or (game.info.child_type and start_state.child), \
        "Test error: game.info.child_type inconsistent with start_state"

    print(GAMECONF[conf_name])
    print(game)
    print('capt_loc:', capt_loc)

    mdata = mancala.MoveData(game, None)   # move isn't used in capturer
    mdata.direct = game.info.sow_direct
    mdata.seeds = 4                        # make an input??
    mdata.capt_loc = capt_loc

    game.deco.capturer.do_captures(mdata)

    # check the expected outputs and changes
    assert mdata.capt_loc == eloc
    assert mdata.capt_changed == ecchg
    assert mdata.captured == ecapt

    assert game.board == list(eboard)
    assert game.store == list(estore)
    assert game.child == list(echild)

    # confirm nothing else changed and board is valid
    assert game.mcount == start_state.mcount
    assert game.turn == turn
    if start_state.blocked:
        assert game.blocked == list(start_state.blocked)
    if start_state.owner:
        assert game.owner == list(start_state.owner)
    assert game.inhibitor.get_state() == start_state.istate

    assert sum(game.store) + sum(game.board) == game.cts.total_seeds
