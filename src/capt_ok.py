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
import game_info as gi


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

        if not self.game[loc] in self.game.info.capt_on:
            return False
        return self.decorator.capture_ok(mdata, loc)


class CaptEvens(CaptOkIf):
    """Capture on Evens that are > 0."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if self.game[loc] % 2:
            return False
        return self.decorator.capture_ok(mdata, loc)


class CaptMax(CaptOkIf):
    """Capture on values <= capt_max."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if self.game[loc] > self.game.info.capt_max:
            return False
        return self.decorator.capture_ok(mdata, loc)


class CaptMin(CaptOkIf):
    """Capture on values >= capt_min."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if self.game[loc] < self.game.info.capt_min:
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
                game.cts.my_side(turn, mdata.capt_start)

        elif game.info.capt_side == gi.CaptSide.OPP_CONT:
            self.side_ok = lambda mdata, turn, loc: \
                game.cts.opp_side(turn, mdata.capt_start)

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

        if loc >= 0 and not self.side_ok(mdata, self.game.turn, loc):
            return False

        return self.decorator.capture_ok(mdata, loc)


class CaptUnlocked(CaptOkIf):
    """Can't capture from locked holes."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if loc >= 0 and not self.game.unlocked[loc]:
            return False

        return self.decorator.capture_ok(mdata, loc)


class CaptNotChild(CaptOkIf):
    """If  loc is a designated child, can't capture."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if loc >= 0 and self.game.child[loc] is not None:
            return False

        return self.decorator.capture_ok(mdata, loc)


class CaptNeedSeeds(CaptOkIf):
    """If there are no seeds on the board return False,
    else let the deco chain decide.

    Use this when stores are not in play, i.e. incrementer
    will never return a store index."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if not self.game.board[loc]:
            return False

        return self.decorator.capture_ok(mdata, loc)


class CaptNotStoreNeedSeeds(CaptOkIf):
    """If we are given a store, return False--never call
    down the deco chain with a store index.
    If the location is on the board but there are no seeds
    return False. Otherwise, let the deco chain decide.

    Use this when the stores are in play, i.e. the incrementer
    might return a store index, but we should never capture
    when loc is a store."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if loc < 0 or not self.game.board[loc]:
            return False

        return self.decorator.capture_ok(mdata, loc)


class CaptNeedSeedsAnywhere(CaptOkIf):
    """If there are no seeds in the store or board
    loc provided, return False. Otherwise, call down
    the deco chain (even with a store index).

    Use this when the stores are in play and direct
    captures can occur from the stores,
    i.e., loc might be a store index) ."""

    def capture_ok(self, mdata,  loc):
        """Return False if capture from loc is not ok,
        otherwise delegate."""

        if not self.game[loc]:
            return False

        return self.decorator.capture_ok(mdata, loc)


# %%  build deco chain

def _add_seeds_store_deco(game, deco):
    """Check appropriate locations for seeds or filter
    stores if they could be sown but not captured."""

    if game.info.capt_stores:
        deco = CaptNeedSeedsAnywhere(game, deco)

    elif game.info.sow_stores or game.info.play_locs:
        deco = CaptNotStoreNeedSeeds(game, deco)

    else:
        deco = CaptNeedSeeds(game, deco)

    return deco


def deco_capt_basic(game):
    """Build the basic capture check chain based on the params"""

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

    if game.info.child_type.child_but_not_ram():
        capt_ok = CaptNotChild(game, capt_ok)

    capt_ok = _add_seeds_store_deco(game, capt_ok)
    return capt_ok


def deco_capt_check(game):
    """The default capture check conditions under which we can
    never capture."""

    capt_check = CaptTrue(game)

    if game.info.capt_side and not game.info.crosscapt:
        capt_check = CaptSideOk(game, capt_check)

    if game.info.moveunlock:
        # do not include this for gi.AllowRule.MOVE_ALL_HOLES_FIRST games
        capt_check = CaptUnlocked(game, capt_check)

    if game.info.child_type.child_but_not_ram():
        capt_check = CaptNotChild(game, capt_check)

    capt_check = _add_seeds_store_deco(game, capt_check)
    return capt_check
