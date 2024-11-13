# -*- coding: utf-8 -*-
"""Test the allowables.py file.

Created on Sat Jul 15 14:25:17 2023
@author: Ann"""


# %%   imports

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import AllowRule
from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import LapSower

# %%

TEST_COVERS = ['src\\allowables.py']


# %%   constants

HOLES = 3

FALSES = [False] * (HOLES * 2)
NONES = [None] * (HOLES * 2)

T = True
F = False
N = None


# %%

@pytest.mark.filterwarnings("ignore")
class TestAllowables:

    TEST_ALLOW_DATA = [
        (True,  utils.build_board([2, 2, 2], [0, 0, 0]),   # 0
         FALSES, NONES, False, 2, [T, T, T]),
        (True,  utils.build_board([1, 2, 3], [0, 0, 0]),   # 1
         FALSES, NONES, False, 2, [F, T, T]),
        (False, utils.build_board([0, 0, 0], [1, 1, 1]),   # 2
         FALSES, NONES, False, 1,            [T, T, T]),
        (False, utils.build_board([0, 0, 0], [1, 2, 3]),   # 3
          FALSES, NONES, False, 2,           [F, T, T]),

        (True, utils.build_board([2, 2, 0], [1, 0, 0]),    # 4
         FALSES, NONES, True, 1, [T, T, F]),
        (False, utils.build_board([1, 0, 0], [2, 2, 0]),   # 5
         FALSES, NONES, True, 1,             [T, T, F]),
        (True, utils.build_board([8, 1, 0], [0, 0, 0]),    # 6
         FALSES, NONES, True, 1, [T, F, F]),
        (False, utils.build_board([0, 0, 0], [0, 1, 3]),   # 7
         FALSES, NONES, True, 1,             [F, F, T]),

        (True,                                             # 8
         utils.build_board([2, 2, 0], [1, 0, 0]),
         utils.build_board([T, F, T], [T, F, T]), NONES, True, 1,
                           [F, T, F]),
        (True,                                             # 9
         utils.build_board([2, 2, 2], [1, 0, 0]),
         utils.build_board([T, F, F], [T, F, T]),
         utils.build_board([N, T, N], [N, F, T]), True, 1,
                           [F, F, T]),
        (True,                                             # 10
         utils.build_board([2, 2, 0], [1, 0, 0]),
         utils.build_board([F, T, F], [T, F, T]),
         utils.build_board([N, T, N], [N, F, T]), True, 1,
                           [T, F, F]),

        # opp has seeds, skip mustshare move simul, even though
        # not all playable
        (True, utils.build_board([2, 2, 0], [1, 0, 0]),    # 11
          FALSES, NONES, True, 2, [T, T, F]),

        ]

    @pytest.mark.parametrize(
        'turn, board, blocked, child, mustshare, min_move, eresult',
        TEST_ALLOW_DATA,
        ids=[f'case_{cnt}' for cnt in range(len(TEST_ALLOW_DATA))])
    def test_allowables(self, turn, board, blocked, child,
                        mustshare, min_move, eresult, request):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                min_move=min_move,
                                mustshare=mustshare,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board.copy()
        game.blocked = blocked.copy()
        game.child = child.copy()

        seeds = game.cts.total_seeds - sum(game.board)
        quot, rem = divmod(seeds, 2)
        game.store = [quot, quot + rem]

        assert game.deco.allow.get_allowable_holes() == eresult


    @pytest.mark.parametrize(
        'turn, board, blocked, child, mustshare, min_move, eresult',
        TEST_ALLOW_DATA,
        ids=[f'case_{cnt}' for cnt in range(len(TEST_ALLOW_DATA))])
    def test_ml3_allowables(self, turn, board, blocked, child,
                            mustshare, min_move, eresult):
        """Use the same test data for move triples, but only check
        the 3 (of 6) elements from the results against the expected
        results."""

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                goal=2,
                                goal_param=6,
                                stores=True,
                                min_move=min_move,
                                mustshare=mustshare,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board.copy()
        game.blocked = blocked.copy()
        game.child = child.copy()

        seeds = game.cts.total_seeds - sum(game.board)
        quot, rem = divmod(seeds, 2)
        game.store = [quot, quot + rem]

        res = game.deco.allow.get_allowable_holes()
        if turn:
            assert res[:3] == [F, F, F]
            assert (res[3:])[::-1] == eresult
        else:
            assert res[3:] == [F, F, F]
            assert res[:3] == eresult


    TEST_NOGS_DATA = \
        [
            # GS doesn't do anything,  no opp seeds
            (True,  utils.build_board([2, 2, 2], [0, 0, 0]),
             NONES, False, 1, [T, T, T]),
            (False,  utils.build_board([0, 0, 0], [2, 2, 2]),
             NONES, False, 1, [T, T, T]),

            # GS doesn't do anything,  no opp seeds outside children
            (True,  utils.build_board([2, 2, 2], [2, 0, 0]),
                    utils.build_board([F, N, N], [T, N, N]),
                    False, 1, [F, T, T]),
            (False, utils.build_board([2, 0, 0], [2, 2, 2]),
                    utils.build_board([F, N, N], [T, N, N]),
                    False, 1, [F, T, T]),

            # GS doesn't do anything, no captures
            (True,  utils.build_board([2, 2, 2], [2, 2, 2]),
             NONES, False, 1, [T, T, T]),
            (False,  utils.build_board([2, 2, 2], [2, 2, 2]),
             NONES, False, 1, [T, T, T]),

            # GS doesn't do anything, captures & not all allowable before GS
            (False,  utils.build_board([2, 2, 2], [2, 1, 1]),
             NONES, False, 2, [T, F, F]),
            (True,  utils.build_board([2, 1, 1], [2, 2, 2]),
             NONES, False, 2, [T, F, F]),

            # GS prevented
            (True, utils.build_board([2, 2, 0], [1, 0, 0]),
             NONES, False, 1, [T, F, F]),
            (False,  utils.build_board([0, 0, 1], [0, 2, 2]),
             NONES, False, 1, [F, F, T]),

            # GS prevented, with child
            (True, utils.build_board([2, 2, 0], [1, 1, 0]),
                   utils.build_board([N, N, N], [T, N, N]),
                   False, 1,         [F, T, F]),
            (False,  utils.build_board([0, 1, 1], [0, 2, 2]),
                     utils.build_board([N, N, T], [N, N, N]),
                    False, 1,                     [F, T, F]),

        ]

    @pytest.mark.parametrize(
        'turn, board, child, mustshare, min_move, eresult',
        TEST_NOGS_DATA,
        ids=[f'case_{cnt}' for cnt in range(len(TEST_NOGS_DATA))])
    def test_nograndslam(self, turn, board, child, mustshare, min_move,
                         eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                min_move=min_move,
                                mustshare=mustshare,
                                grandslam=GrandSlam.NOT_LEGAL,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board
        game.child = child

        seeds = game.cts.total_seeds - sum(game.board)
        quot, rem = divmod(seeds, 2)
        game.store = [quot, quot + rem]

        assert game.deco.allow.get_allowable_holes() == eresult


    def test_mlap_allowables(self):
        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                crosscapt=True,
                                grandslam=GrandSlam.NOT_LEGAL,
                                mlaps=LapSower.LAPPER,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = True
        game.board = utils.build_board([1, 3, 1],
                                       [0, 1, 0])

        seeds = game.cts.total_seeds - sum(game.board)
        quot, rem = divmod(seeds, 2)
        game.store = [quot, quot + rem]

        assert game.deco.allow.get_allowable_holes() == [T, T, T]


    def test_sown_n_capt(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[1, 2],
                                multicapt=True,
                                mustshare=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        game.turn = True
        game.board = utils.build_board([2, 0, 20],
                                       [0, 0, 0])
        game.store[0] = game.cts.total_seeds - sum(game.board)

        assert game.deco.allow.get_allowable_holes() == [F, F, T]


class TestMemoize:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                stores=True,
                                capt_on=[2],
                                mustshare=True,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_memoize_avail(self, game):

        game.turn = False
        game.board = utils.build_board([1, 0, 0],
                                       [2, 2, 0])

        assert game.deco.allow.get_allowable_holes() == [T, T, F]

        # assure the rest of the chain cannot be used
        game.deco.allow.decorator = None
        assert game.deco.allow.get_allowable_holes() == [T, T, F]


    def test_memoize_not_avail(self, game):

        game.turn = False
        game.board = utils.build_board([1, 0, 0],
                                       [2, 2, 0])

        assert game.deco.allow.get_allowable_holes() == [T, T, F]
        game.turn = True

        # assure the rest of the chain cannot be used
        game.deco.allow.decorator = None

        with pytest.raises(AttributeError):
            game.deco.allow.get_allowable_holes()


class TestNoSidesAllow:

    TEST_DATA = \
        [([2, 2, 2, 0, 0, 0],   # 0
          FALSES, NONES, 2,
          [T, T, T, F, F, F]),

         ([1, 2, 3, 0, 0, 0],   # 1
          FALSES, NONES, 2,
          [F, T, T, F, F, F]),

         ([0, 0, 0, 1, 1, 1],   # 2
          FALSES, NONES, 1,
          [F, F, F, T, T, T]),

         ([2, 2, 0, 1, 0, 0],    # 3
          FALSES, NONES, 2,
          [T, T, F, F, F, F]),

         ([2, 2, 0, 1, 0, 0],
          [T, F, T, T, F, T], NONES, 2,
          [F, T, F, F, F, F]),

         ([2, 2, 2, 1, 0, 0],
          [T, F, F, T, F, T],
          [N, T, N, N, F, T], 2,
          [F, F, T, F, F, F]),

         ([2, 2, 0, 1, 0, 0],
          [F, T, F, T, F, T],
          [N, T, N, N, F, T], 2,
          [T, F, F, F, F, F]),
         ]

    @pytest.mark.parametrize('turn', [False, True])
    @pytest.mark.parametrize(
        'board, blocked, child, min_move, eresult',
        TEST_DATA)
    def test_allowables(self, turn, board, blocked, child, min_move, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                no_sides=True,
                                stores=True,
                                min_move=min_move,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board
        game.blocked = blocked
        game.child = child

        assert game.deco.allow.get_allowable_holes() == eresult


class TestOppEmpty:

    @pytest.mark.parametrize(
        'board, turn, eresult',
        [([3, 1, 0, 0, 1, 0], False, [T, T, F]),
         ([3, 1, 0, 0, 1, 1], True, [T, F, F]),

        ([4] * 6,  True, [T, T, T]),
        ])
    def test_allowables(self, board, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.OPP_OR_EMPTY,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult


class TestSingleToEmpty:

    TEST_STE_DATA = \
        [(Direct.CCW, [4] * 8,  True, [T, T, T, T]),

         (Direct.CCW, utils.build_board([0, 1, 0, 2],
                                        [3, 1, 0, 2]), False, [T, T, F, T]),
         (Direct.CCW, utils.build_board([0, 1, 2, 2],
                                        [3, 0, 1, 2]), False, [T, F, F, T]),
         (Direct.CCW, utils.build_board([1, 2, 0, 2],
                                        [3, 1, 0, 2]), True, [F, T, F, T]),

         (Direct.CW, utils.build_board([0, 1, 0, 2],
                                       [3, 1, 0, 2]), False, [T, F, F, T]),
         (Direct.CW, utils.build_board([0, 1, 2, 2],
                                       [3, 1, 0, 2]), False, [T, F, F, T]),
         (Direct.CW, utils.build_board([1, 2, 0, 2],
                                       [3, 1, 0, 2]), True, [F, T, F, T]),
         (Direct.CW, utils.build_board([1, 0, 2, 2],
                                       [3, 1, 0, 2]), True, [T, F, T, T]),

         (Direct.SPLIT, utils.build_board([0, 1, 1, 0],
                                          [0, 1, 1, 0]), True, [F, T, T, F]),
         (Direct.SPLIT, utils.build_board([0, 1, 1, 0],
                                          [0, 1, 1, 0]), False, [F, T, T, F]),
         (Direct.SPLIT, utils.build_board([1, 2, 0, 1],
                                          [1, 2, 0, 1]), True, [F, T, F, F]),
         (Direct.SPLIT, utils.build_board([1, 2, 0, 1],
                                          [1, 2, 0, 1]), False, [F, T, F, F]),
        ]

    @pytest.mark.parametrize(
        'direct, board, turn, eresult',
        TEST_STE_DATA,
        ids=[f'case_{cnt}' for cnt in range(len(TEST_STE_DATA))])
    def test_allowables(self, direct, board, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=direct,
                                allow_rule=AllowRule.SINGLE_TO_ZERO,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult


class TestOnlyIfAll:

    @pytest.mark.parametrize(
        'board, turn, eresult',
        [([4] * 8,  True, [T, T, T, T]),

         (utils.build_board([0, 1, 0, 2],
                            [3, 1, 0, 2]), False, [T, F, F, T]),
         (utils.build_board([1, 2, 0, 2],
                            [3, 1, 0, 2]), True, [F, T, F, T]),

         (utils.build_board([0, 1, 1, 0],
                            [0, 1, 1, 0]), True, [F, T, T, F]),
         (utils.build_board([0, 1, 1, 0],
                            [0, 1, 1, 0]), False, [F, T, T, F]),
        ],
        ids=[f'case_{cnt}' for cnt in range(5)])
    def test_1_allowables(self, board, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.SINGLE_ONLY_ALL,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult



class TestOnlyIfAllToZero:

    @pytest.mark.parametrize(
        'board, turn, eresult',
        [([4] * 8,  True, [T, T, T, T]),

         (utils.build_board([0, 1, 0, 2],
                            [3, 1, 0, 2]), False, [T, F, F, T]),
         (utils.build_board([1, 2, 0, 2],
                            [3, 1, 0, 2]), True, [F, T, F, T]),

         (utils.build_board([0, 1, 1, 0],
                            [0, 1, 1, 0]), True, [F, T, F, F]),
         (utils.build_board([0, 1, 1, 0],
                            [0, 1, 1, 0]), False, [F, F, T, F]),

         (utils.build_board([1, 1, 0, 1],
                            [1, 1, 1, 0]), False, [F, F, T, F]),
         (utils.build_board([1, 1, 0, 1],
                            [1, 1, 1, 0]), True, [F, F, F, T]),
        ],
        ids=[f'case_{cnt}' for cnt in range(7)])
    def test_1_allowables(self, board, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.SINGLE_ALL_TO_ZERO,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult



    @pytest.mark.parametrize(
        'board, turn, eresult',
        [([4] * 8,  True, [T, T, T, T]),

         (utils.build_board([0, 1, 0, 2],
                            [3, 1, 0, 2]), False, [T, T, F, F]),
         (utils.build_board([1, 2, 0, 2],
                            [3, 1, 0, 2]), True, [T, F, F, F]),

         (utils.build_board([0, 2, 2, 0],
                            [0, 2, 2, 0]), True, [F, T, T, F]),
         (utils.build_board([0, 2, 2, 0],
                            [0, 2, 2, 0]), False, [F, T, T, F]),
        ],
        ids=[f'case_{cnt}' for cnt in range(5)])
    def test_2_allowables(self, board, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.TWO_ONLY_ALL,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult


class TestTwosRight:

    @pytest.mark.parametrize(
        'board, turn, eresult',
        [([4] * 8,  True, [T, T, T, T]),

         (utils.build_board([0, 1, 0, 2],
                            [3, 1, 0, 2]), False, [T, T, F, F]),
         (utils.build_board([1, 2, 0, 2],
                            [3, 3, 0, 2]), True, [T, F, F, F]),

         (utils.build_board([0, 2, 2, 0],
                            [0, 2, 2, 0]), True, [F, T, F, F]),
         (utils.build_board([2, 2, 0, 0],
                            [0, 2, 2, 0]), True, [T, F, F, F]),
         (utils.build_board([0, 2, 2, 0],
                            [0, 2, 2, 0]), False, [F, F, T, F]),
         (utils.build_board([0, 2, 2, 0],
                            [2, 2, 0, 0]), False, [F, T, F, F]),

         # the game would have ended ... but test it
         (utils.build_board([0, 0, 0, 0],
                            [0, 0, 0, 0]), False, [F, F, F, F]),
         ],
        ids=[f'case_{cnt}' for cnt in range(8)])
    def test_two_right(self, board, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.TWO_ONLY_ALL_RIGHT,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult



class TestOwnerAllowables:

    @pytest.mark.parametrize(
        'turn, board, owners, eresult',
        [
            (True,
             utils.build_board([2, 2, 0],
                               [1, 0, 2]),
             utils.build_board([T, T, T],
                               [F, F, T]),
             utils.build_board([T, T, F],
                               [F, F, T])),

            (True,
             utils.build_board([2, 2, 0],
                               [0, 0, 2]),
             utils.build_board([T, T, T],
                               [F, F, F]),
             utils.build_board([T, T, F],
                               [F, F, F])),

            (False,
              utils.build_board([0, 2, 0],
                                [1, 0, 2]),
              utils.build_board([T, F, T],
                                [F, F, F]),
              utils.build_board([F, T, F],
                                [F, F, T])),
        ],
        ids=[f'case_{cnt}' for cnt in range(3)])
    def test_allowables(self, turn, board, owners, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                goal=Goal.TERRITORY,
                                goal_param=6,
                                mustshare=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board
        game.owner = owners
        seeds = game.cts.total_seeds - sum(game.board)
        quot, rem = divmod(seeds, 2)
        game.store = [quot, quot + rem]

        assert game.deco.allow.get_allowable_holes() == eresult


class TestOnlyRightTwo:

    @pytest.mark.parametrize(
        'board, blocks, move_nbr, turn, eresult',
        [([4] * 8, [F] * 8, 0, True,  [T, T, F, F]),
         ([4] * 8, [F] * 8, 0, False, [F, F, T, T]),

         (utils.build_board([1, 2, 0, 2],
                            [3, 1, 0, 2]), [F] * 8, 1, True, [T, T, F, T]),
         (utils.build_board([0, 1, 0, 2],
                            [3, 1, 0, 2]), [F] * 8, 1, False, [T, T, F, T]),

         ([4] * 8,
          utils.build_board([T, F, F, F],
                            [F, F, F, T]), 0, True, [F, T, T, F]),
         ([4] * 8,
          utils.build_board([T, F, F, F],
                            [F, F, T, T]), 0, False, [T, T, F, F]),

         # Test non contiguous blocks and < 2 allowables
         ([4] * 8,
          utils.build_board([T, F, T, F],
                            [F, F, F, T]), 0, True, [F, T, F, T]),

         ([4] * 8,
          utils.build_board([T, T, F, T],
                            [F, F, F, T]), 0, True, [F, F, T, F]),
        ],
        ids=[f'case_{cnt}' for cnt in range(8)])
    def test_r2_allowables(self, board, blocks, move_nbr, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                stores=True,
                                blocks=True,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board
        game.blocked = blocks
        game.mcount = move_nbr

        assert game.deco.allow.get_allowable_holes() == eresult


    @pytest.mark.parametrize(
        'board, blocks, move_nbr, turn, eresult',
        [([4] * 8, [F] * 8, 0, True,  [T, T, F, F]),
         ([4] * 8, [F] * 8, 0, False, [F, F, T, T]),

         (utils.build_board([1, 2, 0, 2],
                            [3, 1, 0, 2]), [F] * 8, 1, True, [T, F, F, F]),
         (utils.build_board([0, 1, 0, 2],
                            [3, 1, 0, 2]), [F] * 8, 1, False, [T, T, F, F]),

         (utils.build_board([2, 2, 0, 2],
                            [2, 0, 2, 2]), [F] * 8, 1, True, [T, T, F, T]),
         (utils.build_board([0, 2, 0, 2],
                            [2, 0, 0, 2]), [F] * 8, 1, False, [T, F, F, T]),

        ],
        ids=[f'case_{cnt}' for cnt in range(6)])
    def test_r2a2_allowables(self, board, blocks, move_nbr, turn, eresult):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.RIGHT_2_1ST_THEN_ALL_TWO,
                                stores=True,
                                blocks=True,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board
        game.blocked = blocks
        game.mcount = move_nbr

        assert game.deco.allow.get_allowable_holes() == eresult



class TestBadEnums:

    def test_bad_allow_rule(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'allow_rule', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)
