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
import tkinter as tk


import game_info as gi
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
print_steps = False

def make_animator(game_ui):
    """Make the animator class."""

    global animator

    if ENABLED:
        animator = Animator(game_ui)


def reset():
    """Re-init the animator to be None.
    Do this on destroy of MancalaUI so remnants of a
    previous game do not exsist."""

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


def configure(*, font=None, msg_mult=None, bg_color=None):
    """Configure the animator settings.
    Can't import man_config directly here, so main class
    must configure the animator."""

    if not animator:
        return

    if font:
        animator.font = font

    if msg_mult:
        animator.msg_mult = msg_mult

    if bg_color:
        animator.bg_color = bg_color


def set_rollback():
    """Set the rollback point."""

    if ENABLED and animator and animator.active:
        animator.set_rollback()


def clear_rollback():
    """Clear the rollback point."""

    if ENABLED and animator and animator.active:
        animator.clear_rollback()


def do_rollback():
    """Do the rollback removing the queued events."""

    if ENABLED and animator and animator.active:
        animator.do_rollback()


@contextlib.contextmanager
def one_step():
    """Collect multiple changes into one step.
    This deactivates the animator and then updates the
    game in one step to the current game state
    when the context is exited."""

    if ENABLED and animator:
        saved_state = animator.active
        bstate = animator.game_ui.game.board_state
        animator.active = False

        try:
            yield
        finally:
            animator.active = saved_state
            if animator.game_ui.game.board_state != bstate:
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


    def __add__(self, other):
        """Return a list of the values of both objects."""

        if isinstance(other, AniList):
            ovals = other.values
        else:
            ovals = other

        return self.values + ovals


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
    """Animation action base class.

    Data is collected in the derived class __init__ so that the
    action can be simulated later. Each class type records it's
    own data.

    At a later time, the do_it operation will be called to effect
    the action on the ani_state provided."""

    @abc.abstractmethod
    def do_it(self, game_ui, ani_state):
        """Execture the action"""


    @staticmethod
    def update_store(game_ui, ani_state, turn):
        """Make the store match the animation state.
        UI stores are in the opposite order from game stores."""

        row = not turn
        mover = bool(turn if game_ui.game.mdata.repeat_turn else not turn)

        game_ui.stores[row].set_store(ani_state.store[turn],
                                      game_ui.game.turn == mover)


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
    """Generate a message in the animation sequence.
    Two actions are needed: the do_it creates and popups
    the message.  Later the close can be scheduled via a
    ScheduleCallback to destroy the window."""

    def __init__(self, message, font, bg_color):

        self.message = message
        self.font = font
        self.bg_color = bg_color

        self.tipwindow = None


    def __str__(self):

        return f"Message({self.message})"


    def do_it(self, game_ui, ani_state):
        """Execute the action."""

        self.tipwindow = tk.Toplevel(game_ui)
        self.tipwindow.wm_overrideredirect(1)

        xoffset = self.font.measure(self.message) // 2
        yoffset = self.font.metrics('linespace') // 2

        xpos = game_ui.winfo_rootx() + game_ui.winfo_width() // 2  - xoffset
        ypos = game_ui.winfo_rooty() + game_ui.winfo_height() // 2 - yoffset
        self.tipwindow.wm_geometry(f'+{xpos}+{ypos}')

        label = tk.Label(self.tipwindow, text=self.message, justify=tk.CENTER,
                         background=self.bg_color,
                         font=self.font)
        label.pack()


    def close(self):
        """Close the tip window."""

        save_tip = self.tipwindow
        self.tipwindow = None
        if save_tip:
            save_tip.destroy()



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

    Collects a queue of state changes/animator action
    and replays them one at a time in do_animation.

    active: are the animation activated. Don't collect
    animation events when this is off. Best to set
    with the global function 'animator.set_active'

    delay: milliseconds to delay (via after) between
    animation events. Best to set with the global
    function 'animator.set_delay'

    _queue: a dequeue of pending animation events.
    append at right, pop from left.

    _ani_state: the current state of the replaying
    animations, reflects what the current game state is
    for the state variables that are animated.

    _rollback_pt: a point to which the animator queue
    can be rolled backed, eliminating elements queued
    since the rollback point was set.
    """

    def __init__(self, game_ui):

        self.active = ENABLED
        self.delay = DEFAULT_DELAY

        self.game_ui = game_ui
        self._queue = collections.deque()
        self._ani_state = None
        self._rollback_pt = None
        self._pending_after = False

        self.msg_mult = 6
        self.font = None   # tkfont.Font(font=("garamond", "22", "bold"))
        self.bg_color = "#e0ffe0"


    def clear_queue(self):
        """Clear the animation queue."""

        self._queue.clear()


    def add(self, anie):
        """Queue an event.
        If we haven't yet captured the starting game state,
        capture it"""

        if not self._ani_state:
            self._ani_state = AniGameState(self.game_ui.game)

        self._queue.append(anie)


    def flash(self, turn, *, move=None, loc=None):
        """Record a button flash action, if active."""

        if self.active:
            row, pos = None, None

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
        """Record a message in the animation sequence, if active."""

        if self.active:
            anie_msg = Message(message, self.font, self.bg_color)
            self.add(anie_msg)
            self.add(ScheduleCallback(anie_msg.close))


    def queue_callback(self, func):
        """Put a function callback event into the animation
        queue, if active."""

        if self.active:
            self.add(ScheduleCallback(func))


    def set_rollback(self):
        """Set the rollback point to the current length
        of the animation queue."""

        self._rollback_pt = len(self._queue)


    def clear_rollback(self):
        """Clear the rollback point."""

        self._rollback_pt = None


    def do_rollback(self):
        """Remove any animation events that were queued after
        the rollback point was set."""

        if self._rollback_pt is None:
            print("do_rollback called without calling set_rollback.")
            return

        for _ in range(self._rollback_pt, len(self._queue)):
            self._queue.pop()
        self._rollback_pt = None


    def _adjust_delay(self, anie):
        """Lengthen the delay after some animation classes."""

        delay = self.delay
        if isinstance(anie, NewGameState):
            delay = int(delay * 1.5)

        elif isinstance(anie, Message):
            delay = int(delay * self.msg_mult)

        return delay


    def do_animation(self, first=True):
        """Do an event from the queue and if there is more to
        do schedule it."""

        # cancel any pending rollback point
        self._rollback_pt = None

        if first and self._pending_after:
            # don't start a second series of afters
            return

        if self.active and self._queue:
            self.game_ui.config(cursor=ui_utils.ANI_ACTIVE)
            anie = self._queue.popleft()
            if print_steps:
                print(anie)    # for debugging
            anie.do_it(self.game_ui, self._ani_state)

            if self._queue:
                self._pending_after = True
                self.game_ui.after(self._adjust_delay(anie),
                                   lambda: self.do_animation(False))

            else:
                self._ani_state = None
                self._pending_after = False
                self.game_ui.config(cursor=ui_utils.NORMAL)

        else:
            # an active playback was stopped
            self._ani_state = None
            self._pending_after = False
            self._queue.clear()
            self.game_ui.config(cursor=ui_utils.NORMAL)
            self.game_ui.refresh()
