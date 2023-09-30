# -*- coding: utf-8 -*-
"""Define the capturer decorators.

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


# %% capt method enums and interface


class CaptMethodIf(abc.ABC):
    """Interface for capturers."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def do_captures(self, loc, direct):
        """Do captures.
        Return True if captures were done, False otherwise."""


# %% capture base

class CaptNone(CaptMethodIf):
    """No captures."""

    def do_captures(self, loc, direct):
        return False


# %% capture decorators


class CaptSingle(CaptMethodIf):
    """Capture on selected values (CaptOn or Evens),
    no multi, no cross."""

    def do_captures(self, loc, direct):

        if self.game.deco.capt_ok.capture_ok(loc):

            self.game.store[self.game.turn] += self.game.board[loc]
            self.game.board[loc] = 0
            return True
        return False


class CaptMultiple(CaptMethodIf):
    """Multi capture, in specified direction.
    capt_ok_deco encapsulates many of the capture parameters incl side."""

    def do_captures(self, loc, direct):
        """Capture loop"""
        captures = False
        while self.game.deco.capt_ok.capture_ok(loc):

            self.game.store[self.game.turn] += self.game.board[loc]
            self.game.board[loc] = 0
            captures = True

            loc = self.game.deco.incr.incr(loc, direct, NOSKIPSTART)

        return captures


class CaptOppDirMultiple(CaptMethodIf):
    """Multi capture, opposite direction.
    capt_ok_deco encapsulates many of the capture parameters incl side."""

    def do_captures(self, loc, direct):
        """Change direction then use the deco chain."""
        return self.decorator.do_captures(loc, direct.opp_dir())


class CaptCross(CaptMethodIf):
    """Cross capture, no pick own."""

    def do_captures(self, loc, direct):
        """Do cross capture"""

        cross = self.game.cts.dbl_holes - loc - 1

        if (self.game.board[loc] == 1
                and self.game.deco.capt_ok.capture_ok(cross)):

            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[cross] = 0
            return True

        return False


class CaptCrossPickOwnOnCapt(CaptMethodIf):
    """Cross capture, pick own if capture, but do not
    pick from a designated child or a locked hole.

    Don't used capt_ok, because oppsidecapt might prevent
    picking."""

    def do_captures(self, loc, direct):
        """Test for and pick own."""

        captures = self.decorator.do_captures(loc, direct)

        if (captures
                and self.game.child[loc] is None
                and self.game.unlocked[loc]):

            self.game.store[self.game.turn] += 1
            self.game.board[loc] = 0

        return captures


class CaptCrossPickOwn(CaptMethodIf):
    """Cross capture, pick own even if no capture,
    but do not pick from a designated child
    or a locked hole."""

    def do_captures(self, loc, direct):
        """Test for and pick own."""

        captures = self.decorator.do_captures(loc, direct)

        side_ok = True
        if self.game.info.flags.oppsidecapt:
            side_ok = self.game.cts.my_side(self.game.turn, loc)

        if (side_ok
                and self.game.board[loc] == 1
                and self.game.child[loc] is None
                and self.game.unlocked[loc]):

            self.game.store[self.game.turn] += 1
            self.game.board[loc] = 0
            if not captures:
                captures = PICKED
            game_log.step('Capturer (picked own w/o)', self)

        return captures


class CaptContinueXCapt(CaptMethodIf):
    """Continue xcross capture this is actually the multicapture for
    cross capture.
    otherwise run the other decorators to do xpick and optional pick
    if there was a capture, check for continued capture."""

    def do_captures(self, loc, direct):

        captures = self.decorator.do_captures(loc, direct)
        if captures == PICKED:
            return True
        if not captures:
            return False

        while True:

            loc = self.game.deco.incr.incr(loc, direct, NOSKIPSTART)
            cross = self.game.cts.dbl_holes - loc - 1

            if (not self.game.board[loc]
                    and self.game.deco.capt_ok.capture_ok(cross)):

                self.game.store[self.game.turn] += self.game.board[cross]
                self.game.board[cross] = 0

            else:
                break

        return captures


class GrandSlamCapt(CaptMethodIf):
    """Grand Slam capturer and tester.
    This class is still abstract."""

    def is_grandslam(self, loc, direct):
        """Return True if the capture was a grandslam and
        True if there were any captures.

        It would be better if the presence of seeds could be
        tested before sowing. If the opponent has no seeds
        with captures on 1s, the game ends and the opponent
        gets all of my seeds."""

        opp_rng = self.game.cts.get_opp_range(self.game.turn)
        start_seeds = any(self.game.board[tloc] for tloc in opp_rng)
        captures = self.decorator.do_captures(loc, direct)

        if start_seeds and captures:
            end_seeds = any(self.game.board[tloc] for tloc in opp_rng)
            return not end_seeds, True

        return False, captures


class GSNone(GrandSlamCapt):
    """A grand slam does not capture, reset the game state."""

    def do_captures(self, loc, direct):

        saved_state = self.game.state

        is_gs, captures = self.is_grandslam(loc, direct)
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

    def do_captures(self, loc, direct):

        saved_state = self.game.state

        is_gs, captures = self.is_grandslam(loc, direct)
        if is_gs:

            turn = self.game.turn
            save_loc = self.keep[turn]
            seeds = saved_state.board[save_loc]
            if seeds:
                game_log.add('GRANDSLAM: keep', game_log.IMPORT)

                self.game.board[save_loc] = seeds
                self.game.store[turn] -= seeds

                # did we capture anything other the the keep hole?
                return saved_state != self.game.state

        return captures


class GSOppGets(GrandSlamCapt):
    """On a grand slam your seed are collect by your opponent."""

    def do_captures(self, loc, direct):

        is_gs, captures = self.is_grandslam(loc, direct)
        if is_gs:
            game_log.add('GRANDSLAM: opp gets', game_log.IMPORT)
            opp_turn = not self.game.turn
            for tloc in self.game.cts.get_my_range(self.game.turn):
                self.game.store[opp_turn] += self.game.board[tloc]
                self.game.board[tloc] = 0

        return captures


class MakeChild(CaptMethodIf):
    """If the hole constains convert_cnt seeds
    and the side test is good, designate a child.
    If a child is made don't do any other captures."""

    def do_captures(self, loc, direct):

        if self.game.board[loc] == self.game.info.flags.convert_cnt:
            if ((self.game.info.flags.oppsidecapt
                    and self.game.cts.opp_side(self.game.turn, loc))
                    or not self.game.info.flags.oppsidecapt):

                self.game.child[loc] = self.game.turn
                return True
            return False

        return self.decorator.do_captures(loc, direct)


# %% build deco chains

def _add_cross_capt_deco(game, gflags, capturer):
    """Add the cross capture decorators to the capturer deco.

    crosscapt and multicapt is always captsamedir"""

    capturer = CaptCross(game, capturer)

    if gflags.xcpickown == CrossCaptOwn.PICK_ON_CAPT:
        capturer = CaptCrossPickOwnOnCapt(game, capturer)

    elif gflags.xcpickown == CrossCaptOwn.ALWAYS_PICK:
        capturer = CaptCrossPickOwn(game, capturer)

    if gflags.multicapt:
        capturer = CaptContinueXCapt(game, capturer)

    return capturer


def _add_grand_slam_deco(game, gflags, capturer):
    """Add the grand slam decorators to the capturer deco."""

    if gflags.grandslam == GrandSlam.NO_CAPT:
        capturer = GSNone(game, capturer)

    elif gflags.grandslam in (GrandSlam.LEAVE_LEFT, GrandSlam.LEAVE_RIGHT):
        capturer = GSKeep(game, gflags.grandslam, capturer)

    elif gflags.grandslam == GrandSlam.OPP_GETS_REMAIN:
        capturer = GSOppGets(game, capturer)

    return capturer


def deco_capturer(game):
    """Build capture chain and return it."""

    gflags = game.info.flags

    capturer = CaptNone(game)

    if gflags.crosscapt:
        capturer = _add_cross_capt_deco(game, gflags, capturer)

    elif gflags.multicapt:
        capturer = CaptMultiple(game, capturer)

        if not gflags.capsamedir:
            capturer = CaptOppDirMultiple(game, capturer)

    elif gflags.evens or game.info.capt_on:
        capturer = CaptSingle(game)

    capturer = _add_grand_slam_deco(game, gflags, capturer)

    if gflags.child:
        capturer = MakeChild(game, capturer)

    return capturer
