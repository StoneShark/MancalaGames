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

# %%  capture ok

class CaptOkIf(deco_chain_if.DecoChainIf):
    """Interface for capture tests, capture_ok."""

    @abc.abstractmethod
    def capture_ok(self, loc):
        """Return True if capture from loc is ok."""


# %%  base capt ok

class CaptTrue(CaptOkIf):
    """Found no reason not to do the capture, return True."""

    def capture_ok(self, loc):
        """Return True if capture from loc is ok"""
        return True


# %%  decorators

class CaptOn(CaptOkIf):
    """Test for Capture On values."""

    def capture_ok(self, loc):
        """Return True if capture from loc is ok"""

        if not self.game.board[loc] in self.game.info.capt_on:
            return False
        return self.decorator.capture_ok(loc)


class CaptEvens(CaptOkIf):
    """Capture on Evens that are > 0."""

    def capture_ok(self, loc):
        """Return True if capture from loc is ok"""

        if self.game.board[loc] % 2:
            return False
        return self.decorator.capture_ok(loc)


class CaptMax(CaptOkIf):
    """Capture on values <= capt_max."""

    def capture_ok(self, loc):
        """Return True if capture from loc is ok"""

        if self.game.board[loc] > self.game.info.capt_max:
            return False
        return self.decorator.capture_ok(loc)


class CaptMin(CaptOkIf):
    """Capture on values >= capt_min."""

    def capture_ok(self, loc):
        """Return True if capture from loc is ok"""

        if self.game.board[loc] < self.game.info.capt_min:
            return False
        return self.decorator.capture_ok(loc)


class CaptOppSide(CaptOkIf):
    """Capture from opposite side only."""

    def capture_ok(self, loc):
        """Return True if capture from loc is ok"""

        if not self.game.cts.opp_side(self.game.turn, loc):
            return False

        return self.decorator.capture_ok(loc)


class CaptUnlocked(CaptOkIf):
    """Can't capture from locked holes."""

    def capture_ok(self, loc):
        """Return True if capture from loc is ok"""

        if not self.game.unlocked[loc]:
            return False

        return self.decorator.capture_ok(loc)


class CaptNeedSeedsNotChild(CaptOkIf):
    """If there are no seeds or loc is a designated child, can't capture.
    Stack this one on top, so it's called first.
    Either condition should end a sequence of captures.
    Blocked holes will have zero seeds."""

    def capture_ok(self, loc):
        """is capture ok"""

        if not self.game.board[loc] or self.game.child[loc] is not None:
            return False

        return self.decorator.capture_ok(loc)


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

    if game.info.oppsidecapt:
        capt_ok = CaptOppSide(game, capt_ok)

    if game.info.moveunlock:
        # do not include this for gi.AllowRule.MOVE_ALL_HOLES_FIRST games
        capt_ok = CaptUnlocked(game, capt_ok)

    capt_ok = CaptNeedSeedsNotChild(game, capt_ok)

    return capt_ok
