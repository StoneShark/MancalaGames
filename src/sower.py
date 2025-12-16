# -*- coding: utf-8 -*-
"""Decos to preform the seed sowing step, that is, increment
around the game board, dropping one seed into each hole.

The incrementer deco is used to select the increment options.

Grouped into
    single sowers
    presow capture sowers
    continuer testers for mlap sowing
    end lap operations
    multilap sowers
    prescribed opening sowers

An interface is also provided to determine if an optional
animation message should be displayed at the game start.

Created on Fri Apr  7 15:57:47 2023
@author: Ann"""


# %% imports

import abc
import copy

import animator
import deco_chain_if
import game_info as gi
import incrementer

from game_logger import game_log


# %% constants

MAX_LAPS = 75


# %%  local incrementers


class SowIncBase(incrementer.IncrementerIf):
    """Need to use the base incrementer. Derived classes might
    change the incrementer so we need to look it up."""

    def incr(self, loc, direct, turn, start=incrementer.NOSKIPSTART):
        return self.game.deco.incr.incr(loc, direct, turn, start)


class SowIncPastMax(incrementer.IncrementerIf):
    """Skip past maxed holes using the main incrementer."""

    def __init__(self, game, max_seeds, decorator=None):

        super().__init__(game, decorator)
        self.max_seeds = max_seeds

    def incr(self, loc, direct, turn, start=incrementer.NOSKIPSTART):

        loc = self.game.deco.incr.incr(loc, direct, turn, start)
        while self.game.board[loc] >= self.max_seeds:
            loc = self.game.deco.incr.incr(loc, direct, turn, start)

        return loc


class SowIncPastOppSkips(incrementer.IncrementerIf):
    """Skip past values in skip_set using the main incrementer."""

    def __init__(self, game, skip_set, decorator=None):

        super().__init__(game, decorator)
        self.skip_set = skip_set

    def incr(self, loc, direct, turn, start=incrementer.NOSKIPSTART):

        loc = self.game.deco.incr.incr(loc, direct, turn, start)
        while (self.game.cts.opp_side(turn, loc)
               and self.game.board[loc] in self.skip_set):
            loc = self.game.deco.incr.incr(loc, direct, turn, start)

        return loc


class SowIncPastChild(incrementer.IncrementerIf):
    """Skip past childrenusing the main incrementer."""

    def incr(self, loc, direct, turn, start=incrementer.NOSKIPSTART):

        loc = self.game.deco.incr.incr(loc, direct, turn, start)
        while self.game.child[loc] is not None:
            loc = self.game.deco.incr.incr(loc, direct, turn, start)

        return loc


class SowIncPastOppChild(incrementer.IncrementerIf):
    """Skip past opposite children using the main incrementer."""

    def incr(self, loc, direct, turn, start=incrementer.NOSKIPSTART):

        loc = self.game.deco.incr.incr(loc, direct, turn, start)
        while self.game.child[loc] == (not turn):
            loc = self.game.deco.incr.incr(loc, direct, turn, start)

        return loc



# %%  sow interface

class SowMethodIf(deco_chain_if.DecoChainIf):
    """Interface for sowing."""

    @abc.abstractmethod
    def sow_seeds(self, mdata):
        """Sow seeds from mdata.cont_sow_loc.
        Update mdata.capt_start with the last sow location."""

    def get_single_sower(self):
        """Return the first non-lap sower in the deco chain.
        Used to decide if allowable test OPP_OR_EMPTY is met."""
        return self


# %%  base sower

class SowSeeds(SowMethodIf):
    """Basic sower.  Handles direction, skip_start and blocks
    (via the incr)."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        animator.do_flash(self.game.turn, loc=loc)
        for _ in range(mdata.seeds):

            loc = self.game.deco.incr.incr(loc,
                                           mdata.direct,
                                           mdata.player,
                                           mdata.cont_sow_loc)
            self.game.board[loc] += 1

        mdata.capt_start = loc


# %%  more single sowers

class SowIncrSeeds(SowMethodIf):
    """Sow methods that skip additional holes,
    accomplished by using a custom incrementer before
    calling the game.deco.incr (which must be done for
    the derived classes that patch the incrementer)."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        self.incr = self.expand_incr(game)
        self.rturn_test = self.choose_rturn_test(game)


    def __str__(self):

        return self.str_deco_detail('incr:  ' + str(self.incr))


    @staticmethod
    def expand_incr(game):
        """Select the incrementer wrapper for the SowRule."""

        if game.info.sow_rule == gi.SowRule.NO_SOW_OPP_NS:
            incr = SowIncPastOppSkips(game, {game.info.sow_param})

        elif game.info.sow_rule == gi.SowRule.MAX_SOW:
            incr = SowIncPastMax(game, game.info.sow_param)

        elif game.info.sow_rule == gi.SowRule.NO_CHILDREN:
            incr = SowIncPastChild(game)

        elif game.info.sow_rule == gi.SowRule.NO_OPP_CHILD:
            incr = SowIncPastOppChild(game)

        else:
            incr = SowIncBase(game)

        return incr


    @staticmethod
    def choose_rturn_test(game):
        """Choose the repeat turn test function."""
        # pylint: disable=unnecessary-lambda-assignment

        if game.info.sow_stores in (gi.SowStores.OWN,
                                    gi.SowStores.BOTH):
            rturn_test = lambda store, turn: True

        elif game.info.sow_stores == gi.SowStores.BOTH_NR_OPP:
            rturn_test = lambda store, turn: store == turn

        elif game.info.sow_stores == gi.SowStores.BOTH_NR_OWN:
            rturn_test = lambda store, turn: store == (not turn)

        else:
            rturn_test = lambda store, turn: False

        return rturn_test


    def sow_seeds(self, mdata):
        """Sow seeds."""

        turn = mdata.player
        start_loc = mdata.cont_sow_loc
        loc = mdata.cont_sow_loc
        animator.do_flash(self.game.turn, loc=loc)

        for _ in range(mdata.seeds):
            loc = self.incr.incr(loc, mdata.direct, turn, start_loc)
            self.game[loc] += 1

        if loc < 0 and (rturn := self.rturn_test(-loc - 1, turn)):
            mdata.repeat_turn = rturn
            game_log.add('Sow ended in store REPEAT TURN', game_log.INFO)

        mdata.capt_start = loc


class DivertSkipBlckdSower(SowMethodIf):
    """Divert blocked holes on opp side out of play (to store 0).
    Skip sowing blocked holes on own side of board.

    Don't use the incrementer because it will skip blocks.
    The option to select this is:  sow_rule: SOW_BLKD_DIV"""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        animator.do_flash(self.game.turn, loc=loc)

        seeds = mdata.seeds
        while seeds > 0:

            loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            while self.game.blocked[loc]:
                if self.game.cts.opp_side(self.game.turn, loc):

                    self.game.store[0] += 1
                    seeds -= 1
                    if not seeds:
                        mdata.capt_start = loc
                        return

                loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            self.game.board[loc] += 1
            seeds -= 1

        mdata.capt_start = loc


class SowClosed(SowMethodIf):
    """For SOW_BLKD_DIV without multilap sowing,
    check for closing, remove the final seeds
    from play (to store 0) and block the hole."""

    def __init__(self, game, not_right=False, decorator=None):
        super().__init__(game, decorator)
        if not_right:
            self.no_close = (game.cts.holes - 1, game.cts.dbl_holes - 1)
        else:
            self.no_close = set()

    def sow_seeds(self, mdata):
        """Sow seeds."""

        self.decorator.sow_seeds(mdata)
        loc = mdata.capt_start

        if (loc not in self.no_close
                and self.game.board[loc] == self.game.info.sow_param
                and self.game.cts.opp_side(self.game.turn, loc)
                and not self.game.inhibitor.stop_me_capt(self.game.turn)):

            seeds = self.game.board[loc]
            self.game.board[loc] = 0
            self.game.store[0] += seeds
            self.game.blocked[loc] = True


class SowEnPassant(SowMethodIf):
    """The en passant captures (also called passing captures).

    ENPAS enum name order is
        which holes, who gets non-final, who gets final (sower default)

    If the final seed goes to the owner and not the sower it must
    be done here, otherwise let the capturer do it."""

    def __init__(self, game, decorator=None):
        """Create a list of conditions (as lambda functions)
        to be tested for each hole sown.
        Prototype is cfunc(seed#, loc, turn)

        Define an captor function with prototype owner(loc, turn)"""

        super().__init__(game, decorator)
        self.conds = []

        self.cond_strs = []

        if game.info.sow_rule == gi.SowRule.ENPAS_SOW_SOWER:
            # restricted to sower's holes
            self.conds += [lambda scnt, loc, turn: turn == game.owner[loc]]
            self.cond_strs += ['turn == owner']

        if game.info.sow_rule == gi.SowRule.ENPAS_OPP_SOWER:
            # restricted to opponent's holes
            self.conds += [lambda scnt, loc, turn: turn != game.owner[loc]]
            self.cond_strs += ['turn != owner']

        if game.info.sow_rule in (gi.SowRule.ENPAS_ALL_OWNER_OWN,
                                  gi.SowRule.ENPAS_ALL_OWNER_SOW):
            self.captor = lambda loc, turn: game.owner[loc]
            self.take_str = 'owner'
        else:
            self.captor = lambda loc, turn: turn
            self.take_str = 'turn'

        if game.info.sow_rule != gi.SowRule.ENPAS_ALL_OWNER_OWN:
            # let the capturer do all but owner getting final capture
            self.conds += [lambda scnt, loc, turn: scnt > 1]
            self.cond_strs += ['seeds > 1']


    def __str__(self):

        detail = 'captor:  ' + self.take_str
        if self.cond_strs:
            detail += '\n   conds:  ' + ', '.join(self.cond_strs)

        return self.str_deco_detail(detail)


    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        animator.do_flash(self.game.turn, loc=loc)

        for scnt in range(mdata.seeds, 0, -1):

            loc = incr(loc, mdata.direct, mdata.player, mdata.cont_sow_loc)
            self.game.board[loc] += 1

            if (all(cfunc(scnt, loc, self.game.turn) for cfunc in self.conds)
                    and not self.game.inhibitor.stop_me_capt(self.game.turn)
                    and self.game.deco.capt_basic.capture_ok(mdata, loc)):

                captor = self.captor(loc, self.game.turn)
                game_log.step(f'Capture from {loc} by {captor}')
                seeds = self.game.board[loc]
                self.game.board[loc] = 0
                self.game.store[captor] += seeds

        mdata.capt_start = loc


class SowSkipOppChildUnlessFinal(SowMethodIf):
    """Skip sowing opponents children until the final seed."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        animator.do_flash(self.game.turn, loc=loc)

        for rem_seeds in range(mdata.seeds, 0, -1):

            loc = incr(loc, mdata.direct, mdata.player, mdata.cont_sow_loc)

            if rem_seeds > 1:
                while self.game.child[loc] == (not self.game.turn):
                    loc = incr(loc, mdata.direct, mdata.player,
                               mdata.cont_sow_loc)

            self.game.board[loc] += 1

        mdata.capt_start = loc


class SowOppCaptsLast(SowMethodIf):
    """A sower that wraps another sower until we are down to
    the last few seeds.

    When down to the last seeds (sow_param): seeds sown on the
    opponent's side are captured by the opponent. If the last
    seed would do a normal capture, the sower takes those seeds,
    including the last seed sown."""

    def sow_seeds(self, mdata):

        # use a base sower until down to the spec number of seeds
        if sum(self.game.board) > self.game.info.sow_param:
            self.decorator.sow_seeds(mdata)
            return

        incr = self.game.deco.incr.incr
        opp_side = self.game.cts.opp_side
        capt_basic = self.game.deco.capt_basic.capture_ok

        loc = mdata.cont_sow_loc
        animator.do_flash(self.game.turn, loc=loc)

        opp_took = 0
        for rem_seeds in range(mdata.seeds, 0, -1):

            loc = incr(loc, mdata.direct, mdata.player, mdata.cont_sow_loc)
            self.game.board[loc] += 1    # for capt_basic test

            if (opp_side(self.game.turn, loc)
                    and (rem_seeds > 1 or not capt_basic(mdata, loc))):
                self.game.board[loc] -= 1
                self.game.store[not self.game.turn] += 1
                opp_took += 1
                mdata.captured = True

        if opp_took:
            game_log.add(gi.PLAYER_NAMES[not self.game.turn] \
                         + f' takes own {opp_took}.',
                         game_log.DETAIL)

        mdata.capt_start = loc


# %% presow capture decorators

# captures occur after prescribed openings, (i.e. don't occur if
# there was a prescribed opening) and before the rest of the sower

# choosing not to set captured --
#   no repeat turn; Mancala doesn't need to print as changes logged below

class SCaptOne(SowMethodIf):
    """Take one seeds on the opening move."""

    def sow_seeds(self, mdata):

        self.game.store[self.game.turn] += 1
        mdata.seeds -= 1
        game_log.step('Presow Capt from lap', self.game, game_log.DETAIL)

        self.decorator.sow_seeds(mdata)


class SCaptCrossOnOne(SowMethodIf):
    """If one seed then capture any cross.
    SOW_START and XDRAW_1_XCAPT will capture the 1 drawn seed
    when there are two seeds in the start hole. Warning is produced."""

    def sow_seeds(self, mdata):

        cross = self.game.cts.cross_from_loc(mdata.cont_sow_loc)

        if (mdata.seeds == 1
            and self.game.board[cross]
            and self.game.child[cross] is None):

            seeds = self.game.board[cross]
            self.game.board[cross] = 0
            self.game.store[self.game.turn] += seeds

            game_log.step(f'Presow Capt Cross at {mdata.cont_sow_loc}',
                          self.game, game_log.DETAIL)
            animator.do_message(
                 f"Pre-Sow Captures across from {mdata.cont_sow_loc}")

        self.decorator.sow_seeds(mdata)


class SCaptCrossSingles(SowMethodIf):
    """Capture across from any holes that have a singleton"""

    def _messages(self, log):
        """Create the animation message and log it."""

        holes = self.game.cts.holes
        dholes = self.game.cts.dbl_holes
        slog = [str(loc + 1 if loc < holes else dholes - loc) for loc in log]

        if len(log) > 1:
            where = ', '.join(slog[:-1])
            where += ' & ' + str(slog[-1])
        else:
            where = str(slog[0])

        msg = f"Presow Captures across from 1s: {where}"
        game_log.step(msg, self.game, game_log.DETAIL)

        animator.do_message(msg)


    def sow_seeds(self, mdata):

        log = []

        for loc in self.game.cts.get_my_range(self.game.turn):
            cross = self.game.cts.cross_from_loc(loc)

            if (mdata.board[loc] == 1
                and self.game.board[cross]
                and self.game.child[cross] is None):

                seeds = self.game.board[cross]
                self.game.board[cross] = 0
                self.game.store[self.game.turn] += seeds
                log += [cross]

        if log:
            self._messages(log)

        self.decorator.sow_seeds(mdata)


# %% prescribed opening moves

# use prescribed openings if the first player has a choice
# if it's a standard pattern use start_pattern

class SowPrescribedIf(SowMethodIf):
    """A deco that does prescribed moves for one or more turns.
    Concrete subclasses should not provide sow_seeds.

    If count is > 1 apply it to the movers count--repeat turns are
    not counted as seperate moves and moves is inited to 1.

    Otherwise apply to mcount--every move include repeat turns."""

    def __init__(self, game, count, decorator=None):

        if not decorator:
            raise gi.GameInfoError(
                "Prescribed sowers must have follow-on decorators")

        super().__init__(game, decorator)
        self.dispose = count if count == 1 else (count - 1)
        self.cnt_attr = 'mcount' if count == 1 else 'movers'


    def __str__(self):

        return self.str_deco_detail('dispose:  ' + str(self.dispose)
                                    + '\n   cnt attr:  ' + self.cnt_attr)


    @abc.abstractmethod
    def do_prescribed(self, mdata):
        """Do the prescribed opening moves."""


    def sow_seeds(self, mdata):
        """If the decorator has expired, call the child sower."""

        if getattr(self.game, self.cnt_attr) > self.dispose:
            self.decorator.sow_seeds(mdata)
        else:
            game_log.add(f"Prescribed sower used: {self.__class__.__name__}")
            self.do_prescribed(mdata)


    def get_single_sower(self):
        """Get the non-prescribed single sower. Skip past
        the self and get the single sower of the next
        deco--there must be one because that's how prescribed
        sowers work.

        This is not what the allowables test wants  (for
        do_sow simulation), it should  not use it. Rules
        should prevent it.

        BearOff uses this to wrap the single sower."""

        return self.decorator.get_single_sower()


class SowPresSowerMixin:
    """A mixin to print the sower deco used for the
    prescribed sow."""

    sower = None

    def __str__(self):

        return self.str_deco_detail('sower:  ' + str(self.sower))


class SowBasicFirst(SowPresSowerMixin, SowPrescribedIf):
    """Use the default basic sower for the first sows."""

    def __init__(self, game, count, decorator=None):
        super().__init__(game, count, decorator)
        self.sower = SowSeeds(game)


    def do_prescribed(self, mdata):
        self.sower.sow_seeds(mdata)


class SowOneOpp(SowPrescribedIf):
    """The last seed must be on the opponents side of the board
    skip our own holes, if required, to make that happen."""

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        incer = self.game.deco.incr.incr

        for _ in range(mdata.seeds - 1):

            loc = incer(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1

        loc = incer(loc, mdata.direct, mdata.cont_sow_loc)
        while not self.game.cts.opp_side(self.game.turn, loc):
            loc = incer(loc, mdata.direct, mdata.cont_sow_loc)
        self.game.board[loc] += 1

        mdata.capt_start = loc


class SowPlus1Minus1Capt(SowPrescribedIf):
    """Starting after the selected move one seed forward
    in every other hole."""

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        self.game.board[loc] = mdata.seeds
        incer = self.game.deco.incr.incr

        add_one = False
        while True:
            loc = incer(loc, mdata.direct, mdata.cont_sow_loc)
            if loc == mdata.cont_sow_loc:
                break
            self.game.board[loc] += 1 if add_one else -1
            add_one = not add_one

        cross = self.game.cts.cross_from_loc(mdata.cont_sow_loc)
        self.game.board[cross] += 1

        mdata.capt_start = cross


class SowNoUdirFirsts(SowPrescribedIf):
    """For the prescribed sows, only sow in the direction
    of the base game, no UDIR sowing."""

    def do_prescribed(self, mdata):

        mdata.direct = self.game.info.sow_direct
        self.decorator.sow_seeds(mdata)


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

        loc = self.game.deco.incr.incr(mdata.capt_start,
                                       mdata.direct,
                                       mdata.player)
        if self.game[loc]:
            mdata.capt_start = loc
            return True
        return False


class DivertBlckdLapper(LapContinuerIf):
    """Continue sowing if we ended on a blocked hole
    (will be opp side, i.e. last seed was taken out
     of play)."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""
        return not self.game.blocked[mdata.capt_start]


class StopMakeChild(LapContinuerIf):
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
            return False

        return self.decorator.do_another_lap(mdata)


class StopSingleSeed(LapContinuerIf):
    """A wrapper: stop if there is zero or one seed
    (the one we just sowed)."""

    def do_another_lap(self, mdata):

        if self.game[mdata.capt_start] <= 1:
            game_log.add('MLap stop single seed')
            return False
        return self.decorator.do_another_lap(mdata)


class GapNextCapt(LapContinuerIf):
    """A wrapper: if the final seed falls in an occupied house,
    possibly do a capture, then continue sowing from
    the current hole (capture or not).

    mdata.capt_start must be returned to the location that
    it started, so the sowing continues from there."""

    def do_another_lap(self, mdata):

        if self.game[mdata.capt_start] > 1:
            saved_loc = mdata.capt_start
            self.game.capture_seeds(mdata)

            mdata.capt_start = saved_loc
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

        if mdata.capt_start < 0 or self.game.board[mdata.capt_start] != 1:
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

    Need to use capt_basic to test for the capture, because
    the previous sowing might have already set mdata.captured
    via LAP_CAPT_OPP_GETS."""

    def do_another_lap(self, mdata):

        if not self.game.deco.capt_basic.capture_ok(mdata, mdata.capt_start):
            return self.decorator.do_another_lap(mdata)

        self.game.capture_seeds(mdata)
        mdata.capt_start = self.game.deco.incr.incr(mdata.capt_start,
                                                    mdata.direct,
                                                    mdata.player)
        return True


class StopOnChild(LapContinuerIf):
    """A wrapper: stop if the sow would continue from a child."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        if game.info.mlaps == gi.LapSower.LAPPER_NEXT:
            self.test_loc = lambda mdata: self.game.deco.incr.incr(mdata.capt_start,
                                                                   mdata.direct,
                                                                   mdata.player)
        else:
            self.test_loc = lambda mdata: mdata.capt_start

    def do_another_lap(self, mdata):

        test_loc = self.test_loc(mdata)

        if (mdata.capt_start >= 0
                and self.game.child[test_loc] is not None):
            game_log.add('MLap stop in child')
            return False

        return self.decorator.do_another_lap(mdata)


class ContWithCaptSeeds(LapContinuerIf):
    """A wrapper: check if there is a capture.
    If did a capture, continue lap with the seeds captured
    along with the seeds from the last hole sown.

    The stores are not in play, so all seeds collected
    in a store during the capture are put back into play.

    mdata.captured must be left set to whether a capture
    has occured during the sow. If it was previously set,
    it must stay set, even if we don't do a capture now."""

    def do_another_lap(self, mdata):

        saved = mdata.captured
        mdata.captured = False              # temp clear for test

        with animator.one_step():
            self.game.capture_seeds(mdata)

            if mdata.captured:
                self.game.board[mdata.capt_start] += \
                    self.game.store[self.game.turn]
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
                and self.game.deco.capt_basic.capture_ok(mdata, mdata.capt_start)):
            game_log.add('MLap stop for capture')
            return False
        return self.decorator.do_another_lap(mdata)


class StopXCapt(LapContinuerIf):
    """Stop if we can do a cross capture.
    Only use this with lapper_next (instead of StopSingleSeed)."""

    def do_another_lap(self, mdata):

        cross = self.game.cts.cross_from_loc(mdata.capt_loc)

        if (mdata.capt_start >= 0
                and self.game.board[mdata.capt_start] == 1
                and self.game.deco.capt_basic.capture_ok(mdata, cross)):
            game_log.add('MLap stop for cross capture')
            return False
        return self.decorator.do_another_lap(mdata)


class StopCaptureSimul(LapContinuerIf):
    """A wrapper: stop based on simulated capture.
    Use this instead of StopCaptureSeeds when capt_basic
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

    def stop_check(self, mdata):
        """Check the stop conditions sequentially, doing as little
        work as possible."""

        # not first lap
        if mdata.lap_nbr:
            return False

        # first lap ended on opposite side
        if self.game.cts.opp_side(self.game.turn, mdata.capt_start):
            return False

        # there are more seeds than at the start in any hole on opp side
        opp_range = self.game.cts.get_opp_range(self.game.turn)
        if any(self.game.board[loc] > mdata.board[loc] for loc in opp_range):
            return False

        return True


    def do_another_lap(self, mdata):

        if self.stop_check(mdata):
            game_log.add("First mlap didn't reach opp")
            return False

        return self.decorator.do_another_lap(mdata)


class StopNotN(LapContinuerIf):
    """A wrapper: Stop if the number of seeds in the final sown hole
    does not equal sow_param seeds."""

    def do_another_lap(self, mdata):

        if self.game[mdata.capt_start] != self.game.info.mlap_param:
            game_log.add(f"Stop mlap not {self.game.info.mlap_param} seeds")
            return False

        return self.decorator.do_another_lap(mdata)


class StopLessN(LapContinuerIf):
    """A wrapper: Stop if the number of seeds in the final sown hole
    is less than sow_param seeds."""

    def do_another_lap(self, mdata):

        if self.game[mdata.capt_start] < self.game.info.mlap_param:
            game_log.add(f"Stop mlap < {self.game.info.mlap_param} seeds")
            return False

        return self.decorator.do_another_lap(mdata)


class StopNotSide(LapContinuerIf):
    """A wrapper: Stop mlap'ing based on side of the board."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        if game.info.mlap_cont == gi.SowLapCont.OWN_SIDE:
            self.test_func = self.game.cts.opp_side
            self.side = 'opposite'
        else:
            self.test_func = self.game.cts.my_side
            self.side = 'own'


    def __str__(self):
        """A recursive func to print the whole decorator chain."""

        return self.str_deco_detail(f'Stop side: {self.side}')


    def do_another_lap(self, mdata):

        if self.test_func(self.game.turn, mdata.capt_start):
            game_log.add(f"Stop when last hole is on {self.side} side.")
            return False

        return self.decorator.do_another_lap(mdata)


class StopStore(LapContinuerIf):
    """A wrapper: two enums supported:
    STOP_STORE: stop if the last seed lands in the store
    NOT_FROM_STORE: stop if the lap sower would continue from
    the store (this is only different from the above condition
    for LAPPER_NEXT)."""

    def __init__(self, game, decorator):

        super().__init__(game, decorator)
        if (game.info.mlap_cont == gi.SowLapCont.NOT_FROM_STORE
                and game.info.mlaps == gi.LapSower.LAPPER_NEXT):
            self.test_loc = lambda mdata: self.game.deco.incr.incr(mdata.capt_start,
                                                                   mdata.direct,
                                                                   mdata.player)
        else:
            self.test_loc = lambda mdata: mdata.capt_start

    def do_another_lap(self, mdata):

        if self.test_loc(mdata) < 0:
            return False
        return self.decorator.do_another_lap(mdata)


class StopNoOppSeeds(LapContinuerIf):
    """A wrapper to stop MLAP sowing when the opponent does
    not have any seeds.

    Automatically included for any LAP_CAPT sow rule without
    stores."""

    def do_another_lap(self, mdata):

        opp_range = self.game.cts.get_opp_range(self.game.turn)
        if not any(self.game.board[loc] for loc in opp_range):
            game_log.add('MLap stopped, opp has no seeds.')
            return False

        return self.decorator.do_another_lap(mdata)


class StopRepeatTurn(LapContinuerIf):
    """A wrapper: stop if we know it's a repeat turn.
    This must be at the top so we don't try to use
    REPEAT_TURN as an index."""

    def do_another_lap(self, mdata):

        if mdata.repeat_turn:
            game_log.add('MLap stop for for repeat turn')
            return False
        return self.decorator.do_another_lap(mdata)


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

        loc = mdata.capt_start
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

class MlapSowerIf(SowMethodIf):
    """An interface and init for mlap sowers."""

    def __init__(self, game, decorator, lap_cont, end_lap_op):

        super().__init__(game, decorator)
        self.lap_cont = lap_cont
        self.end_lap_op = end_lap_op

    def __str__(self):
        """Added lap continuer and end lap op to the string."""

        return self.str_deco_detail(
            '\n   '.join(['lap cont:  ' + str(self.lap_cont),
                          'end l op:  ' + str(self.end_lap_op)]))


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
                loc = mdata.capt_start
                mdata.cont_sow_loc = loc
                mdata.seeds = self.game[loc]

                self.end_lap_op.do_op(mdata)
                self.game[loc] = 0
                mdata.lap_nbr += 1

            else:
                return

        mdata.capt_start = gi.WinCond.ENDLESS


# %% prescribed mlap sower

class SowMlapsFirst(SowPresSowerMixin, SowPrescribedIf):
    """Use the default mlap sower for the first sows."""

    def __init__(self, game, count, decorator=None):
        super().__init__(game, count, decorator)
        sower = SowSeeds(game)
        lap_cont = StopSingleSeed(game, LapContinue(game))
        self.sower = SowMlapSeeds(game, sower, lap_cont, NoOp(game))


    def do_prescribed(self, mdata):
        self.sower.sow_seeds(mdata)


# %% build deco chain

def _add_blkd_divert_sower(game):
    """Implement the sow_blkd_div sower.
    When sowing seeds, blocked holes on own side of the board are
    skipped and seeds for blocked opponent holes are diverted out
    of play (actually store 0)."""

    sower = DivertSkipBlckdSower(game)
    if game.info.mlaps == gi.LapSower.OFF:
        sower = SowClosed(game,
                          game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV_NR,
                          sower)
    return sower


def _add_base_sower(game):
    """Choose the base sower."""
    # pylint: disable=too-complex
    # pylint: disable=too-many-branches

    sower = None
    if game.info.sow_rule:
        if game.info.sow_rule in (gi.SowRule.SOW_BLKD_DIV,
                                  gi.SowRule.SOW_BLKD_DIV_NR):
            sower = _add_blkd_divert_sower(game)

        elif game.info.sow_rule.is_en_passant():
            sower = SowEnPassant(game)

        elif game.info.sow_rule in (gi.SowRule.NO_SOW_OPP_NS,
                                    gi.SowRule.MAX_SOW,
                                    gi.SowRule.NO_OPP_CHILD,
                                    gi.SowRule.NO_CHILDREN):
            sower = SowIncrSeeds(game)

        elif game.info.sow_rule == gi.SowRule.OPP_CHILD_ONLY1:
            sower = SowSkipOppChildUnlessFinal(game)

        elif game.info.sow_rule == gi.SowRule.LAP_CAPT_OPP_GETS:
            sower = SowSeeds(game)
            sower = SowOppCaptsLast(game, sower)

        elif game.info.sow_rule in (gi.SowRule.CHANGE_DIR_LAP,
                                    gi.SowRule.LAP_CAPT,
                                    gi.SowRule.LAP_CAPT_SEEDS):
            pass    # pick a base sower below

        else:
            raise NotImplementedError(
                    f"SowRule {game.info.sow_rule} not implemented.")

    if not sower:
        if game.info.sow_stores:
            sower = SowIncrSeeds(game)

        else:
            sower = SowSeeds(game)

    return sower


def _add_pre_sow_capt(game, sower):
    """Add a presow capturer."""

    if game.info.presowcapt == gi.PreSowCapt.CAPT_ONE:
        sower = SCaptOne(game, sower)

    elif game.info.presowcapt == gi.PreSowCapt.ALL_SINGLE_XCAPT:
        sower = SCaptCrossSingles(game, sower)

    elif game.info.presowcapt == gi.PreSowCapt.DRAW_1_XCAPT:
        sower = SCaptCrossOnOne(game, sower)

    else:
        raise NotImplementedError(
                f"PreSowCapt {game.info.presowcapt} not implemented.")

    return sower


def _add_lapt_capt_cont(game, lap_cont):
    """Add the lapt deco's.

    LAP_CONT rules without stores always include a
    StopNoOppSeeds to prevent an endless sow preventing a
    win condition."""

    if game.info.sow_rule in (gi.SowRule.LAP_CAPT,
                              gi.SowRule.LAP_CAPT_OPP_GETS):

        if game.info.crosscapt == gi.XCaptType.ONE_ZEROS:
            lap_cont = ContIfXCapt(game, lap_cont)

        elif game.info.capt_type in (gi.CaptType.NEXT,
                                     gi.CaptType.TWO_OUT):
            lap_cont = GapNextCapt(game, lap_cont)

        else:   # if basic_capt:
            lap_cont = ContIfBasicCapt(game, lap_cont)

    elif game.info.sow_rule == gi.SowRule.LAP_CAPT_SEEDS:
        lap_cont = ContWithCaptSeeds(game, lap_cont)

    if (not game.info.stores
            and game.info.sow_rule in (gi.SowRule.LAP_CAPT,
                                       gi.SowRule.LAP_CAPT_OPP_GETS,
                                       gi.SowRule.LAP_CAPT_SEEDS)):
        lap_cont = StopNoOppSeeds(game, lap_cont)

    return lap_cont


def _add_capt_stop_lap_cont(game, lap_cont):
    """Add the stop on 1 and then, one of the lap capture
    lap-continuer or a stop on capture decos."""

    if game.info.mlaps == gi.LapSower.LAPPER_NEXT:
        if game.info.crosscapt in (gi.XCaptType.ONE_ZEROS,
                                   gi.XCaptType.ONE_ANY):
            lap_cont = StopXCapt(game, lap_cont)

    if game.info.capt_type in (gi.CaptType.NEXT,
                               gi.CaptType.TWO_OUT,
                               gi.CaptType.SINGLETONS,
                               gi.CaptType.CAPT_OPP_1CCW,
                               gi.CaptType.PASS_STORE_CAPT,
                               gi.CaptType.PULL_ACROSS,
                               gi.CaptType.END_OPP_STORE_CAPT):
        # no additional stopping criteria
        pass

    elif game.info.capt_type in (gi.CaptType.MATCH_OPP,
                                 gi.CaptType.SANDWICH_CAPT):
        lap_cont = StopCaptureSimul(game, lap_cont)

    elif game.info.basic_capt and not game.info.crosscapt:
        lap_cont = StopCaptureSeeds(game, lap_cont)

    return lap_cont


def _add_mlap_cont_decos(game, lap_cont):
    """Add any lap continuer wrapper decorators."""

    if game.info.mlap_cont == gi.SowLapCont.VISIT_OPP:
        lap_cont = MustVisitOpp(game, lap_cont)

    elif game.info.mlap_cont == gi.SowLapCont.ON_PARAM:
        lap_cont = StopNotN(game, lap_cont)

    elif game.info.mlap_cont == gi.SowLapCont.GREQ_PARAM:
        lap_cont = StopLessN(game, lap_cont)

    elif game.info.mlap_cont in (gi.SowLapCont.OWN_SIDE,
                                 gi.SowLapCont.OPP_SIDE):
        lap_cont = StopNotSide(game, lap_cont)

    elif game.info.mlap_cont in (gi.SowLapCont.STOP_STORE,
                                 gi.SowLapCont.NOT_FROM_STORE):
        lap_cont = StopStore(game, lap_cont)

    return lap_cont


def _build_lap_cont(game):
    """Choose a base lap continuer, then add any wrappers."""

    if game.info.mlaps == gi.LapSower.LAPPER:

        if game.info.sow_rule in (gi.SowRule.SOW_BLKD_DIV,
                                  gi.SowRule.SOW_BLKD_DIV_NR):
            lap_cont = DivertBlckdLapper(game)
        else:
            lap_cont = LapContinue(game)
        lap_cont = StopSingleSeed(game, lap_cont)

    elif game.info.mlaps == gi.LapSower.LAPPER_NEXT:
        lap_cont = NextLapCont(game)

    else:
        raise NotImplementedError(
            f"LapSower {game.info.mlaps} not implemented.")

    if game.info.child_type.child_but_not_ram():
        lap_cont = StopMakeChild(game, lap_cont)

    lap_cont = _add_capt_stop_lap_cont(game, lap_cont)

    if game.info.mlaps == gi.LapSower.LAPPER:
        lap_cont = _add_lapt_capt_cont(game, lap_cont)

    if game.info.child_type.child_but_not_ram():
        lap_cont = StopOnChild(game, lap_cont)

    lap_cont = _add_mlap_cont_decos(game, lap_cont)

    if game.info.sow_stores and game.info.repeat_turn:
        lap_cont = StopRepeatTurn(game, lap_cont)

    return lap_cont


def _add_mlap_sower(game, sower):
    """Build the deco chain elements for multiple lap sowing.
    Choose:
        1. an op to perform between laps
        2. a lap continue tester
    then build the mlap sower. Wrap if needed, with Visited."""

    if game.info.sow_rule == gi.SowRule.CHANGE_DIR_LAP:
        end_op = DirChange(game)
    elif game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV:
        end_op = CloseOp(game)
    elif game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV_NR:
        end_op = CloseOp(game, True)
    else:
        end_op = NoOp(game)

    lap_cont = _build_lap_cont(game)
    sower = SowMlapSeeds(game, sower, lap_cont, end_op)

    return sower


def _add_prescribed_sower(game, sower):
    """Add the prescribed sowers to the deco chain."""

    if game.info.prescribed == gi.SowPrescribed.SOW1OPP:
        sower = SowOneOpp(game, 2, sower)

    elif game.info.prescribed == gi.SowPrescribed.PLUS1MINUS1:
        sower = SowPlus1Minus1Capt(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.BASIC_SOWER:
        sower = SowBasicFirst(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.MLAPS_SOWER:
        sower = SowMlapsFirst(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT:
        pass    # sower deco not needed

    elif game.info.prescribed == gi.SowPrescribed.NO_UDIR_FIRSTS:
        sower = SowNoUdirFirsts(game, 2, sower)

    else:
        raise NotImplementedError(
                f"SowPrescribed {game.info.prescribed} not implemented.")

    return sower


def deco_sower(game):
    """Build the sower chain."""

    sower = _add_base_sower(game)

    if game.info.presowcapt != gi.PreSowCapt.NONE:
        sower = _add_pre_sow_capt(game, sower)

    if game.info.mlaps != gi.LapSower.OFF:
        sower = _add_mlap_sower(game, sower)

    if game.info.prescribed != gi.SowPrescribed.NONE:
        sower = _add_prescribed_sower(game, sower)

    return sower


# %% start ani message

def start_ani_msg(game):
    """Do a start message for a prescribed opening."""

    if game.info.prescribed == gi.SowPrescribed.SOW1OPP:
        animator.do_message("Prescribed Opening Sow 1 Opposite")

    elif game.info.prescribed == gi.SowPrescribed.PLUS1MINUS1:
        animator.do_message("Prescribed Opening Plus 1 Minus 1")

    elif game.info.prescribed == gi.SowPrescribed.NO_UDIR_FIRSTS:
        animator.do_message(f"First two moves as sown {game.info.sow_direct.name}")
