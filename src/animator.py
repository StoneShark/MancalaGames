# -*- coding: utf-8 -*-
"""Capture changes in state to the mancala class and replay
them as an animation.

Animation actions are supported:

    - state variable update
    - one step update (see context mgr one_step)
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
import contextlib
# import inspect      # used in debug code (might be commented out)

import game_interface as gi
import ui_utils


# %% constants

STORE = 'store'
BOARD = 'board'
DEFAULT_DELAY = 250


# %% the global stuff (not constants)

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


def reset():
    """Re-init the animator to be None.
    Do this on destroy of MancalaUI so remnants of a
    previous game do not exsist."""

    # pylint: disable=global-statement
    global animator

    if ENABLED:
        animator = None


def active():
    """Determine if the animator is currently active.
    A global function in case the animator was not built."""

    return ENABLED and animator and animator.active


def set_active(new_state, clear_queue=False):
    """Set the animator state.
    A global function in case the animator was not built."""

    if ENABLED and animator:
        animator.active = new_state
        if clear_queue:
            animator.clear_queue()


def set_delay(new_delay):
    """Set the animator delay.
    A global function in case the animator was not built."""

    if ENABLED and animator:
        animator.delay = new_delay


@contextlib.contextmanager
def one_step():
    """Collect multiple changes into one step.
    This deactivates the animator and then updates the
    game in one step to the current game state
    when the context is exited."""

    if ENABLED and animator:
        saved_state = animator.active
        animator.active = False

        try:
            yield
        finally:
            animator.active = saved_state
            animator.update_game()

    else:
        yield


@contextlib.contextmanager
def animate_off():
    """Turn the animator off, allow the action to occur,
    then return the animator state.
    Use this when things might change but the state
    variable hooks should be disabled. Examples:
    - when a refresh will happen unconditionally or
    - when the ai player is picking a move or
    - when a part of a move is simulated and the state
    will be restored."""

    if ENABLED and animator:
        saved_state = animator.active
        animator.active = False

        try:
            yield
        finally:
            animator.active = saved_state
    else:
        yield


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


    def __len__(self):

        return len(self.values)


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


    def __iter__(self):

        return self.values.__iter__()


    def __contains__(self, item):

        return item in self.values


    def copy(self):
        """If the 'list' is being copied, it is likely
        for a purpose other than animation.

        Return a copy of the list values."""

        return self.values.copy()


    def count(self, value):
        """Wrap the count operation."""

        return self.values.count(value)


    def index(self, value):
        """Wrap the index operation."""

        return self.values.index(value)


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
    """Animation action base class."""

    @abc.abstractmethod
    def do_it(self, game_ui, ani_state):
        """Execture the action"""


    @staticmethod
    def update_store(game_ui, ani_state, turn):
        """Make the store match the animation state."""

        game_ui.stores[not turn].set_store(ani_state.store[turn],
                                           game_ui.game.turn == bool(turn))


    @staticmethod
    def update_button(game_ui, ani_state, loc):
        """Make the button match the animation state."""

        hprop = gi.HoleProps(seeds=ani_state.board[loc],
                             unlocked=ani_state.unlocked[loc],
                             blocked=ani_state.blocked[loc],
                             ch_owner=ani_state.child[loc],
                             # not animated
                             owner=game_ui.game.owner[loc]
                            )

        row = int(loc < game_ui.game.cts.holes)
        pos = game_ui.game.cts.xlate_pos_loc(row, loc)
        game_ui.disp[row][pos].set_props(hprop, None)


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
    """An animation step, that can be captured and executed later.
    These are generated by the mancala.Mancala state variable hooks."""

    def __init__(self, attrib, idx, value):

        self.attrib = attrib
        self.idx = idx   # turn if attrib is STORE else loc
        self.value = value


    def __str__(self):

        return f"SetStateVar({self.attrib}, {self.idx}, {self.value})"


    def do_it(self, game_ui, ani_state):
        """Execute the action."""

        if self.attrib == STORE:
            ani_state.store[self.idx] = self.value
            self.update_store(game_ui, ani_state, self.idx)

        else:
            ani_state.setvalue(self.attrib, self.idx, self.value)
            self.update_button(game_ui, ani_state, self.idx)


class NewGameState(AniAction):
    """There were multiple changes to the state catch them all
    and update as one animation step.

    Not doing a 'refresh' because we need to keep ani_state
    up-to-date and we don't want any button colors changing."""

    def __init__(self, new_ani_state):

        self.astate = new_ani_state


    def __str__(self):

        return f"NewGameState({self.astate})"


    def do_it(self, game_ui, ani_state):
        """Execute the action."""

        ani_state.store = self.astate.store
        ani_state.board = self.astate.board
        ani_state.unlocked = self.astate.unlocked
        ani_state.blocked = self.astate.blocked
        ani_state.child = self.astate.child

        if game_ui.show_seeds_in_stores():
            for turn in (False, True):
                self.update_store(game_ui, ani_state, turn)

        for loc in range(game_ui.game.cts.dbl_holes):
            self.update_button(game_ui, ani_state, loc)


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
    one at a time when do_animation is called.

    queue: a dequeue of pending animation events.
    append at right, pop from left.

    active: are the animation activated. Don't collect
    animation events when this is off. Best to set
    with the global function 'animator.set_active'

    delay: milliseconds to delay (via after) between
    animation events. Best to set with the global
    function 'animator.set_delay'

    ani_state: the current state of the replaying
    animations, reflects what the current game state is
    for the state variables that are animated.
    """

    def __init__(self, game_ui):

        self.game_ui = game_ui

        self.queue = collections.deque()
        self.active = ENABLED
        self.delay = DEFAULT_DELAY
        self.ani_state = None


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

        if self.active:

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

        if self.active:

            if ((attrib == STORE and not self.game_ui.show_seeds_in_stores())
                    or (attrib == BOARD and self.game_ui.game.blocked[idx])):
                # don't animate things we can't see
                #   - store updates when they are not on the UI
                #   - seeds removed from a blocked hole (already an X)
                return

            # debug code to tell where the assignment was made
            # stack = inspect.stack()
            # caller_frame = stack[2].frame
            # caller_name = caller_frame.f_code.co_name
            # lineno = caller_frame.f_code.co_firstlineno
            # filename = caller_frame.f_code.co_filename

            anim = SetStateVar(attrib, idx, value)
            # print("animator change called from",
            #       f"{filename}:{lineno}:{caller_name}",
            #       f"for {anim}", sep="\n")
            self.add(anim)


    def update_game(self):
        """Do multiple updates to the game as one animation
        step."""

        if self.active:
            self.add(NewGameState(AniGameState(self.game_ui.game)))


    def message(self, message):
        """Record a message in the animation sequence,
        if active."""

        if self.active:
            self.add(Message(message))


    def queue_callback(self, func):
        """Put a function callback event into the animation
        queue, if active."""

        if self.active:
            self.add(ScheduleCallback(func))


    def do_animation(self):
        """Do an event from the queue and if there is more to
        do schedule it."""

        if not self.queue:
            return

        if self.active:
            self.game_ui.config(cursor=ui_utils.ANI_ACTIVE)
            anie = self.queue.popleft()
            # print(anie)    # for debugging
            anie.do_it(self.game_ui, self.ani_state)

            if self.queue:
                self.game_ui.after(self.delay, self.do_animation)

            else:
                # do refresh to hide any errors in collecting ani actions
                self.ani_state = None
                self.game_ui.config(cursor=ui_utils.NORMAL)
                self.game_ui.after(self.delay, self.game_ui.refresh)

        else:
            # an active playback was stopped
            self.ani_state = None
            self.queue.clear()
            self.game_ui.config(cursor=ui_utils.NORMAL)
            self.game_ui.refresh()
