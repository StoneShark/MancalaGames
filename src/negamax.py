# -*- coding: utf-8 -*-
"""Minimaxer for ai player.

Created on Mon Feb 13 15:03:50 2023
@author: Ann"""

# %%  imports

import dataclasses as dc
import random
import sys

import ai_interface


MAX_INT = sys.maxsize
MIN_INT = -sys.maxsize


# %%

@dc.dataclass
class MoveScore:
    """Scores for each move."""

    move: int   # might be int or tuple (int, direction)
    score: int


class NegaMaxer(ai_interface.AiPlayerIf):
    """A class to enable minimax to pick_moves."""

    def __init__(self, game):

        super().__init__(game)

        # this is not in the interface!!
        assert not self.game.info.flags.sow_own_store, \
            "Don't use NegaMax if there can be repeat turns."

        self.max_depth = 5
        self.last_scores = None


    def negamax(self, pmult, depth=0, alpha=MIN_INT, beta=MAX_INT):
        """Run a negamax with alpha/beta pruning from the
        current game state.
        Call w/o paramters on initial call.

        ASUMES alternating turns"""

        moves = self.game.get_moves()
        assert moves, 'Minimaxer called when no moves available.'


        best_moves = []
        best_score = MIN_INT
        last_scores = ''
        saved_state = self.game.state

        for move in moves:
            cond = self.game.move(move)

            if cond and cond.is_ended() or depth + 1 == self.max_depth:
                score = -pmult * self.game.score(cond)
            else:
                score = -self.negamax(-pmult, depth + 1, -beta, -alpha)

            self.game.state = saved_state

            last_scores += f'm{move} {score}, '
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves += [move]

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        if depth > 0:
            return best_score

        self.last_scores = 'AI Player ' + last_scores
        return random.choice(best_moves)


    def pick_move(self):
        """Run negamaxer."""

        return self.negamax(-1 if self.game.is_max_player() else 1)


    def get_move_desc(self):
        """Return a description of the last move."""
        return self.last_scores


    def set_params(self, params):
        """Set the parameters based on difficulty."""
        self.max_depth = params
