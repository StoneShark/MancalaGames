# -*- coding: utf-8 -*-
"""
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

    @staticmethod
    def test(_):
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
            return (self.game.owner[loc] is (not self.game.turn))

        return False


class BullChild(MakeChildIf):
    """Paired capt of child_cvt then child_cvt-1
        or just child_cvt."""

    def test(self, mdata):

        if not self.decorator.test(mdata):
            return False

        loc = mdata.capt_loc
        prev = self.game.deco.incr.incr(loc, mdata.direct.opp_dir())
        return ((self.game.child[loc] is None
                 and self.game.board[loc] == self.game.info.child_cvt - 1
                 and self.game.child[prev] is None
                 and self.game.board[prev] == self.game.info.child_cvt)
                or (self.game.child[loc] is None
                    and self.game.board[loc] == self.game.info.child_cvt))


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

        if self.decorator.test(mdata):
            return self.game.cts.opp_side(self.game.turn, mdata.capt_loc)

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
    """Generate the make_child deco chain.

    Used in
        - the sower to stop mlap sowing (for games using mlap)
        - the capturer to decide make children

    Waldas are completely handled in the capturer."""

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
