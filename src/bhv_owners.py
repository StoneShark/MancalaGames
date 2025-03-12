# -*- coding: utf-8 -*-
"""Button Behaviors that use the Owners global data.

Created on Thu Jan 30 13:31:34 2025
@author: Ann
"""

import tkinter as tk
import textwrap

import behaviors as bhv
import man_config
# from game_logger import game_log


class Owners(bhv.BehaviorGlobal):
    """Global data to store and manage ownership counts.

    This data is shared between each of the behavior objects
    created for the board (holes and stores).

    Only one global instance is created."""

    def __init__(self):

        super().__init__()
        self.active = False
        self.deviat = [0, 0]

        self._top_dev = None
        self._btm_dev = None


    def empty(self):
        """clear the owner deviations"""
        self.deviat = [0, 0]

        if self._btm_dev and self._top_dev:
            self._btm_dev.config(text=f'{self.deviat[0]:3}')
            self._top_dev.config(text=f'{self.deviat[1]:3}')


    def destroy_ui(self):
        """Don't keep local copies of ui elements that are
        destroyed."""

        super().destroy_ui()
        self._top_dev = None
        self._btm_dev = None


    def change_owner(self, owner):
        """The ownership of one hole has toggled, update the
        counts."""

        self.deviat[owner] += 1
        self.deviat[not owner] -= 1

        self._btm_dev.config(text=f'{self.deviat[0]:3}')
        self._top_dev.config(text=f'{self.deviat[1]:3}')


    def fill_it(self, game_ui):
        """Fill the right status frame with controls."""

        self.active = True
        self.game_ui = game_ui
        frame = game_ui.rframe

        text = "Click any hole to toggle it's ownerhsip.\n" \
               "Hole owner change counts must be zero before exit."

        tk.Label(frame, anchor='nw', justify='left', text=text
                 ).pack(side='top', expand=True, fill='both')

        status = tk.Frame(frame)
        status.pack(side='top', expand=True, fill='x')

        tk.Label(status, text='Top').pack(side=tk.LEFT)
        self._top_dev = tk.Label(status, text='   0')
        self._top_dev.pack(side=tk.LEFT)
        tk.Label(status, text='Bottom').pack(side=tk.LEFT)
        self._btm_dev = tk.Label(status, text='  0')
        self._btm_dev.pack(side=tk.LEFT)

        tk.Button(frame, text='Done', command=self.done
                  ).pack(side='bottom')


OWNERS = Owners()


# %% behaviors

class SelectOwnedHoles(bhv.BehaviorIf):
    """A class which allows the winner to select the
    holes they own on the loser side."""

    @classmethod
    def ask_mode_change(cls, game_ui):

        if len(set(game_ui.game.owner[loc]
                   for loc in range(game_ui.game.cts.holes))) == 2:
            loser = False
        elif len(set(game_ui.game.owner[loc]
                     for loc in range(game_ui.game.cts.holes,
                                      game_ui.game.cts.dbl_holes))) == 2:
            loser = True
        else:
            # no mixed hole sides, would be nothing to do
            return False

        ans = tk.messagebox.askquestion(
            title='Change Ownership',
            message=textwrap.fill(textwrap.dedent("""\
                  The winner may choose which holes on the opposite
                  side that they would like to own. The number of
                  holes owned by each player may not be changed.
                  Do you wish to change any hole ownership?"""),
                  width=bhv.FILL_POPUP),
            parent=game_ui)

        if ans != bhv.YES_STR:
            return False

        cls.starter = game_ui.game.turn
        cls.facing = game_ui.vars.facing_players.get()
        game_ui.vars.facing_players.set(False)
        game_ui.toggle_facing()
        game_ui.game.turn = loser

        OWNERS.fill_it(game_ui)
        return True


    @classmethod
    def leave_mode(cls, game_ui):

        if OWNERS.deviat != [0, 0]:
            tk.messagebox.showerror(
                title='Game Mode',
                message=textwrap.fill(textwrap.dedent("""\
                    Hole ownership numbers are not zeros."""), width=40),
                parent=game_ui)
            return False

        game_ui.game.turn = cls.starter
        game_ui.vars.facing_players.set(cls.facing)
        game_ui.toggle_facing()
        return True


    def do_left_click(self):
        """Toggle the hole ownership update the Owners"""

        game = self.btn.game_ui.game
        loc = self.btn.loc

        game.owner[loc] = not game.owner[loc]
        self.btn.props.owner = game.owner[loc]
        self.refresh()

        OWNERS.change_owner(game.owner[loc])


    def do_right_click(self):
        """Right click does nothing in this mode."""


    def refresh(self, bstate=bhv.BtnState.ACTIVE):
        """Make the UI match the behavior and game data."""

        if bstate == bhv.BtnState.DISABLE:
            self.btn['background'] = man_config.CONFIG['system_color']
            self.btn['state'] = tk.DISABLED
        else:
            game = self.btn.game_ui.game
            if self.btn.props.owner == game.turn:
                self.btn['background'] = man_config.CONFIG['move_color']
            else:
                self.btn['background'] = man_config.CONFIG['system_color']
            self.btn['state'] = tk.NORMAL

        otext = ''
        if self.btn.props.owner is True:
            otext += '\u2191 '
        elif self.btn.props.owner is False:
            otext += '\u2193 '

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        elif self.btn.props.seeds:
            self.btn['text'] = otext + str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''
