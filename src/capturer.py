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
    def do_captures(self, mdata, capt_first=True):
        """Do captures. capt_first should never be set when called from
        outside the capture deco chain, e.g. Mancala or Sower.

        Update mdata:

        capt_changed: there was a state change (picked, child made, etc.)
        but not a capture

        captured: there was an actual capture, this will be used
        for repeat turn (CAPT_RTURN)

        capt_next: for base captures this should be set to the location
        to test for a possible multiple capture"""


# %% capture base

class CaptNone(CaptMethodIf):
    """No captures."""

    def do_captures(self, mdata, capt_first=True):
        pass


# %%  base capture decos

class CaptBasic(CaptMethodIf):
    """Capture on selected values, e.g. on basic capture
    via capt_ok deco."""

    def do_captures(self, mdata, capt_first=True):

        if self.game.deco.capt_ok.capture_ok(mdata, mdata.capt_loc):

            self.game.store[self.game.turn] += self.game.board[mdata.capt_loc]
            self.game.board[mdata.capt_loc] = 0

            mdata.captured = True
            mdata.capt_next = self.game.deco.incr.incr(mdata.capt_loc,
                                                       mdata.direct)


class CaptCross(CaptMethodIf):
    """Cross capture.  If first capture, capt_loc must contain
    one seed, otherwise no seeds."""

    def do_captures(self, mdata, capt_first=True):
        """Do cross capture"""

        cross = self.game.cts.cross_from_loc(mdata.capt_loc)

        if (((capt_first and self.game.board[mdata.capt_loc] == 1)
             or (not capt_first and not self.game.board[mdata.capt_loc]))
                and self.game.deco.capt_ok.capture_ok(mdata, cross)):

            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[cross] = 0

            mdata.captured = True
            mdata.capt_next = self.game.deco.incr.incr(mdata.capt_loc,
                                                       mdata.direct)


class CaptNext(CaptMethodIf):
    """If there are seeds in the next hole capture them."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        if game.info.mlaps:
            self.seed_cond = lambda mdata, cfirst, loc, nloc: (
                (cfirst and self.game.deco.capt_ok.capture_ok(mdata, loc))
                or (not cfirst
                    and self.game.deco.capt_ok.capture_ok(mdata, nloc)))
        else:
            self.seed_cond = lambda mdata, cfirst, loc, nloc: (
                self.game.deco.capt_ok.capture_ok(mdata, nloc))


    def do_captures(self, mdata, capt_first=True):

        loc = mdata.capt_loc
        loc_next = self.game.deco.incr.incr(loc, mdata.direct)

        if (self.seed_cond(mdata, capt_first, loc, loc_next)
                and self.game.board[loc_next]):

            self.game.store[self.game.turn] += self.game.board[loc_next]
            self.game.board[loc_next] = 0

            mdata.captured = True
            mdata.capt_next = loc_next


class CaptTwoOut(CaptMethodIf):
    """Capture two out or across the gap.

    When used without laps, the final hole of the sow must
    have been occupied for capture, e.g. the hole does not
    contain just one seed.

    When used with LAPPER, lapping stops if capture conditions
    are met--next hole empty and two out has seeds.

    When used with LAPPER_NEXT, if the next hole for sowing is
    empty, stop lapping and capture any seeds across the gap.

    capt_loc is updated for PickCross of capture location.

    Don't use capt_ok because it might be setup for SOW_CAPT_ALL"""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        if game.info.mlaps:
            self.seed_cond = lambda _: True
        else:
            self.seed_cond = lambda seeds: seeds > 1

    def do_captures(self, mdata, capt_first=True):

        loc = mdata.capt_loc
        direct = mdata.direct
        loc_p1 = self.game.deco.incr.incr(loc, direct)
        loc_p2 = self.game.deco.incr.incr(loc_p1, direct)

        if (self.seed_cond(self.game.board[loc])
                and not self.game.board[loc_p1]
                and self.game.board[loc_p2]
                and self.game.child[loc_p2] is None
                and self.game.unlocked[loc_p2]):

            self.game.store[self.game.turn] += self.game.board[loc_p2]
            self.game.board[loc_p2] = 0

            mdata.captured = True
            mdata.capt_loc = loc_p2
            mdata.capt_next = loc_p2


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


    def do_captures(self, mdata, capt_first=True):

        loc = mdata.capt_loc
        cross = self.game.cts.cross_from_loc(mdata.capt_loc)

        if self.test_match_opp(loc, cross):
            self.game.store[self.game.turn] += self.game.board[loc]
            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[loc] = 0
            self.game.board[cross] = 0

            mdata.captured = True
            mdata.capt_next = self.game.deco.incr.incr(mdata.capt_loc,
                                                       mdata.direct)


# %% cross capt decos

class CaptCrossVisited(CaptMethodIf):
    """Confirm visit to opposite side to stop mlap sowing
    for capture.

    Reject cross capt or repeat turn, if not single seed
    or end on opponent's side (mlap sowing will continue).

    Continue capture chain, if have already captured or
    have sown opp side this turn on first capture.

    Otherwise, if end in empty hole on own side and have
    not sown to the opposite side of the board, do a repeat turn."""

    def do_captures(self, mdata, capt_first=True):

        cts = self.game.cts

        if (capt_first
                and ((self.game.board[mdata.capt_loc] != 1
                      or cts.opp_side(self.game.turn, mdata.capt_loc)))):
            return

        if (not capt_first
                or (capt_first
                    and any(mdata.board[loc] != self.game.board[loc]
                            for loc in cts.get_opp_range(self.game.turn)))):
            self.decorator.do_captures(mdata, capt_first)
            return

        mdata.captured = gi.WinCond.REPEAT_TURN
        game_log.add('XCVisit Repeat Turn', game_log.INFO)


class CaptCrossPickOwnOnCapt(CaptMethodIf):
    """Cross capture, pick own if capture, but do not
    pick from a designated child or a locked hole.

    The capture already confirmed we are on the right
    side if mdata.captured is true; which is opposite
    from capt_side."""

    def do_captures(self, mdata, capt_first=True):
        """Test for and pick own."""

        self.decorator.do_captures(mdata, capt_first)

        if (capt_first
                and mdata.captured is True
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


    def do_captures(self, mdata, capt_first=True):
        """Test for and pick own."""

        self.decorator.do_captures(mdata, capt_first)

        if (capt_first
                and self.side_ok(self.game.turn, mdata.capt_loc)
                and self.game.board[mdata.capt_loc] == 1
                and self.game.child[mdata.capt_loc] is None
                and self.game.unlocked[mdata.capt_loc]):

            self.game.store[self.game.turn] += 1
            self.game.board[mdata.capt_loc] = 0
            mdata.capt_changed = True
            game_log.add('Capturer (picked own w/o)', game_log.INFO)


# %% multiple capture wrappers

class CaptMultiple(CaptMethodIf):
    """A multiple capture wrapper.

    The maximum captures are set by the value of multicapt:
        -1: unlimited captures as long as other conditions are met
        0: this deco not included
        n: the maximum number of captures to do

    mdata.captured is reset each iteration to see if there is another
    capture, before returning it is set True if there were any
    captures.

    The returned mdata.capt_loc is the capt_loc return by the first
    call to the capturer."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        self.max_capt = game.info.multicapt


    def do_captures(self, mdata, capt_first=True):
        """Capture loop"""

        captured = False
        capt_loc = mdata.capt_loc
        cont_capt = self.max_capt    # stop captures when reaches 0

        while True:

            self.decorator.do_captures(mdata, capt_first)
            if capt_first:
                capt_loc = mdata.capt_loc
            cont_capt -= 1

            if not cont_capt or mdata.captured is False:
                mdata.captured = captured
                mdata.capt_loc = capt_loc
                break
            if mdata.captured is gi.WinCond.REPEAT_TURN:
                mdata.capt_loc = capt_loc
                break

            capt_first = False
            captured = True
            mdata.captured = False
            mdata.capt_loc = mdata.capt_next


class CaptOppDir(CaptMethodIf):
    """Capture in the opposite direction.  For multiple captures
    and next or two out.
    Recall mdata.direct is always one of CW or CCW.

    If we can precompute the direction, do so.
    Otherwise, compute it on every move"""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        self.opp_dir = 0
        if game.info.sow_direct in (gi.Direct.CW, gi.Direct.CCW):
            self.opp_dir = game.info.sow_direct.opp_dir()


    def do_captures(self, mdata, capt_first=True):
        """Change direction then use the deco chain."""
        direct = mdata.direct
        mdata.direct = self.opp_dir or mdata.direct.opp_dir()
        self.decorator.do_captures(mdata, capt_first)

        mdata.direct = direct


# %%  grand slam decos

class GrandSlamCapt(CaptMethodIf):
    """Grand Slam capturer and tester.
    This class is still abstract."""

    def is_grandslam(self, mdata, capt_first=True):
        """Return True if the capture was a grandslam"""

        # XXXX the test for start/end seeds could exclude children

        opp_rng = self.game.cts.get_opp_range(self.game.turn)
        start_seeds = any(mdata.board[tloc] for tloc in opp_rng)

        self.decorator.do_captures(mdata, capt_first)

        if start_seeds and mdata.captured:
            return not any(self.game.board[tloc] for tloc in opp_rng)

        return False


class GSNone(GrandSlamCapt):
    """A grand slam does not capture, reset the game state."""

    def do_captures(self, mdata, capt_first=True):

        saved_state = self.game.state

        if self.is_grandslam(mdata, capt_first):
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

    def do_captures(self, mdata, capt_first=True):

        saved_state = self.game.state
        if self.is_grandslam(mdata, capt_first):

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

    def do_captures(self, mdata, capt_first=True):

        if self.is_grandslam(mdata, capt_first):

            game_log.add('GRANDSLAM: opp gets', game_log.IMPORT)
            opp_turn = not self.game.turn
            for tloc in self.game.cts.get_my_range(self.game.turn):
                self.game.store[opp_turn] += self.game.board[tloc]
                self.game.board[tloc] = 0


# %%  child decorators

class MakeChild(CaptMethodIf):
    """Make a child if the conditions are right."""

    def do_captures(self, mdata, capt_first=True):

        if self.game.deco.make_child.test(mdata):

            self.game.child[mdata.capt_loc] = self.game.turn
            mdata.capt_changed = True
            return

        self.decorator.do_captures(mdata, capt_first)


class CaptureToChild(CaptMethodIf):
    """Used when we have no stores, but collect captures into
    children.

    If we have a chilren, use the rest of the deco chain to see
    if captures are made, then move any captured seeds to the
    children."""

    def do_captures(self, mdata, capt_first=True):

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
            self.decorator.do_captures(mdata, capt_first)
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

    def do_captures(self, mdata, capt_first=True):

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

        self.decorator.do_captures(mdata, capt_first)


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

    def do_captures(self, mdata, capt_first=True):

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

        self.decorator.do_captures(mdata, capt_first)


class MakeQur(CaptMethodIf):
    """When making a qur, make both the hole sown to child_cvt
    and the hole opposit QURs."""

    def do_captures(self, mdata, capt_first=True):

        if self.game.deco.make_child.test(mdata):

            self.game.child[mdata.capt_loc] = self.game.turn

            cross = self.game.cts.cross_from_loc(mdata.capt_loc)
            self.game.child[cross] = self.game.turn

            # XXXX equalize seeds (though, how does it effect game play?)

            mdata.capt_changed = True
            return

        self.decorator.do_captures(mdata, capt_first)


# %% pickers

# all one enum so only one of these can be used


class PickFinal(CaptMethodIf):
    """On capture take seeds from final hole sown."""

    def do_captures(self, mdata, capt_first=True):

        self.decorator.do_captures(mdata, capt_first)
        loc = mdata.capt_loc
        if (mdata.captured
                and self.game.board[loc]
                and self.game.child[loc] is None
                and self.game.unlocked[loc]):

            self.game.store[self.game.turn] += self.game.board[loc]
            self.game.board[loc] = 0
            game_log.add(f"Picking Final Hole at {loc}.", game_log.INFO)


class PickCross(CaptMethodIf):
    """Not a cross capture, but if there was a capture take any
    seeds from the opposite side of the board too."""

    def do_captures(self, mdata, capt_first=True):

        self.decorator.do_captures(mdata, capt_first)
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

    def do_captures(self, mdata, capt_first=True):

        self.decorator.do_captures(mdata, capt_first)
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


    def do_captures(self, mdata, capt_first=True):

        self.decorator.do_captures(mdata, capt_first)

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



# %% top level wrappers


class NoSingleSeedCapt(CaptMethodIf):
    """Do not do captures with a single seed sow."""

    def do_captures(self, mdata, capt_first=True):

        if mdata.seeds != 1:
            self.decorator.do_captures(mdata, capt_first)


class NotInhibited(CaptMethodIf):
    """Do not allow captures.
    Child inhibitor is enforced via make_child deco"""

    def do_captures(self, mdata, capt_first=True):

        if not self.game.inhibitor.stop_me_capt(self.game.turn):
            self.decorator.do_captures(mdata, capt_first)


class RepeatTurn(CaptMethodIf):
    """Convert mdata.captured to REPEAT_TURN based on
    configuration of capt_rturn.

    The rturn_cnt is maintained in the parent game because it
    must be part of the game state (decos should not have
    game state)."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        self.count_test = lambda: True
        if game.info.capt_rturn == gi.CaptRTurn.ONCE:
            self.count_test = self.only_once


    def only_once(self):
        """Only do one repeat turn."""

        return self.game.rturn_cnt < 1


    def do_captures(self, mdata, capt_first=True):
        self.decorator.do_captures(mdata, capt_first)

        if mdata.captured:
            if self.count_test():
                game_log.add(f'Capture repeat turn (rcnt={self.game.rturn_cnt})',
                             game_log.INFO)
                mdata.captured = gi.WinCond.REPEAT_TURN
            else:
                game_log.add('Second repeat turn prevented', game_log.INFO)
            self.game.rturn_cnt += 1

        else:
            self.game.rturn_cnt = 0


# %% build deco chains

def _add_cross_capt_deco(game):
    """Choose base the cross capture decorator.
    crosscapt and multicapt is always captsamedir"""

    capturer = CaptCross(game)

    if game.info.xcpickown == gi.CrossCaptOwn.LEAVE:
        pass

    elif game.info.xcpickown == gi.CrossCaptOwn.PICK_ON_CAPT:
        capturer = CaptCrossPickOwnOnCapt(game, capturer)

    elif game.info.xcpickown == gi.CrossCaptOwn.ALWAYS_PICK:
        capturer = CaptCrossPickOwn(game, capturer)

    else:
        raise NotImplementedError(
                f"CrossCaptOwn {game.info.xcpickown} not implemented.")

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


def _add_capt_type_deco(game):
    """Choose a base capture type decos."""

    if game.info.capt_type == gi.CaptType.TWO_OUT:
        capturer = CaptTwoOut(game)

    elif game.info.capt_type == gi.CaptType.NEXT:
        capturer = CaptNext(game)

    elif game.info.capt_type == gi.CaptType.MATCH_OPP:
        capturer = CaptMatchOpp(game)

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

    elif game.info.pickextra == gi.CaptExtraPick.PICKFINAL:
        capturer = PickFinal(game, capturer)

    else:
        raise NotImplementedError(
            f"CaptExtraPick {game.info.pickextra} not implemented.")

    return capturer


def deco_capturer(game):
    """Build capture chain and return it."""

    # choose a base capturer
    if game.info.crosscapt:
        capturer = _add_cross_capt_deco(game)

    elif game.info.capt_type:
        capturer = _add_capt_type_deco(game)

    elif (game.info.evens or game.info.capt_on
          or game.info.capt_max or game.info.capt_min):
        capturer = CaptBasic(game)

    else:
        capturer = CaptNone(game)

    # add decorators to the base capturer
    if game.info.multicapt:
        capturer = CaptMultiple(game, capturer)

    if not game.info.capsamedir:
        # this is used with multi capt, capt next, and capt two out
        capturer = CaptOppDir(game, capturer)

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
