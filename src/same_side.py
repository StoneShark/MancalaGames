# -*- coding: utf-8 -*-
"""SameSide a game class in which sowing for each
player is all done on the same side of the board.

SameSide:  Top only sows the top row. Bottom only sows the bottom row.
Ohojichi: West only west. East only east.

Created on Sun Dec  1 07:10:20 2024
@author: Ann"""

# %% imports

import dataclasses as dc
import textwrap

import cfg_keys as ckey
import diffusion
import incrementer
import game_interface as gi
import ginfo_rules
import mancala

from game_logger import game_log


# %% rules

def build_rules():
    """Build the rules for SameSide."""

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'ss_goal_clear',
        rule=lambda ginfo: not ginfo.goal == gi.Goal.CLEAR,
        msg='SameSide requires CLEAR goal',
        excp=gi.GameInfoError)
        # CLEAR includes many base mancala rules:
        #  GS legal, many options prohibited

    rules.add_rule(
        'ss_no_spatter',
        rule=lambda ginfo: ginfo.start_pattern,
        msg="""SameSide is incompatible with start patterns.""",
        excp=gi.GameInfoError)
        # they all seem odd for the game concept

    rules.add_rule(
        'ss_no_arule',
        rule=lambda ginfo: ginfo.allow_rule,
        msg="""SameSide is incompatible with special allow rules.""",
        excp=gi.GameInfoError)
        # they all seem odd for the game concept

    rules.add_rule(
        'ss_no_sow_own',
        rule=lambda ginfo: ginfo.sow_own_store,
        msg="""SameSide incompatible with SOW_OWN_STORE""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'ss_no_presowcapt',
        rule=lambda ginfo: ginfo.presowcapt,
        msg="""SameSide incompatible with PRESOWCAPT""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'ss_no_sowrule',
        rule=lambda ginfo: ginfo.sow_rule,
        msg="""SameSide incompatible with SOW_RULE""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'ss_no_xcapt',
        rule=lambda ginfo: ginfo.crosscapt,
        msg="""SameSide incompatible with CROSSCAPT""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'ss_side_own',
        rule=lambda ginfo: ginfo.capt_side != gi.CaptSide.OWN_SIDE,
        msg="""SameSide requires that CAPT_SIDE be OWN_SIDE""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'ss_no_moveunlock',
        rule=lambda ginfo: ginfo.moveunlock,
        msg="""SameSide is incompatible with MOVEUNLOCK""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'ss_no_capt_rturn',
        rule=lambda ginfo: ginfo.capt_rturn,
        msg=textwrap.dedent("""\
                            Do not set capt_rturn in SameSide games.
                            Repeat turn on capt is forced to support
                            selecting the opponent's hole for the
                            captured seeds."""),
        excp=gi.GameInfoError)

    rules.add_rule(
        'ss_no_pick',
        rule=lambda ginfo: ginfo.pickextra,
        msg="""SameSide is incompatible with PICKEXTRA""",
        excp=gi.GameInfoError)

    # add in the mancala rules, delete those we don't want
    man_rules = ginfo_rules.build_rules()
    del man_rules['no_sides_bad_capt_side']
    rules |= man_rules

    return rules


def build_ew_rules():
    """Build the rules for SameSide.
    We want the more specific rules first."""

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'oho_even',
        both_objs=True,
        rule=lambda _, holes: holes % 2,
        msg='Ohojichi requires an even number of holes per side',
        excp=gi.GameInfoError)

    rules.add_rule(
        'oho_side_both',
        rule=lambda ginfo: ginfo.capt_side != gi.CaptSide.BOTH,
        msg="Ohojichi requires that CAPT_SIDE be BOTH",
        excp=gi.GameInfoError)

    rules.add_rule(
        'oho_splt_udir_all',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.sow_direct == gi.Direct.SPLIT
                                   and len(ginfo.udir_holes) != holes),
        msg="Ohojichi requires that all holes be UDIR for SPLIT SOW",
        excp=gi.GameInfoError)

    rules.add_rule(
        'oho_udir_all',
        both_objs=True,
        rule=lambda ginfo, holes: (len(ginfo.udir_holes) > 0
                                   and len(ginfo.udir_holes) != holes),
        msg="Ohojichi requires that all holes be UDIR or none of them",
        excp=gi.GameInfoError)


    ss_rules = build_rules()
    del ss_rules['ss_side_own']
    rules |= ss_rules

    return rules


# %% deco additions

class BoardSideIncr(incrementer.IncrementerIf):
    """Increment that keeps seeds only on your own side
    of the board: TOP/BOTTOM
    This is a replacement for the Increment (the base incr class).

    This incrementer is dependent on TURN, which is ok
    because the incrementer will always be used on the same side
    as the current turn.   That is, never a need to increment
    through opponents holes, because sows and captures only
    occur on our side of the board."""

    def incr(self, loc, direct, _=incrementer.NOSKIPSTART):
        """Do an increment."""

        loc = (loc + direct) % self.game.cts.holes
        if self.game.turn:
            loc += self.game.cts.holes

        return loc


class EastWestIncr(incrementer.IncrementerIf):
    """Increment that keeps seeds only on your own side
    of the board: EAST/WEST
    This is a replacement for the Increment (the base incr class)."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        dbl_holes = game.cts.dbl_holes
        half = game.cts.holes // 2
        half_3x = half * 3

        self.ccw_map = list(range(1, dbl_holes)) + [0]
        self.ccw_map[half - 1] = half_3x
        self.ccw_map[half_3x - 1] = half

        self.cw_map = [11] + list(range(dbl_holes - 1))
        self.cw_map[half] = half_3x - 1
        self.cw_map[half_3x] = half - 1


    def incr(self, loc, direct, _=incrementer.NOSKIPSTART):
        """Do an increment. Do the direction check at play-time
        to support UDIR sow."""

        if direct == gi.Direct.CCW:
            return self.ccw_map[loc]

        return self.cw_map[loc]


# %% SameSide game class

@dc.dataclass(frozen=True, kw_only=True)
class SSGameState(mancala.GameState):
    """Create a state for the SameSide game.
    GameStates must be immutable! Especially for the analysis scripts."""

    empty_store: bool = False


class SameSide(mancala.Mancala):
    """Sow only on your side of the board, deposit capture in
    opponents holes."""

    rules = build_rules()

    def __init__(self, game_consts, game_info):

        # override mlength value in the game_info
        object.__setattr__(game_info, ckey.MLENGTH, 3)
        super().__init__(game_consts, game_info)

        self.fix_incr_deco(BoardSideIncr)

         # when true the next turn must empty the store (move seeds to op hole)
        self.empty_store = False


    def fix_incr_deco(self, new_class):
        """Replace the Increment deco with BoardSideIncr.
        Increment is always at the bottom of the deco chain."""

        incr = self.deco.incr
        if isinstance(incr, incrementer.Increment):
            self.deco.incr = new_class(self)
            return

        while (incr.decorator
               and not isinstance(incr.decorator, incrementer.Increment)):
            incr = incr.decorator
        assert incr.decorator, "Didn't find Increment in deco chain."

        incr.decorator = new_class(self)


    @property
    def state(self):
        """Create an SSGameState"""
        return SSGameState(empty_store=self.empty_store,
                           **(dc.asdict(super().state)))


    @state.setter
    def state(self, state):
        """Fill current state.
        The mancala state setter ignores fields in the dataclass
        that it doesn't know about."""

        mancala.Mancala.state.fset(self, state)
        self.empty_store = state.empty_store


    def new_game(self, win_cond=None, new_round_ok=False):

        super().new_game(win_cond, new_round_ok)
        self.empty_store = False


    def end_game(self):
        """call end game and clear the store"""
        cond = super().end_game()
        self.empty_store = False
        return cond


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


    def capture_seeds(self, mdata):
        """Do the base capture seeds, if there was a capture
        setup a repeat turn with empty_store of TRUE."""

        super().capture_seeds(mdata)
        if mdata.captured:
            game_log.add("Repeat turn, select seed location")
            mdata.captured = gi.WinCond.REPEAT_TURN
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

            self._log_turn(cur_turn, move, None)
            self.turn = not self.turn
            return None

        return super().move(move)


# %%

class Ohojichi(SameSide):
    """Sow only on your side of the board east/west,
    deposit capture in opponents holes.

    These build on calls to the mancala.Mancala methods
    not the SameSide method, SameSide does the wrong things."""

    rules = build_ew_rules()

    def __init__(self, game_consts, game_info):
        # pylint: disable=non-parent-init-called
        # pylint: disable=super-init-not-called
        # pylint: disable=duplicate-code

        # override mlength value in the game_info
        object.__setattr__(game_info, ckey.MLENGTH, 3)
        mancala.Mancala.__init__(self, game_consts, game_info)

        self.deco.ender = diffusion.ClearSideEndGame(self)
        self.fix_incr_deco(EastWestIncr)
        self.empty_store = False

        holes = self.cts.holes
        half = holes // 2
        self.true_holes = tuple([True] * half
                                + [False] * holes
                                + [True] * half)


    def get_allowable_holes(self):
        """If EMPTY_STORE allow selection of any of opponents holes.
        Otherwise, only allow own holes that are allowable."""

        if self.empty_store:
            if self.turn:
                allows = [not val for val in self.true_holes]
            else:
                allows = list(self.true_holes)

        else:
            pallow = mancala.Mancala.get_allowable_holes(self)
            allows = [allow and (self.turn == thole)
                      for thole, allow in zip(self.true_holes, pallow)]

        return allows
