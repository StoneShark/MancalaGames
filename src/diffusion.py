# -*- coding: utf-8 -*-
"""Diffusion game by Mark Streere:  marksteeregames.com

Game rules: Copyright (c) January 2006 by Mark Steere

Created on Sat Nov  2 15:39:39 2024
@author: Ann"""

import textwrap

import end_move
import game_interface as gi
import ginfo_rules
import mancala
import sower


FIVE = 5

# %% build rules for Diffusion

def build_rules():
    """Build the rules for Diffusion.
    Not much is allowed:
        - change board size, but it must be even
        - stores can be included or not (useful to know whose turn it is)
          thier contents do not matter to game play
    """

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'even_holes',
        both_objs=True,
        rule=lambda _, nbr_holes: nbr_holes % 2,
        msg='Diffusion requires an even number of holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'no_sides',
        rule=lambda ginfo: not ginfo.no_sides,
        msg='Diffusion require no_sides be true',
        excp=gi.GameInfoError)
        # either player may move from any hole

    rules.add_rule(
        'goal_clear',
        rule=lambda ginfo: not ginfo.goal == gi.Goal.CLEAR,
        msg='Diffusion requires clear goal',
        excp=gi.GameInfoError)

    rules.add_rule(
        'store_for_turn',
        rule=lambda ginfo: not ginfo.stores,
        msg=textwrap.dedent("""\
                            In Diffusion, make stores visible to
                            the current player."""),
        warn=True)

    rules.add_rule(
        'gparam_one',
        rule=lambda ginfo: ginfo.gparam_one,
        msg='GPARAM_ONE is not used in Diffusion.',
        warn=True)

    rules.add_rule(
        'gs_legal',
        rule=lambda ginfo: ginfo.grandslam,
        msg='Grandslam must be legal in Diffusion.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'no_allow_rule',
        rule=lambda ginfo: ginfo.allow_rule,
        msg="""Diffusion is incompatible with special allow rules.""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'min_move_1',
        rule=lambda ginfo: ginfo.min_move != 1,
        msg="""Diffusion requires that min_move be 1.""",
        excp=gi.GameInfoError)

    round_flags = ['blocks', 'rounds', 'round_fill', 'round_starter']
    rules.add_rule(
        'no_rounds',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in round_flags),
        msg="""Diffusion is incompatible with rounds: """ \
            + ', '.join(round_flags),
        excp=gi.GameInfoError)

    rules.add_rule(
        'sow_ccw',
        rule=lambda ginfo: ginfo.sow_direct != gi.Direct.CCW,
        msg=textwrap.dedent("""\
                            Diffusion always sows from most CW hole
                            around start hole in the CCW direction
                            (sow_direct must be CCW)."""),
        excp=gi.GameInfoError)

    sow_flags = ['mlaps', 'move_one', 'moveunlock', 'mustpass', 'mustshare',
                 'prescribed', 'skip_start', 'sow_rule', 'sow_start',
                 'start_pattern', 'udir_holes', 'visit_opp', 'xc_sown']
    rules.add_rule(
        'no_sow_changes',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in sow_flags),
        msg=textwrap.fill("""Diffusion is incompatible with special sow \
                          methods: """ + ', '.join(sow_flags),
                          width=50),
        excp=gi.GameInfoError)

    rules.add_rule(
        'no_sow_own',
        rule=lambda ginfo: ginfo.sow_own_store,
        msg=textwrap.dedent("""\
                            Diffusion incompatible with sow_own_store,
                            2 seeds are automatically sown into the stores
                            when indicated. There is no repeat turn."""),
        excp=gi.GameInfoError)

    child_flags = ['child_cvt', 'child_rule', 'child_type']
    rules.add_rule(
        'no_children',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in child_flags),
        msg=textwrap.fill("""Diffusion is incompatible with children: """ \
                          + ', '.join(child_flags),
                          width=50),
        excp=gi.GameInfoError)

    capt_flags = ['capsamedir', 'capt_max', 'capt_min', 'capt_next',
                  'capt_on', 'capt_rturn', 'capttwoout', 'crosscapt',
                  'evens', 'grandslam', 'multicapt', 'nocaptfirst',
                  'nosinglecapt', 'oppsidecapt', 'pickextra', 'xcpickown']
    rules.add_rule(
        'no_capt_mech',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in capt_flags),
        msg=textwrap.dedent("""\
                            Diffusion moves seeds out of play by limiting
                            seeds per hole to 5 and sowing 2 into the stores,
                            all other capture mechanisms are prohibited: """ \
                          + ', '.join(capt_flags)),
        excp=gi.GameInfoError)

    return rules


# %% deco replacements

class DiffusionSower(sower.SowMethodIf):
    """Sow counter-clockwise around start hole from the hole that is
    most clockwise."""

    def __init__(self, game, decorator=None):

        def one_ccw(loc):
            return (loc + 1) % self.game.cts.dbl_holes

        super().__init__(game, decorator)

        self.incr_ops = [one_ccw,
                         self.game.cts.cross_from_loc,
                         one_ccw,
                         one_ccw,
                         self.game.cts.cross_from_loc]

        btm_left = 0
        btm_right = self.game.cts.holes - 1
        top_right = self.game.cts.holes
        top_left = self.game.cts.dbl_holes - 1

        # dict move_from: divert out of play at loc
        self.divert_loc = {btm_left: top_left,
                           btm_right: btm_right,
                           top_right: btm_right,
                           top_left: top_left}

    def sow_seeds(self, mdata):
        """Sow seeds."""

        move_from = loc = mdata.sow_loc
        divert_loc = self.divert_loc.get(move_from, -1)

        sow_str = 2

        for idx in range(mdata.seeds):

            if sow_str and loc == divert_loc:
                self.game.store[0] += 1
                sow_str -= 1
                # don't move on until we've put 2 seeds in the store

            else:
                loc = self.incr_ops[idx](loc)

                if self.game.board[loc] == FIVE:
                    self.game.store[0] += 1
                else:
                    self.game.board[loc] += 1

        # this isn't actually used because all capts must be off
        mdata.capt_loc = loc


class ClearSideEndGame(end_move.EndTurnIf):
    """Win by giving away all seeds or your left/right side of the board."""

    def __init__(self, game, decorator=None, claimer=None):

        super().__init__(game, decorator, claimer)
        self.win_seeds = -1  # override this value

        total = game.cts.dbl_holes
        half = game.cts.holes // 2
        self.holes = [list(range(half, total - half)),
                      list(range(half)) + list(range(half * 3, total))]

    def game_ended(self, repeat_turn, ended=False):
        """Check for end game."""

        my_seeds = sum(self.game.board[loc]
                       for loc in self.holes[self.game.turn])
        if not my_seeds:
            return gi.WinCond.WIN, self.game.turn

        opp_seeds = sum(self.game.board[loc]
                        for loc in self.holes[not self.game.turn])
        if not opp_seeds:
            return gi.WinCond.WIN, not self.game.turn

        return None, self.game.turn


# %% Diffusion game classes


class DiffusionV2(mancala.Mancala):
    """Diffusion game by Mark Streere:  marksteeregames.com
    Game rules: Copyright (c) January 2006 by Mark Steere
    Version 2: win by top/bottom"""

    rules = build_rules()

    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        self.deco.incr = None   # make certain this isn't used
        self.deco.sower = DiffusionSower(self)


class Diffusion(DiffusionV2):
    """Diffusion game by Mark Streere:  marksteeregames.com
    Game rules: Copyright (c) January 2006 by Mark Steere

         True  | False
         side  | side

      11 10  9 | 8  7  6
       0  1  2 | 3  4  5"""

    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        self.deco.ender = ClearSideEndGame(self)
