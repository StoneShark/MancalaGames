# -*- coding: utf-8 -*-
"""Preform the seed sowing step, that is, increment around
the game board, dropping one seed into each hole.
This file contains the mlap sower and supporting end of lap
ops and lap continuers that decided when to stop lap sowing.

For the multi lap sowers, sowing is terminated after MAX_LAPS
sows returning an error condition.

Created on Fri Apr  7 15:57:47 2023
@author: Ann"""


# %% imports

import abc
import copy

import animator
import deco_chain_if
import game_interface as gi
import sower_decos as sowd

from game_logger import game_log

# %% constants

MAX_LAPS = 75


# %%  lap continue testers

class LapContinuerIf(deco_chain_if.DecoChainIf):
    """Interface for the algorithms that determine if
    sowing should continue."""

    def do_another_lap(self, mdata):
        """Return True if we should continue sowing, False otherwise."""


class LapContinue(LapContinuerIf):
    """A base lap continuer, always continue.
    Wrappers test for other stop conditions."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""
        return True


class NextLapCont(LapContinuerIf):
    """Continue sowing based on seeds being in the next
    hole. If there are any, continue from there.
    This should not be wrapped with StopSingleSeed.

    Laurence Russ calls this Indian Style lapping."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""

        loc = self.game.deco.incr.incr(mdata.capt_loc, mdata.direct)
        if self.game.board[loc]:
            mdata.capt_loc = loc
            return True
        return False


class DivertBlckdLapper(LapContinuerIf):
    """Continue sowing if we ended on a blocked hole
    (will be opp side, i.e. last seed was taken out
     of play)."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""
        return not self.game.blocked[mdata.capt_loc]


class ChildLapCont(LapContinuerIf):
    """Multilap sow in the presence/creation of children:
    Stop sowing if we should make a child.

    Mohr's book states that a turn ends when 'any' seed is sown
    into a child (in rules for Bao), but it doesn't describe
    what to do with the remaining seeds; therefore this
    condition is not implemented here. Russ's book confirms this
    p 44, first paragraph, but he also doesn't describe what to do
    with the remaining seeds."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""
        make_child = self.game.deco.make_child.test(mdata)
        if make_child:
            game_log.add('MLap stop to make child')
        return not make_child


class StopSingleSeed(LapContinuerIf):
    """A wrapper: stop if there is zero or one seed
    (the one we just sowed)."""

    def do_another_lap(self, mdata):

        if self.game.board[mdata.capt_loc] <= 1:
            game_log.add('MLap stop single seed')
            return False
        return self.decorator.do_another_lap(mdata)


class GapNextCapt(LapContinuerIf):
    """A wrapper: if the final seed falls in an occupied house,
    possibly do a capture, then continue sowing from
    the current hole (capture or not).

    mdata.capt_loc must be returned to the location that
    it started, so the sowing continues from there."""

    def do_another_lap(self, mdata):

        if self.game.board[mdata.capt_loc] > 1:
            saved_loc = mdata.capt_loc
            self.game.capture_seeds(mdata)

            mdata.capt_loc = saved_loc
            return True

        return self.decorator.do_another_lap(mdata)


class ContIfXCapt(LapContinuerIf):
    """A wrapper: if there is one seed
    (the one we just sowed), and possibly do a capture.
    If did a capture, continue lap with the one seed sown.

    mdata.captured must be left set to whether a capture
    has occured during the sow. If it was previously set,
    it must stay set, even if we don't do a capture now."""

    def do_another_lap(self, mdata):

        if self.game.board[mdata.capt_loc] != 1:
            return self.decorator.do_another_lap(mdata)

        saved = mdata.captured
        mdata.captured = False              # temp clear for test
        self.game.capture_seeds(mdata)

        cont = mdata.captured
        mdata.captured |= saved
        if cont:
            game_log.add('MLap continues, captured.')
        else:
            game_log.add('MLap stop--no cross capture.')

        return cont


class ContIfBasicCapt(LapContinuerIf):
    """A wrapper: Attempt a basic capture.

    Use only with basic captures alone.  Do not use if
    combined with other capture types.
    If did a capture, continue lapping with the next hole.

    Need to use capt_ok to test for the capture, because
    the previous sowing might have already set mdata.captured
    via LAP_CAPT_OPP_GETS."""

    def do_another_lap(self, mdata):

        if not self.game.deco.capt_ok.capture_ok(mdata, mdata.capt_loc):
            return self.decorator.do_another_lap(mdata)

        self.game.capture_seeds(mdata)
        mdata.capt_loc = self.game.deco.incr.incr(mdata.capt_loc,
                                                  mdata.direct)
        return True


class StopOnChild(LapContinuerIf):
    """A wrapper: stop if we've ended in a child."""

    def do_another_lap(self, mdata):

        if self.game.child[mdata.capt_loc] is not None:
            game_log.add('MLap stop in child')
            return False
        return self.decorator.do_another_lap(mdata)


class ContWithCaptSeeds(LapContinuerIf):
    """A wrapper: check if there is a capture.
    If did a capture, continue lap with the seeds captured
    along with the seeds from the last hole sown.

    mdata.captured must be left set to whether a capture
    has occured during the sow. If it was previously set,
    it must stay set, even if we don't do a capture now."""

    def do_another_lap(self, mdata):

        saved = mdata.captured
        mdata.captured = False              # temp clear for test

        with animator.one_step():
            self.game.capture_seeds(mdata)

            if mdata.captured:
                self.game.board[mdata.capt_loc] += self.game.store[self.game.turn]
                self.game.store[self.game.turn] = 0
                game_log.add('MLap continues with captured seeds.')
                return True

        mdata.captured |= saved
        return self.decorator.do_another_lap(mdata)


class StopCaptureSeeds(LapContinuerIf):
    """A wrapper: stop if we should capture.
    Doesn't need to check for cross-capture because we stop
    on a single seed."""

    def do_another_lap(self, mdata):

        if (not self.game.inhibitor.stop_me_capt(self.game.turn)
                and self.game.deco.capt_ok.capture_ok(mdata, mdata.capt_loc)):
            game_log.add('MLap stop for capture')
            return False
        return self.decorator.do_another_lap(mdata)


class StopCaptureSimul(LapContinuerIf):
    """A wrapper: stop based on simulated capture.
    Use this instead of StopCaptureSeeds when capt_ok
    or StopSingleSeeds are not enough to stop for capture."""

    def do_another_lap(self, mdata):

        if not self.game.inhibitor.stop_me_capt(self.game.turn):

            with self.game.save_restore_state():
                with animator.animate_off():
                    working_mdata = copy.copy(mdata)

                    self.game.capture_seeds(working_mdata)
                    captured = working_mdata.captured

                if captured:
                    game_log.add('MLap stop for simul capture')
                    return False
        return self.decorator.do_another_lap(mdata)


class MustVisitOpp(LapContinuerIf):
    """A wrapper: on the first lap sow, must reach the
    opposite side of the board. In otherwords, a second lap may not
    be started on a players side of the board, unless they have
    passed through the opponents side of the board."""

    def do_another_lap(self, mdata):

        if (not mdata.lap_nbr
                and not (mdata.seeds >= self.game.cts.holes
                         or self.game.cts.opp_side(self.game.turn,
                                                   mdata.capt_loc))):
            game_log.add("First mlap didn't reach opp")
            return False

        return self.decorator.do_another_lap(mdata)


class StopNotN(LapContinuerIf):
    """A wrapper: Stop if the number of seeds in the final sown hole
    does not equal sow_param seeds."""

    def do_another_lap(self, mdata):

        if self.game.board[mdata.capt_loc] != self.game.info.sow_param:
            game_log.add(f"Stop mlap not {self.game.info.sow_param} seeds")
            return False

        return self.decorator.do_another_lap(mdata)


class StopLessN(LapContinuerIf):
    """A wrapper: Stop if the number of seeds in the final sown hole
    is less than sow_param seeds."""

    def do_another_lap(self, mdata):

        if self.game.board[mdata.capt_loc] < self.game.info.sow_param:
            game_log.add(f"Stop mlap < {self.game.info.sow_param} seeds")
            return False

        return self.decorator.do_another_lap(mdata)


class StopRepeatTurn(LapContinuerIf):
    """A wrapper: stop if we know it's a repeat turn.
    This must be at the top so we don't try to use
    REPEAT_TURN as an index."""

    def do_another_lap(self, mdata):

        if mdata.capt_loc is gi.WinCond.REPEAT_TURN:
            game_log.add('MLap stop for for repeat turn')
            return False
        return self.decorator.do_another_lap(mdata)


class AnimateLapStart(LapContinuerIf):
    """A wrapper: do an animation to simulate a new lap start,
    but don't do any other animation in the do_another_lap
    test."""

    def do_another_lap(self, mdata):

        cont = self.decorator.do_another_lap(mdata)

        if cont and animator.active():
            animator.animator.flash(self.game.turn, loc=mdata.capt_loc)

        return cont


# %% operations for each end of lap

class MlapEndOpIf(abc.ABC):
    """An interface for the end of lap operations.
    These are not decorators, one class does the whole operation."""

    def __init__(self, game):
        self.game = game

    def do_op(self, mdata):
        """Do the operation, no return value."""


class NoOp(MlapEndOpIf):
    """No operation"""

    def do_op(self, mdata):
        _ = mdata


class CloseOp(MlapEndOpIf):
    """Test for and close the hole by marking it as blocked."""

    def __init__(self, game, not_right=False):
        super().__init__(game)
        if not_right:
            self.no_close = (game.cts.holes - 1, game.cts.dbl_holes - 1)
        else:
            self.no_close = set()


    def do_op(self, mdata):
        # pylint:  disable=duplicate-code

        loc = mdata.capt_loc
        if (loc not in self.no_close
                and self.game.board[loc] == self.game.info.sow_param
                and self.game.cts.opp_side(self.game.turn, loc)
                and not self.game.inhibitor.stop_me_capt(self.game.turn)):
            self.game.blocked[loc] = True


class DirChange(MlapEndOpIf):
    """Change direction on each lap."""

    def do_op(self, mdata):
        mdata.direct = mdata.direct.opp_dir()


# %%  mlap sowers

class MlapSowerIf(sowd.SowMethodIf):
    """An interface and init for mlap sowers."""

    def __init__(self, game, decorator, lap_cont, end_lap_op):

        super().__init__(game, decorator)
        self.lap_cont = lap_cont
        self.end_lap_op = end_lap_op

    def __str__(self):
        """Added lap continuer and end lap op to the string."""

        my_str = '\n   '.join([repr(self),
                               'lap cont:  ' + str(self.lap_cont),
                               'end l op:  ' + str(self.end_lap_op)])

        if self.decorator:
            return my_str + '\n' + str(self.decorator)
        return my_str  # pragma: no coverage

    def get_single_sower(self):
        """Return the first non-lap sower in the deco chain."""
        return self.decorator.get_single_sower()


class SowMlapSeeds(MlapSowerIf):
    """Do sow operations until until lap continuer test tells
    us to stop. An optional operation is performed between
    each lap (use NoOp to do nothing).

    The extended deco chain sows from each starting hole.
    Here we only decide if we should continue with sowing from
    the ending hole."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        for _ in range(MAX_LAPS):

            self.decorator.sow_seeds(mdata)
            game_log.step(f'Mlap {mdata.lap_nbr} sow from {loc}',
                          self.game, game_log.DETAIL)

            if self.lap_cont.do_another_lap(mdata):
                loc = mdata.capt_loc
                mdata.cont_sow_loc = loc
                mdata.seeds = self.game.board[loc]

                self.end_lap_op.do_op(mdata)
                self.game.board[loc] = 0
                mdata.lap_nbr += 1

            else:
                return

        mdata.capt_loc = gi.WinCond.ENDLESS


# %% prescribed mlap sower


class SowMlapsFirst(sowd.SowPrescribedIf):
    """Use the default mlap sower for the first sows."""

    def __init__(self, game, count, decorator=None):
        super().__init__(game, count, decorator)
        sower = sowd.SowSeeds(game)
        lap_cont = StopSingleSeed(game, LapContinue(game))
        self.sower = SowMlapSeeds(game, sower, lap_cont, NoOp(game))

    def do_prescribed(self, mdata):
        self.sower.sow_seeds(mdata)
