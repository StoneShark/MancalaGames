# -*- coding: utf-8 -*-
"""Keep a history of the last few moves and allow undos and redos.

Created on Tue May 13 12:42:04 2025
@author: Ann"""

import collections
import contextlib

class HistoryManager:
    """Record a series of game state histories.
    Allowing undoing and redoing moves."""

    def __init__(self, nbr_states):

        self.size = nbr_states
        self.history = collections.deque([], nbr_states)
        self.rotated = 0
        self.active = True


    def __str__(self):

        string = f'\nHistoryManager({self.size})\n'
        string += f'    rotated: {self.rotated}\n'
        for state in self.history:
            string += f'    {state.mcount:3} {state.turn:3} '
            string += f'{str(state.store):8} {state.board}\n'

        return string


    def clear(self):
        """Clear the game history."""

        self.history.clear()


    def record(self, game):
        """Record the game state in the history.
        Pop any states rotated to the back of the queue."""

        if not self.active:
            return

        for _ in range(self.rotated):
            self.history.pop()
        self.rotated = 0

        self.history.appendleft(game.state)


    def undo(self):
        """Return the previous game state."""

        hsteps = len(self.history)
        if hsteps <= 1 or self.rotated >= hsteps:
            return None

        self.rotated += 1
        self.history.rotate(-1)
        return self.history[0]


    def redo(self):
        """Return the next game state."""

        if not self.rotated:
            return None

        self.rotated -= 1
        self.history.rotate(1)
        return self.history[0]


    @contextlib.contextmanager
    def off(self):
        """Don't collect history while off."""

        self.active = False

        try:
            yield
        finally:
            self.active = True
