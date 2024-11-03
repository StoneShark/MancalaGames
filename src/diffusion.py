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
        'store_for_turn',
        rule=lambda ginfo: not ginfo.stores,
        msg=textwrap.dedent("""\
                            In Diffusion, keeping track of the
                            current player is hard w/o stores."""),
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
                         self.game.cts.cross_from_loc,
                         one_ccw]   # filler loc, it wont be used

    def sow_seeds(self, mdata):
        """Sow seeds."""

        move_from = mdata.sow_loc
        loc = self.incr_ops[0](move_from)
        sow_str = 2

        for idx in range(mdata.seeds):

            if (sow_str
                and ((move_from == self.game.cts.holes - 1
                      and loc == self.game.cts.holes)
                     or (move_from == self.game.cts.dbl_holes - 1
                         and not loc))):
                self.game.store[0] += 1
                sow_str -= 1
                # don't move on until we've put 2 seeds in the store

            else:
                if self.game.board[loc] == FIVE:
                    self.game.store[0] += 1
                else:
                    self.game.board[loc] += 1

                loc = self.incr_ops[idx + 1](loc)


class CharitySideEndGame(end_move.EndTurnIf):
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

        return None, self.game.turn


# %% Diffusion game class

class Diffusion(mancala.Mancala):
    """Diffusion game by Mark Streere:  marksteeregames.com
    Game rules: Copyright (c) January 2006 by Mark Steere"""

    rules = build_rules()

    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        self.deco.incr = None   # make certain this isn't used
        self.deco.sower = DiffusionSower(self)
        self.deco.ender = CharitySideEndGame(self)
        self.deco.quitter = end_move.QuitToTie(self)

    def win_message(self, win_cond):
        """Return a window title and message string.
        This is only called if win_cond is truthy.
        Ender only returns WIN or none, therefore
        this is only called for win."""

        title = 'Game Over'
        player = 'Left' if self.turn else 'Right'
        message = f'{player} won by giving away all their seeds.'

        return title, message
