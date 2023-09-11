# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 08:22:49 2023
@author: Ann"""



# %% imports

import mancala

from game_interface import WinCond


# %%

class NoSeedGoal(mancala.Mancala):


    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message strings."""

        if win_cond == WinCond.WIN:
            player = 'Top' if self.turn else 'Bottom'
            msg = f'{player} won by eliminating opponent seeds.'

        elif win_cond == WinCond.TIE:
            msg = 'Both players ended with seeds, consider it a tie.'

        elif win_cond == WinCond.ENDLESS:
            msg = 'Game stuck in a loop. No winner.'

        else:
            msg = f'Unexpected end condition {win_cond}.'

        return "Game Over", msg


    def win_conditions(self, _1=False, _2=False):
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
