# -*- coding: utf-8 -*-
"""Determine if children should be made.

Used in
    - the sower to stop mlap sowing (for games using mlap)
    - the capturer to decide make children

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
    """Each player can only have one child."""

    def test(self, mdata):
        game = self.game
        loc = mdata.capt_loc

        return (game.child[loc] is None
                and game.board[loc] == game.info.child_cvt
                and not any(game.child[tloc] is game.turn
                            for tloc in range(game.cts.dbl_holes)))


class QurChild(MakeChildIf):
    """Make a qur when sowing into empty hole
    and opposite side of board has CHILD_CVT seeds."""

    def test(self, mdata):

        game = self.game
        loc = mdata.capt_loc
        cross = game.cts.cross_from_loc(loc)

        return (game.board[loc] == 1
                and game.child[loc] is None
                and game.board[cross] == game.info.child_cvt)


# %% child wrappers


class ChildLocOk(MakeChildIf):
    """Check the allowable child locations.

    Each side of the board is broken up into 5 parts:
         0 1 [3 .. holes-4] holes-2 holes-1

    The pattern_dict describes which players may have children
    in each part.
    """

    @classmethod
    @property
    def pattern_dict(cls):
        """T row  first (top) but reversed from board array; F row second"""

        both = (False, True)
        false = (False,)
        true = (True,)

        return {

            gi.ChildLocs.ENDS_ONLY:
                [[both, None, None, None, both],
                 [both, None, None, None, both]],

            gi.ChildLocs.NO_ENDS:
                [[None, both, both, both, None],
                 [None, both, both, both, None]],

            gi.ChildLocs.INV_ENDS_PLUS_MID:
                [[false, true, true, true, false],
                 [true, false, false, false, true]],

            gi.ChildLocs.ENDS_PLUS_ONE_OPP:
                [[both, false, None, false, both],
                 [both, true, None, true, both]],

            gi.ChildLocs.NO_OWN_RIGHT:
                [[false, both, both, both, both],
                 [both, both, both, both, true]],

            gi.ChildLocs.NO_OPP_RIGHT:
                [[both, both, both, both, true],
                 [false, both, both, both, both]],

            gi.ChildLocs.NO_OPP_LEFT:
                [[true, both, both, both, both],
                 [both, both, both, both, false]],

            gi.ChildLocs.ENDS_PLUS_ALL_OPP:
                [[both, false, false, false, both],
                 [both, true, true, true, both]]

            }

    @classmethod
    @property
    def btrans(cls):
        """How to translate the pattern for shorter boards"""

        return {2: [0, 4, 5, 9],
                3: [0, 2, 4, 5, 7, 9],
                4: [0, 1, 3, 4, 5, 6, 8, 9]}


    def __init__(self, game, decorator, pattern):
        """pattern: select the pattern from PATTERN and adjust
        it so that it is the same order as the a board. Though
        it will always still be 10 elements long.

        loc_trans: an array that is the same length of the game's
        board used to translate between a board location and
        the pattern.  Boards which are shorter than 5, use
        the BTRANS to map the board location to the pattern
        location."""

        super().__init__(game, decorator)

        if pattern not in self.pattern_dict:
            raise NotImplementedError(
                f"ChildLocs {game.info.child_locs} not implemented.")

        plist = self.pattern_dict[pattern]
        self.pattern = plist[1] + plist[0][::-1]

        holes = game.cts.holes
        if holes in ChildLocOk.btrans:
            self.loc_trans = ChildLocOk.btrans[holes]

        else:
            half = [0, 1] + [2] * (holes - 4) + [3, 4]
            self.loc_trans = half + [val + 5 for val in half]


    def test(self, mdata):

        test_loc = self.loc_trans[mdata.capt_loc]
        ok_players = self.pattern[test_loc]

        if bool(ok_players) and self.game.turn in ok_players:
            return self.decorator.test(mdata)

        # game_log.add(f"Bad child loc @ {test_loc}.", game_log.IMPORT)
        return False


class NotSymOpp(MakeChildIf):
    """Children must not be symmetric to eachother. For example,
    in a 9 hole per side game:
          8 7 6 5 4 3 2 1 0
          0 1 2 3 4 5 6 7 8
    children may not be in the same numbered holes."""

    def test(self, mdata):

        loc = mdata.capt_loc
        holes = self.game.cts.holes
        symmetric = (loc + holes) if loc < holes else (loc - holes)

        if self.game.child[symmetric] is None:
            return self.decorator.test(mdata)

        game_log.add(f"NotSymOpp prevented child in symmetric hole @ {loc}.",
                     game_log.IMPORT)
        return False


class NotFacing(MakeChildIf):
    """Children must not be opposite the board from eachother."""

    def test(self, mdata):

        loc = mdata.capt_loc
        cross = self.game.cts.cross_from_loc(loc)

        if self.game.child[cross] is None:
            return self.decorator.test(mdata)

        game_log.add(f"NotFacing prevented child in facing hole @ {loc}.",
                     game_log.IMPORT)
        return False


class OppSideChild(MakeChildIf):
    """Require opposite side of the board"""

    def test(self, mdata):

        if self.game.cts.opp_side(self.game.turn, mdata.capt_loc):
            return self.decorator.test(mdata)

        return False


class OwnSideChild(MakeChildIf):
    """Require own side of the board"""

    def test(self, mdata):

        if self.game.cts.my_side(self.game.turn, mdata.capt_loc):
            return self.decorator.test(mdata)

        return False

class OppOwnerChild(MakeChildIf):
    """Require opposite owner of the board"""

    def test(self, mdata):

        if self.game.owner[mdata.capt_loc] is (not self.game.turn):
            return self.decorator.test(mdata)

        return False


class OwnOwnerChild(MakeChildIf):
    """Require own owner of the board"""

    def test(self, mdata):

        if self.game.owner[mdata.capt_loc] is self.game.turn:
            return self.decorator.test(mdata)

        return False


class NotWithOne(MakeChildIf):
    """Don't make a child if sowing started with one seed.

    When paired with OppSideChild, prevents a single seed
    creating a child in opponent's first hole, BUT also
    requires opposite children only!"""

    def test(self, mdata):

        if mdata.seeds > 1:
            return self.decorator.test(mdata)

        return False


class Not1stOppWithOne(MakeChildIf):
    """Don't make a child if sowing started with one seed
    and crossing the edge of the board."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        self.firsts = {gi.Direct.CW:
                           [self.game.cts.dbl_holes - 1,
                            self.game.cts.holes - 1],

                       gi.Direct.CCW:
                           [self.game.cts.holes, 0]}


    def test(self, mdata):
        """If there's more than one seed we wont prevent
        the child, call the chain. Otherwise, check loc against
        firsts based on direction and turn."""

        if mdata.seeds > 1:
            return self.decorator.test(mdata)

        if mdata.capt_loc == self.firsts[mdata.direct][self.game.turn]:
            return False

        return self.decorator.test(mdata)


class NotInhibited(MakeChildIf):
    """Enforce the no_child inhibitor."""

    def test(self, mdata):

        if self.game.inhibitor.stop_me_child(self.game.turn):
            return False

        return self.decorator.test(mdata)


# %% build the deco

def _add_child_type(game, deco):
    """Add a more specific child type handler"""

    if game.info.child_type == gi.ChildType.BULL:
        deco = BullChild(game, deco)

    elif game.info.child_type == gi.ChildType.ONE_CHILD:
        deco = OneChild(game, deco)

    elif game.info.child_type == gi.ChildType.QUR:
        deco = QurChild(game, deco)

    elif game.info.child_type not in (gi.ChildType.NORMAL,
                                      gi.ChildType.WEG):
        raise NotImplementedError(
            f"ChildType {game.info.child_type} not implemented.")

    return deco


def _add_child_rule_wrapper(game, deco):
    """Add any wrappers for the child rule."""

    if game.info.child_rule == gi.ChildRule.OPP_SIDE_ONLY:
        deco = OppSideChild(game, deco)

    elif game.info.child_rule == gi.ChildRule.OWN_SIDE_ONLY:
        deco = OwnSideChild(game, deco)

    elif game.info.child_rule == gi.ChildRule.NOT_1ST_OPP:
        deco = Not1stOppWithOne(game, deco)

    elif game.info.child_rule == gi.ChildRule.OPPS_ONLY_NOT_1ST:
        deco = OppSideChild(game, deco)
        deco = NotWithOne(game, deco)

    elif (game.info.goal == gi.Goal.TERRITORY
              and game.info.child_rule == gi.ChildRule.OPP_OWNER_ONLY):
        deco = OppOwnerChild(game, deco)

    elif (game.info.goal == gi.Goal.TERRITORY
              and game.info.child_rule == gi.ChildRule.OWN_OWNER_ONLY):
        deco = OwnOwnerChild(game, deco)

    elif game.info.child_rule != gi.ChildRule.NONE:
        raise NotImplementedError(
            f"ChildRule {game.info.child_rule} not implemented.")

    return deco


def _add_child_wrappers(game, deco):
    """Add any child wrappers include handling the child rules."""

    deco = _add_child_rule_wrapper(game, deco)

    if game.info.child_locs == gi.ChildLocs.NOT_SYM_OPP:
        deco = ChildLocOk(game, deco, gi.ChildLocs.NO_OPP_LEFT)
        deco = NotSymOpp(game, deco)

    elif game.info.child_locs == gi.ChildLocs.NOT_FACING:
        deco = ChildLocOk(game, deco, gi.ChildLocs.NO_OPP_RIGHT)
        deco = NotFacing(game, deco)

    elif game.info.child_locs:
        deco = ChildLocOk(game, deco, game.info.child_locs)

    return deco


def deco_child(game):
    """Generate the make_child deco chain."""

    if game.info.child_type == gi.ChildType.NOCHILD:
        return NoChildren(game)

    deco = BaseChild(game)
    deco = _add_child_type(game, deco)
    deco = _add_child_wrappers(game, deco)
    deco = NotInhibited(game, deco)

    return deco
