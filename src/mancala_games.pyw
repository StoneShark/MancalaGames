# -*- coding: utf-8 -*-
"""Create a window that collects the mancala parameters
and then plays the game. Saving and loading parameter
sets to files is supported.


Created on Thu Mar 30 13:43:39 2023
@author: Ann"""


# %% import

import functools as ft
import json
import os.path
import traceback
import warnings
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfile

import pandas as pd

import cfg_keys as ckey
import game_constants as gc
import game_interface as gi
import mancala_ui
import man_config
import man_path

from game_classes import GAME_CLASSES
from game_constants import MAX_HOLES
from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import RoundStarter
from game_interface import StartPattern
from game_log import game_log



# %%  Constants


MAKE_LVARS = {ckey.CAPT_ON: 5,
              ckey.UDIR_HOLES: MAX_HOLES + 1}

# these are the expected tabs, put them in this order (add any extras)
PARAM_TABS = ('Game', 'Dynamics', 'Allow', 'Sow', 'Capture', 'Player')


# widget states
DISABLED = 'disabled'
ACTIVE = 'active'
NORMAL = 'normal'

# types from the params file
INT_TYPE = 'int'
STR_TYPE = 'str'
BOOL_TYPE = 'bool'
MSTR_TYPE = 'multi_str'
LIST_TYPE = 'list[int]'


SKIP_TAB = 'skip'
OPT_TAG = '_'
GI_TAG = 'game_info _'

# %%


def dict_inv_dict(adict):
    """Invert the keys and values for a reverse lookup."""

    vals = adict.values()
    assert len(vals) == len(set(vals)), 'values not unique for adict'
    return [adict, {value: key for key, value in adict.items()}]


string_dicts = {
    'Direct': dict_inv_dict(
        {'Clockwise': Direct.CW,
         'Counter-clockwise': Direct.CCW,
         'Split': Direct.SPLIT}),

    'GrandSlam': dict_inv_dict(
        {"Legal": GrandSlam.LEGAL,
         "Not Legal": GrandSlam.NOT_LEGAL,
         "Legal but no capture": GrandSlam.NO_CAPT,
         "Legal but opp takes remaining": GrandSlam.OPP_GETS_REMAIN,
         "Legal but leave leftmost": GrandSlam.LEAVE_LEFT,
         "Legal but leave rightmost": GrandSlam.LEAVE_RIGHT}),

    'RoundStarter': dict_inv_dict(
        {'Alternate': RoundStarter.ALTERNATE,
         'Round Winner': RoundStarter.WINNER,
         'Round Loser': RoundStarter.LOSER}),

    'CrossCaptOwn': dict_inv_dict(
        {'Leave': CrossCaptOwn.LEAVE,
         'Pick on Capture': CrossCaptOwn.PICK_ON_CAPT,
         'Alway Pick': CrossCaptOwn.ALWAYS_PICK}),

    'StartPattern': dict_inv_dict(
        {'All Equal': StartPattern.ALL_EQUAL,
         'Gamacha': StartPattern.GAMACHA,
         'Alternates': StartPattern.SADEQA_ONE,
         'Alts with 1': StartPattern.SADEQA_TWO,
         'Tapata': StartPattern.TAPATA}),

    'Goal': dict_inv_dict(
        {'Max Seeds': Goal.MAX_SEEDS,
         'Deprive Opponent': Goal.DEPRIVE,
         'Territory': Goal.TERRITORY}),
}


# %%  game params UI

class MancalaGames(tk.Frame):
    """Main interface to select game parameters, save & load games,
    and play Mancala games."""

    def __init__(self):

        self.game = None
        self.params = None
        self.filename = None
        self.loaded_config = None
        self.tkvars = {}
        self.tktexts = {}
        self.udir_frame = None
        self.param_changed = False
        self.tabs = {}
        self.desc = None
        self.prev_option = None

        self.master = tk.Tk()

        self.master.title('Choose Mancala Options')
        self.master.resizable(False, False)
        self.master.wm_geometry('+400+200')
        super().__init__(self.master)
        self.master.report_callback_exception = self._exception_callback
        warnings.showwarning = self._warning
        self.pack()

        self._create_menus()
        self._add_commands_ui()
        self._read_params_file()
        self._add_tabs()
        self._create_desc_pane()

        self._make_tkvars()
        self._make_ui_elements()
        self._reset()  # fill text boxes


    def destroy(self):
        """Remove the traces from the tk variables.
        Don't change the name, we're overriding Frame method."""

        for var in self.tkvars.values():
            if isinstance(var, list):
                for cvar in var:
                    cvar.trace_remove(*cvar.trace_info()[0])
            else:
                var.trace_remove(*var.trace_info()[0])


    @staticmethod
    def _exception_callback(*args):
        """Support debugging by printing the play_log and the traceback."""

        game_log.dump()
        traceback.print_exception(args[0], args[1], args[2])


    @staticmethod
    def _warning(message, *_):
        """Notify user of warnings during parameter test."""

        tk.messagebox.showwarning('Parameter Warning', message)


    @staticmethod
    def _help():
        """Have the os pop open the help file in a browser."""

        os.startfile(man_path.get_path('mancala_help.html'))


    def _create_menus(self):
        """Create the game control menus."""

        self.master.option_add('*tearOff', False)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        gamemenu = tk.Menu(menubar)

        gamemenu.add_command(label='Reset', command=self._reset)
        gamemenu.add_command(label='Help ...', command=self._help)
        menubar.add_cascade(label='Game', menu=gamemenu)


    def _add_commands_ui(self):
        """Add buttons for commands."""

        self.but_frame = tk.Frame(self.master, padx=3, pady=3,
                                  borderwidth=3)
        self.but_frame.pack(side='bottom', expand=True, fill='both')

        tk.Button(self.but_frame, text='Test', command=self._test,
                  ).pack(side='left', expand=True, fill='x')
        tk.Button(self.but_frame, text='Load', command=self._load
                  ).pack(side='left', expand=True, fill='x')
        tk.Button(self.but_frame, text='Save', command=self._save
                  ).pack(side='left', expand=True, fill='x')
        tk.Button(self.but_frame, text='Play', command=self._play
                  ).pack(side='left', expand=True, fill='x')


    def _read_params_file(self):
        """Read the game parameters file."""

        col_types = {'row': int, 'col': int}

        self.params = pd.read_csv('game_params.txt', sep='\t',
                                  dtype=col_types)
        # TODO deal with path exe diff from run directly


    def _param_tuples(self):
        """An iterator that goes through the params as tuples."""

        return self.params.itertuples(index=False)


    def _add_tabs(self):
        """Determine what tabs are needed and add them."""

        extra_tabs =  set(self.params.tab) - {SKIP_TAB} - set(PARAM_TABS)
        tabs = PARAM_TABS + tuple(extra_tabs)

        tab_control = ttk.Notebook(self)
        for tab_name in tabs:

            tab = ttk.Frame(tab_control, padding=3)
            self.tabs[tab_name] = tab
            tab_control.add(tab, text=tab_name, padding=5)
        tab_control.pack(expand = 1, fill ="both")


    def _create_desc_pane(self):
        """Build the label desc pane."""

        dframe = tk.Frame(self)
        dframe.pack(side='bottom')

        self.desc = tk.Text(dframe, width=60, height=8)

        scroll = tk.Scrollbar(dframe)
        self.desc.configure(yscrollcommand=scroll.set)
        self.desc.pack(side='left')

        scroll.config(command=self.desc.yview)
        scroll.pack(side='right', fill='y')
        self.desc.pack(expand=True, fill=tk.BOTH)


    def _update_desc(self, option, _):
        """We've enter a new widget, update desc text."""

        if self.prev_option == option:
            return
        self.prev_option = option

        ptable = self.params
        # TODO there must be a better way to get a single cell from a DF
        desc_text = list(ptable.loc[ptable.option==option].description)[0]

        self.desc.delete('1.0', 'end')
        self.desc.insert('1.0', desc_text)



    @staticmethod
    def _get_construct_default(vtype, cspec, option):
        """The defaults in the parameter table yield a playable game,
        they are not the actual construction defaults."""

        if cspec == GI_TAG:
            return gi.GameInfo.get_default(option)

        if vtype in (STR_TYPE, MSTR_TYPE):
            return ""

        if vtype == INT_TYPE:
            return 0

        return False


    @staticmethod
    def _get_gc_value(game_config, cspec, option):
        """game_config_spec format is one of
            word+  or  word* _
        where option is substituted for _

        Lookup and return the value in a series of nested dictionaries."""

        tags = cspec.split(' ')

        vdict = game_config
        for tag in tags:
            if tag == OPT_TAG:
                if option in vdict:
                    return vdict[option]
                return None

            if tag in vdict:
                vdict = vdict[tag]
            else:
                return None

        return vdict


    @staticmethod
    def _set_gc_value(game_config, cspec, option, value):
        """Set the value in a series of nested dictionaries;
        create empty dictionaries as required."""

        tags = cspec.split(' ')

        vdict = game_config
        for tag in tags[:-1]:
            if tag not in vdict:
                vdict[tag] = {}
            vdict = vdict[tag]

        if tags[-1] == OPT_TAG:
            vdict[option] = value
        else:
            vdict[tags[-1]] = value


    def _get_boxes_config(self, name):
        """Return the number holes for the list for name."""

        if name == ckey.CAPT_ON:
            boxes = 5

        elif name == ckey.UDIR_HOLES:
            ptable = self.params
            boxes = int(ptable.loc[ptable.option==ckey.HOLES].ui_default)

        else:
            raise ValueError(f"Don't know list length for {name}.")

        return boxes


    def _add_watchers(self):
        """Add the watchers to all the tk variables."""

        for var in self.tkvars.values():
            if isinstance(var, list):
                for cvar in var:
                    cvar.trace_add('write', self._tkvalue_changed)
            else:
                var.trace_add('write', self._tkvalue_changed)


    def _make_tkvars(self):
        """Create the tk variables described by the parameters file."""

        for tab, option, _, _, vtype, default, *_ in self._param_tuples():
            if tab == SKIP_TAB or vtype == MSTR_TYPE:
                continue

            if vtype == STR_TYPE:
                self.tkvars[option] = tk.StringVar(self.master, default,
                                                   name=option)
            elif vtype == BOOL_TYPE:
                self.tkvars[option] = tk.BooleanVar(self.master, default,
                                                    name=option)
            elif vtype == INT_TYPE:
                self.tkvars[option] = tk.IntVar(self.master, default,
                                                name=option)
            elif vtype == LIST_TYPE:
                boxes = MAKE_LVARS[option]
                self.tkvars[option] = [tk.BooleanVar(self.master, False,
                                                     name=f'{option}_{i}')
                                       for i in range(boxes)]

            elif vtype in string_dicts:
                _, inv_dict = string_dicts[vtype]
                value = list(inv_dict.values())[eval(default)]
                self.tkvars[option] = tk.StringVar(self.master, value,
                                                   name=option)

        # don't add the traces until all the variables are made
        self._add_watchers()


    def _tkvalue_changed(self, var, index, mode):
        """Called-back whenever any tkvar is changed."""

        _ = (index, mode)
        self.param_changed = True

        if var == ckey.NAME:
            self.filename = self.tkvars[ckey.NAME].get() + '.txt'

        elif var == ckey.HOLES:
            self._resize_udirs()


    def _resize_udirs(self):
        """Change the number of the checkboxes on the screen.
        All the variables were built with the tkvars.
        Destroy any extra widgets or make any required new ones."""

        widgets = self.udir_frame.winfo_children()

        prev_holes = len(widgets)
        holes = self.tkvars[ckey.HOLES].get()

        if holes > MAX_HOLES:
            print('value too big.')
            return

        for idx in range(holes, prev_holes):
            widgets[idx].destroy()

        for idx in range(prev_holes + 1, holes + 1):
            tk.Checkbutton(self.udir_frame, text=str(idx),
                           variable=self.tkvars[ckey.UDIR_HOLES][idx - 1]
                           ).pack(side='left')


    def _make_text_entry(self, frame, option, text, row, col):
        """Make a text box entry with scroll bar."""
        # pylint: disable=too-many-arguments

        tframe = tk.LabelFrame(frame, text=text, labelanchor='nw')
        tframe.grid(row=row, column=col, columnspan=2, rowspan=2)

        text_box = tk.Text(tframe, width=40, height=8)
        self.tktexts[option] = text_box

        scroll = tk.Scrollbar(tframe)
        text_box.configure(yscrollcommand=scroll.set)
        text_box.pack(side='left')

        scroll.config(command=text_box.yview)
        scroll.pack(side='right', fill='y')

        tframe.bind('<Enter>', ft.partial(self._update_desc, option))


    def _make_entry(self, frame, option, text, vtype, row, col):
        """Make a single line string entry."""
        # pylint: disable=too-many-arguments

        length = 5 if vtype == INT_TYPE else 20

        lbl = tk.Label(frame, text=text)
        lbl.grid(row=row, column=col)

        ent = tk.Entry(frame,  width=length,
                 textvariable=self.tkvars[option])
        ent.grid(row=row, column=col + 1)

        lbl.bind('<Enter>', ft.partial(self._update_desc, option))
        ent.bind('<Enter>', ft.partial(self._update_desc, option))


    def _make_checkbox(self, frame, option, text, row, col):
        """Make a labeled checkbox."""
        # pylint: disable=too-many-arguments

        lbl = tk.Label(frame, text=text)
        lbl.grid(row=row, column=col)

        box = tk.Checkbutton(frame, variable=self.tkvars[option])
        box.grid(row=row, column=col + 1)
        box.grid(row=row, column=col + 1)

        lbl.bind('<Enter>', ft.partial(self._update_desc, option))
        box.bind('<Enter>', ft.partial(self._update_desc, option))


    def _make_checkbox_list(self, frame, option, text, row, col):
        """Make a list of checkboxes."""
        # pylint: disable=too-many-arguments

        lbl = tk.Label(frame, text=text)
        lbl.grid(row=row, column=col)

        boxes = self._get_boxes_config(option)
        boxes_fr = tk.Frame(frame)
        boxes_fr.grid(row=row, column=1, columnspan=3)
        if option == ckey.UDIR_HOLES:
            self.udir_frame = boxes_fr

        for nbr in range(1, boxes+1):
            tk.Checkbutton(boxes_fr, text=str(nbr),
                           variable=self.tkvars[option][nbr - 1]
                           ).pack(side='left')

        lbl.bind('<Enter>', ft.partial(self._update_desc, option))
        boxes_fr.bind('<Enter>', ft.partial(self._update_desc, option))


    def _make_option_list(self, frame, option, text, vtype, row, col):
        """Make an option list corresponding to the enum type."""
        # pylint: disable=too-many-arguments

        values = list(string_dicts[vtype][0].keys())

        lbl = tk.Label(frame, text=text)
        lbl.grid(row=row, column=col)

        opmenu = tk.OptionMenu(frame, self.tkvars[option], *values)
        opmenu.config(width=2 + max(len(str(val)) for val in values))
        opmenu.grid(row=row, column=col + 1)

        lbl.bind('<Enter>', ft.partial(self._update_desc, option))
        opmenu.bind('<Enter>', ft.partial(self._update_desc, option))


    def _make_ui_elements(self):
        """Make the UI elements corresponding to the parameter table."""

        for param in self._param_tuples():
            tab, option, text, _, vtype, _, row, col, *_ = param

            if tab == SKIP_TAB:
                continue

            frame = self.tabs[tab]

            if vtype == MSTR_TYPE:
                self._make_text_entry(frame, option, text, row, col)

            elif vtype in (STR_TYPE, INT_TYPE):
                self._make_entry(frame, option, text, vtype, row, col)

            elif vtype == BOOL_TYPE:
                self._make_checkbox(frame, option, text, row, col)

            elif vtype == LIST_TYPE:
                self._make_checkbox_list(frame, option, text, row, col)

            elif vtype in string_dicts:
                self._make_option_list(frame, option, text, vtype, row, col)


    def _fill_tk_from_config(self, game_config):
        """Set the tk vars (display vars) from the game_config
        dict."""

        for tab, option, _, cspec, vtype, *_  in self._param_tuples():
            if tab == SKIP_TAB:
                continue

            value = self._get_gc_value(game_config, cspec, option)
            if value is None:
                value = self._get_construct_default(vtype, cspec, option)

            if vtype == MSTR_TYPE:
                self.tktexts[option].delete('1.0', 'end')
                self.tktexts[option].insert('1.0', value)

            elif vtype in (STR_TYPE, BOOL_TYPE, INT_TYPE):
                self.tkvars[option].set(value)

            elif vtype == LIST_TYPE:

                for var in self.tkvars[option]:
                    var.set(False)

                if value and isinstance(value, list):
                    for val in value:
                        self.tkvars[option][val].set(True)

            elif vtype in string_dicts:

                _, inv_dict = string_dicts[vtype]
                self.tkvars[option].set(inv_dict[value])


    def _make_config_from_tk(self):
        """Get the values from the tkvars and set them into
        the a game_config dict."""

        game_config = {}

        for tab, option, _, cspec, vtype, *_ in self._param_tuples():
            if tab == SKIP_TAB:
                continue

            if vtype == MSTR_TYPE:
                value = self.tktexts[option].get('1.0', 'end')

            elif vtype in (STR_TYPE, BOOL_TYPE, INT_TYPE):
                value = self.tkvars[option].get()

            elif vtype == LIST_TYPE:
                value = [nbr
                         for nbr, var in enumerate(self.tkvars[option])
                         if var.get()]

            elif vtype in string_dicts:
                str_dict, _ = string_dicts[vtype]
                value = self.tkvars[option].get()
                value = str_dict[value]

            self._set_gc_value(game_config, cspec, option, value)

        return game_config


    def _prepare_game(self):
        """Build the two game variables: constants and info
        and then build the game.
        This function should be wrapped with a try because
        exceptions/warnings might be raised."""

        game_config = self._make_config_from_tk()
        game_class = game_config[ckey.GAME_CLASS]
        gclass = GAME_CLASSES[game_class]

        consts = gc.GameConsts(**game_config[ckey.GAME_CONSTANTS])
        info = gi.GameInfo(nbr_holes=consts.holes,
                           rules=gclass.rules,
                           **game_config[ckey.GAME_INFO])
        self.game = gclass(consts, info)

        self.param_changed = False


    def _test(self):
        """Try to build the game params and game,
        trap any exceptions, report to user."""

        self.param_changed |= \
            any(field.edit_modified() for field in self.tktexts.values())
        if self.game and not self.param_changed:
            return

        try:
            self._prepare_game()

        except (gc.GameConstsError, gi.GameInfoError, NotImplementedError
                ) as error:
            message = error.__class__.__name__ + ':  ' + str(error)
            tk.messagebox.showerror('Parameter Error', message)

            self.game = None


    def _load(self):
        """Load params from file. Check size for reasonableness.
        Translate the json string. Convert non-primitive types.
        Build game_consts and game_info.
        json.JSONDecodeError is dervied from ValueError."""

        filename = tkfile.askopenfilename(
            parent=self.master,
            title='Load Parameters',
            initialdir=man_path.get_path('GameProps'))
        if not filename:
            return

        self.filename = os.path.basename(filename)

        try:
            config_dict = man_config.read_game(filename)
        except ValueError as error:
            tk.messagebox.showerror('JSON File Error', error)
            return

        self._fill_tk_from_config(config_dict)
        self.loaded_config = config_dict
        self._test()


    def _save(self):
        """Save params to file.
        Preserve any tags/comments that were in a loaded config."""

        game_config = self._make_config_from_tk()
        if self.loaded_config:
            for tag in self.loaded_config.keys():
                if tag not in game_config:
                    game_config[tag] = self.loaded_config[tag]

        if not self.filename:
            self.filename = game_config[ckey.GAME_INFO][ckey.NAME] + '.txt'

        filename = tkfile.asksaveasfilename(
            parent=self.master,
            title='Save Parameters',
            confirmoverwrite=True,
            initialdir=man_path.get_path('GameProps'),
            initialfile=self.filename,
            filetypes=[('text file', '.txt')],
            defaultextension='.txt')
        if not filename:
            return

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(game_config, file, indent=3)


    def _play(self):
        """Create and play the game. deactivate param ui and block
        while the game is being played. reactivate when the game
        is exited."""

        self._test()
        if not self.game:
            return

        game_ui = mancala_ui.MancalaUI(self.game, {}, self.master)
        # TODO deactivate, but not tabs
        # self._set_active(False)

        # game_ui.grab_set()
        game_ui.wait_window()
        # self._set_active(True)


    def _reset(self):
        """Reset to ui_defaults; clear loaded config dictionary."""

        self.loaded_config = None

        for tab, option, _, _, vtype, default, *_ in self._param_tuples():
            if tab == SKIP_TAB:
                continue

            if vtype == MSTR_TYPE:
                self.tktexts[option].delete('1.0', 'end')
                self.tktexts[option].insert('1.0', default)

            elif vtype in string_dicts:

                _, inv_dict = string_dicts[vtype]
                value = list(inv_dict.values())[eval(default)]
                self.tkvars[option].set(value)

            elif vtype == LIST_TYPE:
                for var in self.tkvars[option]:
                    var.set(False)

            else:
                self.tkvars[option].set(default)




# %%  main

if __name__ == '__main__':

    man_games = MancalaGames()
    man_games.mainloop()
