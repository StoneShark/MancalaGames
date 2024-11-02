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
from game_logger import game_log


class MakeChildIf(deco_chain_if.DecoChainIf):
    """Interface for MakeChild classes."""

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
    """Each player can only have one child and player's
    children must not be symmetric to eachother. For example,
    in a 9 hole per side game:
          8 7 6 5 4 3 2 1 0
          0 1 2 3 4 5 6 7 8
    Tuzdeks may not be in the same numbered holes.

    Children cannot be made in some holes based on the
    sow direction:
        CW: cannot make children in rightmost opposite side hole.
        Hole 0 above.
        CCW: cannot make children in leftmost opposite side hole.
        Hole 8 above.
        others: cannot make children in any end hole. Holes 0 and 8
        above.

    To create Tuzdek add child_rule=opp_only."""

    def __init__(self, game, decorator):

        super().__init__(game, decorator)

        self.no_child_locs = [-1, -1]
        if game.info.sow_direct == gi.Direct.CW:
            self.no_child_locs = [{game.cts.holes}, {0}]

        elif game.info.sow_direct == gi.Direct.CCW:
            self.no_child_locs = [{game.cts.holes - 1},
                                  {game.cts.dbl_holes - 1}]

        else:
            not_ends = {0, game.cts.holes - 1, game.cts.holes,
                                   game.cts.dbl_holes - 1}
            self.no_child_locs = [not_ends, not_ends]


    def test(self, mdata):
        game = self.game
        loc = mdata.capt_loc

        if (game.child[loc] is None
                and game.board[loc] == game.info.child_cvt
                and loc not in self.no_child_locs[game.turn]
                and not any(game.child[tloc] is game.turn
                            for tloc in range(game.cts.dbl_holes))):

            holes = game.cts.holes
            symmetric = (loc + holes) if loc < holes else (loc - holes)

            if game.child[symmetric] is None:
                return True

            game_log.add(f"OneChild prevented child in symmetric hole @ {loc}.",
                         game_log.IMPORT)

        return False



class QurChild(MakeChildIf):
    """Make a qur when sowing into empty hole on own side of
    board and opposite side of board has CHILD_CVT seeds."""

    def test(self, mdata):

        game = self.game
        loc = mdata.capt_loc
        cross = game.cts.cross_from_loc(loc)

        return (game.cts.my_side(game.turn, loc)
                and game.board[loc] == 1
                and game.child[loc] is None
                and game.board[cross] == game.info.child_cvt)


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

        if self.game.inhibitor.stop_me_child(self.game.turn):
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

    elif game.info.child_type == gi.ChildType.QUR:
        deco = QurChild(game, deco)

    elif game.info.child_type not in (gi.ChildType.NORMAL,
                                      gi.ChildType.WALDA):
        raise NotImplementedError(
            f"ChildType {game.info.child_type} not implemented.")

    if game.info.child_rule == gi.ChildRule.OPP_ONLY:
        deco = OppSideChild(game, deco)

    elif game.info.child_rule == gi.ChildRule.NOT_1ST_OPP:
        deco = OppSideChild(game, deco)
        deco = NotWithOne(game, deco)

    elif game.info.child_rule != gi.ChildRule.NONE:
        raise NotImplementedError(
            f"ChildRule {game.info.child_rule} not implemented.")

    deco = NotInhibited(game, deco)

    return deco
