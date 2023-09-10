# -*- coding: utf-8 -*-
"""Game class the mancala game 'qelat'.
No stores are used instead 'walda's are created during
game play.

Created on Thu Jan  5 03:15:41 2023
@author: Ann"""


# %% imports

import functools as ft

import end_move
import game_interface as gi
import ginfo_rules
import mancala


# %% constants

WALDA_BOTH = -1

WALDA_TEST = [[WALDA_BOTH, False],
              [WALDA_BOTH, True]]

# %%

def build_qelat_rules():
    """Refine the GameInfo rules for Qelat."""

    def rev_getattr(name, obj):
        return getattr(obj.flags, name)

    qelat_rules = ginfo_rules.build_rules()

    # add rules
    qelat_rules.add_rule(
        'need_child',
        rule=lambda ginfo: not ginfo.flags.child,
        msg='Qelat requires CHILD.',
        excp=gi.GameInfoError)

    qelat_rules.add_rule(
        'need_convert_cnt',
        rule=lambda ginfo: not ginfo.flags.convert_cnt,
        msg='Qelat requires CONVERT_CNT.',
        excp=gi.GameInfoError)

    qelat_rules.add_rule(
        'capt_conflict',
        rule=lambda ginfo: ginfo.flags.convert_cnt not in ginfo.capt_on,
        msg="Qelat makes children on convert_cnt's, even without capture.",
        warn=True)

    qelat_rules.add_rule(
        'q_not_design',
        rule=lambda ginfo: ginfo.flags.evens or ginfo.flags.moveunlock,
        msg='Qelat not designed to work with EVENS or MOVEUNLOCKS.',
        warn=True)

    bad_flags = ['blocks', 'capsamedir', 'crosscapt', 'mlaps', 'multicapt',
                 'oppsidecapt', 'rounds', 'sow_own_store', 'stores',
                 'visit_opp', 'xcpickown']
    for flag in bad_flags:
        qelat_rules.add_rule(
            f'bad_{flag}',
            rule=ft.partial(rev_getattr, flag),
            msg=f'Qelat cannot be used with {flag.upper()}.',
            excp=gi.GameInfoError)

    return qelat_rules

# %%

class QelatEndMove(end_move.EndTurnIf):
    """The rest of the deco chain may collect seeds into
    the stores (if the game has ended). Move any seeds
    from the stores into available waldas.

    Note that this code is only used if mustpass is changed
    from the default True to False."""

    def game_ended(self, repeat_turn, ended=False):
        """Qelat end move wrapper."""

        end_cond, winner = self.decorator.game_ended(repeat_turn, ended)

        if any(self.game.store):
            walda_locs = self.game.find_waldas()

            if all(loc >= 0 for loc in walda_locs):
                self.game.board[walda_locs[0]] += self.game.store[0]
                self.game.board[walda_locs[1]] += self.game.store[1]

            elif walda_locs[0] >= 0:
                self.game.board[walda_locs[0]] += sum(self.game.store)

            elif walda_locs[1] >= 0:
                self.game.board[walda_locs[1]] += sum(self.game.store)

            if any(loc >= 0 for loc in walda_locs):
                self.game.store = [0, 0]

        assert sum(self.game.store) + sum(self.game.board) == \
            self.game.cts.total_seeds, 'Qelat: seed count error'

        return end_cond, winner


# %%  game class


class Qelat(mancala.Mancala):
    """A single-lap Mancala with two-directional movement
    and created storehouses."""

    rules = build_qelat_rules()

    def __init__(self, game_consts, game_info):
        """Check the game configuration.
        Call parent init.
        Add our own deco to the seed_collector chain.
        Compute the walda possibilities based on the board size."""

        super().__init__(game_consts, game_info)
        self.deco.ender = QelatEndMove(self, self.deco.ender)

        holes = self.cts.holes
        dbl_holes = self.cts.dbl_holes

        self.walda_poses = [None] * dbl_holes
        self.walda_poses[0] = WALDA_BOTH
        self.walda_poses[holes - 1] = WALDA_BOTH
        self.walda_poses[holes] = WALDA_BOTH
        self.walda_poses[dbl_holes - 1] = WALDA_BOTH
        if holes >= 3:
            self.walda_poses[1] = True
            self.walda_poses[holes - 2] = True
            self.walda_poses[holes + 1] = False
            self.walda_poses[dbl_holes - 2] = False


    def find_waldas(self):
        """Find and return a walda for each side,
        if one exists."""

        walda_locs = [-1, -1]
        for side in (False, True):
            for walda in range(self.cts.dbl_holes):
                if self.child[walda] == side:
                    walda_locs[int(side)] = walda
                    break

        return walda_locs


    def capture_seeds(self, loc, _):
        """Create a Walda, if we can.
        Don't capture until Walda is created.
        Then captured seeds are put in a Walda (child)."""

        if (self.board[loc] == self.info.flags.convert_cnt
                and self.child[loc] is None
                and self.walda_poses[loc] in WALDA_TEST[self.turn]):

            self.child[loc] = self.turn

        if self.deco.capt_ok.capture_ok(loc):

            have_walda = False
            for walda in range(self.cts.dbl_holes):
                if self.child[walda] == self.turn:
                    have_walda = True
                    break

            if have_walda:
                self.board[walda] += self.board[loc]
                self.board[loc] = 0
