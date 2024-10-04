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

            'gsnone_pick2': {'stores': True,
                             'capt_on': [2, 3],
                             'grandslam': gi.GrandSlam.NO_CAPT,
                             'pickextra': gi.CaptExtraPick.PICKTWOS,
                             },

            'gsnone_pickend': {'stores': True,
                               'capt_on': [2, 3],
                               'grandslam': gi.GrandSlam.NO_CAPT,
                               'pickextra': gi.CaptExtraPick.PICKLASTSEEDS,
                               },

            'gsopp_pickend': {'stores': True,
                               'capt_on': [2, 3],
                               'grandslam': gi.GrandSlam.OPP_GETS_REMAIN,
                               'pickextra': gi.CaptExtraPick.PICKLASTSEEDS,
                               },

            'pickend': {'stores': True,
                               'capt_on': [2, 3],
                               'pickextra': gi.CaptExtraPick.PICKLASTSEEDS,
                               },

            'lock_pick2x': {'stores': True,
                            'moveunlock': True,
                            'capt_on': [2, 3],
                            'pickextra': gi.CaptExtraPick.PICK2XLASTSEEDS,
                            },

            }


# remember the board setup is after the sow has occured!!

START = {'start':
             mancala.GameState(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                               store=(0, 0),
                               mcount=1,    # mcount is inc'ed at top of move
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N)),

        'sow4':
             mancala.GameState(board=(2, 2, 2, 0, 3, 3, 2, 2, 2, 2),
                               store=(0, 0),
                               mcount=1,
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N)),

        'end_capt':
             mancala.GameState(board=(0, 0, 1, 0, 0, 2, 0, 0, 1, 0),
                               store=(0, 16),
                               mcount=20,
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N)),


        'end_capt2':
             mancala.GameState(board=(0, 0, 3, 0, 0, 2, 0, 0, 0, 0),
                               store=(0, 15),
                               mcount=20,
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N)),

        # unlikely that there will be pickable seeds in a locked hole
        'locked':
             mancala.GameState(board=(0, 0, 3, 0, 0, 2, 0, 0, 0, 0),
                               store=(0, 15),
                               mcount=20,
                               _turn=False,
                               child=(N, N, N, N, N, N, N, N, N, N),
                               unlocked=(T, T, F, T, T, T, T, T, T, T)),


        }

CASES = [('basic', 'start', F, 2,
          2, (2, 2, 0, 2, 2, 2, 2, 2, 2, 2), (2, 0), NCHILD, F, T),

         # capture and pick are gs, don't do either
         ('gsnone_pick2', 'sow4', F, 5,
          5, (2, 2, 2, 0, 3, 3, 2, 2, 2, 2), (0, 0), NCHILD, F, F),

         # no gs, game ends via capt and pick -- see next test
         ('pickend', 'end_capt', F, 5,
          5, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (4, 16), NCHILD, T, T),

         # gs None prevents ending game via capt and pick
         ('gsnone_pickend', 'end_capt', F, 5,
          5, (0, 0, 1, 0, 0, 2, 0, 0, 1, 0), (0, 16), NCHILD, F, F),

         # don't pick from locked holes (this is an unlikely game state)
         ('lock_pick2x', 'locked', F, 5,
          5, (0, 0, 3, 0, 0, 0, 0, 0, 0, 0), (2, 15), NCHILD, F, T ),

         # gs opp doesn't restore the state, when gs any of Fs remaining
         # seeds would go to true but F picked them all
         ('gsopp_pickend', 'end_capt', F, 5,
          5, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (4, 16), NCHILD, T, T),

         # same as above but no pick, gs moves 3 remain F seeds to T
         ('gsopp_pickend', 'end_capt2', F, 5,
          5, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (2, 18), NCHILD, F, T),

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
    print(game)

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


# %%

BAD_CONFIGS = {

    'xc_pickextra':
        ({'stores': True,
          'crosscapt': True,
          'pickextra': gi.CaptExtraPick.PICKCROSS,
          },
         UserWarning),

    'even_xc_pickextra':
        ({'stores': True,
          'evens': True,
          'crosscapt': True,
          'pickextra': gi.CaptExtraPick.PICKCROSS,
          },
        gi.GameInfoError),

    'max_xc_pickextra':
        ({'stores': True,
          'capt_max': 4,
          'crosscapt': True,
          'pickextra': gi.CaptExtraPick.PICKCROSS,
          },
        gi.GameInfoError),

    'min_xc_pickextra':
        ({'stores': True,
          'capt_min': 2,
          'crosscapt': True,
          'pickextra': gi.CaptExtraPick.PICKCROSS,
          },
        gi.GameInfoError),

    'on_xc_pickextra':
        ({'stores': True,
          'capt_on': [2, 3],
          'crosscapt': True,
          'pickextra': gi.CaptExtraPick.PICKCROSS,
          },
        gi.GameInfoError),

    }

@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize('config_dict, result',
                         BAD_CONFIGS.values(),
                         ids=BAD_CONFIGS.keys())
def test_bad_config(config_dict, result):
    """ginfo_rules prevents these games so they are not tested.
    if ginfo_rules is changed to allow them,
    report an error so tests are written."""

    with pytest.raises(result):
        gi.GameInfo(**config_dict,
                    nbr_holes=HOLES,
                    rules=mancala.Mancala.rules)
