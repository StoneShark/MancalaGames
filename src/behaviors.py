# -*- coding: utf-8 -*-
"""The Holebutton and StoreButton classes for Mancala UI with
states that allow the buttons to behave differently in different
game states.

Created on Sun Aug 13 10:06:37 2023
@author: Ann"""


import abc
import enum
import tkinter as tk

import game_info as gi
import game_str
import man_config
import ui_utils

# %%  constants

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

    ACT_CCW_ONLY = enum.auto()
    ACT_CW_ONLY = enum.auto()
    LACT_CCW_ONLY = enum.auto()
    LACT_CW_ONLY = enum.auto()

    def is_active(self):
        """An active state."""
        return self in  {BtnState.ACTIVE,
                         BtnState.ACT_CW_ONLY,
                         BtnState.ACT_CCW_ONLY}

    def is_look_active(self):
        """A look active state."""
        return self in  {BtnState.LOOK_ACTIVE,
                         BtnState.LACT_CW_ONLY,
                         BtnState.LACT_CCW_ONLY}

    def grid_ccw(self):
        """grid for ccw"""
        return self in {BtnState.ACT_CW_ONLY,
                        BtnState.LACT_CW_ONLY}

    def grid_cw(self):
        """grid for cw"""
        return self in {BtnState.ACT_CCW_ONLY,
                        BtnState.LACT_CCW_ONLY}


# %% interfaces


class BehaviorGlobal(abc.ABC):
    """The base class for the behavior global data classes.
    These are the interfaces used in here and in buttons."""

    def __init__(self):
        """self.game_ui is filled in when the menu i rframe is
        filled in the child classes; it is not available
        when behavior globals are created."""

        self.game_ui = None
        self.active = False


    @abc.abstractmethod
    def empty(self):
        """Remove any values from the global"""


    def destroy_ui(self):
        """Remove the children we created in rframe, leaving the
        first one created so that the geometry manager will allow
        shrinking the frame.
        Clear local access to them."""

        for child in self.game_ui.rframe.winfo_children()[1:]:
            child.destroy()


    def done(self):
        """Go back to game play mode."""

        if self.active and self.game_ui.set_gameplay_mode():
            self.destroy_ui()


    def cleanup(self):
        """Abandoning the game mode, cleanup."""

        if self.active:
            self.active = False
            self.empty()
            self.destroy_ui()


class BehaviorIf(abc.ABC):
    """Button behavior interface.

    The button behavior class is sort of the master in determining when
    ok to leave and enter behaviors."""

    def __init__(self, button):
        self.btn = button


    @classmethod
    @abc.abstractmethod
    def ask_mode_change(cls, game_ui):
        """If the user should be asked to consent to the mode
        change, do so. Return True if the mode change is
        ok, False otherwise.

        Class method because this is called before the object
        is instantiated."""


    @classmethod
    def leave_mode(cls, game_ui):
        """Is it ok to leave the mode (presumably to go back to GAMEPLAY).
        Assume it is unless this is overridden.

        Class scope method because it is called where only the
        class mode index is known (no actual behavior objects are
        are available)."""
        _ = game_ui
        return True


    @abc.abstractmethod
    def refresh(self, bstate=BtnState.ACTIVE):
        """Refresh the button appearance."""


    @abc.abstractmethod
    def do_left_click(self):
        """Do the left click action."""


    @abc.abstractmethod
    def do_right_click(self):
        """Do the right click action"""


    def remove_seeds(self, seeds):
        """Remove seeds from the HoleButton and set the cursor
        to a circle."""

        game = self.btn.game_ui.game

        if seeds:
            seeds = game.board[self.btn.loc] - seeds
            game.board[self.btn.loc] = seeds
            self.btn.props.seeds = seeds
            self.refresh()

            self.btn.game_ui.config(cursor=ui_utils.HOLD_SEEDS)


    def orient_text(self):
        """Orient the text according to the display option and
        rotate_text."""

        if self.btn.rotate_text():
            self.btn.itemconfig(self.btn.text_id, angle=180)
        else:
            self.btn.itemconfig(self.btn.text_id, angle=0)


    def owner_arrow(self):
        """Show the owner ship arrow if enabled by the display option."""

        otext = ''
        if self.btn.game_ui.tkvars.owner_arrows.get():
            if self.btn.rotate_text():
                otext += game_str.OWNER[not self.btn.props.owner]

            else:
                otext += game_str.OWNER[self.btn.props.owner]

        return otext


    def refresh_nonplay(self, bstate, bg_color=None):
        """Make the UI match the behavior and game data for the non-play
        behaviors (except setup board)."""

        if bstate == BtnState.DISABLE:
            self.btn['background'] = man_config.CONFIG['system_color']
            self.btn['state'] = tk.DISABLED
        else:
            if not bg_color:
                if self.btn.color_side():
                    bg_color = man_config.CONFIG['north_act_color']
                else:
                    bg_color = man_config.CONFIG['south_act_color']

            self.btn['background'] = bg_color
            self.btn['state'] = tk.NORMAL

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        elif self.btn.props.seeds:
            self.btn['text'] = self.owner_arrow() + str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''

        self.orient_text()

        if (self.btn.non_play_grid
                and self.btn.game_ui.tkvars.touch_screen.get()):
            self.btn.itemconfig(self.btn.rclick_id, state='normal')
        else:
            self.btn.itemconfig(self.btn.rclick_id, state='hidden')


    def _get_child_pointer(self):
        """Return the child pointer. If the text is rotated
        180 degrees, then flip the arrow direction so it points
        at the child owner."""

        if self.btn.rotate_text() and self.btn.props.ch_owner in {True, False}:
            otext = game_str.CHILD[not self.btn.props.ch_owner]
        else:
            otext = game_str.CHILD[self.btn.props.ch_owner]

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


    def _update_grids(self, bstate):
        """Show hide the grids and adjust the mouse bindings."""
        # pylint: disable=too-many-boolean-expressions

        if not self.btn.split_grids:
            self.btn.itemconfig(self.btn.rclick_id, state='hidden')
            return

        gccw = bstate.grid_ccw()
        gcw = bstate.grid_cw()

        top = not self.btn.row
        trot = self.btn.rotate_text()

        # show red grid on right
        if (gccw and not top) or (gcw and top) or (gcw and trot):
            self.btn.itemconfig(self.btn.right_id, state='normal')
            self.btn.itemconfig(self.btn.left_id, state='hidden')

            if trot:
                self.btn.unbind('<Button-1>')
                self.btn.bind('<Button-3>', self.btn.right_click)
            else:
                self.btn.bind('<Button-1>', self.btn.left_click)
                self.btn.unbind('<Button-3>')

            if self.btn.game_ui.tkvars.touch_screen.get():
                self.btn.itemconfig(self.btn.rclick_id, state='normal')
            else:
                self.btn.itemconfig(self.btn.rclick_id, state='hidden')

        # show red grid on left
        elif (gcw and not top) or (gccw and top) or (gccw and trot):
            self.btn.itemconfig(self.btn.right_id, state='hidden')
            self.btn.itemconfig(self.btn.left_id, state='normal')

            if trot:
                self.btn.bind('<Button-1>', self.btn.left_click)
                self.btn.unbind('<Button-3>')
            else:
                self.btn.unbind('<Button-1>')
                self.btn.bind('<Button-3>', self.btn.right_click)

            self.btn.itemconfig(self.btn.rclick_id, state='hidden')

        else:
            self.btn.itemconfig(self.btn.right_id, state='hidden')
            self.btn.itemconfig(self.btn.left_id, state='hidden')
            self.btn.bind('<Button-1>', self.btn.left_click)
            self.btn.bind('<Button-3>', self.btn.right_click)

            if self.btn.game_ui.tkvars.touch_screen.get():
                self.btn.itemconfig(self.btn.rclick_id, state='normal')
            else:
                self.btn.itemconfig(self.btn.rclick_id, state='hidden')


    def _set_btn_ui_props(self, bstate):
        """Set the UI properties of the button"""

        if not self.btn.props.unlocked:
            self.btn['relief'] = 'ridge'
        else:
            self.btn['relief'] = 'raised'

        if bstate is None:
            return

        if self.btn.color_side():
            act_color = man_config.CONFIG['north_act_color']
            not_color = man_config.CONFIG['north_not_color']
        else:
            act_color = man_config.CONFIG['south_act_color']
            not_color = man_config.CONFIG['south_not_color']

        if bstate.is_active():
            self.btn['background'] = act_color
            self.btn['state'] = tk.NORMAL

        else:
            self.btn['state'] = tk.DISABLED
            if bstate.is_look_active():
                self.btn['background'] = act_color

            elif bstate == BtnState.PLAY_DISABLE:
                self.btn['background'] = not_color

            else:
                self.btn['background'] = man_config.CONFIG['inactive_color']

        self._update_grids(bstate)


    def refresh_play(self, bstate):
        """Do the play mode refresh which is also used by the Setup Board"""

        self._set_btn_text()
        self._set_btn_ui_props(bstate)


class StoreBehaviorIf(abc.ABC):
    """Store behavior interface."""

    def __init__(self, store):
        self.str = store

    @abc.abstractmethod
    def set_store(self, seeds, highlight):
        """Set text, props and states of the store."""

    @abc.abstractmethod
    def do_left_click(self):
        """Do the left click action."""

    @abc.abstractmethod
    def do_right_click(self):
        """Do the right click action"""


# %%  Play mode behavior

class PlayButtonBehavior(BehaviorIf):
    """The button behavior during game play."""

    @classmethod
    def ask_mode_change(cls, game_ui):
        """leave_mode of the previous behavior prevents
        leaving if conditions are not good. Here we always
        find with entering GAMEPLAY ok."""

        return True


    def do_left_click(self):
        """Tell parent to move."""
        self.btn.game_ui.move(self.btn.left_move)


    def do_right_click(self):
        """Move for the right click -- unless the hole is udirect
        this is the same as a left click"""
        self.btn.game_ui.move(self.btn.right_move)


    def refresh(self, bstate=BtnState.ACTIVE):
        """Set text and ui props."""

        # XXXX hide a bug in which numbers end up no-move background color
        self.btn.itemconfig(self.btn.text_id, fill='black')

        self.refresh_play(bstate)


# %% no interaction store behavior

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

        self.str.update_color(highlight)


    def do_left_click(self):
        """No interaction, button disabled."""


    def do_right_click(self):
        """No interaction."""


class SowFromBehavior(StoreBehaviorIf):
    """If a move is initiated from a store and there is more
    than one seed there, allow the user to choose the number
    of seeds."""

    def set_store(self, seeds, highlight):
        """Set the properties of the store button."""

        self.str['state'] = tk.NORMAL

        if seeds:
            self.str['text'] = str(seeds)
        else:
            self.str['text'] = ''

        self.str.update_color(highlight)


    def do_left_click(self):
        """If there's more than one seed, request the number
        of seeds to move. Do the move."""

        max_seeds = self.str.game_ui.game.store[self.str.owner]
        if not max_seeds:
            return

        seeds = 0
        if max_seeds == 1:
            seeds = 1
        else:
            seeds = ui_utils.get_nbr_seeds(self.str.game_ui, max_seeds,
                                           font=(man_config.CONFIG['font_family'],
                                                 man_config.CONFIG['pickup_font_size']))

        if seeds:
            self.str.game_ui.move(gi.MoveTpl(-(self.str.owner + 1), seeds))


    def do_right_click(self):
        """Do left click for right too."""

        self.do_left_click()


class SowAllFromBehavior(StoreBehaviorIf):
    """Allow selection of the staore for a move."""

    def set_store(self, seeds, highlight):
        """Set the properties of the store button."""

        self.str['state'] = tk.NORMAL

        if seeds:
            self.str['text'] = str(seeds)
        else:
            self.str['text'] = ''

        self.str.update_color(highlight)


    def do_left_click(self):
        """Move all of the seeds out of the store."""

        seeds = self.str.game_ui.game.store[self.str.owner]
        if seeds:
            self.str.game_ui.move(gi.MoveTpl(-(self.str.owner + 1), seeds))


    def do_right_click(self):
        """Do left click for right too."""

        self.do_left_click()
