# -*- coding: utf-8 -*-
"""Game class the mancala game 'qelat'.
No stores are used instead 'walda's are created during
game play.

Created on Thu Jan  5 03:15:41 2023
@author: Ann"""


# %% imports

import warnings

import game_interface as gi
import mancala
import seed_collector


# %% constants

WALDA_BOTH = -1

#  index matches the gameboard
WALDA_POSS = [WALDA_BOTH, True, None, None, True, WALDA_BOTH,
              WALDA_BOTH, False, None, None, False, WALDA_BOTH]

WALDA_TEST = [[WALDA_BOTH, False],
              [WALDA_BOTH, True]]


# %%

class QelatCollector(seed_collector.SeedCollIf):
    """The rest of the deco chain may collect seeds into
    the stores (if the game has ended). If the game has
    ended or is not playable (store > 0): move the seeds
    from the stores into available waldas."""

    def claim_own_seeds(self, repeat_turn, ended=False):
        """Claim own seeds."""

        store_f, store_t = self.decorator.claim_own_seeds(repeat_turn, ended)

        if any(self.game.store):
            walda_locs = self.game.find_waldas(self)

            if all(walda_locs):
                self.game.board[walda_locs[0]] += self.game.store[0]
                self.game.board[walda_locs[1]] += self.game.store[1]

            elif walda_locs[0]:
                self.game.board[walda_locs[0]] += sum(self.game.store)

            elif walda_locs[1]:
                self.game.board[walda_locs[1]] += sum(self.game.store)

            self.game.store = [0, 0]

        assert sum(self.game.store) + sum(self.game.board) == \
            self.game.cts.total_seeds, 'Qelat: seed count error'

        return store_f, store_t


# %%  game class


class Qelat(mancala.Mancala):
    """A single-lap Mancala with two-directional movement
    and created storehouses."""

    def __init__(self, game_consts, game_info):
        """Check the game configuration.
        Call parent init.
        Add our own deco to the seed_collector chain."""

        self._check_config(game_info)
        super().__init__(game_consts, game_info)

        self.deco.collector = QelatCollector(self, self.deco.collector)


    @staticmethod
    def _check_config(game_info):
        """Check the configuration flags."""

        gflags = game_info.flags

        if not gflags.child:
            raise gi.GameInfoError('Qelat requires CHILD.')

        if not gflags.convert_cnt:
            raise gi.GameInfoError(
                'Qelat requires CONVERT_CNT to define child creation.')

        if gflags.convert_cnt not in game_info.capt_on:
            warnings.warn(
                f'Qelat makes children on {gflags.convert_cnt}s, '
                'even without capture.')

        bad_flags = ['blocks', 'capsamedir', 'crosscapt',
                     'mlaps', 'multicapt', 'oppsidecapt',
                     'rounds', 'sow_own_store', 'stores',
                     'visit_opp', 'xcpickown']

        for flag in bad_flags:
            if getattr(gflags, flag):
                raise gi.GameInfoError(
                    f'Qelat cannot be used with {flag.upper()}.')

        if gflags.evens or gflags.moveunlock:
            warnings.warn(
                'Qelat not designed to work with EVENS or MOVEUNLOCKS.')


    def find_waldas(self):
        """Find and return a walda for each side,
        if one exists."""

        walda_locs = [False, False]
        for side in (False, True):
            for walda in range(self.cts.dbl_holes):
                if self.child[walda] == side:
                    walda_locs[int(side)] = walda
                    break

        return walda_locs


    def end_game(self):
        """The user has requested that the game be ended.
        Split the seeds on the board between the sides.
        return WinCond"""

        seeds = self._get_seeds_for_divvy()
        quot, rem = divmod(seeds, 2)

        walda_locs = self.find_waldas()

        if all(walda_locs):
            self.board[walda_locs[0]] += quot
            self.board[walda_locs[1]] += quot

            store_t = sum(self.board[loc]
                          for loc in range(self.cts.dbl_holes)
                          if self.child[loc] is True)
            store_f = sum(self.board[loc]
                          for loc in range(self.cts.dbl_holes)
                          if self.child[loc] is False)

            if store_t > store_f:
                self.board[walda_locs[1]] += rem
            else:
                self.board[walda_locs[0]] += rem

        elif walda_locs[0]:
            self.board[walda_locs[0]] += seeds

        elif walda_locs[1]:
            self.board[walda_locs[1]] += seeds

        else:
            return gi.WinCond.TIE

        return self.win_conditions()


    def capture_seeds(self, loc, _):
        """Create a Walda, if we can.
        Don't capture until Walda is created.
        Then captured seeds are put in a Walda (child)."""

        if (self.board[loc] == self.info.flags.convert_cnt
                and self.child[loc] is None
                and WALDA_POSS[loc] in WALDA_TEST[self.turn]):

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
