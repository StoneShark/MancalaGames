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
import bhv_hold
import bhv_owners
import man_config


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

                  BTuples(bhv_hold.RndChooseButtonBehavior,
                          behaviors.NoStoreBehavior),

                  BTuples(bhv_hold.RndMoveSeedsButtonBehavior,
                          bhv_hold.RndMoveStoreBehavior),

                  BTuples(bhv_hold.MoveSeedsButtonBehavior,
                          behaviors.NoStoreBehavior),

                  BTuples(bhv_owners.SelectOwnedHoles,
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

    bhv_hold.Hold.cleanup()
    bhv_owners.Owners.cleanup()


# %%  Button Classes

DO_RIGHT = 0.6
TEXT = 'text'

class HoleButton(tk.Canvas):
    """Implements a single hole on the board."""

    def __init__(self, pframe, game_ui, loc, left_move, right_move):
        """Create button.
        loc is the index to use for get/set board/blocked.
        left and right move are the moves for left/right click.

        If the left move is different than the right, create
        a rectangle on the canvas to support touch screen mode
        (e.g. no right clicks)."""
        # pylint: disable=too-many-arguments

        self.frame = pframe
        self.game_ui = game_ui
        self.loc = loc
        self.row = int(loc < self.game_ui.game.cts.holes)
        self.left_move = left_move
        self.right_move = right_move
        self.props = 0
        self.behavior = behaviors.PlayButtonBehavior(self)
        btn_size = man_config.CONFIG.get_int('button_size')

        tk.Canvas.__init__(self, pframe,
                           borderwidth=4, relief='raised',
                           width=btn_size, height=btn_size)

        self.right_id = None
        if left_move != right_move:
            self.right_id = self.create_rectangle(
                *self._get_coords(btn_size, btn_size),
                outline='', fill='grey', stipple='gray25')
            self.tag_bind(self.right_id, "<Button-1>", self.right_click)

            if not self.game_ui.vars.touch_screen.get():
                self.itemconfigure(self.right_id, state='hidden')

        self.text_id = self.create_text(btn_size//2, btn_size//2,
                                        text='',
                                        font=man_config.CONFIG.get_font())

        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-3>', self.right_click)
        self.bind("<Configure>", self._move_text)


    def __setitem__(self, key, value):
        """Capture setting the text attribute and set it on the
        text element on the canvas, otherwise, let the parent
        handle the setting."""

        if key == TEXT:
            self.itemconfig(self.text_id, text=value)
        else:
            super().__setitem__(key, value)


    def _get_coords(self, width, height):
        """Return the coordinates for the touch screen mode
        rectangle for right clicks."""

        if not self.row and self.game_ui.vars.facing_players.get():
            return (8, 8, int(width * (1 - DO_RIGHT)), height)

        return (int(width * DO_RIGHT), 8, width, height)


    def _move_text(self, event):
        """Keep the text widget in the center of the canvas
        and resize the tablet mode rectangle (if there is one)."""

        self.coords(self.text_id, event.width//2, event.height//2)
        if self.right_id:
            self.coords(self.right_id,
                        self._get_coords(event.width, event.height))


    def set_behavior(self, behavior):
        """Set the behavior of the button."""

        self.config(cursor='')
        self.frame.config(cursor='')
        self.behavior = BEHAVIOR_CLASS[behavior].button(self)
        bhv_hold.Hold.empty()
        bhv_owners.Owners.empty()


    def set_props(self, props, bstate):
        """Pass along set_props call."""
        self.behavior.set_props(props, bstate)


    def left_click(self, _=None):
        """Pass along left_click call.
        If the button is in the top row and facing players is set,
        then swap the left and right button actions.
        Don't care about the possible event parameter."""

        if self['state'] == tk.DISABLED:
            return

        if not self.row and self.game_ui.vars.facing_players.get():
            self.behavior.right_click()
        else:
            self.behavior.left_click()


    def right_click(self, _=None):
        """Pass along right_click call.
        If the button is in the top row and facing players is set,
        then swap the left and right button actions.
        Don't care about the possible event parameter."""

        if self['state'] == tk.DISABLED:
            return

        if not self.row and self.game_ui.vars.facing_players.get():
            self.behavior.left_click()
        else:
            self.behavior.right_click()


class StoreButton(tk.Canvas):
    """Implements one of the board stores."""

    def __init__(self, pframe, game_ui, owner):
        """Build the store button"""

        self.game_ui = game_ui
        self.owner = owner
        self.behavior = behaviors.NoStoreBehavior(self)

        btn_size = man_config.CONFIG.get_int('button_size')
        tk.Canvas.__init__(self, pframe,
                           borderwidth=4, relief='ridge',
                           width=btn_size, height=btn_size)

        self.text_id = self.create_text(btn_size, btn_size,
                                        text='',
                                        font=man_config.CONFIG.get_font())

        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-3>', self.right_click)
        self.bind("<Configure>", self._move_text)


    def __setitem__(self, key, value):
        """Capture setting the text attribute and set it on the
        text element on the canvas, otherwise, let the parent
        handle the setting."""

        if key == TEXT:
            self.itemconfig(self.text_id, text=value)
        else:
            super().__setitem__(key, value)

    def _move_text(self, event):
        """Keep the text widget in the center of the canvas)."""

        self.coords(self.text_id, event.width//2, event.height//2)

    def set_behavior(self, behavior):
        """Set the behavior of the store."""
        self.config(cursor='')
        self.game_ui.config(cursor='')
        self.behavior = BEHAVIOR_CLASS[behavior].store(self)


    def set_store(self, seeds, turn):
        """Set text, props and states of the store."""
        self.behavior.set_store(seeds, turn)


    def left_click(self, _=None):
        """pass along left_click call."""
        self.behavior.left_click()


    def right_click(self, _=None):
        """pass along right_click call."""
        self.behavior.right_click()
