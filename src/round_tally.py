# -*- coding: utf-8 -*-
"""Round tally class for mancala games played in rounds
that do not use hole ownership to setup for new rounds.

Created on Sun Nov 10 13:52:08 2024
@author: Ann"""

import game_interface as gi
from game_logger import game_log


class RoundTally:
    """Class to collect game data across multiple rounds.
    Collect them all even though we only use one at a time."""
    # pylint: disable=too-many-instance-attributes

    # TODO the primary param should be on the UI

    # Create a RoundTally for these game goals
    GOALS = {gi.Goal.RND_WIN_COUNT,
             gi.Goal.RND_SEED_COUNT,
             gi.Goal.RND_EXTRA_SEEDS,
             gi.Goal.RND_POINTS}

    PSTR = {gi.Goal.RND_WIN_COUNT: "Round Wins",
            gi.Goal.RND_SEED_COUNT: "Total Seeds",
            gi.Goal.RND_EXTRA_SEEDS: "Extra Seeds",
            gi.Goal.RND_POINTS: "Round Points"}

    def __init__(self, goal, req_win, total_seeds):
        """Clear the counts.
        Setup the parameter and req_win for win_test and end_it."""

        self.round_wins = [0, 0]
        self.seeds = [0, 0]
        self.diff_sums = [0, 0]
        self.score = [0, 0]

        self.skunk_seeds = (total_seeds * 3) // 4
        self.required_win = req_win

        intro = "Game, not round, ended "
        if goal == gi.Goal.RND_WIN_COUNT:
            self.parameter = lambda player: self.round_wins[player]
            self.msg = intro + f"({req_win} rounds won)."

        elif goal == gi.Goal.RND_SEED_COUNT:
            self.parameter = lambda player: self.seeds[player]
            self.msg = intro + f"({req_win} seeds won)."

        elif goal == gi.Goal.RND_EXTRA_SEEDS:
            self.parameter = lambda player: self.diff_sums[player]
            self.msg = intro + f"({req_win} extra seeds collected)."

        elif goal == gi.Goal.RND_POINTS:
            self.parameter = lambda player: self.score[player]
            self.msg = intro + f"({req_win} points won)."

        else:
            raise gi.GameInfoError("RoundTally with inappropriate game goal.")


    def __str__(self):

        rval = 'RoundTally\n'
        rval += f'   required:   {self.required_win:4}\n'
        rval += f'   sk seeds:   {self.skunk_seeds:4}\n'
        rval += f'   round_wins: {self.round_wins[0]:4}  {self.round_wins[1]:4}\n'
        rval += f'   seeds:      {self.seeds[0]:4}  {self.seeds[1]:4}\n'
        rval += f'   diff_sums:  {self.diff_sums[0]:4}  {self.diff_sums[1]:4}\n'
        rval += f'   score:      {self.score[0]:4}  {self.score[1]:4}'
        return rval

    @property
    def state(self):
        """Return the data for the game state."""

        return tuple([tuple(self.round_wins),
                      tuple(self.seeds),
                      tuple(self.diff_sums),
                      tuple(self.score)])

    @state.setter
    def state(self, value):

        self.round_wins = list(value[0])
        self.seeds = list(value[1])
        self.diff_sums = list(value[2])
        self.score = list(value[3])


    def clear(self):
        """Clear the round results tallys.
        This should be called on new_game."""

        self.round_wins = [0, 0]
        self.seeds = [0, 0]
        self.diff_sums = [0, 0]
        self.score = [0, 0]


    def tally(self, win_cond, winner, seeds):
        """Tally the outcome of the game.
        Games are tallied before WIN/TIE are possibly translated
        to ROUND_WIN/ROUND_TIE."""

        if win_cond is gi.WinCond.WIN:
            self.round_wins[winner] += 1
            self.seeds[0] += seeds[0]
            self.seeds[1] += seeds[1]

            if seeds[0] > seeds[1]:
                self.diff_sums[0] += seeds[0] - seeds[1]
                self.score[0] += 1
            elif seeds[1] > seeds[0]:
                self.diff_sums[1] += seeds[1] - seeds[0]
                self.score[1] += 1

            if seeds[0] >= self.skunk_seeds:
                self.score[0] += 1
            elif seeds[1] >= self.skunk_seeds:
                self.score[1] += 1

        if win_cond is gi.WinCond.TIE:
            self.seeds[0] += seeds[0]
            self.seeds[1] += seeds[1]

        game_log.add(str(self), game_log.DETAIL)


    def win_test(self):
        """Test if the game end conditions have been met.
        The claimer and tallier should have already been called."""

        if (self.parameter(False) == self.required_win
                and self.parameter(True) == self.required_win):
            game_log.add(self.msg, game_log.IMPORT)
            return gi.WinCond.TIE, None

        ok_win = [self.parameter(player) >= self.required_win
                  for player in (False, True)]

        if all(ok_win):
            return self.end_it()  # award win to higher total

        elif ok_win[False]:
            return gi.WinCond.WIN, False
        elif ok_win[True]:
            return gi.WinCond.WIN, True

        return None, None


    def end_it(self):
        """The game has ended, determine and outcome and winner.
        The claimer and tallier should have already been called."""

        if self.parameter(0) > self.parameter(1):
            cond, player = gi.WinCond.WIN, False

        elif self.parameter(1) > self.parameter(0):
            cond, player = gi.WinCond.WIN, True

        else:
            cond, player = gi.WinCond.TIE, None

        return cond, player
