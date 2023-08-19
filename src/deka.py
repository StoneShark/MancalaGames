# -*- coding: utf-8 -*-
"""Deka - but adjusted for two rows.  All holes can be blocked.

Created on Thu Jul 27 15:20:35 2023
@author: Ann"""

# %% imports

import game_log
import game_interface as gi
import mancala
import sower

from game_interface import WinCond

# %% constant

# Lots more than base game,
# as we reduce the number of holes, the more laps we do
MAX_LOOPS = 100


# %%  deka sowers

class DekaSower(sower.SowMethodIf):
    """Deka sower, diverts blocked holes on opp side
    to store (out of play)."""

    def sow_seeds(self, start, direct, seeds):
        """Sow seeds."""

        loc = start
        while seeds:

            loc = (loc + direct) % self.game.cts.dbl_holes

            while self.game.blocked[loc]:
                if self.game.cts.opp_side(self.game.turn, loc):
                    self.game.store[0] += 1

                    seeds -= 1
                    if not seeds:
                        return loc

                loc = (loc + direct) % self.game.cts.dbl_holes

            self.game.board[loc] += 1
            seeds -= 1

        return loc


class DekaLapper(sower.LapContinuerIf):
    """Continue sowing if end in hole with > 1 seeds, but
    stop if we ended on a blocked hole (will be opp side,
    i.e. last seed was taken out of play)."""

    def do_another_lap(self, loc, seeds):
        """Determine if we are done sowing."""

        if not self.game.blocked[loc] and self.game.board[loc] > 1:
            return True

        return False


class DekaLapSower(sower.SowMethodIf):
    """Do sow operations until until lap continuer test tells
    us to stop, closing holes along the way."""

    def __init__(self, game, decorator, lap_cont):

        super().__init__(game, decorator)
        self.lap_cont = lap_cont

    def sow_seeds(self, start, direct, seeds):
        """Sow seeds."""

        loc = start
        for _ in range(MAX_LOOPS):

            loc = self.decorator.sow_seeds(loc, direct, seeds)

            if self.lap_cont.do_another_lap(loc, seeds):
                seeds = self.game.board[loc]

                if (self.game.board[loc] == self.game.info.flags.convert_cnt
                        and self.game.cts.opp_side(self.game.turn, loc)):

                    self.game.blocked[loc] = True

                self.game.board[loc] = 0

            else:
                return loc

        game_log.add('MLAP game ENDLESS', game_log.IMPORT)
        return WinCond.ENDLESS


# %%

class Deka(mancala.Mancala):
    """Not really deka but maybe like deka."""

    def __init__(self, game_consts, game_info):
        """Check the game configuration.
        Call parent init.
        Add our own deco to the sower chain."""

        self._check_config(game_info)
        super().__init__(game_consts, game_info)

        self.deco.sower = DekaLapSower(self, DekaSower(self),
                                       DekaLapper(self))


    @staticmethod
    def _check_config(game_info):
        """Check the configuration flags."""

        gflags = game_info.flags

        good_flags = ['blocks']
        for flag in good_flags:
            if not getattr(gflags, flag):
                raise gi.GameInfoError(
                    f'Deka requires {flag.upper()}.')

        bad_flags = ['capsamedir', 'child', 'crosscapt', 'evens',
                     'moveunlock', 'multicapt', 'mustshare', 'mustpass',
                     'oppsidecapt', 'rounds', 'skip_start',
                     'sow_own_store', 'sow_start', 'stores', 'visit_opp']
        for flag in bad_flags:
            if getattr(gflags, flag):
                raise gi.GameInfoError(
                    f'Deka cannot be used with {flag.upper()}.')

        if not gflags.convert_cnt:
            raise gi.GameInfoError(
                'Deka requires CONVERT_CNT to control closing holes.')


    def end_game(self):
        """The user has requested that the game be ended.
        Give the win to the player with the most blocked holes."""

        f_seeds = sum(self.board[loc] for loc in self.cts.false_range)
        t_seeds = sum(self.board[loc] for loc in self.cts.true_range)

        if f_seeds > t_seeds:
            self.turn = False
            return WinCond.WIN

        if t_seeds > f_seeds:
            self.turn = True
            return WinCond.WIN

        return WinCond.TIE


    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message strings."""

        if win_cond in [WinCond.WIN]:
            player = 'Top' if self.turn else 'Bottom'
            msg = f'{player} won by eliminating opponent seeds.'

        elif win_cond in [WinCond.TIE]:
            msg = 'The game was ended by request.'

        elif win_cond == WinCond.ENDLESS:
            msg = 'Game stuck in a loop. No winner.'

        return "Game Over", msg


    def win_conditions(self, repeat_turn=False):
        """Check for end game.

        Return None if no victory/tie conditions are met.
        If there is a winner, turn must be that player!"""

        if all(not self.board[loc] for loc in
               self.cts.get_opp_range(self.turn)):

            return WinCond.WIN

        if all(not self.board[loc] for loc in
               self.cts.get_my_range(self.turn)):

            self.turn = not self.turn
            return WinCond.WIN

        return None
