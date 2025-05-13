# -*- coding: utf-8 -*-
"""SameSide a game class in which sowing for each
player is all done on the same side of the board.

Captured seeds are place in an opponent's hole.

The game goal must be CLEAR (or the round tally version).

SameSide:  Top only sows the top row. Bottom only sows the bottom row.
Ohojichi: West only west. East only east.

Created on Sun Dec  1 07:10:20 2024
@author: Ann"""

# %% imports

import dataclasses as dc

import cfg_keys as ckey
import incrementer
import game_interface as gi
import ginfo_rules
import mancala
import move_data
import two_cycle

from game_logger import game_log


# %% rules

def build_rules():
    """Build the rules for SameSide."""

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'ss_goal_clear',
        rule=lambda ginfo: not ginfo.goal in (gi.Goal.CLEAR,
                                              gi.Goal.RND_WIN_COUNT_CLR),
        msg='SameSide requires CLEAR goal',
        excp=gi.GameInfoError)
        # CLEAR includes many base mancala rules:
        #  GS legal, children, many options prohibited

    rules.add_rule(
        'ss_no_sow_own',
        rule=lambda ginfo: ginfo.sow_own_store,
        msg="""SameSide incompatible with SOW_OWN_STORE""",
        excp=NotImplementedError)
        # The test for when to sow into store requires sowing on both sides

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
        msg="""Do not set capt_rturn in SameSide games.
               Repeat turn on capt is forced to support
               selecting the opponent's hole for the
               captured seeds.""",
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
        msg='Ohojichi requires that CAPT_SIDE be BOTH',
        excp=gi.GameInfoError)

    rules.add_rule(
        'oho_splt_udir_all',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.sow_direct == gi.Direct.SPLIT
                                   and len(ginfo.udir_holes) != holes),
        msg='Ohojichi requires that all holes be UDIR for SPLIT SOW',
        excp=gi.GameInfoError)

    rules.add_rule(
        'oho_udir_all',
        both_objs=True,
        rule=lambda ginfo, holes: (len(ginfo.udir_holes) > 0
                                   and len(ginfo.udir_holes) != holes),
        msg='Ohojichi requires that all holes be UDIR or none of them',
        excp=gi.GameInfoError)


    ss_rules = build_rules()
    del ss_rules['ss_side_own']
    rules |= ss_rules

    return rules


# %% SameSide game class

@dc.dataclass(frozen=True, kw_only=True)
class SSGameState(mancala.GameState):
    """Create a state for the SameSide game.
    GameStates must be immutable! Especially for the analysis scripts."""

    empty_store: bool = False


class SameSide(mancala.Mancala):
    """Sow only on your side of the board, deposit capture in
    opponents holes."""

    @classmethod
    @property
    def rules(cls):
        """The rules for the class but don't build them unless we
        need them."""
        return build_rules()


    def __init__(self, game_consts, game_info):

        # force no_sides to True to allow UI to activate holes on both sides
        # set MLENGTH to 3 (game info didn't do it when it was created)
        object.__setattr__(game_info, ckey.NO_SIDES, True)
        object.__setattr__(game_info, ckey.MLENGTH, 3)

        super().__init__(game_consts, game_info)

        self.deco.replace_deco('incr', incrementer.Increment,
                               two_cycle.NorthSouthIncr(self))

        # when true the next turn must empty the store (move seeds to op hole)
        self.empty_store = False


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


    @property
    def board_state(self):
        """Return the equivalent board state."""

        return SSGameState(empty_store=self.empty_store,
                           **(dc.asdict(super().board_state)))


    def new_game(self, win_cond=None, new_round_ok=False):

        super().new_game(win_cond, new_round_ok)
        self.empty_store = False


    def end_game(self, user=True):
        """call end game and clear the store"""
        cond = super().end_game(user)
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


# %%

class Ohojichi(SameSide):
    """Sow only on your side of the board east/west,
    deposit capture in opponents holes.

    These build on calls to the mancala.Mancala methods
    not the SameSide method, SameSide does the wrong things."""

    @classmethod
    @property
    def rules(cls):
        """The rules for the class but don't build them unless we
        need them."""
        return build_ew_rules()


    def __init__(self, game_consts, game_info):

        two_cycle.patch_ew_cts_ops(game_consts)
        super().__init__(game_consts, game_info)

        self.deco.replace_deco('incr', two_cycle.NorthSouthIncr,
                               two_cycle.EastWestIncr(self))

        self.empty_store = False

        holes = self.cts.holes
        dbl_holes = self.cts.dbl_holes
        half = holes // 2
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
