# -*- coding: utf-8 -*-
"""A UI that brings up a list of games in the GameProps directory

Created on Thu Mar 23 08:10:28 2023
@author: Ann"""

import functools as ft
import os
import textwrap
import tkinter as tk
from tkinter import ttk
import webbrowser

import cfg_keys as ckey
import game_constants as gc
import game_interface as gi
import man_config
import man_path
import mancala_ui
import version

from game_classes import GAME_CLASSES


# %% constants

DIR = 'GameProps'
PATH = man_path.get_path(DIR) + '/'

TXTPART = '.txt'
EXFILE = '_all_params.txt'

# this must not be in any of the enumerations
NOT_FILTERED = -2

OPTIONS = 0
PARAMS = 1
GAMES = 2
ABOUT = 4


SIZES = {'Small (< 6)': lambda holes: holes < 6,
         'Medium (== 6)': lambda holes: holes == 6,
         'Larger (7 - 8)': lambda holes: 7 <= holes <= 8,
         'Largest (>= 9)': lambda holes: holes >= 9}


CAPTS = {'No Capture': lambda ginfo: not any([ginfo.get(ckey.CAPT_MAX, 0),
                                              ginfo.get(ckey.CAPT_MIN, 0),
                                              ginfo.get(ckey.CAPT_ON, 0),
                                              ginfo.get(ckey.EVENS, 0),
                                              ginfo.get(ckey.CROSSCAPT, 0),
                                              ginfo.get(ckey.CAPT_TYPE, 0)]),
         'Basic Capture': lambda ginfo: (any([ginfo.get(ckey.CAPT_MAX, 0),
                                      ginfo.get(ckey.CAPT_MIN, 0),
                                      ginfo.get(ckey.CAPT_ON, 0),
                                      ginfo.get(ckey.EVENS, 0)])
                                 and not any([ginfo.get(ckey.CROSSCAPT, 0),
                                              ginfo.get(ckey.CAPT_TYPE, 0)])),
         'Cross Capture': lambda ginfo: ginfo.get(ckey.CROSSCAPT, 0),
         'Other Capt Type': lambda ginfo: ginfo.get(ckey.CAPT_TYPE, 0)}


# %% helper classes

class Counter:
    """A counter that increments every time the count is retrieved"""

    def __init__(self):
        self.nbr = -1

    @property
    def count(self):
        """increment round and return it"""
        self.nbr += 1
        return self.nbr

    def reset(self):
        self.nbr = 0


# %% frame classes


class EnumFilter(ttk.Frame):
    """A filter category based on enum values."""

    def __init__(self, parent, label, enum):

        super().__init__(parent, borderwidth=3)
        self.parent = parent

        row = Counter()

        ttk.Label(self, text=label).grid(row=row.count,
                                         column=0, columnspan=2)

        self.filt_var = {}
        for enum_val in enum:
            self.filt_var[enum_val.value] = tk.BooleanVar(self, value=1)
            ttk.Checkbutton(self, text=enum_val.name,
                            variable=self.filt_var[enum_val.value],
                            command=parent.update_list
                            ).grid(row=row.count, column=0, columnspan=2,
                                   sticky='ew')

        rnbr = row.count
        ttk.Button(self, text='All',
                   command=self.not_filtered
                   ).grid(row=rnbr, column=0)
        ttk.Button(self, text='None',
                   command=self.all_filtered
                   ).grid(row=rnbr, column=1)


    def not_filtered(self):
        """Set all of the filter variables."""

        for var in self.filt_var.values():
            var.set(1)
        self.parent.update_list()


    def all_filtered(self):
        """Clear all of the filter variables."""

        for var in self.filt_var.values():
            var.set(0)
        self.parent.update_list()


    def show(self, value):
        """Determine if the game associated with value
        should be shown.

        value: the enum value to test (an int)"""

        return self.filt_var[value].get()


class DictFilter(ttk.Frame):
    """A filter category based on a dictionary of rule_name: test"""

    def __init__(self, parent, label, filt_dict):

        super().__init__(parent, borderwidth=3)
        self.parent = parent
        self.filt_dict = filt_dict

        row = Counter()

        ttk.Label(self, text=label).grid(row=row.count,
                                         column=0, columnspan=2)

        self.filt_var = {}
        for fname in filt_dict.keys():
            self.filt_var[fname] = tk.BooleanVar(self, value=1)
            ttk.Checkbutton(self, text=fname,
                            variable=self.filt_var[fname],
                            command=parent.update_list
                            ).grid(row=row.count, column=0, columnspan=2,
                                   sticky='ew')

        rnbr = row.count
        ttk.Button(self, text='All',
                   command=self.not_filtered
                   ).grid(row=rnbr, column=0)
        ttk.Button(self, text='None',
                   command=self.all_filtered
                   ).grid(row=rnbr, column=1)


    def not_filtered(self):
        """Set all of the filter variables."""

        for var in self.filt_var.values():
            var.set(1)
        self.parent.update_list()


    def all_filtered(self):
        """Clear all of the filter variables."""

        for var in self.filt_var.values():
            var.set(0)
        self.parent.update_list()


    def show(self, value):
        """Determine if a the game associated with value
        should be shown.

        value: value of the associated parameter to test"""

        return any([test_func(value)
                   for test_name, test_func in self.filt_dict.items()
                   if self.filt_var[test_name].get()])


class GameFilters(ttk.Frame):
    """A pane to collect all the game filters and the PLAY button."""

    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent
        self.pack()

        col = Counter()

        self.size_filter = DictFilter(self, 'Board Size', SIZES)
        self.size_filter.grid(row=0, column=col.count,
                              stick='ns')

        self.goal_filter = EnumFilter(self, 'Goal', gi.Goal)
        self.goal_filter.grid(row=0, column=col.count,
                              stick='ns')

        self.rnd_filter = EnumFilter(self, 'Rounds', gi.Rounds)
        self.rnd_filter.grid(row=0, column=col.count,
                              stick='ns')

        self.laps_filter = EnumFilter(self, 'Sow Type', gi.LapSower)
        self.laps_filter.grid(row=0, column=col.count,
                              stick='ns')

        self.child_filter = EnumFilter(self, 'Child Type', gi.ChildType)
        self.child_filter.grid(row=0, column=col.count,
                              stick='ns')

        self.capt_filter = DictFilter(self, 'Capture Types', CAPTS)
        self.capt_filter.grid(row=0, column=col.count,
                              stick='ns')

        cmd_col = col.count
        ttk.Button(self, text='Play',
                   command=parent.play_game).grid(
                       row=0, column=cmd_col, sticky='ns')

        self.columnconfigure(tk.ALL, weight=1)



    def show_game(self, game_dict):
        """Test if the game should be shown based on the filter
        settings and the game_dict"""

        gcts = game_dict[ckey.GAME_CONSTANTS]
        ginfo = game_dict[ckey.GAME_INFO]
        return all([self.size_filter.show(gcts[ckey.HOLES]),
                    self.laps_filter.show(ginfo.get(ckey.MLAPS, 0)),
                    self.goal_filter.show(ginfo.get(ckey.GOAL, 0)),
                    self.rnd_filter.show(ginfo.get(ckey.ROUNDS, 0)),
                    self.child_filter.show(ginfo.get(ckey.CHILD_TYPE, 0)),
                    self.capt_filter.show(ginfo),
                    ])


    def update_list(self):
        """Update the parent list of filtered games."""

        self.parent.filter_games()


class SelectList(ttk.Frame):
    """Scrollable tree list for list of filtered games.
    Selecting one tells the parent it was selected."""

    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent

        self.game_list = ttk.Treeview(self,
                                      show='tree',
                                      selectmode='browse')

        scroll = ttk.Scrollbar(self,
                               orient='vertical',
                               command=self.game_list.yview)
        self.game_list.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.game_list.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)

        self.game_list.bind('<<TreeviewSelect>>', self.select_game)


    def select_game(self, _):
        """The user has selected a game, tell the parent
        it was selected."""

        game_name = self.game_list.selection()

        if game_name:
            game_name = game_name[0]
            self.parent.select_game(game_name)


    def clear_glist(self):
        """Clear the game list."""

        for item in self.game_list.get_children():
            self.game_list.delete(item)


    def fill_glist(self, games):
        """Put the games in the treeview"""

        self.clear_glist()

        for name in games:
            self.game_list.insert('', tk.END, iid=name, text=name)




class AboutPane(ttk.Frame):
    """A pane for the game help text (called the 'about' text)"""

    def __init__(self, parent):

        super().__init__(parent)

        self.text_box = tk.Text(self)

        scroll = ttk.Scrollbar(self,
                               orient='vertical',
                               command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=scroll.set)
        self.text_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scroll.config(command=self.text_box.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)


    def clear_text(self):
        """Clear the text in the box."""

        self.text_box.configure(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.configure(state=tk.DISABLED)


    def set_text(self, text):
        """Insert the text in the box"""

        self.text_box.configure(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert('1.0', text)
        self.text_box.configure(state=tk.DISABLED)


class GameChooser(ttk.Frame):
    """Main UI frame for new play_mancala.
    Includes filter, game list, and about panes."""

    def __init__(self, master):

        self.master = master
        self.all_games = None
        self.selected = None

        self.load_game_files()

        self.master.title('Mancala Game Chooser')
        super().__init__(self.master)
        self.pack()

        self.game_filter = GameFilters(self)
        self.game_filter.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.select_list = SelectList(self)
        self.select_list.grid(row=1, column=0, sticky='ns')

        self.about_text = AboutPane(self)
        self.about_text.grid(row=1, column=1, stick=tk.NSEW)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(tk.ALL, weight=1)

        self.select_list.fill_glist(self.all_games.keys())
        self.style()
        self.create_menus()


    def load_game_files(self):
        """Get a list of the game files, read the game_dict,
        create a dictionary of game name and about text."""

        self.all_games = {}
        for file in os.listdir(PATH):

            if file[-4:] != TXTPART or file == EXFILE:
                continue

            game_dict = man_config.read_game(PATH + file)

            game_name = game_dict[ckey.GAME_INFO][ckey.NAME]
            self.all_games[game_name] = game_dict


    @staticmethod
    def style():
        """Define the global styles."""

        # style = ttk.Style()
        # style.theme_use('default')
        # style.configure('.', background='#f0f0f0')
        # style.map('.',
        #           background=[('disabled', '#f0f0f0')],
        #           foreground=[('disabled', 'grey40')])
        # style.configure('TButton', padding=5)


    def create_menus(self):
        """Create the game control menus."""

        self.master.option_add('*tearOff', False)

        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        helpmenu = tk.Menu(self.menubar)
        helpmenu.add_command(label='Help...',
                             command=ft.partial(self.show_help, OPTIONS))
        helpmenu.add_command(label='Parameters...',
                             command=ft.partial(self.show_help, PARAMS))
        helpmenu.add_command(label='Games...',
                             command=ft.partial(self.show_help, GAMES))
        helpmenu.add_separator()
        helpmenu.add_command(label='About...',
                             command=ft.partial(self.show_help, ABOUT))
        self.menubar.add_cascade(label='Help', menu=helpmenu)


    def show_help(self, what=OPTIONS):
        """Have the os pop open the help file in a browser."""

        if what == OPTIONS:
            webbrowser.open(man_path.get_path('mancala_help.html'))

        elif what == PARAMS:
            webbrowser.open(man_path.get_path('game_params.html'))

        elif what == GAMES:
            webbrowser.open(man_path.get_path('about_games.html'))

        elif what == ABOUT:
            mancala_ui.quiet_dialog(self, 'About Manacala Games',
                                    version.RELEASE_TEXT)


    def select_game(self, game_name):
        """On game selection from the tree view,
        put it's help into the about_pane"""

        game_dict = self.all_games[game_name]

        about_str = ''
        if (ckey.GAME_INFO in game_dict
                and ckey.ABOUT in game_dict[ckey.GAME_INFO]):

            about_str = game_dict[ckey.GAME_INFO][ckey.ABOUT]

            paragraphs = about_str.split('\n')
            out_text = ''
            for para in paragraphs:
                fpara = textwrap.fill(para, 65) + '\n'
                out_text += fpara
            about_str = ''.join(out_text)

        self.about_text.set_text(about_str)
        self.selected = game_name


    def filter_games(self):
        """Update the games in select_list to reflect the current
        filter settings."""

        self.about_text.clear_text()
        self.select_list.fill_glist([name
                                     for name, gdict in self.all_games.items()
                                     if self.game_filter.show_game(gdict)])

    def play_game(self):
        """Build the constants and info. Create the game and play it."""

        if not self.selected:
            return

        game_dict = self.all_games[self.selected]

        class_name = game_dict[ckey.GAME_CLASS] \
            if ckey.GAME_CLASS in game_dict else 'Mancala'
        game_class = GAME_CLASSES[class_name]

        game_consts = gc.GameConsts(**game_dict[ckey.GAME_CONSTANTS])

        game_info = gi.GameInfo(**game_dict[ckey.GAME_INFO],
                                nbr_holes=game_consts.holes,
                                rules=game_class.rules)

        player_dict = game_dict[ckey.PLAYER]

        game = game_class(game_consts, game_info)
        game_ui = mancala_ui.MancalaUI(game, player_dict,
                                       root_ui=self.master)
        game_ui.mainloop()


# %%


if __name__ == '__main__':

    root = tk.Tk()
    chooser = GameChooser(root)
    chooser.mainloop()
