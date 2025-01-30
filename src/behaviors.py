# -*- coding: utf-8 -*-
"""The Holebutton and StoreButton classes for Mancala UI with
states that allow the buttons to behave differently in different
game states.

Created on Sun Aug 13 10:06:37 2023
@author: Ann"""


import abc
import enum

import tkinter as tk


# %%  constants

SYSTEM_COLOR = 'SystemButtonFace'
INACTIVE_COLOR = 'grey60'
CHOOSE_COLOR = 'pink2'
SEED_COLOR = 'goldenrod'
MOVE_COLOR = 'sandy brown'

TURN_COLOR = 'LightBlue2'
TURN_DARK_COLOR = 'LightBlue4'

YES_STR = 'yes'
NO_STR = 'no'

FILL_POPUP = 50
FILL_HINTS = 65

# %% enum

class BtnState(enum.Enum):
    """The three states of the button holes."""

    ACTIVE = enum.auto()
    LOOK_ACTIVE = enum.auto()
    DISABLE = enum.auto()
    PLAY_DISABLE = enum.auto()


# %% interface

class BehaviorIf(abc.ABC):
    """Button behavior interface.

    The button behavior class is sort of the master in determining when
    ok to leave and enter behaviors."""

    def __init__(self, button):
        self.btn = button


    def orient_text(self):
        """Orient the text according to the display option and row."""

        if not self.btn.row:
            if self.btn.game_ui.facing_players.get():
                self.btn.itemconfigure(self.btn.text_id, angle=180)
            else:
                self.btn.itemconfigure(self.btn.text_id, angle=0)

    def owner_arrow(self):
        """Show the owner ship arrow if enabled by the display option."""

        otext = ''
        if self.btn.game_ui.owner_arrows.get():
            if self.btn.props.owner is True:
                otext += '\u2191 '
            elif self.btn.props.owner is False:
                otext += '\u2193 '

        return otext

    def refresh_nonplay(self, bstate, bg_color=TURN_COLOR):
        """Make the UI match the behavior and game data for the non-play
        behaviors."""

        if bstate == BtnState.DISABLE:
            self.btn['background'] = SYSTEM_COLOR
            self.btn['state'] = tk.DISABLED
        else:
            self.btn['background'] = bg_color
            self.btn['state'] = tk.NORMAL

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        elif self.btn.props.seeds:
            self.btn['text'] = self.owner_arrow() + str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''

        if self.btn.right_id:
            self.btn.itemconfigure(self.btn.right_id, state='hidden')

        self.orient_text()


    @classmethod
    @abc.abstractmethod
    def ask_mode_change(cls, game_ui):
        """If the user should be asked to consent to the mode
        change, do so. Return True if the mode change is
        ok, False otherwise.

        class method because this is called before the object
        is instantiated."""

    @classmethod
    def leave_mode(cls, game_ui):
        """Is it ok to leave the mode (presumably to go back to GAMEPLAY).
        Assume it is unless this is overridden.

        class method to access any class scope vars set in ask_mode_change."""
        _ = game_ui
        return True

    @abc.abstractmethod
    def set_props(self, props, bstate):
        """Set props and state of the hole."""

    @abc.abstractmethod
    def left_click(self):
        """Do the left click action."""

    @abc.abstractmethod
    def right_click(self):
        """Do the right click action"""


class StoreBehaviorIf(abc.ABC):
    """Store behavior interface."""

    def __init__(self, store):
        self.str = store

    @abc.abstractmethod
    def set_store(self, seeds, highlight):
        """Set text, props and states of the store."""

    @abc.abstractmethod
    def left_click(self):
        """Do the left click action."""

    @abc.abstractmethod
    def right_click(self):
        """Do the right click action"""


# %%    Hole Behaviors

class PlayButtonBehavior(BehaviorIf):
    """The button behavior during game play."""

    @classmethod
    def ask_mode_change(cls, game_ui):
        """leave_mode of the previous behavior prevents
        leaving if conditions are not good. Here we always
        find with entering GAMEPLAY."""

        return True


    def set_props(self, props, bstate):
        """Set props and state of the hole."""

        self.btn.props = props
        self._refresh(bstate)


    def left_click(self):
        """Tell parent to move."""
        self.btn.game_ui.move(self.btn.left_move)


    def right_click(self):
        """Move for the right click -- unless the hole is udirect
        this is the same as a left click"""
        if self.btn['state'] == tk.DISABLED:
            return

        self.btn.game_ui.move(self.btn.right_move)


    def _get_child_pointer(self):
        """Return the child pointer. If the text is rotated
        180 degrees, then flip the arrow direction so it points
        at the child owner."""

        otext = ''
        if not self.btn.row and self.btn.game_ui.facing_players.get():
            if self.btn.props.ch_owner is True:
                otext += '\u02c5 '
            elif self.btn.props.ch_owner is False:
                otext += '\u02c4 '

        elif self.btn.props.ch_owner is True:
            otext += '\u02c4 '

        elif self.btn.props.ch_owner is False:
            otext += '\u02c5 '

        return otext


    def _set_btn_text(self):
        """Set the button text to match the props."""

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        else:
            otext = ''
            otext += self._get_child_pointer()
            otext += self.owner_arrow()

            if self.btn.props.seeds:
                self.btn['text'] = otext + str(self.btn.props.seeds)
            else:
                self.btn['text'] = otext + ''

        self.orient_text()


    def _set_btn_ui_props(self, bstate):
        """Set the UI properties of the button"""

        if not self.btn.props.unlocked:
            self.btn['relief'] = 'ridge'
        else:
            self.btn['relief'] = 'raised'

        if bstate == BtnState.ACTIVE:
            self.btn['background'] = TURN_COLOR
            self.btn['state'] = tk.NORMAL

        else:
            self.btn['state'] = tk.DISABLED
            if bstate == BtnState.LOOK_ACTIVE:
                self.btn['background'] = TURN_COLOR

            elif bstate == BtnState.PLAY_DISABLE:
                self.btn['background'] = TURN_DARK_COLOR

            else:
                self.btn['background'] = INACTIVE_COLOR

        if self.btn.right_id:
            if self.btn.game_ui.touch_screen.get():
                self.btn.itemconfigure(self.btn.right_id, state='normal')
            else:
                self.btn.itemconfigure(self.btn.right_id, state='hidden')


    def _refresh(self, bstate=BtnState.ACTIVE):
        """Set text and ui props."""

        self._set_btn_text()
        self._set_btn_ui_props(bstate)


# %% store behaviors

class NoStoreBehavior(StoreBehaviorIf):
    """Store behavior that has no interaction.
    Background color reflects the current turn."""

    def set_store(self, seeds, highlight):
        """Set the properties of the store button."""

        self.str['state'] = tk.DISABLED

        if seeds:
            self.str['text'] = str(seeds)
        else:
            self.str['text'] = ''

        self.str['background'] = TURN_COLOR if highlight else SYSTEM_COLOR


    def left_click(self):
        """No interaction, button disabled."""


    def right_click(self):
        """No interaction."""
