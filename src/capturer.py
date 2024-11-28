# -*- coding: utf-8 -*-
"""Define the capturer decorators.

The deco chain should return if the state of the board
was modified.

Created on Fri Apr  7 08:52:03 2023
@author: Ann"""


# %% imports

import abc

import deco_chain_if
import game_interface as gi

from game_logger import game_log


# %% capt interface

class CaptMethodIf(deco_chain_if.DecoChainIf):
    """Interface for capturers."""

    @abc.abstractmethod
    def do_captures(self, mdata):
        """Do captures.
        Update mdata (both are inited to False):
            capt_changed: there was a state change (picked, child made, etc.)
        but not a capture
            captured: there was an actual capture,
            this will be used for repeat turn"""


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

        if self.game.deco.capt_ok.capture_ok(mdata, mdata.capt_loc):

            self.game.store[self.game.turn] += self.game.board[mdata.capt_loc]
            self.game.board[mdata.capt_loc] = 0
            mdata.captured = True


class CaptMultiple(CaptMethodIf):
    """Multi capture, in specified direction.
    capt_ok_deco encapsulates many of the capture parameters incl side."""

    def __init__(self, game, max_capt, decorator=None):

        super().__init__(game, decorator)
        self.max_capt = max_capt

    def do_captures(self, mdata):
        """Capture loop"""
        loc = mdata.capt_loc
        capts = self.max_capt

        while capts and self.game.deco.capt_ok.capture_ok(mdata, loc):

            self.game.store[self.game.turn] += self.game.board[loc]
            self.game.board[loc] = 0
            capts -= 1
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
                and self.game.deco.capt_ok.capture_ok(mdata, cross)):

            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[cross] = 0
            mdata.captured = True


class CaptNext(CaptMethodIf):
    """If there are seeds in the next hole capture them
    and call down the deco chain for possible multiple captures."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        if game.info.mlaps:
            self.seed_cond = lambda loc: game.board[loc] == 1
        else:
            self.seed_cond = lambda loc : True

    def do_captures(self, mdata):

        loc = saved_capt_loc = mdata.capt_loc
        direct = mdata.direct
        loc_next = self.game.deco.incr.incr(loc, direct)

        if (self.seed_cond(loc)
                and self.game.board[loc_next]
                and self.game.deco.capt_ok.capture_ok(mdata, loc_next)):

            self.game.store[self.game.turn] += self.game.board[loc_next]
            self.game.board[loc_next] = 0
            mdata.captured = True

            mdata.capt_loc = self.game.deco.incr.incr(loc_next, mdata.direct)
            self.decorator.do_captures(mdata)
            mdata.capt_loc = saved_capt_loc


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


class CaptMatchOpp(CaptMethodIf):
    """If the number of seeds in the capture hole and the
    hole cross, capture them both."""

    def test_match_opp(self, loc, cross):
        """Determine if conditions for a match capt are
        met and not contraindicated at loc and cross"""

        return (self.game.board[loc]
                and self.game.board[loc] == self.game.board[cross]
                and self.game.child[loc] is None
                and self.game.child[cross] is None
                and self.game.unlocked[loc]
                and self.game.unlocked[cross])

    def do_match_capt(self, mdata, loc, cross):
        """Do the actual match opp capt from both sides"""

        self.game.store[self.game.turn] += self.game.board[loc]
        self.game.store[self.game.turn] += self.game.board[cross]
        self.game.board[loc] = 0
        self.game.board[cross] = 0
        mdata.captured = True

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        cross = self.game.cts.cross_from_loc(mdata.capt_loc)

        if self.test_match_opp(loc, cross):
            self.do_match_capt(mdata, loc, cross)


class CaptMatchOppMulti(CaptMatchOpp):
    """If the number of seeds in the capture hole and the
    hole cross, capture them both."""

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        cross = self.game.cts.cross_from_loc(loc)

        while self.test_match_opp(loc, cross):
            self.do_match_capt(mdata, loc, cross)

            loc = self.game.deco.incr.incr(loc, mdata.direct)
            cross = self.game.cts.cross_from_loc(loc)


# %% cross capt decos

class CaptCrossVisited(CaptMethodIf):
    """Reject cross capt and repeat turn, if not single seed or
    end on opponent's side.
    Continue capture chain, if have sown opp side this turn.
    If end in empty hole on own side and have not sown to the
    opposite side of the board, do repeat turn."""

    def do_captures(self, mdata):

        if (self.game.board[mdata.capt_loc] != 1
                or self.game.cts.opp_side(self.game.turn, mdata.capt_loc)):
            return

        if any(mdata.board[loc] != self.game.board[loc]
                for loc in self.game.cts.get_opp_range(self.game.turn)):
            self.decorator.do_captures(mdata)
            return

        mdata.captured = gi.WinCond.REPEAT_TURN
        game_log.add('XCVisit Repeat Turn', game_log.INFO)


class CaptCrossPickOwnOnCapt(CaptMethodIf):
    """Cross capture, pick own if capture, but do not
    pick from a designated child or a locked hole.

    The capture already confirmed we are on the right
    side if mdata.captured is true; which is opposite
    from capt_side."""

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
    or a locked hole. If captures are limited by side, we
    need the opposite side here."""


    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        if game.info.capt_side in (gi.CaptSide.OPP_SIDE,
                                   gi.CaptSide.OPP_CONT):
            self.side_ok = game.cts.my_side

        elif game.info.capt_side in (gi.CaptSide.OWN_SIDE,
                                     gi.CaptSide.OWN_CONT):
            self.side_ok = game.cts.opp_side

        else:
            self.side_ok = lambda _1, _2: True


    def do_captures(self, mdata):
        """Test for and pick own."""

        self.decorator.do_captures(mdata)

        if (self.side_ok(self.game.turn, mdata.capt_loc)
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
                    and self.game.deco.capt_ok.capture_ok(mdata, cross)):

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
        if grandslam == gi.GrandSlam.LEAVE_LEFT:
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
    """Make a child if the conditions are right."""

    def do_captures(self, mdata):

        if self.game.deco.make_child.test(mdata):

            self.game.child[mdata.capt_loc] = self.game.turn
            mdata.capt_changed = True
            return

        self.decorator.do_captures(mdata)


class CaptureToChild(CaptMethodIf):
    """Used when we have no stores, but collect captures into
    children.

    If we have a chilren, use the rest of the deco chain to see
    if captures are made, then move any captured seeds to the
    children."""

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        if self.game.deco.make_child.test(mdata):
            self.game.child[loc] = self.game.turn
            mdata.capt_changed = True
            return

        have_child = False
        for child in range(self.game.cts.dbl_holes):
            if self.game.child[child] == self.game.turn:
                have_child = True
                break

        if have_child:
            self.decorator.do_captures(mdata)
            if mdata.captured:
                self.game.board[child] += self.game.store[self.game.turn]
                self.game.store[self.game.turn] = 0

        assert not sum(self.game.store)


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
        game = self.game
        turn = self.game.turn

        if game.child[loc] is (not turn):

            capts = 2 if game.board[loc] >= 2 else 1
            game.board[loc] -= capts
            game.store[turn] += capts
            mdata.captured = True
            return

        if game.deco.make_child.test(mdata):

            game.child[loc] = turn
            mdata.capt_changed = True
            return

        self.decorator.do_captures(mdata)


class MakeBull(CaptMethodIf):
    """If deco.make_child returns True, we know that we
    can make mdata.capt_loc a child via either:
        - it being child convert
        - the pair convert conditions are met

    We then need to test to see if the previous hole,
    can also be made a child:
        - must not already be a child
        - loc and previous must have convert_cnt and convert - 1
        in them in either order

    There is duplicate work between make_child.test and this
    method, don't see a way around it"""

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        game = self.game

        if game.deco.make_child.test(mdata):

            game.child[loc] = game.turn
            mdata.capt_changed = True

            prev = self.game.deco.incr.incr(loc, mdata.direct.opp_dir())
            if game.child[prev] is None:

                board_set = set([game.board[prev], game.board[loc]])
                req_set = set([game.info.child_cvt - 1, game.info.child_cvt])
                if board_set == req_set:
                    game.child[prev] = game.turn
                    mdata.capt_changed = True
            return

        self.decorator.do_captures(mdata)


class MakeQur(CaptMethodIf):
    """When making a qur, make both the hole sown to child_cvt
    and the hole opposit QURs."""

    def do_captures(self, mdata):

        if self.game.deco.make_child.test(mdata):

            self.game.child[mdata.capt_loc] = self.game.turn

            cross = self.game.cts.cross_from_loc(mdata.capt_loc)
            self.game.child[cross] = self.game.turn

            # XXXX equalize seeds (though, how does it effect game play?)

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
                and self.game.board[cross]
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


class PickLastSeeds(CaptMethodIf):
    """If the specified number of seeds or fewer are left
    on the board either the current player or
    round starter takes them (based on turn_takes).

    Set capt_changed if we change the board.

    Can't check the mdata.captured flag because we want to support and
    sow rules of *_SOW_CAPT_ALL which might move seeds out of play."""

    def __init__(self, game, decorator=None, turn_takes=True):

        super().__init__(game, decorator)

        self.turn_takes = turn_takes

        nbr_start = game.cts.nbr_start
        self.seeds = nbr_start if turn_takes else 2 * nbr_start


    def do_captures(self, mdata):

        self.decorator.do_captures(mdata)

        game = self.game
        seeds = sum(game.board[loc]
                    for loc in range(game.cts.dbl_holes)
                    if game.child[loc] is None
                        and game.unlocked[loc])

        if  0 < seeds <= self.seeds:
            taker = game.turn if self.turn_takes else game.starter

            for loc in range(game.cts.dbl_holes):
                if game.child[loc] is None and game.unlocked[loc]:
                    game.store[taker] += game.board[loc]
                    game.board[loc] = 0

            msg = f'Seeds left <= {self.seeds}, {taker} collected them.'
            game_log.add(msg, game_log.INFO)
            mdata.capt_changed = True



# %% some wrappers

class NoSingleSeedCapt(CaptMethodIf):
    """Do not do captures with a single seed sow."""

    def do_captures(self, mdata):

        if mdata.seeds != 1:
            self.decorator.do_captures(mdata)


class NotInhibited(CaptMethodIf):
    """Do not allow captures.
    Child inhibitor is enforced via make_child deco"""

    def do_captures(self, mdata):

        if not self.game.inhibitor.stop_me_capt(self.game.turn):
            self.decorator.do_captures(mdata)


class RepeatTurn(CaptMethodIf):
    """Convert mdata.captured to REPEAT_TURN."""

    def do_captures(self, mdata):
        self.decorator.do_captures(mdata)
        if mdata.captured:
            game_log.add('Capture repeat turn', game_log.INFO)
            mdata.captured = gi.WinCond.REPEAT_TURN


# %% build deco chains

def _add_cross_capt_deco(game, capturer):
    """Add the cross capture decorators to the capturer deco.
    crosscapt and multicapt is always captsamedir"""

    capturer = CaptCross(game, capturer)

    if game.info.xcpickown == gi.CrossCaptOwn.LEAVE:
        pass

    elif game.info.xcpickown == gi.CrossCaptOwn.PICK_ON_CAPT:
        capturer = CaptCrossPickOwnOnCapt(game, capturer)

    elif game.info.xcpickown == gi.CrossCaptOwn.ALWAYS_PICK:
        capturer = CaptCrossPickOwn(game, capturer)

    else:
        raise NotImplementedError(
                f"CrossCaptOwn {game.info.xcpickown} not implemented.")

    if game.info.multicapt:
        capturer = CaptContinueXCapt(game, capturer)

    if game.info.xc_sown:
        capturer = CaptCrossVisited(game, capturer)

    return capturer


def _add_grand_slam_deco(game, capturer):
    """Add the grand slam decorators to the capturer deco."""

    if game.info.grandslam == gi.GrandSlam.NO_CAPT:
        capturer = GSNone(game, capturer)

    elif game.info.grandslam in (gi.GrandSlam.LEAVE_LEFT,
                                 gi.GrandSlam.LEAVE_RIGHT):
        capturer = GSKeep(game, game.info.grandslam, capturer)

    elif game.info.grandslam == gi.GrandSlam.OPP_GETS_REMAIN:
        capturer = GSOppGets(game, capturer)

    elif game.info.grandslam in (gi.GrandSlam.LEGAL,
                                 gi.GrandSlam.NOT_LEGAL):
        # grand slam rule does not need a capture deco
        pass

    else:
        raise NotImplementedError(
                f"GrandSlam {game.info.grandslam} not implemented.")

    return capturer


def _add_child_deco(game, capturer):
    """Add a child handling deco if needed.
    only one child handler: bull/weg/waldas/tuzdek/children"""

    if game.info.child_type == gi.ChildType.NOCHILD:
        pass

    elif game.info.child_type in (gi.ChildType.NORMAL,
                                  gi.ChildType.ONE_CHILD):

        if game.info.stores:
            capturer = MakeChild(game, capturer)
        else:
            capturer = CaptureToChild(game, capturer)

    elif game.info.child_type == gi.ChildType.WEG:
        capturer = MakeWegCapture(game, capturer)

    elif game.info.child_type == gi.ChildType.BULL:
        capturer = MakeBull(game, capturer)

    elif game.info.child_type == gi.ChildType.QUR:
        capturer = MakeQur(game, capturer)

    else:
        raise NotImplementedError(
                f"ChildType {game.info.child_type} not implemented.")

    return capturer


def _add_capt_next_deco(game, capturer):
    """Capt two out may be done with or without changing direction
    or capturing multiples.
    NOTE: multipcapt value is one less because CaptNext does first capture"""

    if game.info.multicapt:
        capturer = CaptMultiple(game, game.info.multicapt - 1, capturer)

    capturer = CaptNext(game, capturer)

    if not game.info.capsamedir:
        capturer = CaptOppDirMultiple(game, capturer)

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


def _add_capt_type_deco(game, capturer):
    """Add the capture type decos along the multicapt decos,
    if supported by generic decos: CaptMultiple and CaptOppDirMultiple"""

    if game.info.capt_type == gi.CaptType.TWO_OUT:
        capturer = _add_capt_two_out_deco(game, capturer)

    elif game.info.capt_type == gi.CaptType.NEXT:
        capturer = _add_capt_next_deco(game, capturer)

    elif game.info.capt_type == gi.CaptType.MATCH_OPP:
        if game.info.multicapt:
            capturer = CaptMatchOppMulti(game, capturer)
            if not game.info.capsamedir:
                capturer = CaptOppDirMultiple(game, capturer)
        else:
            capturer = CaptMatchOpp(game, capturer)

    else:
        raise NotImplementedError(
            f"CaptType {game.info.capt_type} not implemented.")

    return capturer


def _add_capt_pick_deco(game, capturer):
    """Add any extra pickers."""

    if game.info.pickextra == gi.CaptExtraPick.NONE:
        pass

    elif game.info.pickextra == gi.CaptExtraPick.PICKCROSS:
        capturer = PickCross(game, capturer)

    elif game.info.pickextra == gi.CaptExtraPick.PICKTWOS:
        capturer = PickOppTwos(game, capturer)

    elif game.info.pickextra == gi.CaptExtraPick.PICKLASTSEEDS:
        capturer = PickLastSeeds(game, capturer, turn_takes=True)

    elif game.info.pickextra == gi.CaptExtraPick.PICK2XLASTSEEDS:
        capturer = PickLastSeeds(game, capturer, turn_takes=False)

    else:
        raise NotImplementedError(
            f"CaptExtraPick {game.info.pickextra} not implemented.")

    return capturer


def deco_capturer(game):
    """Build capture chain and return it."""

    capturer = CaptNone(game)

    if game.info.crosscapt:
        capturer = _add_cross_capt_deco(game, capturer)

    elif game.info.capt_type:
        # opp dir and multicapt handled
        capturer = _add_capt_type_deco(game, capturer)

    elif game.info.multicapt:
        capturer = CaptMultiple(game, game.info.multicapt, capturer)
        if not game.info.capsamedir:
            capturer = CaptOppDirMultiple(game, capturer)

    elif (game.info.evens or game.info.capt_on
          or game.info.capt_max or game.info.capt_min):
        capturer = CaptSingle(game)

    capturer = _add_child_deco(game, capturer)
    capturer = _add_capt_pick_deco(game, capturer)
    capturer = _add_grand_slam_deco(game, capturer)

    if game.info.nosinglecapt:
        capturer = NoSingleSeedCapt(game, capturer)

    if (game.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT
            or game.info.round_fill == gi.RoundFill.SHORTEN
            or game.info.nocaptmoves):
        capturer = NotInhibited(game, capturer)

    if game.info.capt_rturn:
        capturer = RepeatTurn(game, capturer)

    return capturer
