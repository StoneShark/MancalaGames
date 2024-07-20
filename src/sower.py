# -*- coding: utf-8 -*-
"""Preform the seed sowing step, that is, increment around
the game board, dropping one seed into each hole.

Any 'soft' direction (e.g. split, user choice) has already been
translated to clockwise or counter-clockwise (i.e. CW or CCW).
The sow_starter deco chain has already adjusted the start hole
contents and determined the number of seeds to sow.

The incrementer deco is used to select the increment options.

For the multi lap sowers, sowing is terminated after MAX_LAPS
sows returning an error condition.

Created on Fri Apr  7 15:57:47 2023
@author: Ann"""


# %% imports

import abc

import deco_chain_if
import game_interface as gi

from game_logger import game_log


# %% constants

MAX_LAPS = 50


# %%  sow interface

class SowMethodIf(deco_chain_if.DecoChainIf):
    """Interface for sowing."""

    @abc.abstractmethod
    def sow_seeds(self, mdata):
        """Sow seeds from mdata.cont_sow_loc.
        Update mdata.capt_loc with the last sow location."""

    def get_single_sower(self):
        """Return the first non-lap sower in the deco chain.
        Used to deicede if allowable test OPP_OR_EMPTY is met."""
        return self


# %%  base sower

class SowSeeds(SowMethodIf):
    """Basic sower.  Handles direction, skip_start and blocks
    (via the incr)."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        for _ in range(mdata.seeds):

            loc = self.game.deco.incr.incr(loc,
                                           mdata.direct,
                                           mdata.cont_sow_loc)
            self.game.board[loc] += 1

        mdata.capt_loc = loc


# %%  more single sowers

class SowSeedsNStore(SowMethodIf):
    """Sow a seed into the player's own store when passing it.

    If the sow ends in the store, return WinCond.REPEAT_TURN.

    Poses: don't bother looking up fill_store if loc isn't
    in this tuple.

    Fill Store: If we have just incremented past current
    player's store, eval True to state that we should stop
    and put a seed into the store."""

    def __init__(self, game, decorator=None):
        super().__init__(game, decorator)

        self.fill_store = ((self.game.cts.holes - 1,       # for CW not turn
                            self.game.cts.dbl_holes - 1),  # for CW turn
                           (0, 0),                         # not used
                           (self.game.cts.holes, 0))       # for CCW

        if game.info.sow_direct == gi.Direct.CW:
            self.poses = (self.game.cts.holes - 1,
                          self.game.cts.dbl_holes - 1)
        elif game.info.sow_direct == gi.Direct.CCW:
            self.poses = (0, self.game.cts.holes)
        else:
            self.poses = (0, self.game.cts.holes - 1,
                          self.game.cts.holes, self.game.cts.dbl_holes - 1)


    def sow_seeds(self, mdata):
        """Sow seeds."""

        turn = self.game.turn
        incr = self.game.deco.incr.incr

        loc = mdata.cont_sow_loc
        seeds = mdata.seeds

        while seeds > 0:

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            if (loc in self.poses
                    and loc == self.fill_store[mdata.direct + 1][turn]):

                self.game.store[turn] += 1
                seeds -= 1
                if not seeds:
                    mdata.capt_loc = gi.WinCond.REPEAT_TURN
                    return mdata

            self.game.board[loc] += 1
            seeds -= 1

        mdata.capt_loc = loc


class DivertSkipBlckdSower(SowMethodIf):
    """Divert blocked holes on opp side out of play (to store 0).
    Skip sowing blocked holes on own side of board.

    Don't use the incrementer because it will skip blocks.
    The option to select this is:  sow_rule: SOW_BLKD_DIV

    XXXX  visit_opp is not currently supported because we need to
    close the hole if we end on gparam_one seeds (ie. block it).
    This needs to occur if lapping or not.
    This doesn't quite fit the model of the code right now but might
    in the future."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        seeds = mdata.seeds
        while seeds > 0:

            loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            while self.game.blocked[loc]:
                if self.game.cts.opp_side(self.game.turn, loc):

                    self.game.store[0] += 1
                    seeds -= 1
                    if not seeds:
                        mdata.capt_loc = loc
                        return

                loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            self.game.board[loc] += 1
            seeds -= 1

        mdata.capt_loc = loc


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
        loc = mdata.capt_loc

        if (loc not in self.no_close
                and self.game.board[loc] == self.game.info.gparam_one
                and self.game.cts.opp_side(self.game.turn, loc)
                and not self.game.inhibitor.stop_me_capt(self.game.turn)):

            self.game.store[0] += self.game.board[loc]
            self.game.board[loc] = 0
            self.game.blocked[loc] = True


class SowCaptOwned(SowMethodIf):
    """Any holes sown to allow capture are captured by the hole's
    owner.

    OWN_SOW_CAPT_ALL:

    LAPPER: Owner's capture seeds with capt_ok, until the last seed.
    The hole that the last seed is sown into may be captured from
    the  opponent's hole (let the capturer deal with it).

    LAPPER_NEXT: Any seed with capt_ok is captured by the hole
    owner.

    SOW_SOW_CAPT_ALL:
        similar to above, but only the sower captures on from
        the opponents holes.
    """

    def __init__(self, game, decorator=None):
        """Create a list of conditions (as lambda functions)
        to be tested for each hole sown.
        Prototype is cfunc(seed#, loc, turn)

        Define an owner function with prototype owner(loc, turn)"""

        super().__init__(game, decorator)

        self.conds = []

        if self.game.info.sow_rule == gi.SowRule.OWN_SOW_CAPT_ALL:

            # no added conditions, only need to determine owner

            if self.game.info.goal == gi.Goal.TERRITORY:
                self.owner = lambda loc, turn: game.owner[loc]

            else:
                self.owner = lambda loc, turn: game.cts.board_side(loc)

        else:  #  self.game.info.sow_rule == gi.SowRule.SOW_SOW_CAPT_ALL

            # capturer is always current player,
            # but the hole must belong to the opponent

            self.owner = lambda loc, turn: turn

            if self.game.info.goal == gi.Goal.TERRITORY:
                self.conds += [lambda scnt, loc, turn:
                                   turn != game.owner[loc]]
            else:
                self.conds += [lambda scnt, loc, turn:
                                   turn != game.cts.board_side(loc)]

        if self.game.info.mlaps == gi.LapSower.LAPPER:
            self.conds += [lambda scnt, loc, turn: scnt > 1]


    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        for scnt in range(mdata.seeds, 0, -1):

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1

            if (all(cfunc(scnt, loc, self.game.turn) for cfunc in self.conds)
                    and not self.game.inhibitor.stop_me_capt(self.game.turn)
                    and self.game.deco.capt_ok.capture_ok(loc)):

                owner = self.owner(loc, self.game.turn)
                game_log.step(f'Capture from {loc} by {owner}')
                self.game.store[owner] += self.game.board[loc]
                self.game.board[loc] = 0

        mdata.capt_loc = loc


class SowSkipOppN(SowMethodIf):
    """Skip sowing holes with a specified number of seeds in them
    on the opponents side of the board."""

    def __init__(self, game, skip_set, decorator=None):
        super().__init__(game, decorator)
        self.skip_set = skip_set

    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        for _ in range(mdata.seeds):

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            while (self.game.cts.opp_side(self.game.turn, loc)
                   and self.game.board[loc] in self.skip_set):

                loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            self.game.board[loc] += 1

        mdata.capt_loc = loc


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
        return not self.game.deco.make_child.test(mdata)


class StopSingleSeed(LapContinuerIf):
    """A wrapper: stop if there is zero or one seed
    (the one we just sowed)."""

    def do_another_lap(self, mdata):

        if self.game.board[mdata.capt_loc] <= 1:
            return False
        return self.decorator.do_another_lap(mdata)


class StopOnChild(LapContinuerIf):
    """A wrapper: stop if we've ended in a child."""

    def do_another_lap(self, mdata):

        if self.game.child[mdata.capt_loc] is not None:
            return False
        return self.decorator.do_another_lap(mdata)


class StopCaptureSeeds(LapContinuerIf):
    """A wrapper: stop if we should capture."""

    def do_another_lap(self, mdata):

        if self.game.deco.capt_ok.capture_ok(mdata.capt_loc):
            return False
        return self.decorator.do_another_lap(mdata)


class StopRepeatTurn(LapContinuerIf):
    """A wrapper: stop if we know it's a repeat turn.
    This must be at the top so we don't try to use
    REPEAT_TURN as an index."""

    def do_another_lap(self, mdata):

        if mdata.capt_loc is gi.WinCond.REPEAT_TURN:
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

        loc = mdata.capt_loc
        if (loc not in self.no_close
                and self.game.board[loc] == self.game.info.gparam_one
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
            game_log.step(f'Mlap sow from {loc}', self.game, game_log.DETAIL)

            if self.lap_cont.do_another_lap(mdata):
                loc = mdata.capt_loc
                mdata.cont_sow_loc = loc
                mdata.seeds = self.game.board[loc]

                self.end_lap_op.do_op(mdata)
                self.game.board[loc] = 0

            else:
                return

        mdata.capt_loc = gi.WinCond.ENDLESS


class SowVisitedMlap(SowMethodIf):
    """Enforce an mlap option in which the first sow, must reach or
    pass through the opponents side of the board before a second
    lap may begin. A sow that does not reach the opponents side of
    the board, ends the turn. In otherwords, a second lap may not
    be started on a players side of the board, unless they have
    passed through the opponents side of the board.

    Can check the child array even if the child flag not set, because
    it is initialized to None (not a designated child)."""

    def __init__(self, game, single_sower, lap_sower, lap_cont):

        super().__init__(game, lap_sower)
        self.lap_cont = lap_cont
        self.single_sower = single_sower


    def __str__(self):
        """Add single sower and lap continuer to the string."""

        my_str = '\n   '.join([repr(self),
                               'single s: ' + str(self.single_sower),
                               'lap cont: ' + str(self.lap_cont)])

        if self.decorator:
            return my_str + '\n' + str(self.decorator)
        return my_str   # pragma: no coverage


    def get_single_sower(self):
        """Return the first non-lap sower in the deco chain.
        This is not a single sower, override the default to call
        down the deco chain"""
        return self.decorator.get_single_sower()


    def sow_seeds(self, mdata):
        """Do the first sow."""

        self.single_sower.sow_seeds(mdata)
        game_log.step(f'Vis Mlap sow from {mdata.cont_sow_loc}',
                      self.game, game_log.DETAIL)
        if mdata.capt_loc is gi.WinCond.REPEAT_TURN:
            return

        visited_opp = (mdata.seeds >= self.game.cts.holes
                       or self.game.cts.opp_side(self.game.turn,
                                                 mdata.capt_loc))
        if not visited_opp:
            return

        if self.lap_cont.do_another_lap(mdata):
            loc = mdata.capt_loc
            mdata.cont_sow_loc = loc
            mdata.seeds = self.game.board[loc]
            self.game.board[loc] = 0
            self.decorator.sow_seeds(mdata)


# %% prescribed opening moves

# use prescribed openings if the first player has a choice
# if it's a standard pattern use start_pattern


class SowPrescribedIf(SowMethodIf):
    """A deco that does prescribed moves for one or more turns.
    Concrete subclasses should not provide sow_seeds."""

    def __init__(self, game, count, decorator=None):

        super().__init__(game, decorator)
        self.dispose = count

    @abc.abstractmethod
    def do_prescribed(self, mdata):
        """Do the prescribed opening moves."""

    def sow_seeds(self, mdata):
        """If the decorator has expired, call the child sower."""

        if self.game.mcount > self.dispose:
            self.decorator.sow_seeds(mdata)
        else:
            self.do_prescribed(mdata)

    def get_single_sower(self):    # pragma: no coverage
        """ginfo rules should prevent this from being called.
        don't try to force do_prescribed into valid sower rules
        (until we want it :)"""
        raise NotImplementedError(
            "SowPrescribedIf doesn't know how to get single sower")


class SowBasicFirst(SowPrescribedIf):
    """Use the default basic sower for the first sows."""

    def __init__(self, game, count, decorator=None):
        super().__init__(game, count, decorator)
        self.sower = SowSeeds(game)

    def do_prescribed(self, mdata):
        self.sower.sow_seeds(mdata)


class SowMlapsFirst(SowPrescribedIf):
    """Use the default mlap sower for the first sows."""

    def __init__(self, game, count, decorator=None):
        super().__init__(game, count, decorator)
        sower = SowSeeds(game)
        lap_cont = StopSingleSeed(game, LapContinue(game))
        self.sower = SowMlapSeeds(game, sower, lap_cont, NoOp(game))

    def do_prescribed(self, mdata):
        self.sower.sow_seeds(mdata)


class SowOneOpp(SowPrescribedIf):
    """The last seed must be on the opponents side of the board
    skip our own holes, if required, to make that happen."""

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        incrementer = self.game.deco.incr.incr

        for _ in range(mdata.seeds - 1):

            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1

        loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
        while not self.game.cts.opp_side(self.game.turn, loc):
            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
        self.game.board[loc] += 1

        mdata.capt_loc = loc


class SowPlus1Minus1Capt(SowPrescribedIf):
    """Starting after the selected move one seed forward
    in every other hole."""

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        self.game.board[loc] = mdata.seeds
        incrementer = self.game.deco.incr.incr

        for cnt in range(self.game.cts.dbl_holes - 1):
            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1 if cnt % 2 else -1

        cross = self.game.cts.cross_from_loc(mdata.cont_sow_loc)
        self.game.board[cross] += 1

        mdata.capt_loc = cross


# %% build deco chain

def deco_blkd_divert_sower(game):
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


def deco_base_sower(game):
    """Choose the base sower."""

    sower = None
    if game.info.sow_rule:
        if game.info.sow_rule in {gi.SowRule.SOW_BLKD_DIV,
                                  gi.SowRule.SOW_BLKD_DIV_NR}:
            sower = deco_blkd_divert_sower(game)

        elif game.info.sow_rule in {gi.SowRule.OWN_SOW_CAPT_ALL,
                                    gi.SowRule.SOW_SOW_CAPT_ALL}:
            sower = SowCaptOwned(game)

        elif game.info.sow_rule == gi.SowRule.NO_SOW_OPP_2S:
            sower = SowSkipOppN(game, {2})

        elif game.info.sow_rule in (gi.SowRule.NONE,
                                    gi.SowRule.CHANGE_DIR_LAP):
            # pick a base sower below
            pass

        else:
            raise NotImplementedError(
                    f"SowRule {game.info.sow_rule} not implemented.")

    if not sower:
        if game.info.sow_own_store:
            sower = SowSeedsNStore(game)

        else:
            sower = SowSeeds(game)

    return sower


def deco_build_lap_cont(game):
    """Choose a base lap continuer, then add any wrappers."""

    if game.info.mlaps == gi.LapSower.LAPPER:

        if game.info.child_type:
            lap_cont = ChildLapCont(game)

        elif game.info.sow_rule in {gi.SowRule.SOW_BLKD_DIV,
                                    gi.SowRule.SOW_BLKD_DIV_NR}:
            lap_cont = DivertBlckdLapper(game)
        else:
            lap_cont = LapContinue(game)

        lap_cont = StopSingleSeed(game, lap_cont)

    elif game.info.mlaps == gi.LapSower.LAPPER_NEXT:
        lap_cont = NextLapCont(game)

    else:
        raise NotImplementedError(
                    f"LapSower {game.info.mlaps} not implemented.")

    if game.info.child_type:
        lap_cont = StopOnChild(game, lap_cont)

    if (any([game.info.evens,
             game.info.capt_on,
             game.info.capt_max,
             game.info.capt_min])
        and game.info.mlaps is not gi.LapSower.LAPPER_NEXT):
        lap_cont = StopCaptureSeeds(game, lap_cont)

    if game.info.sow_own_store:
        lap_cont = StopRepeatTurn(game, lap_cont)

    return lap_cont


def deco_mlap_sower(game, sower):
    """Build the deco chain elements for multiple lap sowing.
    Choose:
        1. an op to perform between laps
        2. a lap continue tester
    then build the mlap sower. Wrap if needed, with Visited."""

    pre_lap_sower = sower

    if game.info.sow_rule == gi.SowRule.CHANGE_DIR_LAP:
        end_op = DirChange(game)
    elif game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV:
        end_op = CloseOp(game)
    elif game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV_NR:
        end_op = CloseOp(game, True)
    else:
        end_op = NoOp(game)

    lap_cont = deco_build_lap_cont(game)
    sower = SowMlapSeeds(game, sower, lap_cont, end_op)

    if game.info.visit_opp:
        sower = SowVisitedMlap(game, pre_lap_sower, sower, lap_cont)

    return sower


def deco_prescribed_sower(game, sower):
    """Add the prescribed sowers to the deco chain."""

    if game.info.prescribed == gi.SowPrescribed.SOW1OPP:
        sower = SowOneOpp(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.PLUS1MINUS1:
        sower = SowPlus1Minus1Capt(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.BASIC_SOWER:
        sower = SowBasicFirst(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.MLAPS_SOWER:
        sower = SowMlapsFirst(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT:
        # sower deco not needed
        pass

    else:
        raise NotImplementedError(
                f"SowPrescribed {game.info.prescribed} not implemented.")

    return sower


def deco_sower(game):
    """Build the sower chain."""

    sower = deco_base_sower(game)

    if game.info.mlaps != gi.LapSower.OFF:
        sower = deco_mlap_sower(game, sower)

    if game.info.prescribed != gi.SowPrescribed.NONE:
        sower = deco_prescribed_sower(game, sower)

    return sower
