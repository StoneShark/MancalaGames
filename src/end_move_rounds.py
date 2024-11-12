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
        gparam_one = game.info.gparam_one
        intro = "Game, not round, ended (too few seeds to fill "

        if game.info.goal == gi.Goal.TERRITORY:
            req_holes = game.cts.dbl_holes - gparam_one + 1
            self.req_seeds = self.round_seeds_for_win(req_holes, nbr_start)
            self.msg = intro + f"at least {req_holes} holes)."

        elif game.info.round_fill == gi.RoundFill.UMOVE:
            self.req_seeds = game.cts.holes + game.info.min_move - 1
            self.msg = intro + "a playable side)."

        elif game.info.gparam_one > 0:
            # max seeds games do not round seeds
            self.req_seeds = game.info.gparam_one * nbr_start
            self.msg = intro + f"at least {gparam_one} holes)."

        else:
            self.req_seeds = nbr_start
            self.msg = intro + "a hole)."

    def game_ended(self, repeat_turn, ended=False):

        cond, player = self.decorator.game_ended(repeat_turn, ended)
        if ended or not cond:
            return cond, player

        seeds = self.sclaimer.claim_seeds()
        if seeds[True] < self.req_seeds or seeds[False] < self.req_seeds:
            game_log.add(self.msg, game_log.IMPORT)
            return cond, player

        if cond == gi.WinCond.WIN:
            return gi.WinCond.ROUND_WIN, player

        # if cond == gi.WinCond.TIE:
        return gi.WinCond.ROUND_TIE, player



class RoundTallyWinner(emd.EndTurnIf):
    """"If the game is played in rounds, let the rest of the
    chain decide the outcome, then adjust for end of game or
    end of round based on the tallier."""

    def end_it(self, cond):
        """The game has ended pick a winner.
        The claimer here is not a taker, but we called down the
        deco chain to EndGameWinner which is configured with a
        taker to determine this games outcome."""

        seeds = self.sclaimer.claim_seeds()
        self.game.rtally.tally(cond, self.game.turn, seeds)

        return self.game.rtally.end_it()


    def game_ended(self, repeat_turn, ended=False):

        cond, player = self.decorator.game_ended(repeat_turn, ended)
        if not cond:
            return cond, player

        if ended:
            game_log.add("Calling RoundTallyWinner.end_it.")
            return self.end_it(cond)

        seeds = self.sclaimer.claim_seeds()
        self.game.rtally.tally(cond, player, seeds)
        rcond, rplayer = self.game.rtally.win_test()
        if rcond in (gi.WinCond.WIN, gi.WinCond.TIE):
            return rcond, rplayer

        if cond == gi.WinCond.WIN:
            return gi.WinCond.ROUND_WIN, player

        # if cond == gi.WinCond.TIE:
        return gi.WinCond.ROUND_TIE, player


# %%  quitter

class QuitRoundTally(emd.EndTurnIf):
    """End a round tally game. Decorator is used to end the current
    game then the tallier decides the game outcome."""

    def game_ended(self, repeat_turn, ended=False):

        cond, player = self.decorator.game_ended(repeat_turn, ended)
        seeds = self.sclaimer.claim_seeds()
        self.game.rtally.tally(cond, player, seeds)

        return self.game.rtally.end_it()
