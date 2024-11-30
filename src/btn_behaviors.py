# -*- coding: utf-8 -*-
"""The Holebutton and StoreButton classes for Mancala UI with
states that allow the buttons to behave differently in different
game states.

Created on Sun Aug 13 10:06:37 2023
@author: Ann"""

import collections
import enum

import tkinter as tk

import behaviors


# %% enum, class list and global function

@enum.unique
class Behavior(enum.IntEnum):
    """Enum for the button behaviors."""

    GAMEPLAY = 0
    RNDCHOOSE = 1
    RNDMOVE = 2
    MOVESEEDS = 3
    RNDCHOWN = 4


BTuples = collections.namedtuple('BTuples', ['button', 'store'])


BEHAVIOR_CLASS = (BTuples(behaviors.PlayButtonBehavior,
                          behaviors.NoStoreBehavior),
                  BTuples(behaviors.RndChooseButtonBehavior,
                          behaviors.NoStoreBehavior),
                  BTuples(behaviors.RndMoveSeedsButtonBehavior,
                          behaviors.RndMoveStoreBehavior),
                  BTuples(behaviors.MoveSeedsButtonBehavior,
                          behaviors.NoStoreBehavior),
                  BTuples(behaviors.SelectOwnedHoles,
                          behaviors.NoStoreBehavior),
                  )


def ask_mode_change(old_behavior, new_behavior, game_ui):
    """If leaving a non-GAMEPLAY behavior, ask the button class (master)
    if it's ok to leave (this might do some side effect operations).
    If current behavior says it's ok, ask the new behavior if it's ok,
    which generally asks the user when leaving GAMEPLAY."""

    if new_behavior == Behavior.GAMEPLAY:
        if not BEHAVIOR_CLASS[old_behavior].button.leave_mode(game_ui):
            return False

    return BEHAVIOR_CLASS[new_behavior].button.ask_mode_change(game_ui)


def force_mode_change():
    """Do any cleanup because the mode change will be forced."""

    behaviors.Hold.cleanup()
    behaviors.Owners.cleanup()


# %%  Button Classes

class HoleButton(tk.Button):
    """Implements a single hole on the board."""

    def __init__(self, pframe, game_ui, loc, left_move, right_move):
        """Create button.
        loc is the index to use for get/set board/blocked.
        left and right move are the moves for left/right click"""
        # pylint: disable=too-many-arguments

        self.frame = pframe
        self.game_ui = game_ui
        self.loc = loc
        self.row = int(loc < self.game_ui.game.cts.holes)
        self.left_move = left_move
        self.right_move = right_move
        self.props = 0
        self.behavior = behaviors.PlayButtonBehavior(self)

        tk.Button.__init__(self, pframe, borderwidth=2, height=3, width=8,
                           text='',
                           disabledforeground='black', foreground='black',
                           anchor='center', font='bold, 14',
                           command=self.left_click)
        self.bind('<Button-3>', self.right_click)


    def set_behavior(self, behavior):
        """Set the behavior of the button."""

        self.config(cursor='')
        self.frame.config(cursor='')
        self.behavior = BEHAVIOR_CLASS[behavior].button(self)
        behaviors.Hold.empty()
        behaviors.Owners.empty()


    def set_props(self, props, bstate):
        """Pass along set_props call."""
        self.behavior.set_props(props, bstate)


    def left_click(self):
        """Pass along left_click call."""
        self.behavior.left_click()


    def right_click(self, _=None):
        """Pass along right_click call.
        Don't care about the possible event parameter."""
        self.behavior.right_click()


class StoreButton(tk.Button):
    """Implements one of the board stores."""

    def __init__(self, pframe, game_ui, owner):
        """Build the store button"""

        self.game_ui = game_ui
        self.owner = owner
        self.behavior = behaviors.NoStoreBehavior(self)

        tk.Button.__init__(self, pframe, borderwidth=2, height=3, width=7,
                           text='', padx=5, pady=10,
                           disabledforeground='black', foreground='black',
                           anchor='center', font='bold, 14', relief='ridge',
                           command=self.left_click)
        self.bind('<Button-3>', self.right_click)


    def set_behavior(self, behavior):
        """Set the behavior of the store."""
        self.config(cursor='')
        self.game_ui.config(cursor='')
        self.behavior = BEHAVIOR_CLASS[behavior].store(self)


    def set_store(self, seeds, turn):
        """Set text, props and states of the store."""
        self.behavior.set_store(seeds, turn)


    def left_click(self):
        """pass along left_click call."""
        self.behavior.left_click()


    def right_click(self, _=None):
        """pass along right_click call."""
        self.behavior.right_click()
