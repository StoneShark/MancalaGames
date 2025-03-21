# -*- coding: utf-8 -*-
"""Determine if capture is ok from a single hole.
This also stops a multi-capture sequence.

Each decorator acts as an ANDed condition. As soon as we know
a capture cannot occur, return False. If a deco determines the capture
is ok based on it's condition, continue the chain.

The deco chain effectively decides if a capture cannot occur.

Created on Fri Apr  7 08:52:03 2023
@author: Ann"""

# %% imports

import abc

import deco_chain_if
import game_interface as gi


# %%  capture ok

class CaptOkIf(deco_chain_if.DecoChainIf):
    """Interface for capture tests, capture_ok."""

    @abc.abstractmethod
    def capture_ok(self, mdata, loc):
        """Return True if capture from loc is ok,
        return False otherwise."""


# %%  base capt ok

class CaptTrue(CaptOkIf):
    """Found no reason not to do the capture, return True."""

    def capture_ok(self, _1,  _2):
        """Return True"""
        return True


# %%  decorators

class CaptOn(CaptOkIf):
    """Test for Capture On values."""

    def capture_ok(self, mdata,  loc):
        """Return True if capture from loc is ok"""

        if not self.game.board[loc] in self.game.info.capt_on:
            return False
        return self.decorator.capture_ok(mdata, loc)


class CaptEvens(CaptOkIf):
    """Capture on Evens that are > 0."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if self.game.board[loc] % 2:
            return False
        return self.decorator.capture_ok(mdata, loc)


class CaptMax(CaptOkIf):
    """Capture on values <= capt_max."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if self.game.board[loc] > self.game.info.capt_max:
            return False
        return self.decorator.capture_ok(mdata, loc)


class CaptMin(CaptOkIf):
    """Capture on values >= capt_min."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if self.game.board[loc] < self.game.info.capt_min:
            return False
        return self.decorator.capture_ok(mdata, loc)


class CaptSideOk(CaptOkIf):
    """Capture from specified side."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        if game.info.capt_side == gi.CaptSide.OPP_SIDE:
            self.side_ok = lambda _, turn, loc: game.cts.opp_side(turn, loc)

        elif game.info.capt_side == gi.CaptSide.OWN_SIDE:
            self.side_ok = lambda _, turn, loc: game.cts.my_side(turn, loc)

        elif game.info.capt_side == gi.CaptSide.OWN_CONT:
            self.side_ok = lambda mdata, turn, loc: \
                game.cts.my_side(turn, mdata.capt_loc)

        elif game.info.capt_side == gi.CaptSide.OPP_CONT:
            self.side_ok = lambda mdata, turn, loc: \
                game.cts.opp_side(turn, mdata.capt_loc)

        elif game.info.capt_side == gi.CaptSide.OPP_TERR:
            self.side_ok = lambda _, turn, loc: game.owner[loc] == (not turn)

        elif game.info.capt_side == gi.CaptSide.OWN_TERR:
            self.side_ok = lambda _, turn, loc: game.owner[loc] == turn

        else:
            raise NotImplementedError(
                f"CaptSide {game.info.capt_side} is not implemented")

    def capture_ok(self, mdata, loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if not self.side_ok(mdata, self.game.turn, loc):
            return False

        return self.decorator.capture_ok(mdata, loc)


class CaptUnlocked(CaptOkIf):
    """Can't capture from locked holes."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if not self.game.unlocked[loc]:
            return False

        return self.decorator.capture_ok(mdata, loc)


class CaptNeedSeedsNotChild(CaptOkIf):
    """If there are no seeds or loc is a designated child, can't capture.
    Stack this one on top, so it's called first.
    Either condition should end a sequence of captures.
    Blocked holes will have zero seeds."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if not self.game.board[loc] or self.game.child[loc] is not None:
            return False

        return self.decorator.capture_ok(mdata, loc)


# %%  build deco chain

def deco_capt_ok(game):
    """Build the capture ok chain based on the params."""

    capt_ok = CaptTrue(game)

    if game.info.capt_on:
        capt_ok = CaptOn(game, capt_ok)

    if game.info.evens:
        capt_ok = CaptEvens(game, capt_ok)

    if game.info.capt_min:
        capt_ok = CaptMin(game, capt_ok)

    if game.info.capt_max:
        capt_ok = CaptMax(game, capt_ok)

    if game.info.capt_side:
        capt_ok = CaptSideOk(game, capt_ok)

    if game.info.moveunlock:
        # do not include this for gi.AllowRule.MOVE_ALL_HOLES_FIRST games
        capt_ok = CaptUnlocked(game, capt_ok)

    capt_ok = CaptNeedSeedsNotChild(game, capt_ok)

    return capt_ok
