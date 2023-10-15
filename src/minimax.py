# -*- coding: utf-8 -*-
"""Minimaxer for ai player.

Created on Mon Feb 13 15:03:50 2023
@author: Ann"""

# %%  imports

import dataclasses as dc
import operator as op
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


class MiniMaxer(ai_interface.AiAlgorithmIf):
    """A class to enable minimax to pick_moves."""

    def __init__(self, game, player):

        super().__init__(game, player)

        self.max_depth = 3
        self.last_scores = None


    def minimax_ab(self, depth=0, alpha=MIN_INT, beta=MAX_INT):
        """Run a minimax with alpha/beta pruning from the
        current game state.
        Call w/o paramters on initial call."""

        moves = self.game.get_moves()
        assert moves, 'Minimaxer called when no moves available.'

        max_player = self.player.is_max_player()
        comparer = op.gt if max_player else op.lt

        best_moves = []
        best_score = MIN_INT if max_player else MAX_INT
        last_scores = ''
        saved_state = self.game.state

        for move in moves:
            cond = self.game.move(move)

            if cond and cond.is_ended() or depth + 1 == self.max_depth:
                score = self.player.score(cond)
            else:
                score = self.minimax_ab(depth + 1, alpha, beta)

            self.game.state = saved_state

            last_scores += f'm{move} {score}, '
            if comparer(score, best_score):
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves += [move]

            if max_player:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)
            if alpha >= beta:
                break

        if depth > 0:
            return best_score

        self.last_scores = 'Minimaxer ' + last_scores[:-2] + '.'
        return random.choice(best_moves)


    def pick_move(self):
        """Call the minimaxer."""

        return self.minimax_ab()


    def get_move_desc(self):
        """Return a description of the last move."""
        return self.last_scores


    def set_params(self, *args):
        """Set the max depth."""

        self.max_depth = args[0]
