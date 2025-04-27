# -*- coding: utf-8 -*-
"""Simplified game & related stuff to test the
monte carlo tree search algorithm.

Created on Fri Jul 19 09:52:07 2024
@author: Ann"""

import enum
import contextlib
import dataclasses as dc

from context import ai_interface


# %% a game result enum

class GameResult(enum.Enum):

    DRAW = None   # want falsy
    LOSS = False
    WIN = True

    def is_ended(self):
        # if we have a game result, the game is over
        return True

    def is_win(self):
        return self.value


# %%   a hashable game state

@dc.dataclass(frozen=True, kw_only=True)
class ConnectState(ai_interface.StateIf):

    board: tuple
    _turn: bool

    @property
    def turn(self):
        return self._turn

    def __str__(self):
        return ''.join(str(b) for b in self.board) + '  ' + str(self._turn)


# %% the game


"""connect 4 is actually a 6 row, 7 column game"""

SIDE = 4
BSIZE = SIDE * SIDE

# cols, rows, diags -- columns first
BRD_TPLS = [(0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
            (0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15),
            (0, 5, 10, 15), (3, 6, 9, 12)]

PLAYERS = [1, 2]

class ConnectFour(ai_interface.AiGameIf):

    def __init__(self, board=None, turn=None):

        if board and turn:
            self.board = board
            self.turn = turn

        elif board or turn:
            assert "ConnectFour needs both or neither: board and turn."

        else:
            self.turn = True
            self.board = [0] * BSIZE

    def __str__(self):
        rval = '\n'
        for r in range(SIDE):
            for c in range(SIDE):
                rval += f'{self.board[r * SIDE + c]:2}  '
            rval += '\n'
        rval += f'Turn: {self.turn}\n'

        return rval

    @property
    def state(self):
        return ConnectState(board=tuple(self.board), _turn=self.turn)

    @state.setter
    def state(self, state):
        self.board = list(state.board)
        self.turn = state.turn

    @property
    def board_state(self):
        return ConnectState(board=tuple(self.board), _turn=self.turn)

    @contextlib.contextmanager
    def save_restore_state(self):
        """A context manager that saves and restores state"""

        saved_state = self.state

        try:
            yield
        finally:
            self.state = saved_state

    def get_turn(self):
        return self.turn

    def get_winner(self):
        return self.turn

    def get_moves(self):
        return [col for col in range(SIDE) if not self.board[col]]

    def game_result(self):
        """Returns win, loss or draw in terms of the current player.
        Return DRAW as soon as we know there cannot be a winner."""

        poswin = []
        for wtpl in BRD_TPLS:
            tokens = [self.board[pos] for pos in wtpl if self.board[pos]]
            tkn_cnt = len(set(tokens))

            if len(tokens) == 4 and tkn_cnt == 1:
                if tokens[0] == self.turn:
                    return GameResult.WIN
                elif tokens[0] != self.turn:
                    return GameResult.LOSS

            poswin += [tkn_cnt == 1]

        if not any(poswin) or all(self.board[pos] for pos in range(BSIZE)):
            return GameResult.DRAW

        return None

    def move(self, column):
        """Drop a token in column and change the turn. """

        for cpos in reversed(BRD_TPLS[column]):
            if not self.board[cpos]:
                self.board[cpos] = self.turn
                break
        else:
            assert False, 'Invalid move'

        result = self.game_result()
        if not result:
            if self.turn == PLAYERS[0]:
                self.turn = PLAYERS[1]
            else:
                self.turn = PLAYERS[0]

        return result


# %% the player

class DumbPlayer(ai_interface.AiPlayerIf):

    def __init__(self, _1, _2):
        pass
    def difficulty(self):  # from game
        pass
    def pick_move(self):   # from game
        pass
    def get_move_desc(self):  # from game
        pass
    def clear_history(self):  # from game
        pass
    def is_max_player(self):  # mcts doesn't use
        pass
    def score(self, _):        # mcts doesn't use
        pass
