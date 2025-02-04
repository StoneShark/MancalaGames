# -*- coding: utf-8 -*-
"""A UI that brings up a list of games in the GameProps directory
showing the about text as a tool time.

Created on Thu Mar 23 08:10:28 2023
@author: Ann"""

import functools as ft
import os
import textwrap
import tkinter as tk

import cfg_keys as ckey
import man_config
import man_path
import mancala_ui


# %% constants

DIR = 'GameProps'
PATH = man_path.get_path(DIR) + '/'

TXTPART = '.txt'
EXFILE = '_all_params.txt'


# %%  load games

def load_game_files():
    """Get a list of the game files, read the game_dict,
    create a dictionary of game name and about text."""

    choices = {}
    for file in os.listdir(PATH):

        if file[-4:] != TXTPART or file == EXFILE:
            continue

        game_dict = man_config.read_game(PATH + file)

        about_str = ''
        if (ckey.GAME_INFO in game_dict
                and ckey.ABOUT in game_dict[ckey.GAME_INFO]):

            about_str = game_dict[ckey.GAME_INFO][ckey.ABOUT]

            paragraphs = about_str.split('\n')
            out_text = ''
            for para in paragraphs:
                fpara = textwrap.fill(para, 45) + '\n'
                out_text += fpara
            about_str = ''.join(out_text)

        choices[file[:-4]] = about_str

    return choices


# %%  game select

class GameSelect(tk.Frame):
    """Create a game select frame with popup tools tips
    that provide the game overview."""

    def __init__(self, return_list):
        """Show a menu."""

        self.selected = return_list
        self.tipwindow = None

        self.master = tk.Tk()

        self.master.title('Choose Variant')
        self.master.resizable(False, False)
        self.master.wm_geometry('+200+150')
        super().__init__(self.master)

        self.cur_button = None
        self.master.bind('<Leave>', self._remove_tooltip)

        self.pack()

        new_col = self._item_per_row(len(CHOICES))
        row = 0
        col = 0
        for name, about in CHOICES.items():

            button = tk.Button(self, borderwidth=2, width=20, text=name,
                               command=ft.partial(self._save_game, name),
                               anchor='center', font='bold')
            button.grid(row=row, column=col)
            button.bind('<Enter>', ft.partial(self._enter, button, about))
            button.bind('<Leave>', ft.partial(self._enter, button))

            if row >= new_col:
                row = 0
                col += 1
            else:
                row += 1


    @staticmethod
    def _item_per_row(nitems):
        """Compute a nice number of elements for each row.
        Start with a number less than the square root,
        if columns can be even use that number."""

        start = int(nitems ** 0.4) + 1
        for ritems in range(start, 1, -1):
            if not nitems % ritems:
                return max(ritems, nitems // ritems)

        return max(start, nitems // start)


    def _enter(self, button, text, _=None):
        """Popup tooltip/overview window.

        There is a race condition: _leave may be called after _enter
        and no popup is visible.  Add extra logic to force _leave of previous
        button if we are a on new one. Then prevent a later _leave from
        doing anything."""

        if self.tipwindow and self.cur_button == button:
            return

        last_button = self.cur_button
        self.cur_button = button
        if last_button:
            self._leave(last_button)

        xpos = button.winfo_rootx() + 137
        ypos = button.winfo_rooty() + 17

        self.tipwindow = tk.Toplevel(button)
        self.tipwindow.wm_overrideredirect(1)
        self.tipwindow.wm_geometry(f'+{xpos}+{ypos}')

        label = tk.Label(self.tipwindow, text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID,
                         borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(expand=True, fill='x')


    def _leave(self, button, _=None):
        """Destroy the window if it exits.  See _enter for race comment."""

        if self.cur_button == button:
            return

        self._remove_tooltip()


    def _remove_tooltip(self, _=None):
        """Mouse has left the window. Destroy tooltip if it exists."""

        save_tip = self.tipwindow
        self.tipwindow = None

        if save_tip:
            save_tip.destroy()


    def _save_game(self, maker):
        """set the global with the maker class."""

        self.selected += [maker]
        self.master.destroy()


    def destroy(self):
        """window was closed."""
        self._remove_tooltip()


def select_game():
    """Create the GameSelect window and run it.
    This list business is to get a return value from the popup."""

    game_list = []
    gsel = GameSelect(game_list)
    gsel.mainloop()

    if game_list:
        return game_list[0]
    return None


# %% play a game

def play_game(gamename):
    """Load the config file, create the game and play it."""

    filename = PATH + gamename + TXTPART
    game, player_dict = man_config.make_game(filename)

    game_ui = mancala_ui.MancalaUI(game, player_dict)
    game_ui.mainloop()


# %%


if __name__ == '__main__':

    CHOICES = load_game_files()

    while True:
        game_name = select_game()

        if game_name:
            play_game(game_name)
        else:
            break
