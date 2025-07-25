# -*- coding: utf-8 -*-
"""Sow in a ZigZag pattern.

Created on Thu Jun 12 05:27:58 2025
@author: Ann"""

import allowables
import game_info as gi
import get_direction
import incrementer
import mancala
import rule_tester


# %%  rule tester

def test_rules(ginfo, holes, skip=None):
    """Test the rules for ZigZag game class."""

    tester = rule_tester.RuleTester(ginfo, holes, skip)

    tester.test_rule(
        'zz_tocenter',
        rule=lambda ginfo: ginfo.sow_direct != gi.Direct.TOCENTER,
        msg="""ZigZag requires SOW_DIRECT be TOCENTER""",
        excp=gi.GameInfoError)
        # ZigZag requires TOCENTER so we know which deco to replace
        # and the rules will catch an error with an odd number of holes
        # and missing udir.

    mancala.Mancala.rules(ginfo, holes, skip=skip)


# %% decos

class ZigZagGetDir(get_direction.GetDirIf):
    """Get starting direction for zigzag sow.

    The sow must be toward the center line of the board,
    so the direction is picked to make that happen based
    on the cycle.

    If there are an odd number of holes the center hole
    must be udir."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        half = game.cts.half_holes

        # bottom = [gi.Direct.CW if idx % 2 else gi.Direct.CCW
        #           for idx in range(half)]
        # bottom = bottom + bottom[::-1]
        # top = [gi.Direct.CCW if idx % 2 else gi.Direct.CW
        #         for idx in range(half)]
        # top = top + top[::-1]

        cw_odd = [gi.Direct.CW if idx % 2 else gi.Direct.CCW
                  for idx in range(half)]
        ccw_odd = [gi.Direct.CCW if idx % 2 else gi.Direct.CW
                    for idx in range(half)]

        if game.cts.holes % 2:
            bottom = cw_odd + [None] + cw_odd
            top = bottom
        else:
            bottom = cw_odd + cw_odd[::-1]
            top = ccw_odd + ccw_odd[::-1]

        self.direction = bottom + top


    def __str__(self):
        dirs = [d.name if d else d for d in self.direction]
        return self.str_deco_detail('dir:  ' + str(dirs))


    def get_direction(self, mdata):

        return self.direction[mdata.sow_loc]


class ZigZagIncr(incrementer.MapIncrement):
    """Increment in a zigzag pattern.
    The sow pattern is a single cycle.
    This is a replacement for the Increment (the base incr class)."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        dbl_holes = game.cts.dbl_holes
        cycle = self.compute_cycle(game.cts.holes, dbl_holes)

        self.ccw_map = [cycle[(cycle.index(idx) + 1) % dbl_holes]
                         for idx in range(dbl_holes)]

        self.cw_map =  [cycle[(cycle.index(idx) - 1) % dbl_holes]
                         for idx in range(dbl_holes)]


    @staticmethod
    def compute_cycle(holes, dbl_holes):
        """Compute the zigzag cycle starting from hole 0
        and going in a counter-clockwise direction."""

        cycle = [0] * dbl_holes

        for idx in range(holes - 1):
            if idx % 2:
                cycle[idx] = idx + 1
            else:
                cycle[idx] = dbl_holes - idx - 2

        cycle[holes - 1] = holes if holes % 2 else holes - 1

        for idx in range(holes, dbl_holes - 1):
            if idx % 2:
                cycle[idx] = dbl_holes - idx - 2
            else:
                cycle[idx] = idx + 1

        return cycle


class DontUndoMoveOne(allowables.DontUndoMoveOne):
    """Don't allow moving a singleton back across the board side
    in the immediate next move unless it captured.

    Inheriting from the main DontUndoMoveOne because with the
    appropriate cross_sets and an initial filter we can re-use
    most of the work that it does.

    cross_sets: sets that are the start & end points for
                moves that should not be undone."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        holes = game.cts.holes
        half = game.cts.half_holes

        self.cross_sets = [{half - 1, holes + half - 1},
                           {half, holes + half}]


    def get_allowable_holes(self):

        mdata = self.game.mdata
        if not mdata or mdata.captured:
            return self.decorator.get_allowable_holes()

        return super().get_allowable_holes()



# %% ZigZag game class

class ZigZag(mancala.Mancala):
    """A game class that sows in a zig zag pattern."""

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """Test the game class rules before the game class is created."""
        test_rules(ginfo, holes, skip)


    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        self.deco.replace_deco('get_dir',
                               get_direction.CenterLineDir,
                               ZigZagGetDir(self))
        self.deco.replace_deco('incr',
                               incrementer.Increment,
                               ZigZagIncr(self))

        self._add_dont_undo_deco()


    def _add_dont_undo_deco(self):
        """Add the DoneUndoMoveOne deco if
              - min_move is 1 and
              - there are not any udirect holes and
              - there are an even number of holes per side.

        Put is right after the optional decos DontAnimateAllowable
        and MemoizeAllowable."""

        if (self.info.min_move == 1
                and not self.info.udirect
                and not self.cts.holes % 1):

            self.deco.append_deco('allow',
                                  (allowables.DontAnimateAllowable,
                                   allowables.MemoizeAllowable),
                                  DontUndoMoveOne(self))


    def disallow_endless(self, disallow):
        """Rebuild the allowable deco with or without the
        deco to prevent moves from holes that would be endless
        sows.  Then patch it again."""

        super().disallow_endless(disallow)
        self._add_dont_undo_deco()
