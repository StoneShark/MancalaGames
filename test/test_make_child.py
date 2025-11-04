# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:31:23 2023
@author: Ann"""


import pytest
pytestmark = pytest.mark.unittest

import utils

from context import animator
from context import game_constants as gconsts
from context import game_info as gi
from context import make_child
from context import mancala
from context import move_data


# %% constants

TEST_COVERS = ['src\\make_child.py']

T = True
F = False
N = None

CW = gi.Direct.CW
CCW = gi.Direct.CCW


# %% test wrappers


class TestChildInhibitor:
    """Complicated game to get Inhibitor both."""

    def test_inhibited(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(prescribed=gi.SowPrescribed.ARNGE_LIMIT,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                rounds=gi.Rounds.NO_MOVES,
                                blocks=True,
                                round_fill=gi.RoundFill.SHORTEN,
                                stores=True,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = 3
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = True
        game.inhibitor.set_on(game.turn)
        assert game.inhibitor.stop_me_child(game.turn)
        assert not game.deco.make_child.test(mdata)

        game.inhibitor.set_off()
        assert not game.inhibitor.stop_me_child(game.turn)
        assert game.deco.make_child.test(mdata)


class TestOppChild:

    def test_opp_child(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OPP_SIDE_ONLY,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert not game.deco.make_child.static_ok(True, 3)
        assert game.deco.make_child.static_ok(True, 2)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = True
        mdata.capt_start = 3
        assert not game.deco.make_child.test(mdata)

        mdata.capt_start = 2
        assert game.deco.make_child.test(mdata)


class TestOwnChild:

    def test_opp_child(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OWN_SIDE_ONLY,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert not game.deco.make_child.static_ok(False, 3)
        assert game.deco.make_child.static_ok(False, 2)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        game.turn = False
        mdata.capt_start = 3
        assert not game.deco.make_child.test(mdata)

        mdata.capt_start = 2
        assert game.deco.make_child.test(mdata)


class TestOppNotWithOne:

    @pytest.mark.parametrize('turn, hole, seeds, etest',
                             [(False, 3, 1, False),
                              (False, 3, 2, True),
                              (False, 4, 2, True),
                              (False, 1, 2, False),   # not opp side
                              (True, 0, 1, False),
                              (True, 0, 2, True),
                              (True, 2, 2, True),
                              (True, 4, 2, False),    # not opp side

                              # wouldn't happen w/o sow_stores,
                              # but make_child doesn't check sow_stores
                              (True, -1, 2, False),
                              ])
    def test_opp_child(self, turn, hole, seeds, etest):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OPPS_ONLY_NOT_1ST,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = turn
        mdata.capt_start = hole
        mdata.seeds = seeds
        assert game.deco.make_child.test(mdata) == etest


class TestNotWithOne:

    cases = [(False, CCW, 1, [T, T, T, F, T, T]),
             (True,  CCW, 1, [F, T, T, T, T, T]),
             (False,  CW, 1, [T, T, T, T, T, F]),
             (True,   CW, 1, [T, T, F, T, T, T]),
             ] + \
            [(turn, direct, 2, [T, T, T, T, T, T])
             for turn in [False, True]
             for direct in [CW, CCW]]

    @pytest.mark.parametrize('turn, direct, seeds, expect', cases)
    def test_opp_child(self, turn, direct, seeds, expect):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.NOT_1ST_OPP,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn

        actual = []
        for hole in range(game.cts.dbl_holes):
            mdata = move_data.MoveData(game, None)
            mdata.direct = direct
            mdata.board = tuple(game.board)
            mdata.capt_start = hole
            mdata.seeds = seeds

            actual += [game.deco.make_child.test(mdata)]

        assert actual == expect


class TestOppOwner:

    @pytest.mark.parametrize('turn, hole, seeds, etest',
                             [
                                 # basic test for owner
                                 (False, 1, 3, False),
                                 (False, 2, 3, True),
                                 (False, 3, 3, False),
                                 (False, 4, 3, True),

                                 (True, 1, 3, True),
                                 (True, 2, 3, False),
                                 (True, 3, 3, True),
                                 (True, 4, 3, False),

                                  # wrong number of seeds
                                 (True, 1, 2, True),
                                 (False, 2, 2, True),

                                 # already a child
                                 (True, 0, 3, False),
                                 (False, 5, 3, False),
                              ])
    def test_opp_owner(self, turn, hole, seeds, etest):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(goal=gi.Goal.TERRITORY,
                                goal_param=6,
                                stores=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OPP_OWNER_ONLY,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.owner = [F, F, T, F, T, T]
        game.child = [F, N, N, N, N, T]

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = turn
        mdata.capt_start = hole
        mdata.seeds = seeds
        assert game.deco.make_child.test(mdata) == etest


class TestOwnOwner:

    @pytest.mark.parametrize('turn, hole, seeds, etest',
                             [
                                 # basic test for owner
                                 (True, 1, 3, False),
                                 (True, 2, 3, True),
                                 (True, 3, 3, False),
                                 (True, 4, 3, True),

                                 (False, 1, 3, True),
                                 (False, 2, 3, False),
                                 (False, 3, 3, True),
                                 (False, 4, 3, False),

                                  # wrong number of seeds
                                 (False, 1, 2, True),
                                 (True, 2, 2, True),

                                 # already a child
                                 (False, 0, 3, False),
                                 (True, 5, 3, False),
                              ])
    def test_opp_owner(self, turn, hole, seeds, etest):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(goal=gi.Goal.TERRITORY,
                                goal_param=6,
                                stores=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_rule=gi.ChildRule.OWN_OWNER_ONLY,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.owner = [F, F, T, F, T, T]
        game.child = [F, N, N, N, N, T]

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = turn
        mdata.capt_start = hole
        mdata.seeds = seeds
        assert game.deco.make_child.test(mdata) == etest


class TestChildLocs:

    @pytest.fixture
    def game(self, request):
        """game is built so that all holes have child_cvt seeds.
        BaseChild should always return True"""

        (holes, options) = TestChildLocs.GAME_OPTS[request.param]
        game_consts = gconsts.GameConsts(nbr_start=3, holes=holes)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    GAME_OPTS = {
        'ends2': (2, {'child_locs': gi.ChildLocs.ENDS_ONLY}),
        'ends3': (3, {'child_locs': gi.ChildLocs.ENDS_ONLY}),
        'ends5': (5, {'child_locs': gi.ChildLocs.ENDS_ONLY}),
        'ends6': (6, {'child_locs': gi.ChildLocs.ENDS_ONLY}),

        'noends2': (2, {'child_locs': gi.ChildLocs.NO_ENDS}),
        'noends4': (4, {'child_locs': gi.ChildLocs.NO_ENDS}),

        'iemid7': (7, {'child_locs': gi.ChildLocs.INV_ENDS_PLUS_MID}),

        'epoo4': (4, {'child_locs': gi.ChildLocs.ENDS_PLUS_ONE_OPP}),
        'epoo5': (5, {'child_locs': gi.ChildLocs.ENDS_PLUS_ONE_OPP}),

        'eopp5': (5, {'child_locs': gi.ChildLocs.ENDS_PLUS_ALL_OPP}),

        }

    @staticmethod
    def make_cases():

        # case_name, game, turn, loc, echild
        cases = []

        # ends config
        cases += [(f'ends2-{turn}-{loc}', 'ends2', turn, loc, True)
                     for turn in [False, True]
                     for loc in range(4)]

        ends_e3 = [T, F, T, T, F, T]
        cases += [(f'ends3-{turn}-{loc}', 'ends3', turn, loc, ends_e3[loc])
                     for turn in [False, True]
                     for loc in range(6)]

        ends_e5 = [T, F, F, F, T, T, F, F, F, T]
        cases += [(f'ends5-{turn}-{loc}', 'ends5', turn, loc, ends_e5[loc])
                     for turn in [False, True]
                     for loc in range(10)]

        ends_e6 = [T, F, F, F, F, T, T, F, F, F, F, T]
        cases += [(f'ends6-{turn}-{loc}', 'ends6', turn, loc, ends_e6[loc])
                     for turn in [False, True]
                     for loc in range(12)]

        cases += [(f'noends2-{turn}-{loc}', 'noends2', turn, loc, False)
                     for turn in [False, True]
                     for loc in range(4)]

        noes_e4 = [F, T, T, F, F, T, T, F]
        cases += [(f'noends4-{turn}-{loc}', 'noends4', turn, loc, noes_e4[loc])
                     for turn in [False, True]
                     for loc in range(8)]

        iem7F = [F, T, T, T, T, T, F, T, F, F, F, F, F, T]
        iem7T = [T, F, F, F, F, F, T, F, T, T, T, T, T, F]
        cases += [(f'iem7-False-{loc}', 'iemid7', False, loc, iem7F[loc])
                     for loc in range(7)]
        cases += [(f'iem7-True-{loc}', 'iemid7', True, loc, iem7T[loc])
                     for loc in range(7, 14)]

        epoo4F = [T, F, F, T, T, T, T, T]
        epoo4T = [T, T, T, T, T, F, F, T]
        cases += [(f'epoo4-False-{loc}', 'epoo4', False, loc, epoo4F[loc])
                     for loc in range(4)]
        cases += [(f'epoo4-True-{loc}', 'epoo4', True, loc, epoo4T[loc])
                     for loc in range(4, 8)]

        epoo5F = [T, F, F, F, T, T, T, F, T, T]
        epoo5T = [T, T, F, T, T, T, F, F, F, T]
        cases += [(f'epoo5-False-{loc}', 'epoo5', False, loc, epoo5F[loc])
                     for loc in range(5)]
        cases += [(f'epoo5-True-{loc}', 'epoo5', True, loc, epoo5T[loc])
                     for loc in range(5, 10)]

        eopp5F = [T, F, F, F, T, T, T, T, T, T]
        eopp5T = [T, T, T, T, T, T, F, F, F, T]
        cases += [(f'eopp5-False-{loc}', 'eopp5', False, loc, eopp5F[loc])
                  for loc in range(10)]
        cases += [(f'eopp5-True-{loc}', 'eopp5', True, loc, eopp5T[loc])
                  for loc in range(10)]

        # NO_OPP_LEFT and NO_OPP_RIGHT are tested with OneChild below

        return cases

    CL_CASES = make_cases()

    @pytest.mark.parametrize('case_name, game, turn, loc, echild',
                             CL_CASES,
                             ids=[case[0] for case in CL_CASES],
                             indirect=['game'])
    def test_child_locs(self, case_name, game, turn, loc, echild):

        game.turn = turn

        # print(game.deco.make_child)
        # print(game.deco.make_child.decorator.pattern)
        # print(game.deco.make_child.decorator.loc_trans)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)
        mdata.capt_start = loc

        assert game.deco.make_child.test(mdata) == echild

        if echild:
            assert game.deco.make_child.static_ok(turn, loc)
        else:
            # this is not always true, but is for the current test cases
            # will fail when a reason other than location prevents a child
            assert not game.deco.make_child.static_ok(turn, loc)


class TestNotFacing:

    @pytest.mark.parametrize('turn, hole, opp_child, etest',
                             [
                                 # basic test for loc, w & wo children
                                 (True, 1, 4, False),
                                 (True, 2, N, True),

                                 (False, 0, N, True),
                                 (False, 3, 4, False),

                                 # not opp right
                                 (False, 3, N, False),
                                 (True, 0, N, False),

                                 # already a child
                                 (False, 0, 0, False),
                                 (True, 5, 5, False),
                              ])
    def test_facing(self, turn, hole, opp_child, etest):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(goal=gi.Goal.TERRITORY,
                                goal_param=6,
                                stores=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_locs=gi.ChildLocs.NOT_FACING,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        if opp_child is not None:
            game.child[opp_child] = True
        print(game)
        print(game.deco.make_child)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = turn
        mdata.capt_start = hole
        assert game.deco.make_child.test(mdata) == etest



# %%  test base classes

class TestNoChildren:

    def test_opp_child(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.board = tuple(game.board)

        game.turn = True
        mdata.capt_start = 1
        mdata.seeds = 1
        assert game.deco.make_child.test(mdata) == False

        assert not any(game.deco.make_child.static_ok(turn, loc)
                       for turn in (False, True)
                       for loc in range(6))


class TestBaseChild:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=5)
        game_info = gi.GameInfo(capt_on=[4],
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=4,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    # TODO write a test!!


class TestBull:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=4,
                                child_type=gi.ChildType.BULL,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([4, 0, 4, 0],
                                       [3, 4, 3, 0])
        game.store = [7, 7]
        return game

    BULL_CASES = [(0, True),
                  (1, True),
                  (2, True),
                  (3, False),
                  (4, False),
                  (5, True),
                  (6, False),
                  (7, True),
                ]

    @pytest.mark.parametrize('turn', (False, True))
    @pytest.mark.parametrize('loc, ebull', BULL_CASES)
    def test_bull(self, game, turn, loc, ebull):
        """Test basic bull making in the absence of
        existing bulls."""

        game.turn = turn
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert game.deco.make_child.test(mdata) == ebull


    WBULL_CASES = [(0, False),
                   (1, True),
                   (2, True),
                   (3, False),
                   (4, False),
                   (5, True),
                   (6, False),
                   (7, False),
                  ]
    @pytest.mark.parametrize('loc, ebull', WBULL_CASES)
    def test_with_bulls(self, game, loc, ebull):
        """Test same basic cases but set holes 0 and 7
        to already be bulls."""

        game.turn = True
        game.child[0] = False
        game.child[7] = True

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert game.deco.make_child.test(mdata) == ebull



class TestOneChild:
    """Expose errors in make_child.test for OneChild"""

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=3,
                                child_type=gi.ChildType.ONE_CHILD,
                                child_locs=gi.ChildLocs.NOT_SYM_OPP,
                                sow_direct=gi.Direct.CCW,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('loc', range(8))
    @pytest.mark.parametrize('turn', [False, True])
    @pytest.mark.parametrize('clocs, evals',
         [[ gi.ChildLocs.NO_OPP_LEFT,
           [[T, T, T, T, T, T, T, F],   # False locations allowed
            [T, T, T, F, T, T, T, T]]],   # True locations allowed

          [gi.ChildLocs.NO_OPP_RIGHT,
           [[T, T, T, T, F, T, T, T],
            [F, T, T, T, T, T, T, T]]],

          [gi.ChildLocs.NO_ENDS,
           [[F, T, T, F, F, T, T, F],
            [F, T, T, F, F, T, T, F]]],
          ], ids=['no_opp_left', 'no_opp_right', 'no_ends'])
    def test_disallowed(self, loc, turn, clocs, evals):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=3,
                                child_type=gi.ChildType.ONE_CHILD,
                                child_locs=clocs,
                                sow_direct=gi.Direct.CCW,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        game.turn = turn
        game.board[loc] = 3
        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert game.deco.make_child.test(mdata) == evals[turn][loc]


    @pytest.mark.parametrize('loc, turn',
                              [(7, False),
                               (3, True),
                              ])
    @pytest.mark.parametrize('board',
                             [# opp side
                              utils.build_board([None, None, False, None],
                                                [None, True, None, None]),
                              # own side
                              utils.build_board([None, None, True, None],
                                                [None, False, None, None]),
                              # both T side
                              utils.build_board([None, False, True, None],
                                                [None, None, None, None]),
                              # both F side
                              utils.build_board([None, None, None, None],
                                                [None, False, True, None]),
                             ])
    def test_only_one(self, game, turn, loc, board):
        """All boards have children for both players and so
        none should be allowed."""

        game.turn = turn
        game.child = board
        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert not game.deco.make_child.test(mdata)


    @pytest.mark.parametrize('loc, child_loc',
                             [(1, 5), (5, 1), (2, 6), (6, 2)])
    @pytest.mark.parametrize('turn', [False, True])
    def test_not_opp(self, game, turn, loc, child_loc):
        """Put a opponents child in symmetrically opp hole (child_loc),
        no child should be allowed in loc."""

        game.turn = turn
        game.child[child_loc] = not turn
        # print(game)
        # print(loc)

        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert not game.deco.make_child.test(mdata)


class TestTuzdek:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(child_cvt=3,
                                child_type=gi.ChildType.ONE_CHILD,
                                child_rule=gi.ChildRule.OPP_SIDE_ONLY,
                                child_locs=gi.ChildLocs.NOT_SYM_OPP,
                                sow_direct=gi.Direct.CW,
								stores=True,
                                capt_on=[3],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('loc, turn, emake',
                             [(0, False, False),
                              (3, False, False),
                              (4, False, True),
                              (7, False, False),
                              (0, True, True),
                              (3, True, False),
                              (4, True, False),
                              (7, True, False),
                              ])
    def test_tuzdek_creation(self, game, turn, loc, emake):

        game.turn = turn

        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert game.deco.make_child.test(mdata) == emake


    @pytest.mark.parametrize('loc, turn',
                             [(7, False),
                              (3, True),
                              ])
    def test_only_one(self, game, turn, loc):

        game.turn = turn
        game.child = utils.build_board([None, None, False, None],
                                       [None, True, None, None])
        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert not game.deco.make_child.test(mdata)


    @pytest.mark.parametrize('loc, turn, child',
                             [(6, False, 2),
                              (5, True, 1),
                              ])
    def test_not_opp(self, game, turn, loc, child):

        game.turn = turn
        game.child[child] = True

        mdata = move_data.MoveData(game, None)
        mdata.direct = gi.Direct.CCW
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert not game.deco.make_child.test(mdata)


class TestQur:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(child_cvt=3,
                                child_type=gi.ChildType.QUR,
                                child_rule=gi.ChildRule.OWN_SIDE_ONLY,
                                crosscapt=True,
                                xcpickown=1,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([2, 3, 1, 1],
                                       [1, 1, 3, 2])
        game.store = [1, 1]
        return game

    QCASES = [
        (False, 0, [], False),  # don't make, opp side wrong, but capt
        (False, 3, [], False),  # don't make, not single seed
        (False, 1, [], True),   # make
        (False, 1, [1], False),  # don't make or capt, already child

        (True, 0, [], False),  # don't make, not single seed
        (True, 2, [], True),   # make
        (True, 2, [2], False),  # don't make already child
        (True, 3, [], False),  # don't make, opp side wrong

              ]
    @pytest.mark.parametrize('turn, pos, child_cols, emake',
                             QCASES,
                             ids=[f'case_{f}' for f in range(len(QCASES))])
    def test_makin_qur(self, game, turn, pos, child_cols, emake):

        game.turn = turn
        for col in child_cols:
            cross = game.cts.cross_from_loc(col) # pos == loc for False
            game.child[col] = True
            game.child[cross] = True

        loc = game.cts.xlate_pos_loc(not turn, pos)
        cross = game.cts.cross_from_loc(loc)

        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert game.deco.make_child.test(mdata) == emake


class TestWeg:

    @pytest.fixture
    def game(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(stores=True,
                                goal=gi.Goal.TERRITORY,
                                goal_param=8,
                                child_cvt=3,
                                child_type=gi.ChildType.WEG,
                                child_rule=gi.ChildRule.OPP_OWNER_ONLY,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        game.board = utils.build_board([2, 3, 2, 1],
                                       [2, 3, 2, 1])
        game.store = [3, 5]
        game.owner = utils.build_board([F, F, T, T],
                                       [T, T, F, F])
        game.child = utils.build_board([N, N, F, F],
                                       [N, N, T, T])
        return game

    # putting this here keeps it out of the error trace
    WEG_CASES = [(0, T, F),
                 (1, T, F),
                 (2, T, F),
                 (3, T, F),
                 (4, T, F),
                 (5, T, F),
                 (6, T, T),
                 (7, T, F),
                 (0, F, F),
                 (1, F, T),
                 (2, F, F),
                 (3, F, F),
                 (4, F, F),
                 (5, F, F),
                 (6, F, F),
                 (7, F, F),
                ]

    @pytest.mark.parametrize('loc, turn, eweg', WEG_CASES)
    def test_wegs(self, game, loc, turn, eweg):
        """Test eweg making and captures:
        eweg - should weg/child be created"""

        game.turn = turn
        mdata = move_data.MoveData(game, None)
        mdata.direct = game.info.sow_direct
        mdata.capt_start = loc
        mdata.board = tuple(game.board)
        mdata.seeds = 2

        assert game.deco.make_child.test(mdata) == eweg


class TestRam:

    CASES = [({'sow_direct': gi.Direct.CCW},
              [7, 7, 2, 5, 3, 7, 2, 2],
              [F, T, F, T, F, T, F, F]),

             ({'sow_direct': gi.Direct.CW},
              [7, 7, 2, 5, 7, 7, 7, 7],
              [T, T, F, F, T, T, T, F]),

             ({'sow_direct': gi.Direct.CCW,
               'sow_stores':gi.SowStores.OWN},
              [7, 7, 7, 7, 3, 7, 2, 2],
              [F, F, T, T, F, F, F, F]),

             ({'sow_direct': gi.Direct.CCW,
               'sow_stores':gi.SowStores.BOTH},
              [7, 7, 7, 7, 3, 7, 2, 2],
              [F, F, F, T, F, F, F, F]),
             ]

    @pytest.mark.parametrize('options, board, echild', CASES)
    def test_ram(self, options, board, echild):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(stores=True,
                                goal=gi.Goal.MAX_SEEDS,
                                child_type=gi.ChildType.RAM,
                                **options,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game =  mancala.Mancala(game_consts, game_info)
        game.board = board
        result = [0] * 8

        for loc in range(8):

            mdata = move_data.MoveData(game, None)
            mdata.direct = game.info.sow_direct
            mdata.capt_start = loc
            result[loc] = game.deco.make_child.test(mdata)

        assert result == echild


    def test_bad_enum(self):

        game_consts = gconsts.GameConsts(nbr_start=3, holes=4)

        with pytest.raises(NotImplementedError):
            game_info = gi.GameInfo(stores=True,
                                    goal=gi.Goal.MAX_SEEDS,
                                    sow_direct=gi.Direct.SPLIT,
                                    child_type=gi.ChildType.RAM,
                                    child_cvt=4,
                                    nbr_holes=game_consts.holes,
                                    rules=mancala.Mancala.rules)

        game_info = gi.GameInfo(stores=True,
                                goal=gi.Goal.MAX_SEEDS,
                                sow_direct=gi.Direct.CCW,
                                child_type=gi.ChildType.RAM,
                                child_cvt=4,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        object.__setattr__(game_info, 'sow_direct', gi.Direct.SPLIT)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


class TestBadEnums:

    def test_bad_child_type_decos(self):
        """Two decos should raise the error, check both"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        object.__setattr__(game.info, 'child_type', 12)

        with pytest.raises(NotImplementedError):
            make_child.deco_child(game)


    def test_bad_child_rule(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        object.__setattr__(game.info, 'child_type', gi.ChildType.NORMAL)
        object.__setattr__(game.info, 'child_rule', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


    def test_bad_child_locs(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[4],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        object.__setattr__(game.info, 'child_type', gi.ChildType.NORMAL)
        object.__setattr__(game.info, 'child_locs', 12)

        with pytest.raises(NotImplementedError):
            mancala.Mancala(game_consts, game_info)


class TestAnimator:

    @pytest.mark.animator
    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('loctype, board, child, emake',
         [
             # child not made due to bad location, message
             (gi.ChildLocs.NOT_SYM_OPP, [3, 3, 1, 2, 3, 3], [T, N, N, N, N, N], False),
             (gi.ChildLocs.NOT_FACING,  [3, 3, 3, 3, 3, 2], [T, N, N, N, N, N], False),
             (gi.ChildLocs.NO_ENDS,     [3, 3, 3, 3, 3, 2], [N, N, N, N, N, N], False),

             # child not made due to wrong count, no message
             (gi.ChildLocs.NOT_SYM_OPP, [3, 3, 1, 1, 3, 3], [T, N, N, N, N, N], None),
             (gi.ChildLocs.NOT_FACING,  [3, 3, 3, 3, 3, 1], [T, N, N, N, N, N], None),
             (gi.ChildLocs.NO_ENDS,     [3, 3, 3, 3, 3, 1], [N, N, N, N, N, N], None),

             # child made, no message
             (gi.ChildLocs.NOT_SYM_OPP, [3, 3, 1, 2, 3, 3], [N, N, N, N, N, N], True),
             (gi.ChildLocs.NOT_FACING,  [3, 3, 3, 3, 3, 2], [N, N, N, N, N, N], True),
             (gi.ChildLocs.NO_ENDS,     [3, 3, 2, 3, 2, 2], [N, N, N, N, N, N], True),
             ])
    def test_grandslam(self, mocker, loctype, board, child, emake):

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mocker.patch('animator.one_step')
        mocker.patch('animator.ANIMATOR.change')
        mocker.patch('animator.ANIMATOR.do_flash')
        mobj = mocker.patch('animator.ANIMATOR.do_message')

        game_consts = gconsts.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(stores=True,
                                evens=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=3,
                                child_locs=loctype,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.board = board
        game.child = child
        game.store = [3*3*2 - sum(board), 0]
        game.turn = False

        # print(game.deco.make_child)

        game.move(2)
        # print(game)
        # print(game.mdata)

        if emake is True:
            assert game.mdata.capt_changed
            mobj.assert_not_called()

        elif emake is None:
            assert not game.mdata.capt_changed
            mobj.assert_not_called()

        else:
            assert not game.mdata.capt_changed
            mobj.assert_called_once()
