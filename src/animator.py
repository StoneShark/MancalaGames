# -*- coding: utf-8 -*-
"""Capture changes in state to the mancala class and replay
them as an animation.

Created on Sun Apr 13 05:25:44 2025
@author: Ann"""

# %% imports


import abc
import collections

import game_interface as gi


# %% constants

STORE = 'store'
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
    animator = Animator(game_ui)


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
        self.running = False


    @property
    def active(self):
        """The active property.
        Want special actions to occur when setting false."""
        return self._active


    @active.setter
    def active(self, value):
        """If turning off animation, clear the queue."""

        if not value:
            self.queue.clear()
        self._active = value


    def set_speed(self, speed):
        """Set the delay associated with the speed 1 fast ..3 slow"""

        self.active = True
        self.delay = DELAYS[speed - 1]


    def add(self, anie):
        """Queue an event.
        If we haven't yet captured the starting game state,
        capture it"""

        if not self.ani_state:
            self.ani_state = AniGameState(self.game_ui.game)

        self.queue.append(anie)


    def change(self, attrib, idx, value):
        """Record a change in state that should be animated.
        If we are active, have been given the game_ui, and
        are in normal game play mode."""

        if self._active and self.game_ui and not self.game_ui.mode:
            self.add(SetStateVar(attrib, idx, value))


    def message(self, message):
        """Record a message in the animation sequence.
        If we are active, have been given the game_ui, and
        are in normal game play mode."""

        if self._active and self.game_ui and not self.game_ui.mode:
            self.add(Message(message))


    def queue_callback(self, func):
        """Put a function callback event into the animation
        queue."""

        if self._active and self.game_ui and not self.game_ui.mode:
            self.add(ScheduleCallback(func))


    def do_animation(self):
        """Do an event from the queue and if there is more to
        do schedule it."""

        if not self.queue:
            return

        self.running = True
        anie = self.queue.popleft()
        anie.do_it(self.game_ui, self.ani_state)

        if self.queue:
            self.game_ui.after(self.delay, self.do_animation)

        else:
            self.running = False
            self.ani_state = None
            self.game_ui.after(self.delay, self.game_ui.refresh)
