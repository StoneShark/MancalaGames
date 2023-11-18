# -*- coding: utf-8 -*-
"""Define the capturer decorators.

The deco chain should return if the state of the board
was modified.

Created on Fri Apr  7 08:52:03 2023
@author: Ann"""


# %% imports

import abc

from game_interface import CaptExtraPick
from game_interface import ChildType
from game_interface import CrossCaptOwn
from game_interface import GrandSlam
from game_interface import WinCond
from game_log import game_log


# %% capt interface


class CaptMethodIf(abc.ABC):
    """Interface for capturers."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def do_captures(self, mdata):
        """Do captures.
        Update mdata (both are inited to False):
            capt_changed: there was a state change (picked, child made, etc.)
        but not a capture
            captured: there was an actual capture, this will be used for repeat turn
        """


# %% capture base

class CaptNone(CaptMethodIf):
    """No captures."""

    def do_captures(self, mdata):
        pass


# %%  basic decos


class CaptSingle(CaptMethodIf):
    """Capture on selected values (CaptOn or Evens),
    no multi, no cross."""

    def do_captures(self, mdata):

        if self.game.deco.capt_ok.capture_ok(mdata.capt_loc):

            self.game.store[self.game.turn] += self.game.board[mdata.capt_loc]
            self.game.board[mdata.capt_loc] = 0
            mdata.captured = True


class CaptMultiple(CaptMethodIf):
    """Multi capture, in specified direction.
    capt_ok_deco encapsulates many of the capture parameters incl side."""

    def do_captures(self, mdata):
        """Capture loop"""
        loc = mdata.capt_loc

        while self.game.deco.capt_ok.capture_ok(loc):

            self.game.store[self.game.turn] += self.game.board[loc]
            self.game.board[loc] = 0
            mdata.captured = True

            loc = self.game.deco.incr.incr(loc, mdata.direct)


class CaptOppDirMultiple(CaptMethodIf):
    """Multi capture, opposite direction."""

    def do_captures(self, mdata):
        """Change direction then use the deco chain."""
        mdata.direct = mdata.direct.opp_dir()
        self.decorator.do_captures(mdata)


class CaptCross(CaptMethodIf):
    """Cross capture."""

    def do_captures(self, mdata):
        """Do cross capture"""

        cross = self.game.cts.cross_from_loc(mdata.capt_loc)

        if (self.game.board[mdata.capt_loc] == 1
                and self.game.deco.capt_ok.capture_ok(cross)):

            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[cross] = 0
            mdata.captured = True


class CaptNext(CaptMethodIf):
    """If there are seeds in the next hole capture them."""

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        direct = mdata.direct
        loc_next = self.game.deco.incr.incr(loc, direct)

        if (self.game.board[loc] == 1
                and self.game.board[loc_next]
                and self.game.deco.capt_ok.capture_ok(loc_next)):

            self.game.store[self.game.turn] += self.game.board[loc_next]
            self.game.board[loc_next] = 0
            mdata.captured = True


class CaptTwoOut(CaptMethodIf):
    """If the final contents of the hole (# of seeds) and
    capture count meet the 'seed_cond' condition,
    and the next hole is empty, capture the seeds in the
    following hole.

    capt_loc is updated for both MultiCaptTwoOut and PickCross.

    Don't use capt_ok because it might be setup for sow_Capt_all"""

    def __init__(self, game, seed_cond, decorator=None):

        super().__init__(game, decorator)
        self.seed_cond = seed_cond

    def do_captures(self, mdata, cnt=1):

        loc = mdata.capt_loc
        direct = mdata.direct
        loc_p1 = self.game.deco.incr.incr(loc, direct)
        loc_p2 = self.game.deco.incr.incr(loc_p1, direct)

        if (self.seed_cond(self.game.board[loc], cnt)
                and not self.game.board[loc_p1]
                and self.game.board[loc_p2]
                and self.game.child[loc_p2] is None
                and self.game.unlocked[loc_p2]):

            self.game.store[self.game.turn] += self.game.board[loc_p2]
            self.game.board[loc_p2] = 0
            mdata.captured = True
            mdata.capt_loc = loc_p2


class MultiCaptTwoOut(CaptMethodIf):
    """Multiple captures of two out are:
         1 0 s1 0 s2 0 s3 ...
       as long as there are alternating empty and occupied holes.

       This adds its CaptTwoOut to the deco chain, because it
       gets called directly with an additional parameter.

       If capttwoout did a capture, it updates capt_loc."""

    def __init__(self, game, decorator=None):
        """Create the CaptTwoOut decorator."""

        def check_seeds(seeds, cnt):
            return cnt == 1 or (cnt > 1 and not seeds)

        next_deco = CaptTwoOut(game, check_seeds, decorator)
        super().__init__(game, next_deco)


    def do_captures(self, mdata):
        """Capture loop"""
        loc = mdata.capt_loc

        cnt = 1
        while True:

            self.decorator.do_captures(mdata, cnt)
            if loc == mdata.capt_loc:
                return

            loc = mdata.capt_loc
            cnt += 1


# %% cross capt decos


class CaptCrossVisited(CaptMethodIf):
    """First, reject cross capt if not single seed or opponent's side.
    Second, reject cross capt if have't sown opp hole this turn.
    If rejecting cross capt, do repeat turn."""

    def do_captures(self, mdata):

        if (self.game.board[mdata.capt_loc] != 1
                or self.game.cts.opp_side(self.game.turn, mdata.capt_loc)):
            return

        cross = self.game.cts.cross_from_loc(mdata.capt_loc)
        if mdata.board[cross] < self.game.board[cross]:
            self.decorator.do_captures(mdata)
            return

        mdata.captured = WinCond.REPEAT_TURN
        game_log.add('XCVisit Repeat Turn', game_log.INFO)


class CaptCrossPickOwnOnCapt(CaptMethodIf):
    """Cross capture, pick own if capture, but do not
    pick from a designated child or a locked hole.

    Don't used capt_ok, because oppsidecapt might prevent
    picking."""

    def do_captures(self, mdata):
        """Test for and pick own."""

        self.decorator.do_captures(mdata)

        if (mdata.captured is True
                and self.game.child[mdata.capt_loc] is None
                and self.game.unlocked[mdata.capt_loc]):

            self.game.store[self.game.turn] += 1
            self.game.board[mdata.capt_loc] = 0


class CaptCrossPickOwn(CaptMethodIf):
    """Cross capture, pick own even if no capture,
    but do not pick from a designated child
    or a locked hole."""

    def do_captures(self, mdata):
        """Test for and pick own."""

        self.decorator.do_captures(mdata)

        side_ok = True
        if self.game.info.oppsidecapt:
            side_ok = self.game.cts.my_side(self.game.turn, mdata.capt_loc)

        if (side_ok
                and self.game.board[mdata.capt_loc] == 1
                and self.game.child[mdata.capt_loc] is None
                and self.game.unlocked[mdata.capt_loc]):

            self.game.store[self.game.turn] += 1
            self.game.board[mdata.capt_loc] = 0
            mdata.capt_changed = True
            game_log.add('Capturer (picked own w/o)', game_log.INFO)


class CaptContinueXCapt(CaptMethodIf):
    """Continue xcross capture this is actually the multicapture for
    cross capture.
    Otherwise run the other decorators to do xpick and optional pick
    if there was a capture, check for continued capture."""

    def do_captures(self, mdata):

        self.decorator.do_captures(mdata)
        if not mdata.captured:
            return

        loc = mdata.capt_loc
        while True:

            loc = self.game.deco.incr.incr(loc, mdata.direct)
            cross = self.game.cts.cross_from_loc(loc)

            if (not self.game.board[loc]
                    and self.game.deco.capt_ok.capture_ok(cross)):

                self.game.store[self.game.turn] += self.game.board[cross]
                self.game.board[cross] = 0

            else:
                return


# %%  grand slam decos

class GrandSlamCapt(CaptMethodIf):
    """Grand Slam capturer and tester.
    This class is still abstract."""

    def is_grandslam(self, mdata):
        """Return True if the capture was a grandslam"""

        # XXXX the test for start/end seeds could exclude children

        opp_rng = self.game.cts.get_opp_range(self.game.turn)
        start_seeds = any(mdata.board[tloc] for tloc in opp_rng)

        self.decorator.do_captures(mdata)

        if start_seeds and mdata.captured:
            return not any(self.game.board[tloc] for tloc in opp_rng)

        return False


class GSNone(GrandSlamCapt):
    """A grand slam does not capture, reset the game state."""

    def do_captures(self, mdata):

        saved_state = self.game.state

        if self.is_grandslam(mdata):
            game_log.add('GRANDSLAM: no capture', game_log.IMPORT)
            self.game.state = saved_state
            mdata.capt_changed = False
            mdata.captured = False


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
        if self.is_grandslam(mdata):

            turn = self.game.turn
            save_loc = self.keep[turn]
            seeds = saved_state.board[save_loc]
            if seeds:
                game_log.add('GRANDSLAM: keep', game_log.IMPORT)

                self.game.board[save_loc] = seeds
                self.game.store[turn] -= seeds

                # did we capture anything other than the keep hole?
                mdata.captured = saved_state != self.game.state


class GSOppGets(GrandSlamCapt):
    """On a grand slam your seeds are collect by your opponent."""

    def do_captures(self, mdata):

        if self.is_grandslam(mdata):

            game_log.add('GRANDSLAM: opp gets', game_log.IMPORT)
            opp_turn = not self.game.turn
            for tloc in self.game.cts.get_my_range(self.game.turn):
                self.game.store[opp_turn] += self.game.board[tloc]
                self.game.board[tloc] = 0


# %%  child decorators

class MakeChild(CaptMethodIf):
    """If the hole constains child_cvt seeds
    and the side test is good, designate a child.
    If a child is made don't do any other captures."""

    def do_captures(self, mdata):

        if self.game.board[mdata.capt_loc] == self.game.info.child_cvt:
            if ((self.game.info.oppsidecapt
                    and self.game.cts.opp_side(self.game.turn, mdata.capt_loc))
                    or not self.game.info.oppsidecapt):

                self.game.child[mdata.capt_loc] = self.game.turn
                mdata.capt_changed = True
                return

        self.decorator.do_captures(mdata)


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
        if (self.game.board[loc] == self.game.info.child_cvt
                and self.game.child[loc] is None
                and self.walda_poses[loc] in
                    CaptureToWalda.WALDA_TEST[self.game.turn]):

            self.game.child[loc] = self.game.turn
            mdata.capt_changed = True
            return

        have_walda = False
        for walda in range(self.game.cts.dbl_holes):
            if self.game.child[walda] == self.game.turn:
                have_walda = True
                break

        if have_walda:
            self.decorator.do_captures(mdata)
            if mdata.captured:
                self.game.board[walda] += self.game.store[self.game.turn]
                self.game.store[self.game.turn] = 0

        assert not sum(self.game.store)


class MakeTuzdek(CaptMethodIf):
    """A tuzdek (child) may not be made in leftmost hole on
    either side.  Each player can only have one tuzdek and player's
    tuzdeks must not be opposite eachother on the board.

    This is the ONE_CHILD implementation."""

    def _tuzdek_test(self, loc):
        """Put the test in a function to keep the linter from
        complaining that it's too complex"""

        cross = self.game.cts.cross_from_loc(loc)
        opp_range = self.game.cts.get_opp_range(self.game.turn)

        return (self.game.cts.opp_side(self.game.turn, loc)
                and self.game.child[loc] is None
                and self.game.child[cross] is None
                and self.game.board[loc] == self.game.info.child_cvt
                and self.game.cts.loc_to_left_cnt(loc)
                and not any(self.game.child[tloc] is not None
                            for tloc in opp_range))

    def do_captures(self, mdata):

        loc = mdata.capt_loc

        if self._tuzdek_test(loc):
            self.game.child[loc] = self.game.turn
            mdata.capt_changed = True
            return

        self.decorator.do_captures(mdata)


class MakeWegCapture(CaptMethodIf):
    """If the last seed falls into an opponents weg, capture
    the seed just sown and one more (if there is one)
    and take another turn.
    If the last seed falls into non-weg and it has convert_cnt
    seeds and is owned by the opponent, convert it to a weg.
    If neither of those occur, check if any other capture
    criteria are met (not part of standard weg game)."""

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        turn = self.game.turn

        if self.game.child[loc] is (not turn):

            capts = 2 if self.game.board[loc] >= 2 else 1
            self.game.board[loc] -= capts
            self.game.store[turn] += capts
            mdata.captured = True
            return

        if (self.game.board[loc] == self.game.info.child_cvt
                and self.game.owner[loc] is (not turn)):

            self.game.child[loc] = turn
            mdata.capt_changed = True
            return

        self.decorator.do_captures(mdata)


# %% pickers

# all one enum so only one of these can be used


class PickCross(CaptMethodIf):
    """Not a cross capture, but if there was a capture take any
    seeds from the opposite side of the board too."""

    def do_captures(self, mdata):

        self.decorator.do_captures(mdata)
        cross = self.game.cts.cross_from_loc(mdata.capt_loc)
        if (mdata.captured
                and self.game.child[cross] is None
                and self.game.unlocked[cross]):

            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[cross] = 0
            game_log.add(f"Picking Cross at {cross}.", game_log.INFO)


class PickOppTwos(CaptMethodIf):
    """When there is a capture pick all 2s from opponent."""

    def do_captures(self, mdata):

        self.decorator.do_captures(mdata)
        if mdata.captured:

            msg = ''
            for loc in self.game.cts.get_opp_range(self.game.turn):
                if (self.game.board[loc] == 2
                        and self.game.child[loc] is None
                        and self.game.unlocked[loc]):

                    msg += f' {loc}'
                    self.game.store[self.game.turn] += self.game.board[loc]
                    self.game.board[loc] = 0

            msg = 'Pick 2s from' + msg if msg else 'Pick 2s but None'
            game_log.add(msg, game_log.INFO)


# %% some wrappers

class NoSingleSeedCapt(CaptMethodIf):
    """Do not do captures with a single seed sow."""

    def do_captures(self, mdata):

        if mdata.seeds != 1:
            self.decorator.do_captures(mdata)


class RepeatTurn(CaptMethodIf):
    """Convert mdata.captured to REPEAT_TURN."""

    def do_captures(self, mdata):
        self.decorator.do_captures(mdata)
        if mdata.captured:
            game_log.add('Capture repeat turn', game_log.INFO)
            mdata.captured = WinCond.REPEAT_TURN


# %% build deco chains

def _add_cross_capt_deco(game, capturer):
    """Add the cross capture decorators to the capturer deco.
    crosscapt and multicapt is always captsamedir"""

    capturer = CaptCross(game, capturer)

    if game.info.xc_sown:
        capturer = CaptCrossVisited(game, capturer)

    if game.info.xcpickown == CrossCaptOwn.PICK_ON_CAPT:
        capturer = CaptCrossPickOwnOnCapt(game, capturer)

    elif game.info.xcpickown == CrossCaptOwn.ALWAYS_PICK:
        capturer = CaptCrossPickOwn(game, capturer)

    if game.info.multicapt:
        capturer = CaptContinueXCapt(game, capturer)

    return capturer


def _add_grand_slam_deco(game, capturer):
    """Add the grand slam decorators to the capturer deco."""

    if game.info.grandslam == GrandSlam.NO_CAPT:
        capturer = GSNone(game, capturer)

    elif game.info.grandslam in (GrandSlam.LEAVE_LEFT, GrandSlam.LEAVE_RIGHT):
        capturer = GSKeep(game, game.info.grandslam, capturer)

    elif game.info.grandslam == GrandSlam.OPP_GETS_REMAIN:
        capturer = GSOppGets(game, capturer)

    return capturer


def _add_child_deco(game, capturer):
    """Add a child handling deco if needed.
    only one child handler: weg/waldas/tuzdek/children"""

    if game.info.child_type == ChildType.WALDA:
        capturer =  CaptureToWalda(game, capturer)

    elif game.info.child_type == ChildType.ONE_CHILD:
        capturer = MakeTuzdek(game, capturer)

    elif game.info.child_type == ChildType.NORMAL:
        capturer = MakeChild(game, capturer)

    elif game.info.child_type == ChildType.WEG:
        capturer = MakeWegCapture(game, capturer)

    return capturer


def _add_capt_two_out_deco(game, capturer):
    """There are three flavors of capt two out:
    single lap, capture if sow in occupied hole, empty hole, occupied hole
    multi lap, sing capt: capture on empty hole, occupied hole
    multi lap, multi capt: capture on (empty hole, occupied hole) repeating

    MultiCaptTwoOut adds the CaptTwoOut child decorator."""

    if game.info.mlaps:
        if game.info.multicapt:
            capturer = MultiCaptTwoOut(game)
        else:
            capturer = CaptTwoOut(game, lambda _1, _2: True)
    else:
        capturer = CaptTwoOut(game, lambda seeds, _: seeds > 1)

    return capturer


def _add_capt_pick_deco(game, capturer):
    """Add any extra pickers."""

    if game.info.pickextra == CaptExtraPick.PICKCROSS:
        capturer = PickCross(game, capturer)

    elif game.info.pickextra == CaptExtraPick.PICKTWOS:
        capturer = PickOppTwos(game, capturer)

    return capturer


def deco_capturer(game):
    """Build capture chain and return it."""

    capturer = CaptNone(game)

    if game.info.crosscapt:
        capturer = _add_cross_capt_deco(game, capturer)

    elif game.info.capttwoout:
        # must check before mulitcapt
        capturer = _add_capt_two_out_deco(game, capturer)

    elif game.info.multicapt:
        capturer = CaptMultiple(game, capturer)

        if not game.info.capsamedir:
            capturer = CaptOppDirMultiple(game, capturer)

    elif game.info.capt_next:
        capturer = CaptNext(game)

    elif (game.info.evens or game.info.capt_on
          or game.info.capt_max or game.info.capt_min):
        capturer = CaptSingle(game)

    capturer = _add_grand_slam_deco(game, capturer)
    capturer = _add_child_deco(game, capturer)
    capturer = _add_capt_pick_deco(game, capturer)

    if game.info.nosinglecapt:
        capturer = NoSingleSeedCapt(game, capturer)

    if game.info.capt_rturn:
        capturer = RepeatTurn(game, capturer)

    return capturer
