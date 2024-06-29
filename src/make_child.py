# -*- coding: utf-8 -*-
"""Determine if children should be made.

Used in
    - the sower to stop mlap sowing (for games using mlap)
    - the capturer to decide make children

Waldas are completely handled in the capturer.

Created on Sat Jun 29 14:21:46 2024
@author: Ann"""

import abc
import deco_chain_if

import game_interface as gi


class MakeChildIf(deco_chain_if.DecoChainIf):
    """Generate a hole string."""

    @abc.abstractmethod
    def test(self, mdata):
        """Test to see if child should be made."""


class NoChildren(MakeChildIf):
    """Never make children for this game.
    Don't stack this with other decos."""

    def test(self, mdata):
        _ = mdata
        return False


class BaseChild(MakeChildIf):
    """Base case of making child, not already a child
    and has child convert count seeds.

    This deco assumes that it is at the base of the chain."""

    def test(self, mdata):
        loc = mdata.capt_loc
        return (self.game.child[loc] is None
                and self.game.board[loc] == self.game.info.child_cvt)


class WegChild(MakeChildIf):
    """Make a weg if base child and opponent is owner."""

    def test(self, mdata):

        loc = mdata.capt_loc
        if self.decorator.test(mdata):
            return self.game.owner[loc] is (not self.game.turn)

        return False


class BullChild(MakeChildIf):
    """One or two children can be made:

        - one, if loc is not a child and has child_cvt
        - two, if neither loc or prev is a child AND
        they contain child_cvt and child_cvt - 1 (in either order)

        Return True if children can be made, False otherwise.

        BullChild does not call down the deco chain!"""

    def test(self, mdata):

        loc = mdata.capt_loc
        game = self.game

        if game.child[loc] is not None:
            return False

        prev = game.deco.incr.incr(loc, mdata.direct.opp_dir())

        if game.child[prev] is None:
            board_set = set([game.board[prev], game.board[loc]])
            req_set = set([game.info.child_cvt - 1, game.info.child_cvt])
            if board_set == req_set:
                # we can make two children
                return True

        # test for one child
        return game.board[loc] == game.info.child_cvt


class OneChild(MakeChildIf):
    """Test the one child rule (tuzdek).

    A tuzdek (child) may not be made in leftmost hole on
    either side.  Each player can only have one tuzdek and player's
    tuzdeks must not be opposite eachother on the board."""

    def test(self, mdata):
        game = self.game
        loc = mdata.capt_loc
        cross = game.cts.cross_from_loc(loc)
        opp_range = game.cts.get_opp_range(game.turn)

        return (game.cts.opp_side(game.turn, loc)
                and game.child[loc] is None
                and game.child[cross] is None
                and game.board[loc] == game.info.child_cvt
                and game.cts.loc_to_left_cnt(loc)
                and not any(game.child[tloc] is not None
                            for tloc in opp_range))


class OppSideChild(MakeChildIf):
    """Require opposite side of the board"""

    def test(self, mdata):

        if self.game.cts.opp_side(self.game.turn, mdata.capt_loc):
            return self.decorator.test(mdata)

        return False


class NotWithOne(MakeChildIf):
    """Don't make a child if sowing started with one seed.

    When paired with OppSideChild, prevents a single seed
    creating a child in opponent's first hole."""

    def test(self, mdata):

        if mdata.seeds > 1:
            return self.decorator.test(mdata)

        return False


class NotInhibited(MakeChildIf):
    """Enforce the no_child inhibitor."""

    def test(self, mdata):

        if self.game.deco.inhibitor.stop_me_child(self.game.turn):
            return False

        return self.decorator.test(mdata)


def deco_child(game):
    """Generate the make_child deco chain."""


    if game.info.child_type == gi.ChildType.NOCHILD:
        return NoChildren(game)

    deco = BaseChild(game)

    if game.info.child_type == gi.ChildType.BULL:
        deco = BullChild(game, deco)

    elif game.info.child_type == gi.ChildType.WEG:
        deco = WegChild(game, deco)

    elif game.info.child_type == gi.ChildType.ONE_CHILD:
        deco = OneChild(game, deco)

    if game.info.child_rule == gi.ChildRule.OPP_ONLY:
        deco = OppSideChild(game, deco)

    if game.info.child_rule == gi.ChildRule.NOT_1ST_OPP:
        deco = OppSideChild(game, deco)
        deco = NotWithOne(game, deco)

    deco = NotInhibited(game, deco)

    return deco
