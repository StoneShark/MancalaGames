# -*- coding: utf-8 -*-
"""A north-south and an east-wet two cycle game.
Only sow on own side of the board.

Attempted to leave as many game options as possible
available--might lead to some very weird dynamics.

Two cycle game class will not likely be built on
these, there's very little added value, but
the decos and support functions that might likely
be used.

Created on Sun Dec  1 07:10:20 2024
@author: Ann"""

# %% imports

import allowables
import cfg_keys as ckey
import incrementer
import game_info as gi
import mancala
import rule_tester
import sower_decos


# %% North south rules

def test_ns2_rules(gclass_name, ginfo, holes, skip=None):
    """Test rules for NorthSouthCycle."""

    tester = rule_tester.RuleTester(ginfo, holes, skip)

    tester.test_rule(
        'ns2_not_territory',
        rule=lambda ginfo: ginfo.goal == gi.Goal.TERRITORY,
        msg=f'{gclass_name} incompatible with Territory GOAL',
        excp=gi.GameInfoError)
        # ownership of holes is fixed to board side

    tester.test_rule(
        'ns2_no_mshare',
        rule=lambda ginfo: ginfo.mustshare,
        msg=f'{gclass_name} incompatible with MUSTSHARE',
        excp=gi.GameInfoError)
        # can't sow opponents holes

    tester.test_rule(
        'ns2_no_sowrule',
        rule=lambda ginfo: ginfo.sow_rule in (
            # do not use the incr, so will fail
            gi.SowRule.SOW_BLKD_DIV,
            gi.SowRule.SOW_BLKD_DIV_NR,
            # not sowing op side
            gi.SowRule.NO_SOW_OPP_NS,
            gi.SowRule.NO_OPP_CHILD,
            gi.SowRule.LAP_CAPT_OPP_GETS,
            gi.SowRule.OPP_CHILD_ONLY1,
            ),
        msg=f'{gclass_name} incompatible with selected SOW_RULE',
        excp=gi.GameInfoError)

    tester.test_rule(
        'ns2_no_vis_opp',
        rule=lambda ginfo: ginfo.visit_opp,
        msg=f'{gclass_name} incompatible with VISIT_OPP',
        excp=gi.GameInfoError)

    tester.test_rule(
        'ns2_noside_wegs',
        rule=lambda ginfo: (ginfo.child_type == gi.ChildType.WEG
                            and not ginfo.no_sides),
        msg="NorthSouthCycle without NO_SIDES, opponent's Weg "
            "children cannot be sown into",
        excp=gi.GameInfoError)
        # cannot create children on opponents side, so opp will never sow

    tester.test_rule(
        'ns2_child_rules',
        rule=lambda ginfo: ginfo.child_rule in (gi.ChildRule.OPP_SIDE_ONLY,
                                                gi.ChildRule.OPPS_ONLY_NOT_1ST,
                                                gi.ChildRule.OWN_OWNER_ONLY,
                                                gi.ChildRule.NOT_1ST_OPP),
        msg=f'{gclass_name} incompatible with Child Rule',
        excp=gi.GameInfoError)
        # child test is always on side of the board with sown seed
        # Qurs can still be made opposite

    skip_set = skip if skip else set()
    skip_set |= {'xcapt_multi_same'}
    mancala.Mancala.rules(ginfo, holes, skip=skip_set)


def test_ew2_rules(ginfo, holes, skip=None):
    """Test the rules for EastWestCycle."""

    tester = rule_tester.RuleTester(ginfo, holes, skip)

    tester.test_rule(
        'ew2_even_holes',
        both_objs=True,
        rule=lambda _, nbr_holes: nbr_holes % 2,
        msg='EastWestCycle requires an even number of holes',
        excp=gi.GameInfoError)

    test_ns2_rules('EastWestCycles', ginfo, holes, skip)



# %% deco additions

class NorthSouthIncr(incrementer.IncrementerIf):
    """Increment that keeps seeds only on your own side
    of the board: TOP/BOTTOM
    This is a replacement for the Increment (the base incr class).
    """

    def incr(self, loc, direct, _=incrementer.NOSKIPSTART):
        """Do an increment."""

        rloc = (loc + direct) % self.game.cts.holes

        if loc >= self.game.cts.holes:
            rloc += self.game.cts.holes

        return rloc


class NorthSouthSowSeedsNStore(sower_decos.SowSeedsNStore):
    """Sow a seed into the player's own store when passing it
    for north/south two cycle games.

    Only need to replace the sow_store test functions.
    Because the top row is indexed in reverse, this doesn't
    depend on board side."""

    def __init__(self, game, decorator=None):

        def ccw_store(ploc, loc):
            """Return True if  we've wrapped the board in a
            counter-clockwise direction."""

            return ploc != gi.WinCond.REPEAT_TURN and ploc >= loc

        def cw_store(ploc, loc):
            """Return True if we've wrapped the board in a
            clockwise direction."""

            return ploc != gi.WinCond.REPEAT_TURN and ploc <= loc

        super().__init__(game, decorator)

        self.sow_store = {gi.Direct.CCW: [ccw_store, ccw_store],
                          gi.Direct.CW: [cw_store, cw_store]}


class EastWestIncr(incrementer.MapIncrement):
    """Increment that keeps seeds only on your own side
    of the board: EAST/WEST
    This is a replacement for the Increment (the base incr class)."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        dbl_holes = game.cts.dbl_holes
        half = game.cts.holes // 2
        half_3x = half * 3

        self.ccw_map = list(range(1, dbl_holes)) + [0]
        self.ccw_map[half - 1] = half_3x
        self.ccw_map[half_3x - 1] = half

        self.cw_map = [dbl_holes - 1] + list(range(dbl_holes - 1))
        self.cw_map[half] = half_3x - 1
        self.cw_map[half_3x] = half - 1


class EastWestAllowable(allowables.AllowableIf):
    """Base allowable for east/west games."""

    def get_allowable_holes(self):

        my_range = self.game.cts.get_my_range(self.game.turn)

        return [loc in my_range and self.allow_move(loc)
                for loc in range(self.game.cts.dbl_holes)]


# %% support function


def patch_ew_cts_ops(cts):
    """Patch the false_range and true_range--this makes many of
    the cts operations work as expected. board_side has to be
    replaced.

    Separate function because there is no real advantange of
    east-west games to be built on EastWestCycle.
    Especially, if there is another game class
    that provides more specialization
    (eg. Diffusion -> DiffusionV2 and  Ohojochi -> SameSide)."""

    holes = cts.holes
    dbl_holes = cts.dbl_holes
    half = holes // 2
    half_x3 = half * 3

    object.__setattr__(cts, 'false_range', range(half, half_x3))

    true_locs = tuple(range(half_x3, dbl_holes)) + tuple(range(half))
    object.__setattr__(cts, 'true_range', true_locs)

    object.__setattr__(cts, 'board_side',
                       lambda loc: not half <= loc < half_x3)


# %% game classes

class NorthSouthCycle(mancala.Mancala):
    """A north-south two cycle game players only move on their own
    side of the board."""

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """The rules for the class but don't build them unless we
        need them."""
        test_ns2_rules('NorthSouthCycle', ginfo, holes, skip)


    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        self.deco.replace_deco('incr', incrementer.Increment,
                               NorthSouthIncr(self))
        if self.info.sow_own_store:
            self.deco.replace_deco('sower', sower_decos.SowSeedsNStore,
                                   NorthSouthSowSeedsNStore(self))


class EastWestCycle(mancala.Mancala):
    """An East-West two cycle game players only move on their own
    side of the board.

    There is no current way to make an interesting game
    with this class. Player's actions cannot effect eachother."""

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """Test the game class rules before the game class is created."""
        test_ew2_rules(ginfo, holes, skip)


    def __init__(self, game_consts, game_info):

        patch_ew_cts_ops(game_consts)
        object.__setattr__(game_info, ckey.MLENGTH, 3)

        super().__init__(game_consts, game_info)

        self.deco.replace_deco('incr', incrementer.Increment,
                               EastWestIncr(self))

        self.deco.replace_deco('allow', allowables.AllowableTriples,
                               EastWestAllowable(self))


    def disallow_endless(self, disallow):
        """Rebuild the allowable deco chain with or without
        the prohibition for endless sows.
        Then patch for east west sowing."""

        super().disallow_endless(disallow)
        self.deco.replace_deco('allow', allowables.AllowableTriples,
                               EastWestAllowable(self))
