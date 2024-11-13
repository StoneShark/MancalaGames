# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 08:54:42 2024

@author: Ann
"""


# %% imports

import collections

import pytest
pytestmark = pytest.mark.unittest


from context import claimer
from context import game_constants as gc
from context import game_interface as gi
from context import mancala


# %%

TEST_COVERS = ['src\\claimer.py']


# %% some constants

N = None
T = True
F = False

REPEAT_TURN = True
ENDED = True

# %%  test cases


Case = collections.namedtuple('Case',
                              ['board', 'child', 'store', 'results'])
Result = collections.namedtuple('Result',
                                ['board', 'store', 'seeds', 'error'])


TNAMES = ['ClaimSeeds',
          'ChildClaimSeeds',
          'ClaimOwnSeeds',
          'TakeOwnSeeds',
          'TakeOnlyChildNStores',
          'DivvySeedsStores',
          'DivvySeedsChildOnly']


CASES = [
    Case(board=[2, 2, 2, 2, 2, 2, 2, 2],
         child=[None, None, None, None, None, None, None, None],
         store=[0, 0],
         results={'ClaimSeeds': Result(board=[2, 2, 2, 2, 2, 2, 2, 2],
                                       store=[0, 0],
                                       seeds=[0, 0],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[2, 2, 2, 2, 2, 2, 2, 2],
                                            store=[0, 0],
                                            seeds=[0, 0],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[2, 2, 2, 2, 2, 2, 2, 2],
                                          store=[0, 0],
                                          seeds=[8, 8],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[0, 0, 0, 0, 0, 0, 0, 0],
                                         store=[8, 8],
                                         seeds=[8, 8],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[0, 0, 0, 0, 0, 0, 0, 0],
                                                 store=[0, 0],
                                                 seeds=[0, 0],
                                                 error=True),
                  'DivvySeedsStores': Result(board=[0, 0, 0, 0, 0, 0, 0, 0],
                                             store=[8, 8],
                                             seeds=[8, 8],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[0, 0, 0, 0, 0, 0, 0, 0],
                                                store=[0, 0],
                                                seeds=[8, 8],
                                                error=True)}),

    Case(board=[2, 0, 2, 1, 2, 0, 2, 2],
         child=[None, None, False, None, None, None, True, None],
         store=[4, 1],
         results={'ClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 2],
                                       store=[4, 1],
                                       seeds=[4, 1],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 2],
                                            store=[4, 1],
                                            seeds=[6, 3],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 2],
                                          store=[4, 1],
                                          seeds=[9, 7],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[0, 0, 2, 0, 0, 0, 2, 0],
                                         store=[7, 5],
                                         seeds=[9, 7],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[0, 0, 2, 0, 0, 0, 2, 0],
                                                 store=[4, 1],
                                                 seeds=[6, 3],
                                                 error=True),
                  'DivvySeedsStores': Result(board=[0, 0, 2, 0, 0, 0, 2, 0],
                                             store=[7, 5],
                                             seeds=[9, 7],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[0, 0, 5, 0, 0, 0, 6, 0],
                                                store=[4, 1],
                                                seeds=[5, 6],
                                                error=False)}),

    Case(board=[2, 0, 2, 1, 2, 0, 2, 1],
         child=[None, None, False, None, None, None, True, None],
         store=[4, 2],
         results={'ClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                       store=[4, 2],
                                       seeds=[4, 2],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                            store=[4, 2],
                                            seeds=[6, 4],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                          store=[4, 2],
                                          seeds=[9, 7],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[0, 0, 2, 0, 0, 0, 2, 0],
                                         store=[7, 5],
                                         seeds=[9, 7],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[0, 0, 2, 0, 0, 0, 2, 0],
                                                 store=[4, 2],
                                                 seeds=[6, 4],
                                                 error=True),
                  'DivvySeedsStores': Result(board=[0, 0, 2, 0, 0, 0, 2, 0],
                                             store=[7, 5],
                                             seeds=[9, 7],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[0, 0, 5, 0, 0, 0, 5, 0],
                                                store=[4, 2],
                                                seeds=[5, 5],
                                                error=False)}),

    Case(board=[1, 2, 0, 2, 1, 2, 0, 2],
         child=[None, True, None, None, None, False, None, None],
         store=[2, 4],
         results={'ClaimSeeds': Result(board=[1, 2, 0, 2, 1, 2, 0, 2],
                                       store=[2, 4],
                                       seeds=[2, 4],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[1, 2, 0, 2, 1, 2, 0, 2],
                                            store=[2, 4],
                                            seeds=[4, 6],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[1, 2, 0, 2, 1, 2, 0, 2],
                                          store=[2, 4],
                                          seeds=[7, 9],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[0, 2, 0, 0, 0, 2, 0, 0],
                                         store=[5, 7],
                                         seeds=[7, 9],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[0, 2, 0, 0, 0, 2, 0, 0],
                                                 store=[2, 4],
                                                 seeds=[4, 6],
                                                 error=True),
                  'DivvySeedsStores': Result(board=[0, 2, 0, 0, 0, 2, 0, 0],
                                             store=[5, 7],
                                             seeds=[7, 9],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[0, 5, 0, 0, 0, 5, 0, 0],
                                                store=[2, 4],
                                                seeds=[5, 5],
                                                error=False)}),

    Case(board=[2, 0, 2, 1, 2, 0, 2, 1],
         child=[None, None, None, None, None, None, True, None],
         store=[4, 2],
         results={'ClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                       store=[4, 2],
                                       seeds=[4, 2],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                            store=[4, 2],
                                            seeds=[4, 4],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                          store=[4, 2],
                                          seeds=[9, 7],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[0, 0, 0, 0, 0, 0, 2, 0],
                                         store=[9, 5],
                                         seeds=[9, 7],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[0, 0, 0, 0, 0, 0, 2, 0],
                                                 store=[4, 2],
                                                 seeds=[4, 4],
                                                 error=True),
                  'DivvySeedsStores': Result(board=[0, 0, 0, 0, 0, 0, 2, 0],
                                             store=[8, 6],
                                             seeds=[8, 8],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[0, 0, 0, 0, 0, 0, 10, 0],
                                                store=[4, 2],
                                                seeds=[0, 10],
                                                error=False)}),

    Case(board=[2, 0, 2, 1, 2, 0, 2, 1],
         child=[None, None, False, None, None, None, None, None],
         store=[4, 2],
         results={'ClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                       store=[4, 2],
                                       seeds=[4, 2],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                            store=[4, 2],
                                            seeds=[6, 2],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[2, 0, 2, 1, 2, 0, 2, 1],
                                          store=[4, 2],
                                          seeds=[9, 7],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[0, 0, 2, 0, 0, 0, 0, 0],
                                         store=[7, 7],
                                         seeds=[9, 7],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[0, 0, 2, 0, 0, 0, 0, 0],
                                                 store=[4, 2],
                                                 seeds=[6, 2],
                                                 error=True),
                  'DivvySeedsStores': Result(board=[0, 0, 2, 0, 0, 0, 0, 0],
                                             store=[8, 6],
                                             seeds=[10, 6],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[0, 0, 10, 0, 0, 0, 0, 0],
                                                store=[4, 2],
                                                seeds=[10, 0],
                                                error=False)}),

    Case(board=[1, 2, 0, 2, 0, 3, 0, 0],
         child=[None, False, None, None, None, True, None, None],
         store=[2, 6],
         results={'ClaimSeeds': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                       store=[2, 6],
                                       seeds=[2, 6],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                            store=[2, 6],
                                            seeds=[4, 9],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                          store=[2, 6],
                                          seeds=[7, 9],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[0, 2, 0, 0, 0, 3, 0, 0],
                                         store=[5, 6],
                                         seeds=[7, 9],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[0, 2, 0, 0, 0, 3, 0, 0],
                                                 store=[2, 6],
                                                 seeds=[4, 9],
                                                 error=True),
                  'DivvySeedsStores': Result(board=[0, 2, 0, 0, 0, 3, 0, 0],
                                             store=[4, 7],
                                             seeds=[6, 10],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[0, 4, 0, 0, 0, 4, 0, 0],
                                                store=[2, 6],
                                                seeds=[4, 4],
                                                error=False)}),

    Case(board=[1, 2, 0, 2, 0, 3, 0, 0],
         child=[False, False, None, False, None, True, None, None],
         store=[2, 6],
         results={'ClaimSeeds': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                       store=[2, 6],
                                       seeds=[2, 6],
                                       error=False),
                  'ChildClaimSeeds': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                            store=[2, 6],
                                            seeds=[7, 9],
                                            error=False),
                  'ClaimOwnSeeds': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                          store=[2, 6],
                                          seeds=[7, 9],
                                          error=False),
                  'TakeOwnSeeds': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                         store=[2, 6],
                                         seeds=[7, 9],
                                         error=False),
                  'TakeOnlyChildNStores': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                                 store=[2, 6],
                                                 seeds=[7, 9],
                                                 error=False),
                  'DivvySeedsStores': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                             store=[2, 6],
                                             seeds=[7, 9],
                                             error=False),
                  'DivvySeedsChildOnly': Result(board=[1, 2, 0, 2, 0, 3, 0, 0],
                                                store=[2, 6],
                                                seeds=[5, 3],
                                                error=False)}),

    ]

# %%


# TODO Territory claiming isn't really tested


class TestClaimers:

    @pytest.fixture(params=[gi.Goal.MAX_SEEDS, gi.Goal.TERRITORY])
    def game(self, request):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                goal=request.param,
                                goal_param=8,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('tname', TNAMES)
    @pytest.mark.parametrize('case', CASES)
    def test_claimer(self, game, tname, case):

        game.board = case.board.copy()
        game.child = case.child.copy()
        game.store = case.store.copy()

        assert sum(game.board) + sum(game.store) == game.cts.total_seeds, \
            "Game setup error."

        tclass = getattr(claimer, tname)
        sclaimer = tclass(game)
        seeds = sclaimer.claim_seeds()

        assert game.board == case.results[tname].board
        assert game.store == case.results[tname].store
        assert seeds == case.results[tname].seeds
        if case.results[tname].error:
            assert sum(game.board) + sum(game.store) != game.cts.total_seeds
        else:
            assert sum(game.board) + sum(game.store) == game.cts.total_seeds
