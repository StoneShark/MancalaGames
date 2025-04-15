# -*- coding: utf-8 -*-
"""Negamaxer for ai player.

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

# pylint: disable=duplicate-code

@dc.dataclass
class MoveScore:
    """Scores for each move."""

    move: int   # might be int or tuple (int, direction)
    score: int


class NegaMaxer(ai_interface.AiAlgorithmIf):
    """A class to enable negamax to pick_moves.
    Like minimax, but requires that player's alternate turns
    (no repeat turns)."""

    def __init__(self, game, player):

        super().__init__(game, player)

        self.max_depth = 5
        self.last_scores = None

    def __str__(self):
        return f'NegaMaxer(max_depth={self.max_depth})'


    def negamax(self, pmult, depth=0, alpha=MIN_INT, beta=MAX_INT):
        """Run a negamax with alpha/beta pruning from the
        current game state.
        Call w/o paramters on initial call.

        ASSUMES alternating turns"""

        moves = self.game.get_moves()
        assert moves, 'Negamaxer called when no moves available.'

        best_moves = []
        best_score = MIN_INT
        last_scores = ''
        saved_state = self.game.state

        for move in moves:
            cond = self.game.move(move)

            if cond and cond.is_ended() or depth + 1 == self.max_depth:
                score = -pmult * self.player.score(cond)
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

        self.last_scores = 'Negamaxer ' + last_scores[:-2] + '.'
        return random.choice(best_moves)


    def pick_move(self):
        """Run negamaxer."""

        return self.negamax(-1 if self.player.is_max_player() else 1)


    def get_move_desc(self):
        """Return a description of the last move."""
        return self.last_scores


    def set_params(self, *args):
        """Set the max depth."""

        self.max_depth = args[0]
