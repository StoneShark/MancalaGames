# -*- coding: utf-8 -*-
"""Define the capturer decorators.

The deco chain should return if the state of the board
was modified.

Created on Fri Apr  7 08:52:03 2023
@author: Ann"""


# %% imports

import abc

from game_interface import CrossCaptOwn
from game_interface import GrandSlam
from game_log import game_log
from incrementer import NOSKIPSTART


# %% enum

# picked own but did not capture, must be truthy
PICKED = 2


# %% capt interface


class CaptMethodIf(abc.ABC):
    """Interface for capturers."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def do_captures(self, mdata):
        """Do captures.
        Return True if captures were done, False otherwise."""


# %% capture base

class CaptNone(CaptMethodIf):
    """No captures."""

    def do_captures(self, mdata):
        return False



# %%  basic decos


class CaptSingle(CaptMethodIf):
    """Capture on selected values (CaptOn or Evens),
    no multi, no cross."""

    def do_captures(self, mdata):

        if self.game.deco.capt_ok.capture_ok(mdata.capt_loc):

            self.game.store[self.game.turn] += self.game.board[mdata.capt_loc]
            self.game.board[mdata.capt_loc] = 0
            return True
        return False


class CaptMultiple(CaptMethodIf):
    """Multi capture, in specified direction.
    capt_ok_deco encapsulates many of the capture parameters incl side."""

    def do_captures(self, mdata):
        """Capture loop"""
        captures = False
        loc = mdata.capt_loc

        while self.game.deco.capt_ok.capture_ok(loc):

            self.game.store[self.game.turn] += self.game.board[loc]
            self.game.board[loc] = 0
            captures = True

            loc = self.game.deco.incr.incr(loc, mdata.direct, NOSKIPSTART)

        return captures


class CaptOppDirMultiple(CaptMethodIf):
    """Multi capture, opposite direction.
    capt_ok_deco encapsulates many of the capture parameters incl side."""

    def do_captures(self, mdata):
        """Change direction then use the deco chain."""
        mdata.direct = mdata.direct.opp_dir()
        return self.decorator.do_captures(mdata)


class CaptCross(CaptMethodIf):
    """Cross capture, no pick own."""

    def do_captures(self, mdata):
        """Do cross capture"""

        cross = self.game.cts.cross_from_loc(mdata.capt_loc)

        if (self.game.board[mdata.capt_loc] == 1
                and self.game.deco.capt_ok.capture_ok(cross)):

            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[cross] = 0
            return True

        return False


class CaptTwoOut(CaptMethodIf):
    """If the seed ended in a hole which previously had seeds,
    and the next hole is empty, capture the seeds in the
    following hole."""

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        direct = mdata.direct
        loc_p1 = self.game.deco.incr.incr(loc, direct, NOSKIPSTART)
        loc_p2 = self.game.deco.incr.incr(loc_p1, direct, NOSKIPSTART)

        if (self.game.board[loc] > 1
                and not self.game.board[loc_p1]
                and self.game.board[loc_p2]
                and self.game.deco.capt_ok.capture_ok(loc_p2)):

            self.game.store[self.game.turn] += self.game.board[loc_p2]
            self.game.board[loc_p2] = 0
            return True
        return False


# %% cross capt decos

class CaptCrossPickOwnOnCapt(CaptMethodIf):
    """Cross capture, pick own if capture, but do not
    pick from a designated child or a locked hole.

    Don't used capt_ok, because oppsidecapt might prevent
    picking."""

    def do_captures(self, mdata):
        """Test for and pick own."""

        captures = self.decorator.do_captures(mdata)

        if (captures
                and self.game.child[mdata.capt_loc] is None
                and self.game.unlocked[mdata.capt_loc]):

            self.game.store[self.game.turn] += 1
            self.game.board[mdata.capt_loc] = 0

        return captures


class CaptCrossPickOwn(CaptMethodIf):
    """Cross capture, pick own even if no capture,
    but do not pick from a designated child
    or a locked hole."""

    def do_captures(self, mdata):
        """Test for and pick own."""

        captures = self.decorator.do_captures(mdata)

        side_ok = True
        if self.game.info.oppsidecapt:
            side_ok = self.game.cts.my_side(self.game.turn, mdata.capt_loc)

        if (side_ok
                and self.game.board[mdata.capt_loc] == 1
                and self.game.child[mdata.capt_loc] is None
                and self.game.unlocked[mdata.capt_loc]):

            self.game.store[self.game.turn] += 1
            self.game.board[mdata.capt_loc] = 0
            if not captures:
                captures = PICKED
            game_log.step('Capturer (picked own w/o)', self)

        return captures


class CaptContinueXCapt(CaptMethodIf):
    """Continue xcross capture this is actually the multicapture for
    cross capture.
    Otherwise run the other decorators to do xpick and optional pick
    if there was a capture, check for continued capture."""

    def do_captures(self, mdata):

        captures = self.decorator.do_captures(mdata)
        if captures == PICKED:
            return True
        if not captures:
            return False

        loc = mdata.capt_loc
        while True:

            loc = self.game.deco.incr.incr(loc, mdata.direct, NOSKIPSTART)
            cross = self.game.cts.cross_from_loc(loc)

            if (not self.game.board[loc]
                    and self.game.deco.capt_ok.capture_ok(cross)):

                self.game.store[self.game.turn] += self.game.board[cross]
                self.game.board[cross] = 0

            else:
                break

        return captures


# %%  grand slam decos

class GrandSlamCapt(CaptMethodIf):
    """Grand Slam capturer and tester.
    This class is still abstract."""

    def is_grandslam(self, mdata):
        """Return True if the capture was a grandslam and
        True if there were any captures."""

        # XXXX the test for start/end seeds could exclude children

        opp_rng = self.game.cts.get_opp_range(self.game.turn)
        start_seeds = any(mdata.board[tloc] for tloc in opp_rng)

        captures = self.decorator.do_captures(mdata)

        if start_seeds and captures:
            end_seeds = any(self.game.board[tloc] for tloc in opp_rng)
            return not end_seeds, True

        return False, captures


class GSNone(GrandSlamCapt):
    """A grand slam does not capture, reset the game state."""

    def do_captures(self, mdata):

        saved_state = self.game.state

        is_gs, captures = self.is_grandslam(mdata)
        if is_gs:
            game_log.add('GRANDSLAM: no capture', game_log.IMPORT)
            self.game.state = saved_state
            return False

        return captures


class GSKeep(GrandSlamCapt):
    """A grand slam does not capture left/right.
    Left/right is from the perspective of the player who just sowed."""

    def __init__(self, game, grandslam, decorator=None):

        super().__init__(game, decorator)
        if grandslam == GrandSlam.LEAVE_LEFT:
            self.keep = (game.cts.dbl_holes - 1, game.cts.holes - 1)
        else:
            self.keep = (game.cts.holes, 0)

    def do_captures(self, mdata):

        saved_state = self.game.state

        is_gs, captures = self.is_grandslam(mdata)
        if is_gs:

            turn = self.game.turn
            save_loc = self.keep[turn]
            seeds = saved_state.board[save_loc]
            if seeds:
                game_log.add('GRANDSLAM: keep', game_log.IMPORT)

                self.game.board[save_loc] = seeds
                self.game.store[turn] -= seeds

                # did we capture anything other than the keep hole?
                return saved_state != self.game.state

        return captures


class GSOppGets(GrandSlamCapt):
    """On a grand slam your seeds are collect by your opponent."""

    def do_captures(self, mdata):

        is_gs, captures = self.is_grandslam(mdata)
        if is_gs:
            game_log.add('GRANDSLAM: opp gets', game_log.IMPORT)
            opp_turn = not self.game.turn
            for tloc in self.game.cts.get_my_range(self.game.turn):
                self.game.store[opp_turn] += self.game.board[tloc]
                self.game.board[tloc] = 0

        return captures


# %%  child decorators

class MakeChild(CaptMethodIf):
    """If the hole constains convert_cnt seeds
    and the side test is good, designate a child.
    If a child is made don't do any other captures."""

    def do_captures(self, mdata):

        if self.game.board[mdata.capt_loc] == self.game.info.convert_cnt:
            if ((self.game.info.oppsidecapt
                    and self.game.cts.opp_side(self.game.turn, mdata.capt_loc))
                    or not self.game.info.oppsidecapt):

                self.game.child[mdata.capt_loc] = self.game.turn
                return True
            return False

        return self.decorator.do_captures(mdata)


class CaptureToWalda(CaptMethodIf):
    """Test to make a walda base on allowable walda locations
    and on captures put the seeds into a walda. If a walda is
    made don't do any other captures.

    If we have a walda, use the rest of the deco chain to see
    if captures are made, then move any captured seeds to the
    walda."""

    WALDA_BOTH = -1

    WALDA_TEST = [[WALDA_BOTH, False],
                  [WALDA_BOTH, True]]

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        holes = self.game.cts.holes
        dbl_holes = self.game.cts.dbl_holes

        self.walda_poses = [None] * dbl_holes
        self.walda_poses[0] = CaptureToWalda.WALDA_BOTH
        self.walda_poses[holes - 1] = CaptureToWalda.WALDA_BOTH
        self.walda_poses[holes] = CaptureToWalda.WALDA_BOTH
        self.walda_poses[dbl_holes - 1] = CaptureToWalda.WALDA_BOTH
        if holes >= 3:
            self.walda_poses[1] = True
            self.walda_poses[holes - 2] = True
            self.walda_poses[holes + 1] = False
            self.walda_poses[dbl_holes - 2] = False


    def do_captures(self, mdata):

        loc = mdata.capt_loc
        if (self.game.board[loc] == self.game.info.convert_cnt
                and self.game.child[loc] is None
                and self.walda_poses[loc] in
                    CaptureToWalda.WALDA_TEST[self.game.turn]):

            self.game.child[loc] = self.game.turn
            return True

        captures = False
        have_walda = False
        for walda in range(self.game.cts.dbl_holes):
            if self.game.child[walda] == self.game.turn:
                have_walda = True
                break

        if have_walda:
            if self.decorator.do_captures(mdata):
                self.game.board[walda] += self.game.store[self.game.turn]
                self.game.store[self.game.turn] = 0
                captures = True

        assert not sum(self.game.store)
        return captures


class MakeTuzdek(CaptMethodIf):
    """A tuzdek (child) may not be made in leftmost hole on
    either side.  Each player can only have one tuzdek and player's
    tuzdeks must not be opposite eachother on the board.

    This is the ONE_CHILD implementation."""

    def tuzdek_test(self, loc):
        """Put the test in a function to keep the linter from
        complaining that it's too complex"""

        cross = self.game.cts.cross_from_loc(loc)
        opp_range = self.game.cts.get_opp_range(self.game.turn)

        return (self.game.cts.opp_side(self.game.turn, loc)
                and self.game.child[loc] is None
                and self.game.child[cross] is None
                and self.game.board[loc] == self.game.info.convert_cnt
                and self.game.cts.loc_to_left_cnt(loc)
                and not any(self.game.child[tloc] is not None
                            for tloc in opp_range))

    def do_captures(self, mdata):

        loc = mdata.capt_loc

        if self.tuzdek_test(loc):
            self.game.child[loc] = self.game.turn
            return True

        return self.decorator.do_captures(mdata)


# %% no single wrapper

class NoSingleSeedCapt(CaptMethodIf):
    """Do not do captures with a single seed sow."""

    def do_captures(self, mdata):

        if mdata.seeds == 1:
            return False

        return self.decorator.do_captures(mdata)


# %% build deco chains

def _add_cross_capt_deco(game, ginfo, capturer):
    """Add the cross capture decorators to the capturer deco.

    crosscapt and multicapt is always captsamedir"""

    capturer = CaptCross(game, capturer)

    if ginfo.xcpickown == CrossCaptOwn.PICK_ON_CAPT:
        capturer = CaptCrossPickOwnOnCapt(game, capturer)

    elif ginfo.xcpickown == CrossCaptOwn.ALWAYS_PICK:
        capturer = CaptCrossPickOwn(game, capturer)

    if ginfo.multicapt:
        capturer = CaptContinueXCapt(game, capturer)

    return capturer


def _add_grand_slam_deco(game, ginfo, capturer):
    """Add the grand slam decorators to the capturer deco."""

    if ginfo.grandslam == GrandSlam.NO_CAPT:
        capturer = GSNone(game, capturer)

    elif ginfo.grandslam in (GrandSlam.LEAVE_LEFT, GrandSlam.LEAVE_RIGHT):
        capturer = GSKeep(game, ginfo.grandslam, capturer)

    elif ginfo.grandslam == GrandSlam.OPP_GETS_REMAIN:
        capturer = GSOppGets(game, capturer)

    return capturer


def deco_capturer(game):
    """Build capture chain and return it."""

    capturer = CaptNone(game)

    if game.info.crosscapt:
        capturer = _add_cross_capt_deco(game, game.info, capturer)

    elif game.info.multicapt:
        capturer = CaptMultiple(game, capturer)

        if not game.info.capsamedir:
            capturer = CaptOppDirMultiple(game, capturer)

    elif game.info.capttwoout:
        capturer = CaptTwoOut(game)

    elif (game.info.evens or game.info.capt_on
          or game.info.capt_max or game.info.capt_min):
        capturer = CaptSingle(game)

    capturer = _add_grand_slam_deco(game, game.info, capturer)

    # only one child handler: waldas/tuzdek/children
    if game.info.waldas:
        capturer =  CaptureToWalda(game, capturer)
    elif game.info.one_child:
        capturer = MakeTuzdek(game, capturer)
    elif game.info.child:
        capturer = MakeChild(game, capturer)

    if game.info.nosinglecapt:
        capturer = NoSingleSeedCapt(game, capturer)

    return capturer
