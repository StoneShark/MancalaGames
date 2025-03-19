# -*- coding: utf-8 -*-
"""A UI that brings up a list of games in the GameProps directory.

Created on Thu Mar 23 08:10:28 2023
@author: Ann"""

import abc
import os
import textwrap
import tkinter as tk
from tkinter import ttk

import cfg_keys as ckey
import game_constants as gconsts
import game_interface as gi
import man_config
import man_path
import mancala_ui
import ui_utils


from game_classes import GAME_CLASSES


# %% constants

DIR = 'GameProps'
PATH = man_path.get_path(DIR) + '/'

TXTPART = '.txt'
EXFILE = '_all_params.txt'

# this must not be in any of the enumerations
NOT_FILTERED = -2

SMALL = 6
LARGER = 7
LARGEST = 9

SIZES = {'Small (< 6)': lambda holes: holes < SMALL,
         'Medium (== 6)': lambda holes: holes == SMALL,
         'Larger (7 - 8)': lambda holes: LARGER <= holes < LARGEST,
         'Largest (>= 9)': lambda holes: holes >= LARGEST}

GOALS = {'Max Seeds': lambda goal: goal == gi.Goal.MAX_SEEDS,
         'Territory': lambda goal: goal == gi.Goal.TERRITORY,
         'Clear Own': lambda goal: goal == gi.Goal.CLEAR,
         'Deprive Opponent': lambda goal: goal == gi.Goal.DEPRIVE,
         'Round Tally': lambda goal: goal in (gi.Goal.RND_SEED_COUNT,
                                              gi.Goal.RND_EXTRA_SEEDS,
                                              gi.Goal.RND_POINTS,
                                              gi.Goal.RND_WIN_COUNT)}

ROUNDS = {'No Rounds': lambda rounds: not rounds,
          'Rounds': lambda rounds: rounds}

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



# %% frame classes

class BaseFilter(ttk.Frame, abc.ABC):
    """A filter category.  Checkboxes are created for each
    name, value pair return from the parent's items method.

    A dictionary of the tkvariables for the checkboxes is
    created. The keys will be either the value or the name
    based on value_keys."""

    def __init__(self, parent, filt_obj, label, value_keys):

        super().__init__(parent, borderwidth=3)
        self.parent = parent
        self.filt_obj = filt_obj

        row = ui_utils.Counter()

        lbl = ttk.Label(self, text=label, style='Title.TLabel')
        lbl.grid(row=row.count, column=0, columnspan=2, sticky='ew')
        lbl.configure(anchor='center')  # anchor in style is ignored

        self.filt_var = {}
        for name, value in self.items():

            key = value if value_keys else name
            self.filt_var[key] = tk.BooleanVar(self, value=1)

            ttk.Checkbutton(self, text=name,
                            variable=self.filt_var[key],
                            command=filt_obj.update_list
                            ).grid(row=row.count, column=0, columnspan=2,
                                   sticky='ew')

        rnbr = row.count
        ttk.Button(self, text='All',
                   command=self.not_filtered,
                   style='Filt.TButton'
                   ).grid(row=rnbr, column=0, padx=3, pady=3)
        ttk.Button(self, text='None',
                   command=self.all_filtered,
                   style='Filt.TButton'
                   ).grid(row=rnbr, column=1, padx=3, pady=3)


    def not_filtered(self):
        """Set all of the filter variables."""

        for var in self.filt_var.values():
            var.set(1)
        self.filt_obj.update_list()


    def all_filtered(self):
        """Clear all of the filter variables."""

        for var in self.filt_var.values():
            var.set(0)
        self.filt_obj.update_list()


    @abc.abstractmethod
    def items(self):
        """Return name, value pairs for each filter option.
        Name is shown on the UI for the filter option.
        Value can be what ever the show method will use to
        decide if a game should be included.

        If value is not immutable, be sure to create with
        value_keys of False."""


class VListFilter(BaseFilter):
    """A filter category based on a list of values."""

    def __init__(self, parent, filt_obj, label, val_list):

        self.val_list = val_list
        super().__init__(parent, filt_obj, label, value_keys=True)


    def items(self):
        """Return the this name and value pairs for this filter"""

        for evalue in self.val_list:
            yield evalue, evalue


    def show(self, value):
        """Determine if the game associated with value
        should be shown.

        value: the enum value to test (an int)"""

        return self.filt_var[value].get()


class EnumFilter(VListFilter):
    """A filter category based on enum values."""

    def items(self):
        """Return the name and value pairs for this filter"""

        for evalue in self.val_list:
            yield evalue.name, evalue.value


class DictFilter(BaseFilter):
    """A filter category based on a dictionary of rule_name: test"""

    def __init__(self, parent, filt_obj, label, filt_dict):

        self.filt_dict = filt_dict
        super().__init__(parent, filt_obj, label, value_keys=False)


    def items(self):
        """Return the name and value pairs for this filter"""

        return self.filt_dict.items()


    def show(self, value):
        """Determine if a the game associated with value
        should be shown.

        value: value of the associated parameter to test"""

        return any(test_func(value)
                   for test_name, test_func in self.filt_dict.items()
                   if self.filt_var[test_name].get())


class GameFilters(ttk.Frame):
    """A pane to collect all the game filters and the PLAY button.

    XXXX create 6 column frames so that the filters can be packed
    closer together--when a second row of filters is added."""

    def __init__(self, parent):

        super().__init__(parent, padding=3)
        self.parent = parent
        self.pack()

        col = ui_utils.Counter()

        filt_frame = ttk.Labelframe(self,
                                    text='Filters', labelanchor='nw',
                                    padding=3)
        filt_frame.grid(row=0, column=col.count, sticky=tk.NSEW)
        fcol = ui_utils.Counter()

        self.size_filter = DictFilter(filt_frame, self, 'Board Size', SIZES)
        self.size_filter.grid(row=0, column=fcol.count, sticky='ns')

        self.goal_filter = DictFilter(filt_frame, self, 'Goal', GOALS)
        self.goal_filter.grid(row=0, column=fcol.count, sticky='ns')

        self.rnd_filter = DictFilter(filt_frame, self, 'Rounds', ROUNDS)
        self.rnd_filter.grid(row=0, column=fcol.count, sticky='ns')

        self.laps_filter = EnumFilter(filt_frame, self, 'Lap Type', gi.LapSower)
        self.laps_filter.grid(row=0, column=fcol.count, sticky='ns')

        self.child_filter = EnumFilter(filt_frame, self, 'Child Type', gi.ChildType)
        self.child_filter.grid(row=0, column=fcol.count, sticky='ns')

        self.capt_filter = DictFilter(filt_frame, self, 'Capture Types', CAPTS)
        self.capt_filter.grid(row=0, column=fcol.count, sticky='ns')

        # this does not break the game list into useful groups
        # leave as example VListFilter
        # fcol.reset()
        # self.class_filter = VListFilter(filt_frame, self, 'Game Class',
        #                                list(GAME_CLASSES.keys()))
        # self.class_filter.grid(row=1, column=fcol.count, sticky='ns')

        filt_frame.columnconfigure(tk.ALL, weight=1)

        cmd_col = col.count
        ttk.Button(self, text='Play',
                   command=parent.play_game,
                   style='Play.TButton').grid(
                       row=0, column=cmd_col, sticky='ns')

        self.columnconfigure(tk.ALL, weight=1)


    def not_filtered(self):
        """Clear all of the filters."""

        # self.class_filter.not_filtered()
        self.size_filter.not_filtered()
        self.laps_filter.not_filtered()
        self.goal_filter.not_filtered()
        self.rnd_filter.not_filtered()
        self.child_filter.not_filtered()
        self.capt_filter.not_filtered()


    def all_filtered(self):
        """Set all of the filters."""

        # self.class_filter.all_filtered()
        self.size_filter.all_filtered()
        self.laps_filter.all_filtered()
        self.goal_filter.all_filtered()
        self.rnd_filter.all_filtered()
        self.child_filter.all_filtered()
        self.capt_filter.all_filtered()


    def show_game(self, game_dict):
        """Test if the game should be shown based on the filter
        settings and the game_dict"""


        gcts = game_dict[ckey.GAME_CONSTANTS]
        ginfo = game_dict[ckey.GAME_INFO]
        return all([# self.class_filter.show(game_dict[ckey.GAME_CLASS]),
                    self.size_filter.show(gcts[ckey.HOLES]),
                    self.laps_filter.show(ginfo.get(ckey.MLAPS, 0)),
                    self.goal_filter.show(ginfo.get(ckey.GOAL, 0)),
                    self.rnd_filter.show(ginfo.get(ckey.ROUNDS, 0)),
                    self.child_filter.show(ginfo.get(ckey.CHILD_TYPE, 0)),
                    self.capt_filter.show(ginfo),
                    ])


    def update_list(self):
        """Update the parent's list of filtered games."""

        self.parent.filter_games()


class SelectList(ttk.Labelframe):
    """Scrollable tree list for list of filtered games.
    Selecting one tells the parent it was selected."""

    def __init__(self, parent):

        super().__init__(parent, text='Game List', labelanchor='nw',
                         padding=3)
        self.parent = parent

        self.game_list = ttk.Treeview(self, show='tree', selectmode='browse')

        scroll = ttk.Scrollbar(self,
                               orient='vertical',
                               command=self.game_list.yview)
        self.game_list.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.Y)

        self.game_list.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)

        self.game_list.bind('<<TreeviewSelect>>', self.select_game)
        self.game_list.bind('<Double-Button-1>', self.play_game)


    def select_game(self, _=None):
        """The user has selected a game, tell the parent
        it was selected."""

        game_name = self.game_list.selection()

        if game_name:
            game_name = game_name[0]
            self.parent.select_game(game_name)


    def play_game(self, _=None):
        """Play the game."""

        self.select_game()
        self.parent.play_game()


    def clear_glist(self):
        """Clear the game list."""

        for item in self.game_list.get_children():
            self.game_list.delete(item)


    def fill_glist(self, games):
        """Put the games in the treeview"""

        self.clear_glist()

        for name in games:
            self.game_list.insert('', tk.END, iid=name, text=name)


class AboutPane(ttk.Labelframe):
    """A pane for the game help text (called the 'about' text)."""

    def __init__(self, parent):

        super().__init__(parent, text='Game Overview', labelanchor='nw',
                         padding=3)

        self.text_box = tk.Text(self)

        scroll = ttk.Scrollbar(self,
                               orient='vertical',
                               command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=scroll.set)
        self.text_box.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)

        scroll.config(command=self.text_box.yview)
        scroll.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.Y)


    def clear_text(self):
        """Clear the text in the box."""

        self.text_box.configure(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.configure(state=tk.DISABLED)


    def set_text(self, text):
        """Set the text in the box"""

        self.text_box.configure(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert('1.0', text)
        self.text_box.configure(state=tk.DISABLED)


    @staticmethod
    def format_para(text):
        """Format a paragraph for the description."""

        paragraphs = text.split('\n')
        out_text = ''
        for para in paragraphs:
            fpara = textwrap.fill(para, 65) + '\n'
            out_text += fpara

        return ''.join(out_text)


    def describe_game(self, game_dict):
        """Build a description of the game for the text window.
        Use the about text and any extra keys (not the standard
        game config keys)."""

        dtext = ''
        if (ckey.GAME_INFO in game_dict
                and ckey.ABOUT in game_dict[ckey.GAME_INFO]):

            dtext = self.format_para(game_dict[ckey.GAME_INFO][ckey.ABOUT])

        for key, text in game_dict.items():
            if key not in [ckey.GAME_CLASS, ckey.GAME_CONSTANTS,
                           ckey.GAME_INFO, ckey.PLAYER]:

                dtext += '\n'
                dtext += self.format_para(key.title() + ':  ' + text)

        self.set_text(dtext)


class GameChooser(ttk.Frame):
    """Main UI frame for new play_mancala.
    Includes filter, game list, and about panes."""

    def __init__(self, master):

        self.master = master
        self.all_games = None
        self.selected = None

        self.load_game_files()
        ui_utils.setup_styles(master)

        self.master.title('Play Mancala - Game Chooser')
        super().__init__(self.master)
        self.master.resizable(False, True)
        self.pack(expand=tk.TRUE, fill=tk.BOTH)

        self.game_filter = GameFilters(self)
        self.game_filter.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.select_list = SelectList(self)
        self.select_list.grid(row=1, column=0, sticky='ns')

        self.about_text = AboutPane(self)
        self.about_text.grid(row=1, column=1, sticky=tk.NSEW)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(tk.ALL, weight=1)

        self.select_list.fill_glist(self.all_games.keys())
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


    def create_menus(self):
        """Create the game control menus."""

        self.master.option_add('*tearOff', False)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        playmenu = tk.Menu(menubar)
        playmenu.add_command(label='Play...', command=self.play_game)
        menubar.add_cascade(label='Play', menu=playmenu)

        filtmenu = tk.Menu(menubar)
        filtmenu.add_command(label='No Filters',
                             command=self.game_filter.not_filtered)
        filtmenu.add_command(label='All Filtered',
                             command=self.game_filter.all_filtered)
        menubar.add_cascade(label='Filters', menu=filtmenu)

        ui_utils.add_help_menu(menubar, self)


    def select_game(self, game_name):
        """On game selection from the tree view,
        put it's help into the about_pane"""

        game_dict = self.all_games[game_name]
        self.about_text.describe_game(game_dict)
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

        game_consts = gconsts.GameConsts(**game_dict[ckey.GAME_CONSTANTS])

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
