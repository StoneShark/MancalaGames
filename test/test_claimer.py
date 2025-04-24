# -*- coding: utf-8 -*-
"""Test the claimers.

Created on Mon Nov 11 08:54:42 2024
@author: Ann"""


# %% imports

import pytest
pytestmark = pytest.mark.unittest


from context import claimer
from context import game_constants as gconsts
from context import game_interface as gi
from context import mancala
from context import move_data

import utils


# %%

TEST_COVERS = ['src\\claimer.py']


# %% constants

N = None
T = True
F = False

NO_CHANGE = -4
BRD_ZEROS = [0, 0, 0, 0, 0, 0, 0, 0]


# %%  tests


GAMECONF = {
    'basic':
        {'evens': True,
         'stores': True},   # avoid the capt warnings

    'children':
        {'evens': True,
         'stores': True,
         'child_type': gi.ChildType.NORMAL,
         'child_cvt': 4},

    'territory':
        {'evens': True,
         'stores': True,
         'goal': gi.Goal.TERRITORY,
         'goal_param': 6,
         'child_type': gi.ChildType.NORMAL,
         'child_cvt': 4},

    'child_lmover':
        {'evens': True,
         'stores': True,
         'child_type': gi.ChildType.NORMAL,
         'child_cvt': 4,
         'unclaimed': gi.EndGameSeeds.LAST_MOVER},

    'child_ms_unfed':
        {'evens': True,
         'stores': True,
         'child_type': gi.ChildType.NORMAL,
         'child_cvt': 4,
         'mustshare': True,
         'unclaimed': gi.EndGameSeeds.UNFED_PLAYER},
        }


STATE = {'start':
             utils.make_state(board=(2, 2, 2, 2, 2, 2, 2, 2),
                              store=(0, 0)),

        'child_fgr':
            utils.make_state(board=(2, 0, 2, 1, 2, 0, 2, 2),
                             child=(N, N, F, N, N, N, T, N),
                             store=(4, 1)),

        'child_tgr':
            utils.make_state(board=(2, 0, 2, 2, 2, 0, 4, 1),
                             child=(N, N, F, N, N, N, T, N),
                             store=(2, 1)),

        'childT':
            utils.make_state(board=(2, 0, 2, 1, 2, 0, 2, 2),
                             child=(N, N, N, N, N, N, T, N),
                             store=(4, 1)),

        'childF':
            utils.make_state(board=(2, 0, 2, 1, 2, 0, 2, 2),
                             child=(N, N, F, N, N, N, N, N),
                             store=(4, 1)),

        'child_all':
            utils.make_state(board=(0, 0, 9, 0, 0, 0, 0, 7),
                             child=(N, N, F, N, N, N, N, T),
                             store=(0, 0)),

        'owners':
            utils.make_state(board=(2, 0, 2, 1, 2, 0, 2, 2),
                             owner=(T, F, T, F, T, T, F, F),
                             store=(4, 1)),

        'own_wchild':
            utils.make_state(board=(2, 0, 2, 1, 2, 0, 2, 2),
                             owner=(T, F, T, F, T, T, F, F),
                             child=(N, N, T, N, N, N, F, N),
                             store=(4, 1)),

        'ended':
             utils.make_state(board=(0, 0, 0, 0, 0, 0, 0, 0),
                              store=(10, 6)),

        'odd_uncl_fgr':
            utils.make_state(board=(2, 0, 2, 1, 2, 0, 2, 2),
                             store=(4, 1)),

        'odd_uncl_tgr':
            utils.make_state(board=(2, 0, 2, 1, 2, 0, 2, 2),
                             store=(1, 4),
                             turn=True),

         }


CASES = [
    ('basic', 'start', 'ClaimSeeds',
     [0, 0], NO_CHANGE, NO_CHANGE, F),

    ('basic', 'child_fgr', 'ClaimSeeds',
     [4, 1], NO_CHANGE, NO_CHANGE, F),


    ('basic', 'start', 'ChildClaimSeeds',
     [0, 0], NO_CHANGE, NO_CHANGE, F),

    ('children', 'child_fgr', 'ChildClaimSeeds',
     [6, 3], NO_CHANGE, NO_CHANGE, F),


    ('basic', 'start', 'ClaimOwnSeeds',
     [8, 8], NO_CHANGE, NO_CHANGE, F),

    ('children', 'child_fgr', 'ClaimOwnSeeds',
     [9, 7], NO_CHANGE, NO_CHANGE, F),

    ('territory', 'child_fgr', 'ClaimOwnSeeds',
     [9, 7], NO_CHANGE, NO_CHANGE, F),

    ('territory', 'owners', 'ClaimOwnSeeds',
     [9, 7], NO_CHANGE, NO_CHANGE, F),


    # TakeOwnSeeds - take seeds by owner (side or owner), don't move child seeds
    ('basic', 'start', 'TakeOwnSeeds',
     [8, 8], BRD_ZEROS, [8, 8], F),

    ('children', 'child_fgr', 'TakeOwnSeeds',
     [9, 7], [0, 0, 2, 0, 0, 0, 2, 0], [7, 5], F),

    ('territory', 'owners', 'TakeOwnSeeds',
     [9, 7], BRD_ZEROS, [9, 7], F),

    ('territory', 'ended', 'TakeOwnSeeds',
     [10, 6], NO_CHANGE, NO_CHANGE, F),

    ('territory', 'own_wchild', 'TakeOwnSeeds',
     [9, 7], [0, 0, 2, 0, 0, 0, 2, 0], [7, 5], F),


    # TakeOnlyChildNStore
    # removes unclaimed seeds from the board, they are not put into the stores
    ('basic', 'start', 'TakeOnlyChildNStores',
     [0, 0], BRD_ZEROS, NO_CHANGE, T),

    ('children', 'child_fgr', 'TakeOnlyChildNStores',
     [6, 3], [0, 0, 2, 0, 0, 0, 2, 0], NO_CHANGE, T),

    ('territory', 'owners', 'TakeOnlyChildNStores',
     [4, 1], BRD_ZEROS, NO_CHANGE, T),

    ('territory', 'ended', 'TakeOnlyChildNStores',
     [10, 6], NO_CHANGE, NO_CHANGE, F),     # no seeds are removed from play

    ('territory', 'own_wchild', 'TakeOnlyChildNStores',
     [6, 3], [0, 0, 2, 0, 0, 0, 2, 0], NO_CHANGE, T),


    # TakeAllUnclaimed requires unclaimed to be one of LAST_MOVER or UNFED_PLAYER
    # turn and last_mover are the same for all these tests, see test_collector
    ('child_lmover', 'odd_uncl_fgr', 'TakeAllUnclaimed',
     [15, 1], BRD_ZEROS, [15, 1], F),            # last_mover is F

    ('child_lmover', 'odd_uncl_tgr', 'TakeAllUnclaimed',
     [1, 15], BRD_ZEROS, [1, 15], F),             # last_mover is T

    ('child_lmover', 'child_fgr', 'TakeAllUnclaimed',
     [13, 3], [0, 0, 2, 0, 0, 0, 2, 0], [11, 1], F),     # last_mover is F

    ('child_ms_unfed', 'odd_uncl_fgr', 'TakeAllUnclaimed',
     [15, 1], BRD_ZEROS, [15, 1], F),

    ('child_ms_unfed', 'odd_uncl_tgr', 'TakeAllUnclaimed',
     [1, 15], BRD_ZEROS, [1, 15], F),

    ('child_ms_unfed', 'child_fgr', 'TakeAllUnclaimed',
     [13, 3], [0, 0, 2, 0, 0, 0, 2, 0], [11, 1], F),


    # DivvySeedsStores
    # assumption for divvier is that unclaimed seeds could belong to either player
    ('basic', 'start', 'DivvySeedsStores',
     [8, 8], BRD_ZEROS, [8, 8], F),

    ('basic', 'ended', 'DivvySeedsStores',  # no unclaimed seeds
     [10, 6], BRD_ZEROS, [10, 6], F),

    ('basic', 'odd_uncl_tgr', 'DivvySeedsStores',
     [7, 9], BRD_ZEROS, [7, 9], F),

    ('basic', 'odd_uncl_fgr', 'DivvySeedsStores',
     [9, 7], BRD_ZEROS, [9, 7], F),

    ('children', 'child_fgr', 'DivvySeedsStores',
     [9, 7], [0, 0, 2, 0, 0, 0, 2, 0], [7, 5], F),


    # DivvySeedsChildOnly
    # there wouldn't normally be any seeds in the stores, they are ignored
    ('basic', 'start', 'DivvySeedsChildOnly',
     [8, 8], BRD_ZEROS, NO_CHANGE, T),

    ('basic', 'ended', 'DivvySeedsChildOnly',  # no unclaimed seeds, no children TIE
     [8, 8], BRD_ZEROS, NO_CHANGE, F),

    ('children', 'child_all', 'DivvySeedsChildOnly',
     [9, 7], NO_CHANGE, NO_CHANGE, F),

    ('children', 'child_fgr', 'DivvySeedsChildOnly',
     [5, 6], [0, 0, 5, 0, 0, 0, 6, 0], NO_CHANGE, F),

    ('children', 'child_tgr', 'DivvySeedsChildOnly',
     [6, 7], [0, 0, 6, 0, 0, 0, 7, 0], NO_CHANGE, F),

    ('children', 'childT', 'DivvySeedsChildOnly',
     [0, 11], [0, 0, 0, 0, 0, 0, 11, 0], NO_CHANGE, F),

    ('children', 'childF', 'DivvySeedsChildOnly',
     [11, 0], [0, 0, 11, 0, 0, 0, 0, 0], NO_CHANGE, F),

    ]

CIDS = [f'{case[0]}-{case[1]}-{case[2]}-{idx}' for idx, case in enumerate(CASES)]

# @pytest.mark.usefixtures('logger')
@pytest.mark.parametrize('conf_name, state_name, sclaimer,'
                         'eseeds, eboard, estore, eloss',
                         CASES, ids=CIDS)
def test_claimer(conf_name, state_name, sclaimer,
                 eseeds, eboard, estore, eloss):
    """Test the specified game configuration with state applied,
    for the claimer. Note the claimer might/might not be
    used anywhere in the game."""

    game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
    game_info = gi.GameInfo(**GAMECONF[conf_name],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game =  mancala.Mancala(game_consts, game_info)

    gstate = STATE[state_name]
    game.state = gstate

    # make_state sets the game.turn to False
    # it can be overridden in the state, so don't make mdata until state is set
    # mdata.turn is used in TakeAllUnclaimed
    game.mdata = move_data.MoveData(game, None)

    # print(GAMECONF[conf_name])
    # print(game)

    tclass = getattr(claimer, sclaimer)
    sclaimer = tclass(game)
    seeds = sclaimer.claim_seeds()
    # print(seeds)
    # print(game)

    assert seeds == eseeds
    if eboard == NO_CHANGE:
        assert game.board == list(gstate.board)
    else:
        assert game.board == eboard
    if estore == NO_CHANGE:
        assert game.store == list(gstate.store)
    else:
        assert game.store == estore

    # some claimer take seeds off the board
    if eloss:
        assert sum(game.board) + sum(game.store) != game.cts.total_seeds
    else:
        assert sum(game.board) + sum(game.store) == game.cts.total_seeds


@pytest.mark.parametrize ('conf_name', ['child_lmover', 'child_ms_unfed'])
@pytest.mark.parametrize ('last_mover', [False, True])
@pytest.mark.parametrize ('unfed', [False, True])
def test_collector(conf_name, last_mover, unfed):
    """Test the combinations of last_mover and unfed/turn to make
    certain that the right collector is used."""

    game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
    game_info = gi.GameInfo(**GAMECONF[conf_name],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game =  mancala.Mancala(game_consts, game_info)

    gstate = STATE['child_fgr']
    game.state = gstate
    game.turn = unfed

    game.mdata = move_data.MoveData(game, None)
    game.mdata.last_mover = last_mover

    sclaimer = claimer.TakeAllUnclaimed(game)

    if conf_name == 'last_mover':
        assert sclaimer.collector(game) == last_mover
    elif conf_name == 'unfed':
        assert sclaimer.collector(game) == unfed


def test_unkn_collector():
    """Test the unknown collector error.
    Can't be reached in the GameInfo contructor."""

    game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
    game_info = gi.GameInfo(evens=True,
                            stores=True,
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    game =  mancala.Mancala(game_consts, game_info)

    with pytest.raises(gi.GameInfoError) as error:
        claimer.TakeAllUnclaimed(game)

    assert 'collector' in str(error)
