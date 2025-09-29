# -*- coding: utf-8 -*-
"""Gratuitous is a game class in which 'captured' seeds
from your own side of the board are forced upon your
opponent. When a capture is done a second turn allows
selection of an opponent's hole to define where the capture
should be 'shared'.

Always placed with two cycle games of either
North/South or East/West.

The game goal must be CLEAR (or the round tally version).

Created on Sun Dec  1 07:10:20 2024
@author: Ann"""

# %% imports

import abc
import dataclasses as dc

import cfg_keys as ckey
import game_info as gi
import mancala
import move_data
import rule_tester
import two_cycle

from game_logger import game_log


# %% rules

def test_grat_rules(ginfo, holes, skip):
    """Build the rules for Gratuitous."""

    tester = rule_tester.RuleTester(ginfo, holes, skip)

    tester.test_rule(
        'grat_goal_clear',
        rule=lambda ginfo: not ginfo.goal in (gi.Goal.CLEAR,
                                              gi.Goal.RND_WIN_COUNT_CLR),
        msg='Gratuitous requires CLEAR goal',
        excp=gi.GameInfoError)
        # CLEAR includes many base mancala rules:
        #  GS legal, children, many options prohibited

    tester.test_rule(
        'grat_no_sow_own',
        rule=lambda ginfo: ginfo.sow_stores,
        msg="""Gratuitous incompatible with SOW_STORES""",
        excp=NotImplementedError)
        # stores are only used (when wanted) to show whose turn it is

    tester.test_rule(
        'grat_board_only',
        rule=lambda ginfo: ginfo.play_locs,
        msg="Gratuitous may only be played from the board; bad PLAY_LOCS",
        excp=gi.GameInfoError)
        # store are not used even if visible

    tester.test_rule(
        'grat_no_sowrule',
        rule=lambda ginfo: ginfo.sow_rule,
        msg="""Gratuitous incompatible with SOW_RULE""",
        excp=gi.GameInfoError)

    tester.test_rule(
        'grat_no_mlap_cont',
        rule=lambda ginfo: ginfo.mlap_cont,
        msg="""Gratuitous incompatible with MLAP_CONT""",
        excp=gi.GameInfoError)

    tester.test_rule(
        'grat_no_xcapt',
        rule=lambda ginfo: ginfo.crosscapt,
        msg="""Gratuitous incompatible with CROSSCAPT""",
        excp=gi.GameInfoError)

    tester.test_rule(
        'grat_side_own',
        rule=lambda ginfo: ginfo.capt_side != gi.CaptSide.OWN_SIDE,
        msg="""Gratuitous requires that CAPT_SIDE be OWN_SIDE""",
        excp=gi.GameInfoError)

    tester.test_rule(
        'grat_no_moveunlock',
        rule=lambda ginfo: ginfo.moveunlock,
        msg="""Gratuitous is incompatible with MOVEUNLOCK""",
        excp=gi.GameInfoError)

    tester.test_rule(
        'grat_no_capt_rturn',
        rule=lambda ginfo: ginfo.capt_rturn,
        msg="""Do not set capt_rturn in Gratuitous games.
               Repeat turn on capt is forced to support
               selecting the opponent's hole for the
               captured seeds.""",
        excp=gi.GameInfoError)

    tester.test_rule(
        'grat_no_rturn',
        rule=lambda ginfo: ginfo.repeat_turn,
        msg="""Gratuitous is incompatible with any other repeat turn option""",
        excp=gi.GameInfoError)
        # catch any repeat turn opts not already covered by other other rules

    tester.test_rule(
        'grat_no_pick',
        rule=lambda ginfo: ginfo.pickextra,
        msg="""Gratuitous is incompatible with PICKEXTRA""",
        excp=gi.GameInfoError)

    skip_set = skip if skip else set()
    skip_set |= {'no_sides_bad_capt_side'}
    mancala.Mancala.rules(ginfo, holes, skip=skip_set)


# %% Gratuitous abstract class

@dc.dataclass(frozen=True, kw_only=True)
class GratState(mancala.GameState):
    """Create a state for the Gratuitous game.
    GameStates must be immutable! Especially for the analysis scripts."""

    empty_store: bool = False


class Gratuitous(mancala.Mancala, abc.ABC):
    """Gratuitous is a game class in which 'captured' seeds
    from your own side of the board are forced upon your
    opponent. When a capture is done a second turn allows
    selection of an opponent's hole to define where the capture
    should be 'shared'.

    An abc because it doesn't make sense to use this if all
    holes are sown."""

    def __init__(self, game_consts, game_info):

        # force no_sides to True to allow UI to activate holes on both sides
        # set MLENGTH to 3 (game info didn't do it when it was created)
        object.__setattr__(game_info, ckey.NO_SIDES, True)
        object.__setattr__(game_info, ckey.MLENGTH, 3)

        super().__init__(game_consts, game_info)

        # when true the next turn must empty the store (move seeds to op hole)
        self.empty_store = False


    @property
    def state(self):
        """Create an SSGameState"""
        return GratState(empty_store=self.empty_store,
                         **(dc.asdict(super().state)))


    @state.setter
    def state(self, state):
        """Fill current state.
        The mancala state setter ignores fields in the dataclass
        that it doesn't know about."""

        mancala.Mancala.state.fset(self, state)
        self.empty_store = state.empty_store


    @property
    def board_state(self):
        """Return the equivalent board state."""

        return GratState(empty_store=self.empty_store,
                         **(dc.asdict(super().board_state)))


    def new_game(self, new_round=False):

        super().new_game(new_round)
        self.empty_store = False


    def end_game(self, *, quitter, user, game=True):
        """call end game and clear the store"""
        cond = super().end_game(quitter=quitter, user=user, game=game)
        self.empty_store = False
        return cond


    def capture_seeds(self, mdata):
        """Do the base capture seeds, if there was a capture
        setup a repeat turn with empty_store of TRUE."""

        super().capture_seeds(mdata)
        if mdata.captured:
            game_log.add("Repeat turn, select seed location")
            mdata.captured = gi.WinCond.REPEAT_TURN
            mdata.repeat_turn = True
            self.empty_store = True


    def move(self, move):
        """If the move is an EMPTY_STORE, move the store
        seeds to the selected hole, log move and swap turn.
        In this case the game cannot end, the previous
        non-EMPTY_STORE move would have detected the win.

        Otherwise, have the parent class do the move."""

        if self.empty_store:
            game_log.add(f"Empty store move @ {move}")
            cur_turn = self.turn
            coll = self.cts.xlate_pos_loc(move[0], move[1])
            self.board[coll] += self.store[self.turn]
            self.store[self.turn] = 0
            self.empty_store = False

            self.turn = not self.turn
            self._log_turn(move_data.MoveData.make_move(cur_turn, move))
            return None

        return super().move(move)


# %%  concrete classes

class NSGratuitous(Gratuitous, two_cycle.NorthSouthCycle):
    """Pair the Gratuitous mixin-ish with North South Cycles."""

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """Test rules for the class."""

        test_grat_rules(ginfo, holes, skip)
        two_cycle.NorthSouthCycle.rules(ginfo, holes, skip)


    def get_allowable_holes(self):
        """If EMPTY_STORE allow selection of any of opponents holes.
        Otherwise, only allow own holes that are allowable."""

        if self.empty_store:
            holes = self.cts.holes
            if self.turn:
                allows = [True] * holes + [False] * holes
            else:
                allows = [False] * holes + [True] * holes

        else:
            allows = super().get_allowable_holes()
            for loc in self.cts.get_opp_range(self.turn):
                allows[loc] = False

        return allows


class EWGratuitous(Gratuitous, two_cycle.EastWestCycle):
    """Pair the Gratuitous mixin-like class with East West Cycles."""

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """Test rules for the class."""

        test_grat_rules(ginfo, holes, skip)
        two_cycle.EastWestCycle.rules(ginfo, holes, skip)


    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        dbl_holes = self.cts.dbl_holes
        half = self.cts.half_holes
        half_x3 = half * 3
        self.false_side = [loc in range(half, half_x3)
                           for loc in range(dbl_holes)]
        self.true_side =  [not val for val in self.false_side]


    def get_allowable_holes(self):
        """If EMPTY_STORE allow selection of any of opponents holes.
        Otherwise, only allow own holes that are allowable."""

        if self.empty_store:
            if self.turn:
                allows = self.false_side
            else:
                allows = self.true_side

        else:
            pallow = mancala.Mancala.get_allowable_holes(self)
            allows = [allow and (self.turn == thole)
                      for thole, allow in zip(self.true_side, pallow)]

        return allows
