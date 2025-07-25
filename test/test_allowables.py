# -*- coding: utf-8 -*-
"""Test the allowables.py file.

Created on Sat Jul 15 14:25:17 2023
@author: Ann"""


# %%   imports

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import allowables
from context import animator
from context import game_classes
from context import game_constants as gconsts
from context import game_info as gi
from context import mancala

from game_info import AllowRule
from game_info import Direct
from game_info import Goal
from game_info import GrandSlam
from game_info import LapSower

# %%

TEST_COVERS = ['src\\allowables.py']


# %%   constants

HOLES = 3

FALSES = [False] * (HOLES * 2)
NONES = [None] * (HOLES * 2)

T = True
F = False
N = None

CW = Direct.CW
CCW = Direct.CCW


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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                goal=Goal.TERRITORY,
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
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
        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[1, 2],
                                multicapt=-1,
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.OPP_OR_EMPTY,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = board

        assert game.deco.allow.get_allowable_holes() == eresult


class TestOccupied:

    @pytest.mark.parametrize(
        'board, turn, eresult',
        [([1, 2, 0, 0, 1, 0], False, [T, F, F]),
         ([3, 1, 0, 1, 0, 1], True, [T, F, F]),

        ([4] * 6,  True, [T, T, T]),
        ])
    def test_allowables(self, board, turn, eresult):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                allow_rule=AllowRule.OCCUPIED,
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
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
        game.movers = move_nbr

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

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
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
        game.movers = move_nbr

        assert game.deco.allow.get_allowable_holes() == eresult


def reverse(lst):

    lst.reverse()
    return lst


class TestMoveAllFirst:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                allow_rule=AllowRule.MOVE_ALL_HOLES_FIRST,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    HCASES = [
        #start state
        ['start',
         utils.make_state(board=(4, 4, 4, 4, 4, 4, 4, 4),
                          store=[0, 0],
                          unlocked=(F, F, F, F, F, F, F, F),
                         ),
         [T, T, T, T], [T, T, T, T]],

        ['moves2',
         utils.make_state(board=(3, 4, 6, 4, 2, 1, 5, 4),
                          store=[0, 0],
                          unlocked=(F, T, F, F, F, F, F, T),
                         ),
         [T, F, T, T], reverse([T, T, T, F])],

        ['all',
         utils.make_state(board=(3, 4, 6, 4, 2, 1, 5, 4),
                          store=[0, 0],
                          unlocked=(T, T, T, T, T, T, T, T),
                         ),
         [T, T, T, T], [T, T, T, T]],

        ]

    @pytest.mark.parametrize('state, efresult, etresult',
                             [case[1:] for case in HCASES],
                             ids=[case[0] for case in HCASES])
    def test_maf_half(self, game, state, efresult, etresult):

        game.state = state
        game.turn = True
        assert game.deco.allow.get_allowable_holes() == etresult

        game.turn = False
        assert game.deco.allow.get_allowable_holes() == efresult


    @pytest.fixture
    def fgame(self):
        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                goal=Goal.TERRITORY,
                                goal_param=6,
                                rounds=gi.Rounds.NO_MOVES,
                                allow_rule=AllowRule.MOVE_ALL_HOLES_FIRST,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    FCASES = [
        ['start',
         utils.make_state(board=(4, 4, 4, 4, 4, 4, 4, 4),
                          store=[0, 0],
                          unlocked=(F, F, F, F, F, F, F, F),
                          owner=(F, F, F, F, T, T, T, T),
                         ),
         [T, T, T, T, F, F, F, F],
         [F, F, F, F, T, T, T, T]],

        ['moves2',
         utils.make_state(board=(3, 4, 6, 4, 2, 1, 5, 4),
                          store=[0, 0],
                          unlocked=(F, T, F, F, F, F, F, T),
                          owner=(F, F, F, F, T, T, T, T),
                         ),
         [T, F, T, T, F, F, F, F],
         [F, F, F, F, T, T, T, F]],

        ['all',
         utils.make_state(board=(3, 4, 6, 4, 2, 1, 5, 4),
                          store=[0, 0],
                          unlocked=(T, T, T, T, T, T, T, T),
                          owner=(F, F, F, F, T, T, T, T),
                        ),
         [T, T, T, T, F, F, F, F],
         [F, F, F, F, T, T, T, T]],

        ['start_own',
         utils.make_state(board=(4, 4, 4, 4, 4, 4, 4, 4),
                          store=[0, 0],
                          unlocked=(F, F, F, F, F, F, F, F),
                          owner=(F, F, T, T, T, T, T, F),
                         ),
         [T, T, F, F, F, F, F, T],
         [F, F, T, T, T, T, T, F]],

        ['moves2_own',
         utils.make_state(board=(3, 4, 6, 4, 2, 1, 5, 4),
                          store=[0, 0],
                          unlocked=(F, T, F, F, F, F, T, F),
                          owner=   (F, F, T, T, T, T, T, F),
                         ),
         [T, F, F, F, F, F, F, T],
         [F, F, T, T, T, T, F, F]],

        ['all_own',
         utils.make_state(board=(3, 4, 6, 4, 2, 1, 5, 4),
                          store=[0, 0],
                          unlocked=(T, T, T, T, T, T, T, T),
                          owner=(F, F, T, T, T, T, T, F),
                        ),
         [T, T, F, F, F, F, F, T],
         [F, F, T, T, T, T, T, F]],
        ]

    @pytest.mark.parametrize('state, efresult, etresult',
                             [case[1:] for case in FCASES],
                             ids=[case[0] for case in FCASES])
    def test_maf_full(self, fgame, state, efresult, etresult):

        fgame.state = state
        fgame.turn = True
        # print(fgame)
        assert fgame.deco.allow.get_allowable_holes() == etresult

        fgame.turn = False
        # print(fgame)
        assert fgame.deco.allow.get_allowable_holes() == efresult


class TestNotXFrom1:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                allow_rule=AllowRule.NOT_XFROM_1S,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)

    CASES = [
         ['start',
          utils.make_state(board=(4, 4, 4, 4, 4, 4, 4, 4),
                           store=[0, 0],
                          ),
          [T, T, T, T], [T, T, T, T]],

         ['ones',
          utils.make_state(board=(4, 4, 1, 4, 1, 4, 4, 4),
                           store=[0, 0],
                          ),
          [T, T, T, F], [T, T, F, T]],

     ]

    @pytest.mark.parametrize('state, efresult, etresult',
                             [case[1:] for case in CASES],
                             ids=[case[0] for case in CASES])
    def test_not_xfrom_1(self, game, state, efresult, etresult):

        game.state = state
        game.turn = True
        assert game.deco.allow.get_allowable_holes() == etresult

        game.turn = False
        assert game.deco.allow.get_allowable_holes() == efresult


class TestDontUndoMoveOne:

    GAME_CFG =  {'no_sides': {'no_sides': True},
                 'not_split': {'sow_direct': gi.Direct.CCW},
                 'udir': {'sow_direct': gi.Direct.SPLIT,
                          'udir_holes': [1, 2]},
                 'ns_split': {'no_sides': True,
                              'sow_direct': gi.Direct.SPLIT,
                                       'udir_holes': [1]},
                 'include': {'sow_direct': gi.Direct.SPLIT,
                             'udir_holes': [1]},
                }

    @pytest.fixture
    def game(self, request):

        game_props = TestDontUndoMoveOne.GAME_CFG[request.param]
        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on=[5],
                                stores=True,
                                **(game_props),
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    INCLUDE =  {'no_sides': False,
                'not_split': False,
                'udir': False,
                'ns_split': True,
                'include': True,
                }

    @pytest.mark.parametrize('key, game', zip(INCLUDE.keys(), INCLUDE.keys()),
                             ids=INCLUDE.keys(),
                             indirect=['game'])
    def test_include(self, key, game):

        if TestDontUndoMoveOne.INCLUDE[key]:
            assert 'DontUndoMoveOne' in str(game.deco.allow)
        else:
            assert 'DontUndoMoveOne' not in str(game.deco.allow)

    CASES = [
        # prevent cases (T, T, T)
        ('include', [1, 2, 0, 0, 2, 0], F, (0, None), [F, T, F]),
        ('include', [0, 2, 1, 0, 2, 0], F, (2, None), [F, T, F]),
        ('include', [0, 2, 0, 1, 2, 0], T, (2, None), [F, T, F]),
        ('include', [0, 2, 0, 0, 2, 1], T, (0, None), [F, T, F]),

        # don't prevent cases -- not one seed at capt_start after move (T, F, T)
        ('include', [1, 2, 0, 0, 2, 1], F, (0, None), [T, T, F]),
        ('include', [0, 2, 1, 1, 2, 0], F, (2, None), [F, T, T]),
        ('include', [0, 2, 1, 1, 2, 0], T, (2, None), [F, T, T]),
        ('include', [1, 2, 0, 0, 2, 1], T, (0, None), [T, T, F]),

        # T, F, F: sow 1, capt_start seeds != 1, sl & cl not edges
        ('include', [2, 1, 2, 0, 2, 2], F, (1, CCW), [T, T, F]),
        # T, T, F: sow 1 seed, capt_start seeds == 1, but sl & cl not edges
        ('include', [2, 1, 0, 0, 2, 2], F, (1, CCW), [T, T, F]),
        # F, T, F: sow 2 seeds, capt_start seeds == 1, sl & cl not edges
        ('include', [2, 2, 0, 3, 0, 0], F, (0, None), [T, T, T]),
        # F, F, F: sow 2 seeds, capt_start seeds > 1, sl & cl not edges
        ('include', [2, 2, 0, 0, 2, 2], F, (0, None), [T, T, F]),

        # hole not allowable to start
        ('include', [0, 2, 1, 1, 2, 0], F, (0, None), [F, T, T]),

        # prevent cases (T, T, T)
        ('ns_split', [1, 2, 0, 0, 2, 0], F, (1, 0, None),
                     [F, T, F, F, T, F]),
        ('ns_split', [0, 2, 1, 0, 2, 0], F, (1, 2, None),
                     [F, T, F, F, T, F]),
        ('ns_split', [0, 2, 0, 1, 2, 0], T, (0, 2, None),
                     [F, T, F, F, T, F]),
        ('ns_split', [0, 2, 0, 0, 2, 1], T, (0, 0, None),
                     [F, T, F, F, T, F]),

        # no prevents
        ('include', [0, 2, 0, 2, 3, 1], F, (0, CCW), [T, T, T]),

        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('game, board, turn, move, eresult',
                             CASES,
                             ids=[f"case_{idx}" for idx in range(len(CASES))],
                             indirect=['game'])
    def test_stop(self, game, board, turn, move, eresult):

        game.board = board
        quot, rem = divmod(12 - sum(board), 2)
        game.store = [quot, quot + rem]
        game.turn = turn
        print(game)
        game.move(move)
        # print(game.mdata)

        assert game.get_allowable_holes() == eresult


    @pytest.mark.parametrize('game',
                             ['include'],
                             indirect=['game'])
    def test_rturn(self, game):
        """Force a test of capt_start == REPEAT TURN"""

        game.board = [2, 2, 2, 2, 2, 2]
        game.store = [0, 0]
        game.turn= False
        game.move((0, CW))

        allowables = game.get_allowable_holes()
        assert allowables == [T, T, T]

        game.mdata.capt_start = gi.WinCond.REPEAT_TURN

        assert game.get_allowable_holes() == allowables


@pytest.mark.filterwarnings("ignore")
class TestMustShareUDir:

    TEST_ALLOW_DATA = [
        [utils.make_state(board=(4, 4, 4, 4, 4, 4)),
         {'udir_holes': [1],
          'sow_direct': gi.Direct.SPLIT},
         [T, T, T]],

        [utils.make_state(board=(2, 4, 4, 0, 0, 0)),  # 0 not udir & no share
         {'udir_holes': [1],
          'sow_direct': gi.Direct.CCW},
         [F, T, T]],

        [utils.make_state(board=(0, 1, 1, 0, 0, 0)),  # swap 2 from T to F, T
         {'udir_holes': [0, 1, 2],
          'sow_direct': gi.Direct.SPLIT},
         [F, F, [F, T]]],

        [utils.make_state(board=(0, 2, 1, 0, 0, 0)),  # leave center True
         {'udir_holes': [1],
          'sow_direct': gi.Direct.SPLIT},
         [F, T, T]],

        [utils.make_state(board=(4, 4, 4, 4, 4, 4)),
         {'udir_holes': [1],
          'goal': Goal.TERRITORY,
          'goal_param': 5,
          'sow_direct': gi.Direct.SPLIT},
         [T, T, T, F, F, F]],

        [utils.make_state(board=(2, 4, 4, 0, 0, 0)),  # 0 not udir & no share
         {'udir_holes': [1],
          'goal': Goal.TERRITORY,
          'goal_param': 5,
          'sow_direct': gi.Direct.CCW},
         [F, T, T, F, F, F]],

        [utils.make_state(board=(0, 1, 1, 0, 0, 0)),  # swap 2 from T to F, T
         {'udir_holes': [0, 1, 2],
          'goal': Goal.TERRITORY,
          'goal_param': 5,
          'sow_direct': gi.Direct.SPLIT},
         [F, F, [F, T], F, F, F]],

        [utils.make_state(board=(0, 2, 1, 0, 0, 0)),  # leave center True
         {'udir_holes': [1],
          'goal': Goal.TERRITORY,
          'goal_param': 5,
          'sow_direct': gi.Direct.SPLIT},
         [F, T, T, F, F, F]],

        ]

    @pytest.mark.parametrize(
        'game_state, game_dict, eresult',
        TEST_ALLOW_DATA,
        ids=[f'case_{cnt}' for cnt in range(len(TEST_ALLOW_DATA))])
    def test_allowables(self, game_state, game_dict, eresult, request):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                mustshare=True,
                                **game_dict,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.state = game_state

        seeds = game.cts.total_seeds - sum(game.board)
        quot, rem = divmod(seeds, 2)
        game.store = [quot, quot + rem]

        assert game.deco.allow.get_allowable_holes() == eresult


@pytest.mark.filterwarnings("ignore")
class TestNoEndlessSows:

    TEST_ALLOW_DATA = [
        # case_0: loc 7: endless sow, loc 9: < min_move
        ['NorthSouthCycle',
         (5, 4),
         {"crosscapt": True,
          "goal": gi.Goal.DEPRIVE,
          "mlaps": gi.LapSower.LAPPER,
          "sow_direct": gi.Direct.CCW,
          "sow_rule": gi.SowRule.LAP_CAPT_SEEDS,
          "min_move": 2,
          },
         utils.make_state(board=(1, 0, 5, 1, 3, 3, 0, 2, 4, 1),
                          turn=True),
         [F, T, F, F, T]],

        # case_1: no capture mechanism, loc 3 is endless sow
        ['Mancala',
         (5, 10),
         {"stores": True,
          "no_sides": True,
          "mlaps": gi.LapSower.LAPPER_NEXT,
          "sow_direct": gi.Direct.CCW,
          },
         utils.make_state(board=(3, 0, 26, 2, 11, 2, 27, 2, 27, 0),
                          turn=True),
         [T, F, T, F, T, T, T, T, T, F]],
        ]

    @pytest.mark.parametrize(
        'gclass, gconst, gdict, gstate, eresult',
        TEST_ALLOW_DATA,
        ids=[f'case_{cnt}' for cnt in range(len(TEST_ALLOW_DATA))])
    def test_allowables(self, gclass, gconst, gdict, gstate, eresult):

        game_consts = gconsts.GameConsts(holes=gconst[0], nbr_start=gconst[1])
        game_info = gi.GameInfo(**gdict,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game_class = game_classes.GAME_CLASSES[gclass]
        game = game_class(game_consts, game_info)
        game.state = gstate
        game.store = [game.cts.total_seeds - sum(game.board), 0]
        game.disallow_endless(True)

        assert 'NoEndlessSows' in str(game.deco.allow)
        assert game.deco.allow.get_allowable_holes() == eresult


class TestRightHalf:

    TEST_ALLOW_DATA = [
        [2, gi.AllowRule.RIGHT_HALF_FIRSTS, [F, T]],
        [5, gi.AllowRule.RIGHT_HALF_FIRSTS, [F, F, F, T, T]],
        [6, gi.AllowRule.RIGHT_HALF_FIRSTS, [F, F, F, T, T, T]],

        [2, gi.AllowRule.RIGHT_HALF_1ST_OPE, [F, T]],
        [5, gi.AllowRule.RIGHT_HALF_1ST_OPE, [F, F, F, T, T]],
        [6, gi.AllowRule.RIGHT_HALF_1ST_OPE, [F, F, F, T, T, T]],

        ]

    @pytest.mark.parametrize(
        'holes, arule, eresult',
        TEST_ALLOW_DATA,
        ids=[f'case_{cnt}' for cnt in range(len(TEST_ALLOW_DATA))])
    def test_allowables(self, holes, arule, eresult):

        game_consts = gconsts.GameConsts(holes=holes, nbr_start=4)
        game_info = gi.GameInfo(stores=True,
                                sow_own_store=True,
                                evens=True,
                                allow_rule=arule,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        game.turn = False
        assert 'RightHalfFirsts' in str(game.deco.allow)
        assert game.deco.allow.get_allowable_holes() == eresult

        game.turn = not game.turn
        game.movers += 1
        assert game.deco.allow.get_allowable_holes() == eresult[::-1]

        game.turn = not game.turn
        game.movers += 1

        if arule == gi.AllowRule.RIGHT_HALF_1ST_OPE:
            fcount = max(0, holes - 4)
            opp_or_empty = [F] * fcount + [T] * (holes - fcount)
            assert game.deco.allow.get_allowable_holes() == opp_or_empty

        else:
            assert all(game.deco.allow.get_allowable_holes())


class TestBadEnums:

    def test_bad_allow_rule(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        object.__setattr__(game_info, 'allow_rule', 22)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)



class TestAnimator:

    @pytest.mark.animator
    def test_animator(self, mocker):

        mobj = mocker.patch('animator.animate_off')

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        assert animator.ENABLED
        game = mancala.Mancala(game_consts, game_info)

        assert isinstance(game.deco.allow,
                          allowables.DontAnimateAllowable)

        game.deco.allow.get_allowable_holes()
        mobj.assert_called_once()


    def test_no_animator(self, mocker):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        assert not animator.ENABLED
        game = mancala.Mancala(game_consts, game_info)

        assert not isinstance(game.deco.allow,
                              allowables.DontAnimateAllowable)
