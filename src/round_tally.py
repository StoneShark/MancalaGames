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

    # Create a RoundTally for these game goals
    GOALS = {gi.Goal.RND_WIN_COUNT_MAX,
             gi.Goal.RND_SEED_COUNT,
             gi.Goal.RND_EXTRA_SEEDS,
             gi.Goal.RND_POINTS,
             gi.Goal.RND_WIN_COUNT_CLR,
             gi.Goal.RND_WIN_COUNT_DEP}

    PSTR = {gi.Goal.RND_WIN_COUNT_MAX: "Round Wins",
            gi.Goal.RND_WIN_COUNT_CLR: "Round Wins",
            gi.Goal.RND_WIN_COUNT_DEP: "Round Wins",
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

        self.goal = goal

        if goal in (gi.Goal.RND_WIN_COUNT_MAX,
                    gi.Goal.RND_WIN_COUNT_CLR,
                    gi.Goal.RND_WIN_COUNT_DEP):
            self.parameter = lambda player: self.round_wins[player]

        elif goal == gi.Goal.RND_SEED_COUNT:
            self.parameter = lambda player: self.seeds[player]

        elif goal == gi.Goal.RND_EXTRA_SEEDS:
            self.parameter = lambda player: self.diff_sums[player]

        elif goal == gi.Goal.RND_POINTS:
            self.parameter = lambda player: self.score[player]

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


    def tally(self, mdata, seeds):
        """Tally the outcome of the game.
        Games are tallied before WIN/TIE are possibly translated
        to ROUND_WIN/ROUND_TIE."""

        extra = 0
        points = 0

        if mdata.win_cond is gi.WinCond.WIN:
            self.round_wins[mdata.winner] += 1
            self.seeds[0] += seeds[0]
            self.seeds[1] += seeds[1]

            if seeds[0] > seeds[1]:
                extra = seeds[0] - seeds[1]
                self.diff_sums[0] += extra
                self.score[0] += 1
            elif seeds[1] > seeds[0]:
                extra = seeds[1] - seeds[0]
                self.diff_sums[1] += extra
                self.score[1] += 1
                points = 1

            if seeds[0] >= self.skunk_seeds:
                self.score[0] += 1
                points += 1
            elif seeds[1] >= self.skunk_seeds:
                self.score[1] += 1
                points += 1

        if mdata.win_cond is gi.WinCond.TIE:
            self.seeds[0] += seeds[0]
            self.seeds[1] += seeds[1]

        if self.goal == gi.Goal.RND_EXTRA_SEEDS and extra:
            mdata.end_msg += '\n' if mdata.end_msg else ''
            mdata.end_msg += f"_winner_ collected {extra} extra seeds."

        elif self.goal == gi.Goal.RND_POINTS and points:
            if points == 1:
                mdata.end_msg += '\n' if mdata.end_msg else ''
                mdata.end_msg += f"_winner_ earned {points} point."
            else:
                mdata.end_msg += '\n' if mdata.end_msg else ''
                mdata.end_msg += f"_winner_ earned {points} " \
                    + f"points due to skunk (>= {self.skunk_seeds})."

        game_log.add(str(self), game_log.DETAIL)


    def win_test(self):
        """Test if the game end conditions have been met.
        The claimer and tallier should have already been called."""

        if (self.parameter(False) == self.required_win
                and self.parameter(True) == self.required_win):
            return gi.WinCond.TIE, None

        ok_win = [self.parameter(player) >= self.required_win
                  for player in (False, True)]

        if all(ok_win):
            return self.end_it()  # award win to higher total

        if ok_win[False]:
            return gi.WinCond.WIN, False

        if ok_win[True]:
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
