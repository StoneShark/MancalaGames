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
import bhv_bsetup
import game_info as gi
import man_config
import ui_utils


# %% top level behavior interfaces for mancala_ui

@enum.unique
class Behavior(enum.IntEnum):
    """Enum for the button behaviors."""

    GAMEPLAY = 0
    RNDCHOOSE = 1
    RNDMOVE = 2
    MOVESEEDS = 3
    RNDCHOWN = 4
    SETUP = 5


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

                  BTuples(bhv_bsetup.SetupButtonBehavior,
                          bhv_bsetup.SetupStoreBehavior),
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

    bhv_hold.HOLD.cleanup()
    bhv_owners.OWNERS.cleanup()
    bhv_bsetup.SETUPHOLD.cleanup()



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

        self.frame = pframe
        self.game_ui = game_ui
        self.loc = loc
        self.row = int(loc < self.game_ui.game.cts.holes)
        self.left_move = left_move
        self.right_move = right_move
        self.props = None
        self.behavior = behaviors.PlayButtonBehavior(self)
        self.active = True       # don't process clicks when False
        self.last_event = 0   # last event.serial

        btn_size = man_config.CONFIG.get_int('button_size')
        tk.Canvas.__init__(self, pframe,
                           borderwidth=4, relief='raised',
                           width=btn_size, height=btn_size)
        self.text_id = self.create_text(btn_size//2, btn_size//2,
                                        text='',
                                        font=man_config.CONFIG.get_font())
        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-3>', self.right_click)
        self.bind('<Configure>', self._move_text)

        self.rclick_id = self.right_id = self.left_id = None
        self.split_grids = left_move != right_move
        self.non_play_grid = (self.game_ui.game.info.round_fill
                                in (gi.RoundFill.UCHOOSE,
                                    gi.RoundFill.UMOVE,
                                    gi.RoundFill.LOSER_ONLY))
        # simulate right click via touch/left click with this
        # rect when in table mode
        if self.split_grids or self.non_play_grid:

            color = man_config.CONFIG['rclick_color']
            density = 'gray' + man_config.CONFIG['grid_density']
            self.rclick_id = self.create_rectangle(
                *self._get_coords(btn_size, btn_size),
                outline='', fill=color, stipple=density)
            self.tag_bind(self.rclick_id, '<Button-1>', self.right_click)

            if (not self.split_grids
                    or not self.game_ui.tkvars.touch_screen.get()):
                self.itemconfig(self.rclick_id, state='hidden')

        # show grids and filter cw/ccw sow based on allowable
        # sow directions
        if self.split_grids:

            gcolor = man_config.CONFIG['grid_color']
            self.right_id = self.create_rectangle(
                *self._get_coords(btn_size, btn_size, False),
                outline='', fill=gcolor, stipple=density)
            self.left_id = self.create_rectangle(
                *self._get_coords(btn_size, btn_size, True),
                outline='', fill=gcolor, stipple=density)
            self.itemconfig(self.right_id, state='hidden')
            self.itemconfig(self.left_id, state='hidden')


    def __setitem__(self, key, value):
        """Capture setting the text attribute and set it on the
        text element on the canvas, otherwise, let the parent
        handle the setting."""

        if key == TEXT:
            self.itemconfig(self.text_id, text=value)
        else:
            super().__setitem__(key, value)


    def hole_owner(self):
        """Return the hole owner or None if not owned."""

        game = self.game_ui.game

        if game.info.no_sides:
            return None

        return self.props.owner


    def color_side(self):
        """Return the which side color to use."""

        game = self.game_ui.game

        if game.info.no_sides:
            return game.turn

        return self.props.owner


    def rotate_text(self):
        """Determine if the text should be rotated for facing
        players. Facing players is not supported for no_sides
        games because both players can play from all holes.
        If board side is True for hole 0 (usually a False hole)
        then use the board_side value. Otherwise check by row
        and/or owner."""

        game = self.game_ui.game
        if (not self.game_ui.tkvars.facing_players.get()
                or game.info.no_sides):
            return False

        if game.cts.board_side(0):
            return game.cts.board_side(self.loc)

        top = not self.row
        owner = self.props.owner
        return ((owner is None and top) or owner)


    def _get_coords(self, width, height, left=None):
        """Return the coordinates for the touch screen mode
        rectangle for right clicks."""

        if (left or (left is None and self.rotate_text())):
            return (8, 8, int(width * (1 - DO_RIGHT)), height)

        return (int(width * DO_RIGHT), 8, width, height)


    def _move_text(self, event):
        """Keep the text widget in the center of the canvas
        and resize the tablet mode and block grid rectangles
        (if they were created)."""

        self.coords(self.text_id, event.width//2, event.height//2)
        if self.rclick_id:
            self.coords(self.rclick_id,
                        self._get_coords(event.width, event.height - 8))

        if self.split_grids:
            self.coords(self.right_id,
                        self._get_coords(event.width, event.height - 8, False))
            self.coords(self.left_id,
                        self._get_coords(event.width, event.height - 8, True))


    def set_behavior(self, behavior):
        """Set the behavior of the button."""

        self.config(cursor=ui_utils.NORMAL)
        self.frame.config(cursor=ui_utils.NORMAL)
        self.behavior = BEHAVIOR_CLASS[behavior].button(self)
        bhv_hold.HOLD.empty()
        bhv_owners.OWNERS.empty()


    def set_props(self, props, bstate):
        """Set props and state of the hole."""
        self.props = props
        self.behavior.refresh(bstate)


    def flash(self):
        """Flash the button:  call 2x to return to normal."""

        fore = self.itemcget(self.text_id, 'fill')
        back = self['background']

        self.itemconfig(self.text_id, fill=back)
        self['background'] = fore


    def left_click(self, event):
        """Pass along left_click call.
        If the button is in the top row and facing players is set,
        then swap the left and right button actions.

        Use event.serial to determine if two events were generated
        from the click--this seems to happen when using right click
        grid in non-play modes. Only process unique events."""

        if (not self.active
                or self['state'] == tk.DISABLED
                or event.time == self.last_event):
            return
        self.last_event = event.time

        if self.rotate_text():
            self.behavior.do_right_click()
        else:
            self.behavior.do_left_click()


    def right_click(self, event):
        """Pass along right_click call.
        If the button is in the top row and facing players is set,
        then swap the left and right button actions.

        Use event.serial to determine if two events were generated
        from the click--this seems to happen when using right click
        grid in non-play modes. Only process unique events."""

        if (not self.active
                or self['state'] == tk.DISABLED
                or event.time == self.last_event):
            return
        self.last_event = event.time

        if self.rotate_text():
            self.behavior.do_left_click()
        else:
            self.behavior.do_right_click()


class StoreButton(tk.Canvas):
    """Implements one of the board stores."""

    def __init__(self, pframe, game_ui, owner):
        """Build the store button"""

        self.game_ui = game_ui
        self.owner = owner
        self.active = True       # don't process clicks when False
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

            if self.game_ui.tkvars.facing_players.get() and self.owner:
                self.itemconfig(self.text_id, angle=180)
            else:
                self.itemconfig(self.text_id, angle=0)
        else:
            super().__setitem__(key, value)


    def _move_text(self, event):
        """Keep the text widget in the center of the canvas)."""

        self.coords(self.text_id, event.width//2, event.height//2)


    def update_color(self, highlight):
        """Update the background color to the turn color."""

        if highlight is not None:
            if highlight:
                if self.owner:
                    color = man_config.CONFIG['north_act_color']
                else:
                    color = man_config.CONFIG['south_act_color']
            else:
                color = man_config.CONFIG['system_color']

            self['background'] = color


    def flash(self):
        """Flash the store:  call 2x to return to normal."""

        fore = self.itemcget(self.text_id, 'fill')
        back = self['background']

        self.itemconfig(self.text_id, fill=back)
        self['background'] = fore


    def set_behavior(self, behavior):
        """Set the behavior of the store."""
        self.config(cursor=ui_utils.NORMAL)
        self.game_ui.config(cursor=ui_utils.NORMAL)

        if (behavior == Behavior.GAMEPLAY
                and self.game_ui.game.info.play_locs == gi.PlayLocs.BRD_OWN_STR_ALL):
            self.behavior = behaviors.SowAllFromBehavior(self)

        elif (behavior == Behavior.GAMEPLAY
                and self.game_ui.game.info.play_locs == gi.PlayLocs.BRD_OWN_STR_CHS):
            self.behavior = behaviors.SowFromBehavior(self)

        else:
            self.behavior = BEHAVIOR_CLASS[behavior].store(self)


    def set_store(self, seeds, turn):
        """Set text, props and states of the store."""
        self.behavior.set_store(seeds, turn)


    def left_click(self, _=None):
        """pass along left_click call."""

        if not self.active:
            return

        self.behavior.do_left_click()


    def right_click(self, _=None):
        """pass along right_click call."""

        if not self.active:
            return

        self.behavior.do_right_click()
