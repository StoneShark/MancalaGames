# -*- coding: utf-8 -*-
"""Diffusion game by Mark Streere:  marksteeregames.com

Game rules: Copyright (c) January 2006 by Mark Steere

Created on Sat Nov  2 15:39:39 2024
@author: Ann"""


import game_info as gi
import mancala
import rule_tester
import sower
import two_cycle


FIVE = 5

# %% build rules for Diffusion

def test_rules(ginfo, holes, skip=None):
    """Test rules for Diffusion.
    Not much is allowed:
        - change board size, but it must be even
    Mancala rules are not tested."""

    tester = rule_tester.RuleTester(ginfo, holes, skip)

    tester.test_rule(
        'even_holes',
        both_objs=True,
        rule=lambda _, nbr_holes: nbr_holes % 2,
        msg='Diffusion requires an even number of holes',
        excp=gi.GameInfoError)

    tester.test_rule(
        'no_sides',
        rule=lambda ginfo: not ginfo.no_sides,
        msg='Diffusion requires no_sides be true',
        excp=gi.GameInfoError)
        # either player may move from any hole

    tester.test_rule(
        'goal_clear',
        rule=lambda ginfo: not ginfo.goal == gi.Goal.CLEAR,
        msg='Diffusion requires clear goal',
        excp=gi.GameInfoError)

    tester.test_rule(
        'store_for_turn',
        rule=lambda ginfo: not ginfo.stores,
        msg="""In Diffusion, make stores visible to
               identify the current player.""",
        warn=True)

    tester.test_rule(
        'goal_param',
        rule=lambda ginfo: ginfo.goal_param,
        msg='GOAL_PARAM is not used with Diffusion',
        warn=True)

    tester.test_rule(
        'gs_legal',
        rule=lambda ginfo: ginfo.grandslam,
        msg='Grandslam must be legal with Diffusion',
        excp=gi.GameInfoError)

    tester.test_rule(
        'no_allow_rule',
        rule=lambda ginfo: ginfo.allow_rule,
        msg="""Diffusion is incompatible with special allow rules""",
        excp=gi.GameInfoError)

    tester.test_rule(
        'min_move_1',
        rule=lambda ginfo: ginfo.min_move != 1,
        msg="""Diffusion requires that min_move be 1""",
        excp=gi.GameInfoError)

    round_flags = ['blocks', 'rounds', 'round_fill', 'round_starter']
    tester.test_rule(
        'no_rounds',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in round_flags),
        msg="""Diffusion is incompatible with rounds:
            """ + ', '.join(round_flags),
        excp=gi.GameInfoError)

    tester.test_rule(
        'sow_ccw',
        rule=lambda ginfo: ginfo.sow_direct != gi.Direct.CCW,
        msg="""Diffusion always sows from most CW hole
               around start hole in the CCW direction
               (sow_direct must be CCW)""",
        excp=gi.GameInfoError)

    sow_flags = ['mlaps', 'move_one', 'moveunlock', 'mustpass', 'mustshare',
                 'prescribed', 'skip_start', 'sow_rule', 'sow_start',
                 'start_pattern', 'udir_holes', 'mlap_cont', 'xc_sown']
    tester.test_rule(
        'no_sow_changes',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in sow_flags),
        msg="""Diffusion is incompatible with special sow
                methods: """ + ', '.join(sow_flags),
        excp=gi.GameInfoError)

    tester.test_rule(
        'no_sow_own',
        rule=lambda ginfo: ginfo.sow_own_store,
        msg="""Diffusion is incompatible with sow_own_store,
               2 seeds are automatically sown into the stores
               when indicated. There is no repeat turn""",
        excp=gi.GameInfoError)

    child_flags = ['child_cvt', 'child_rule', 'child_type']
    tester.test_rule(
        'no_children',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in child_flags),
        msg="""Diffusion is incompatible with children:
                """ + ', '.join(child_flags),
        excp=gi.GameInfoError)

    capt_flags = ['capt_dir', 'capt_max', 'capt_min', 'capt_type',
                  'capt_on', 'capt_rturn', 'crosscapt',
                  'evens', 'grandslam', 'multicapt', 'nocaptmoves',
                  'nosinglecapt', 'capt_side', 'pickextra', 'xcpickown']
    tester.test_rule(
        'no_capt_mech',
        rule=lambda ginfo: any(getattr(ginfo, flag) for flag in capt_flags),
        msg="""Diffusion moves seeds out of play by limiting
               seeds per hole to 5 and sowing 2 into the stores,
               all other capture mechanisms are prohibited:
               """  + ', '.join(capt_flags),
        excp=gi.GameInfoError)



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
        mdata.capt_start = loc


# %% Diffusion game classes


class DiffusionV2(mancala.Mancala):
    """Diffusion game by Mark Streere:  marksteeregames.com
    Game rules: Copyright (c) January 2006 by Mark Steere
    Version 2: win by top/bottom"""

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """Test rules for Diffusion."""
        test_rules(ginfo, holes, skip)


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

        two_cycle.patch_ew_cts_ops(game_consts)
        super().__init__(game_consts, game_info)


    def win_message(self, win_cond):
        """Return a window title and message string.
        This is only called if win_cond is truthy.
        Ender only returns WIN or none, therefore
        this is only called for win."""

        title = 'Game Over'
        player = 'Left' if self.mdata.winner else 'Right'
        message = f'{player} won by clearing all their seeds.'

        return title, message
