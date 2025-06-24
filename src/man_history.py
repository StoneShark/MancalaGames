# -*- coding: utf-8 -*-
"""Keep a history of the last few moves and allow undos and redos.

Created on Tue May 13 12:42:04 2025
@author: Ann"""

import collections
import contextlib

class HistoryManager:
    """Record a series of game state histories.
    Allowing undoing and redoing moves.

    size: number of states saved

    history: the deque for saved states. The currect state is on
    the left.

    rotated: count of states 'undone' or 'rotated' to the right
    end of the queue. The number of steps that can be 'redone'
    and to pop (from the right) if a new state is recorded.

    active: ingore and record calls while active is false. """

    def __init__(self, nbr_states, print_func=str):

        self.size = nbr_states
        self.print_func = print_func

        self.history = collections.deque([], nbr_states)
        self.rotated = 0
        self.active = True


    def __str__(self):

        string = f'\nHistoryManager({self.size})\n'
        string += f'    rotated: {self.rotated}\n'
        string += '\n'.join(self.print_func(state) for state in self.history)

        return string


    def clear(self):
        """Clear the game history."""

        self.rotated = 0
        self.history.clear()


    def record(self, state):
        """Record the state in the history.
        Pop any states rotated to the back of the queue."""

        if not self.active:
            return

        for _ in range(self.rotated):
            self.history.pop()
        self.rotated = 0

        self.history.appendleft(state)


    def undo(self):
        """Return the previous game state."""

        hsteps = len(self.history)
        if hsteps <= 1 or self.rotated >= hsteps - 1:
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


    def end_game_state(self):
        """If we are somewhere in the undo history, return
        the end game state. Otherwise, return None."""

        if not self.rotated:
            return None

        self.history.rotate(self.rotated)
        self.rotated = 0
        return self.history[0]
