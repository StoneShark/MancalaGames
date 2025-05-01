# -*- coding: utf-8 -*-
"""end_move decorators for games played in rounds.

Created on Sun Nov 10 07:12:36 2024
@author: Ann"""

import end_move_decos as emd
import game_interface as gi

from game_logger import game_log


# %%  enders

class RoundWinner(emd.EndTurnIf):
    """"If the game is played in rounds where seeds collected
    are used to setup the board for a new round, let the rest
    of the chain decide the outcome, then adjust for end of
    game or end of round.

    Additionally, the game is over if either player does not have
    the minimum seeds to continue the game.  The claimer is used
    after the game is known to be over to determine if the
    round or game is over."""

    def __init__(self, game, decorator=None, sclaimer=None):
        """Init the parent deco's; then fill:

        req_seeds: the number of seeds required to keep playing
        the game.

        msg: message to log if either player has fewer
        than win_seeds"""

        super().__init__(game, decorator, sclaimer)

        nbr_start = game.cts.nbr_start
        goal_param = game.info.goal_param
        intro = "Game, not round, ended (too few seeds to fill "

        if game.info.goal == gi.Goal.TERRITORY:
            req_holes = game.cts.dbl_holes - goal_param + 1
            self.req_seeds = self.round_seeds_for_win(req_holes, nbr_start)
            self.msg = intro + f"at least {req_holes} holes)."

        elif game.info.round_fill == gi.RoundFill.UMOVE:
            self.req_seeds = game.cts.holes + game.info.min_move - 1
            self.msg = intro + "a playable side)."

        elif game.info.goal_param > 0:
            # max seeds games do not round seed counts
            self.req_seeds = game.info.goal_param * nbr_start
            self.msg = intro + f"at least {goal_param} holes)."

        else:
            self.req_seeds = nbr_start
            self.msg = intro + "a hole)."


    def game_ended(self, mdata):

        ended_in = mdata.ended
        self.decorator.game_ended(mdata)
        if ended_in is True or not mdata.win_cond:
            return

        seeds = self.sclaimer.claim_seeds()
        if seeds[True] < self.req_seeds or seeds[False] < self.req_seeds:
            mdata.end_msg = self.msg
            game_log.add(self.msg, game_log.IMPORT)

        elif mdata.win_cond == gi.WinCond.WIN:
            mdata.win_cond = gi.WinCond.ROUND_WIN

        else:   # if mdata.win_cond == gi.WinCond.TIE:
            mdata.win_cond = gi.WinCond.ROUND_TIE


class RoundTallyWinner(emd.EndTurnIf):
    """"If the game is played in rounds, let the rest of the
    chain decide the outcome, then adjust for end of game or
    end of round based on the tallier."""

    def game_ended(self, mdata):
        """ended can be truthy, but only actually end the game
        if it exactly True; otherwise we are going to end the
        round."""

        ended_in = mdata.ended
        self.decorator.game_ended(mdata)
        if ended_in is True or not mdata.win_cond:
            return

        seeds = self.sclaimer.claim_seeds()
        self.game.rtally.tally(mdata, seeds)
        rcond, rplayer = self.game.rtally.win_test()

        if rcond in (gi.WinCond.WIN, gi.WinCond.TIE):
            mdata.win_cond = rcond
            mdata.winner = rplayer

        elif mdata.win_cond == gi.WinCond.WIN:
            mdata.win_cond = gi.WinCond.ROUND_WIN

        else:  #  if mdata.win_cond == gi.WinCond.TIE:
            mdata.win_cond = gi.WinCond.ROUND_TIE



class RoundEndLimit(emd.EndTurnIf):
    """A round ender deco.  Add below one of the other
    round end decorators.

    If there are fewer than the specified number of seeds
    on the board in play, call down the decorator chain
    with ended = True.

    EndGameWinner will collect seeds as configured
    and when we return to the parent deco, it will decide
    if the game or round has ended."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)

        if game.info.rounds == gi.Rounds.END_S_SEEDS:
            self.stop_at = game.cts.nbr_start
        else:   #  if game.info.rounds == gi.Rounds.END_2S_SEEDS:
            self.stop_at = 2 * game.cts.nbr_start


    def game_ended(self, mdata):

        remaining = 0
        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is None:
                remaining += self.game.board[loc]

        if remaining <= self.stop_at:
            mdata.end_msg = f"Round limit ({self.stop_at}) or fewer seeds " \
                            + " remaining, _thing_ ended."
            game_log.add(mdata.end_msg, game_log.IMPORT)
            mdata.ended = True
            self.decorator.game_ended(mdata)

        else:
            self.decorator.game_ended(mdata)


# %%  quitter

class QuitRoundTally(emd.EndTurnIf):
    """End a round tally game. Decorator is used to end the current
    game then the tallier decides the game outcome."""

    def game_ended(self, mdata):

        self.decorator.game_ended(mdata)
        seeds = self.sclaimer.claim_seeds()
        self.game.rtally.tally(mdata, seeds)

        cond, winner = self.game.rtally.end_it()
        mdata.win_cond = cond
        mdata.winner = winner
