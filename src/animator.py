# -*- coding: utf-8 -*-
"""Capture changes in state to the mancala class and replay
them as an animation.

Three animation actions are supported:

    - state variable update
    - message
    - call back

Mechanics:

Hooks are put into the Mancala class state variables that
get animated, see AniList. Each update to one of these
state variables gets recorded in Animator.queue.

When the first animation action is recorded (add to an
empty queue), the game state is recorded to facilitate
playback of the queue.

In MancalaUI.refresh the animator is started, if refresh
was called where an animation is expected: after a move
and after the ai moves.

Created on Sun Apr 13 05:25:44 2025
@author: Ann"""


# %% imports

import abc
import collections

import game_interface as gi
import ui_utils


# %% constants

STORE = 'store'
BOARD = 'board'
DELAYS = [200, 600, 1000]


# %% the global stuff

# set False to completely disable the animator
# e.g. for analysis scripts
# for full effect set before Mancala and MancalaUI are built

ENABLED = True


# Global so that the mancala.Mancala attributes can access when
# they are AniLists

# pylint:  disable=invalid-name
animator = None

def make_animator(game_ui):
    """Make the animator class."""

    # pylint: disable=global-statement
    global animator

    if ENABLED:
        animator = Animator(game_ui)


def active():
    """Determine if the animator is currently active.
    A global function in case the animator was not built."""

    return ENABLED and animator and animator.active


def set_active(new_state):
    """Set the animator state.
    A global function in case the animator was not built."""

    if ENABLED and animator:
        animator.active = new_state


# %% support classes

class AniList:
    """A replacement class for list state variables in the
    Mancala class. This captures state changes and records
    them as animation events.

    The events still must be executed immediately, in case
    other code makes decisions on the new value."""

    def __init__(self, attrib, value):

        self.attrib = attrib
        self.values = value


    def __str__(self):

        return f"AniList({self.attrib}, {self.values})"


    def __reversed__(self):
        """Return the array in the reversed order.
        The property will convert this back into an AniList on
        assignment"""

        return reversed(self.values)


    def __getitem__(self, key):

        return self.values[key]


    def __setitem__(self, key, value):

        self.values[key] = value
        if animator:
            animator.change(self.attrib, key, value)


    def copy(self):
        """If the 'list' is being copied, it is likely
        for a purpose other than animation.

        Return a copy of the list values."""

        return self.values.copy()


    def count(self, value):
        """Wrap the count operation."""

        return self.values.count(value)


class AniGameState:
    """The game state elements that are animated.

    Captured at the start of an animation sequence and updated
    as animation steps are executed."""

    def __init__(self, game):

        self.board = game.board.copy()
        self.store = game.store.copy()
        self.unlocked = game.unlocked.copy()
        self.blocked = game.blocked.copy()
        self.child = game.child.copy()

    def setvalue(self, attrib, idx, value):
        """Update the list associated with attrib to
        have element idx be value."""

        getattr(self, attrib)[idx] = value


# %%  animation actions

class AniAction(abc.ABC):
    """Interface for animation actions."""

    @abc.abstractmethod
    def do_it(self, game_ui, ani_state):
        """Execture the action"""


class Flash(AniAction):
    """Do a flash of the specified hole. Use this 2x."""

    def __init__(self, row, pos):

        self.row = row
        self.pos = pos

    def __str__(self):

        return f"Flash({self.row}, {self.pos})"


    def do_it(self, game_ui, ani_state):

        game_ui.disp[self.row][self.pos].flash()


class SetStateVar(AniAction):
    """An animation step, that can be captured and executed later"""

    def __init__(self, attrib, idx, value):

        self.attrib = attrib
        self.idx = idx   # turn if attrib is STORE else loc
        self.value = value


    def __str__(self):

        return f"SetStateVar({self.attrib}, {self.idx}, {self.value})"


    def do_it(self, game_ui, ani_state):
        """Execute the action."""

        if self.attrib == STORE:
            store_ui = game_ui.stores[not self.idx]
            store_ui.set_store(self.value, game_ui.game.turn == bool(self.idx))
            ani_state.store[self.idx] = self.value

        else:
            ani_state.setvalue(self.attrib, self.idx, self.value)

            hprop = gi.HoleProps(seeds=ani_state.board[self.idx],
                                 unlocked=ani_state.unlocked[self.idx],
                                 blocked=ani_state.blocked[self.idx],
                                 ch_owner=ani_state.child[self.idx],
                                 # not animated
                                 owner=game_ui.game.owner[self.idx]
                                )

            row = not game_ui.game.cts.board_side(self.idx)
            pos = game_ui.game.cts.xlate_pos_loc(row, self.idx)
            game_ui.disp[row][pos].set_props(hprop, None)


class Message(AniAction):
    """Generate a message in the animation sequence."""

    def __init__(self, message):

        self.message = message


    def __str__(self):

        return f"Message({self.message})"


    def do_it(self, game_ui, ani_state):
        """Execute the action."""

        # TODO put the message some place!


class ScheduleCallback(AniAction):
    """Schedule a callback function."""

    def __init__(self, func):

        self.func = func


    def __str__(self):

        return f"ScheduleCallback({self.func})"


    def do_it(self, game_ui, ani_state):
        """Execute the action."""

        self.func()

# %% the main animator class

class Animator:
    """The animator class.

    Collects a queue of state changes and replays them
    one at a time when do_animation is called."""

    def __init__(self, game_ui):

        self.game_ui = game_ui
        self.queue = collections.deque()
        self.delay = 250

        self._active = ENABLED

        self.ani_state = None


    @property
    def active(self):
        """The active property."""
        return self._active


    @active.setter
    def active(self, value):
        """Set active to value."""


        self._active = value



    def set_speed(self, speed):
        """Set the delay associated with the speed 1 fast ..3 slow"""

        self.active = True
        self.delay = DELAYS[speed - 1]


    def clear_queue(self):
        """Clear the animation queue."""

        self.queue.clear()


    def add(self, anie):
        """Queue an event.
        If we haven't yet captured the starting game state,
        capture it"""

        if not self.ani_state:
            self.ani_state = AniGameState(self.game_ui.game)

        self.queue.append(anie)


    def flash(self, turn, *, move=None, loc=None):
        """Record a button flash action, if active."""

        if self._active:

            if move is not None:
                if isinstance(move, int):
                    row, pos = not turn, move
                elif len(move) == 2:
                    row, pos = not turn, move[0]
                elif len(move) == 3:
                    row, pos = move[0], move[1]

            elif loc < self.game_ui.game.cts.holes:
                row, pos = loc < self.game_ui.game.cts.holes, loc
            else:
                row, pos = (loc < self.game_ui.game.cts.holes,
                            self.game_ui.game.cts.dbl_holes - loc - 1)

            self.add(Flash(row, pos))
            self.add(Flash(row, pos))


    def change(self, attrib, idx, value):
        """Record a change in state that should be animated,
        if active."""


        if self._active:

            if ((attrib == STORE and not self.game_ui.stores)
                    or (attrib == BOARD and self.game_ui.game.blocked[idx])):
                # don't animate things we can't see
                #   - store updates when they are not on the UI
                #   - seeds removed from a blocked hole (already an X)
                return

            self.add(SetStateVar(attrib, idx, value))


    def message(self, message):
        """Record a message in the animation sequence,
        if active."""

        if self._active:
            self.add(Message(message))


    def queue_callback(self, func):
        """Put a function callback event into the animation
        queue, if active."""

        if self._active:
            self.add(ScheduleCallback(func))


    def do_animation(self):
        """Do an event from the queue and if there is more to
        do schedule it."""

        if not self.queue:
            return

        self.game_ui.config(cursor=ui_utils.ANI_ACTIVE)
        anie = self.queue.popleft()
        anie.do_it(self.game_ui, self.ani_state)

        if self.queue:
            self.game_ui.after(self.delay, self.do_animation)

        else:
            self.ani_state = None
            self.game_ui.config(cursor=ui_utils.NORMAL)
            self.game_ui.after(self.delay, self.game_ui.refresh)
