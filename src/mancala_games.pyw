# -*- coding: utf-8 -*-
"""Create a window that collects the mancala parameters
and then plays the game. Saving and loading parameter
sets to files is supported.

The file game_info.txt drives much of what happens here.

Created on Thu Mar 30 13:43:39 2023
@author: Ann"""

# pylint: disable=too-many-lines

# %% import

import collections
import csv
import functools as ft
import json
import os.path
import textwrap
import traceback
import warnings
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfile

import ai_player
import cfg_keys as ckey
import game_constants as gc
import game_interface as gi
import mancala_ui
import man_config
import man_path

from ai_player import ALGORITHM_DICT
from ai_player import AI_PARAM_DEFAULTS
from game_classes import GAME_CLASSES
from game_constants import MAX_HOLES
from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import RoundStarter
from game_interface import StartPattern


# %%  Constants

# how many variables to make for lists
# if the option for a 'list[int]' isn't here, 4 variables will be made
MAKE_LVARS = {ckey.CAPT_ON: 5,
              ckey.UDIR_HOLES: MAX_HOLES + 1}

DESC_WIDTH = 60
DASH_BULLET = '- '
INT_LIST_CHARS = '0123456789, '

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
BLIST_TYPE = 'list[bool]'
ILIST_TYPE = 'list[int]'

SKIP_TAB = 'skip'
OPT_TAG = '_'
GI_TAG = 'game_info _'
AI_TAG = 'player ai_params _'
SCR_TAG = 'player scorer _'


# %% enum dictionaries

LDicts = collections.namedtuple('LDicts', 'str_dict, int_dict, enum_dict')

def lookup_dicts(etype, adict):
    """Return the dict, it's inverse, and enum name: enum dict
    for the enum (etype)."""

    vals = adict.values()
    assert len(vals) == len(set(vals)), 'values not unique for adict'
    return LDicts(adict,
                  {value: key for key, value in adict.items()},
                  {e.name: e for e in etype})


def lookup_strs(strings):
    """The string and values are both the strings.
    Build and return dictionaries."""

    sdict = {s: s for s in strings}
    return LDicts(sdict, sdict, sdict)


STRING_DICTS = {
    'GameClasses': lookup_strs(GAME_CLASSES.keys()),

    'Direct': lookup_dicts(Direct,
        {'Clockwise': Direct.CW,
         'Counter-clockwise': Direct.CCW,
         'Split': Direct.SPLIT}),

    'GrandSlam': lookup_dicts(GrandSlam,
        {"Legal": GrandSlam.LEGAL,
         "Not Legal": GrandSlam.NOT_LEGAL,
         "Legal but no capture": GrandSlam.NO_CAPT,
         "Legal but opp takes remaining": GrandSlam.OPP_GETS_REMAIN,
         "Legal but leave leftmost": GrandSlam.LEAVE_LEFT,
         "Legal but leave rightmost": GrandSlam.LEAVE_RIGHT}),

    'RoundStarter': lookup_dicts(RoundStarter,
        {'Alternate': RoundStarter.ALTERNATE,
         'Round Winner': RoundStarter.WINNER,
         'Round Loser': RoundStarter.LOSER}),

    'CrossCaptOwn': lookup_dicts(CrossCaptOwn,
        {'Leave': CrossCaptOwn.LEAVE,
         'Pick on Capture': CrossCaptOwn.PICK_ON_CAPT,
         'Alway Pick': CrossCaptOwn.ALWAYS_PICK}),

    'StartPattern': lookup_dicts(StartPattern,
        {'All Equal': StartPattern.ALL_EQUAL,
         'Gamacha': StartPattern.GAMACHA,
         'Alternates': StartPattern.ALTERNATES,
         'Alts with 1': StartPattern.ALTS_WITH_1,
         'Tapata': StartPattern.TAPATA}),

    'Goal': lookup_dicts(Goal,
        {'Max Seeds': Goal.MAX_SEEDS,
         'Deprive Opponent': Goal.DEPRIVE,
         'Territory': Goal.TERRITORY}),

    'Algorithm': lookup_strs(ALGORITHM_DICT.keys())
}


# %% helper funcs

MINUS = '-'

def stoi(sval):
    """make, a possibly empty, string a valid int."""

    return int(sval) if sval else 0


def int_validate(value):
    """Only allow empty values, or decimals."""

    if not value or value == MINUS:
        return True

    if ((value[0] != MINUS and not value.isdecimal())
            or (value[0] == MINUS and not value[1:].isdecimal())):
        return False
    return True


def convert_value(value):
    """convert the ui_defaults to nice python types."""

    convert_dict = {'n': None,
                    't': True,
                    'true': True,
                    'f': False,
                    'false': False,
                    }
    elist_str = '[]'
    value = value.strip()

    if (key := value.lower()) in convert_dict:
        return convert_dict[key]

    if value.isdigit() or (value[0] == MINUS and value[1:].isdigit()):
        return int(value)

    if value == elist_str:
        return []

    if (value[0] == elist_str[0]
            and value[-1] == elist_str[-1]
            and all(c in INT_LIST_CHARS for c in value[1:-1])):
        substrs = value[1:-1].split(',')
        return [int(val.strip()) for val in substrs]

    return value


# %%  game params UI

class MancalaGames(tk.Frame):
    """Main interface to select game parameters, save & load games,
    and play Mancala games."""

    def __init__(self, master):

        self.master = master
        self.game = None
        self.params = {}
        self.filename = None
        self.loaded_config = None     # keep for persistent comment entries
        self.game_config = None       # constructed config for playing
        self.tkvars = {}
        self.tktexts = {}
        self.udir_frame = None
        self.param_changed = False
        self.tabs = {}
        self.desc = None
        self.prev_option = None

        super().__init__(self.master)
        self.master.title('Choose Mancala Options')
        self.master.resizable(False, False)
        self.master.wm_geometry('+400+200')
        self.pack()

        self.master.report_callback_exception = self._exception_callback
        warnings.showwarning = self._warning

        self._create_menus()
        self._add_commands_ui()
        self._read_params_file()
        self._add_tabs()
        self._create_desc_pane()
        self._make_tkvars()
        self._make_ui_elements()
        self._reset()


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
        self.but_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        tk.Button(self.but_frame, text='Test', command=self._test,
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(self.but_frame, text='Load', command=self._load
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(self.but_frame, text='Save', command=self._save
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(self.but_frame, text='Play', command=self._play
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)


    def _read_params_file(self):
        """Read the game parameters file."""

        with open(man_path.get_path('game_params.txt'), 'r',
                  encoding='us-ascii') as file:
            reader = csv.reader(file, delimiter='\t')
            data = list(reader)

        fields = data[0]
        option_idx = fields.index('option')
        ui_default_idx = fields.index('ui_default')
        bools = [fields.index(f) for f in
                 ('new_game', 'allow', 'moves', 'incr', 'starter',
                  'get_dir', 'sower', 'capt_ok', 'capturer', 'ender',
                  'quitter', 'gstr')]
        ints = [fields.index(f) for f in ('row', 'col')]

        # pylint: disable=invalid-name
        Params = collections.namedtuple('Params', fields)

        for rec in data[1:]:

            if rec[0] == SKIP_TAB:
                continue

            for idx in bools:
                rec[idx] = bool(rec[idx])
            for idx in ints:
                rec[idx] = int(rec[idx])
            rec[ui_default_idx] = convert_value(rec[ui_default_idx])

            self.params[rec[option_idx]] = Params(*rec)


    def _add_tabs(self):
        """Determine what tabs are needed and add them."""

        tab_set = set(r.tab for r in self.params.values())
        extra_tabs =  tab_set - set(PARAM_TABS)
        tabs = PARAM_TABS + tuple(extra_tabs)

        tab_control = ttk.Notebook(self)
        for tab_name in tabs:

            tab = ttk.Frame(tab_control, padding=3)
            self.tabs[tab_name] = tab
            tab_control.add(tab, text=tab_name, padding=5)
        tab_control.pack(expand = 1, fill =tk.BOTH)


    def _create_desc_pane(self):
        """Build the label desc pane."""

        dframe = tk.LabelFrame(self, text='Param Description',
                               labelanchor='nw')
        dframe.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        self.desc = tk.Text(dframe, width=DESC_WIDTH, height=8)

        scroll = tk.Scrollbar(dframe)
        self.desc.configure(yscrollcommand=scroll.set)
        self.desc.pack(side=tk.LEFT)

        scroll.config(command=self.desc.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.desc.pack(expand=True, fill=tk.BOTH)


    def _update_desc(self, option, _):
        """We've enter a new widget, update desc text.
        Don't let the user edit the description."""

        if self.prev_option == option:
            return
        self.prev_option = option

        text = self.params[option].text
        desc = self.params[option].description

        paragraphs = desc.split('\n')
        out_text = ''
        for para in paragraphs:
            fpara = textwrap.fill(para, DESC_WIDTH) + '\n'
            if para[:2] != DASH_BULLET:
                fpara += '\n'
            out_text += fpara
        desc = ''.join(out_text)

        full_text = f'{text} ({option}):\n{desc}'

        self.desc.config(state=tk.NORMAL)
        self.desc.delete('1.0', tk.END)
        self.desc.insert('1.0', full_text)
        self.desc.config(state=tk.DISABLED)


    def _get_config_value(self, param):
        """Get the value from the configuration, if it's not there
        use the constructor default."""

        value = self._get_gc_value(self.loaded_config,
                                   param.cspec,
                                   param.option)
        if value is None:
            value = self._get_construct_default(param.vtype,
                                                param.cspec,
                                                param.option)
        return value


    @staticmethod
    def _get_construct_default(vtype, cspec, option):
        """The defaults in the parameter table yield a playable game,
        they are not the actual construction defaults.
        Return the construction default."""

        rval = False

        if cspec == GI_TAG:
            rval = gi.GameInfo.get_default(option)

        elif cspec == SCR_TAG:
            rval = ai_player.ScoreParams.get_default(option)

        elif cspec == AI_TAG:
            rval = AI_PARAM_DEFAULTS[option]

        elif option == ckey.ALGORITHM:
            rval = list(ALGORITHM_DICT.keys())[0]

        elif option == ckey.DIFFICULTY:
            rval = 1

        elif vtype in (STR_TYPE, MSTR_TYPE):
            rval = ""

        elif vtype == INT_TYPE:
            rval =  0

        return rval


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


    def _get_boxes_config(self, param):
        """Return the number items for the list for name."""

        if param.option == ckey.UDIR_HOLES:
            boxes = self.params[ckey.HOLES].ui_default

        elif param.option in MAKE_LVARS:
            boxes = MAKE_LVARS[param.option]

        elif param.vtype == ILIST_TYPE:
            boxes = 4

        else:
            raise ValueError(f"Don't know list length for {param.option}.")

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
        """Create the tk variables described by the parameters file.

        multi strs - do not use tkvars and must be handled differently
        int vars - must use a string var and must be converted
        lists - are filled with a simple default here,
                _reset will give it any actual default
        blist - use MAKE_LVARS (want to make all of the udir_hole vars now"""

        for param in self.params.values():
            if param.vtype == MSTR_TYPE:
                continue

            if param.vtype in (STR_TYPE, INT_TYPE):
                self.tkvars[param.option] = tk.StringVar(self.master,
                                                         param.ui_default,
                                                         name=param.option)
            elif param.vtype == BOOL_TYPE:
                self.tkvars[param.option] = tk.BooleanVar(self.master,
                                                          param.ui_default,
                                                          name=param.option)
            elif param.vtype == BLIST_TYPE:
                boxes = MAKE_LVARS[param.option]
                self.tkvars[param.option] = \
                    [tk.BooleanVar(self.master, False,
                                   name=f'{param.option}_{i}')
                     for i in range(boxes)]

            elif param.vtype == ILIST_TYPE:
                boxes = self._get_boxes_config(param)
                self.tkvars[param.option] = \
                    [tk.StringVar(self.master, 0,
                                  name=f'{param.option}_{i}')
                     for i in range(boxes)]

            elif param.vtype in STRING_DICTS:
                _, inv_dict, enum_dict = STRING_DICTS[param.vtype]
                value = inv_dict[enum_dict[param.ui_default]]
                self.tkvars[param.option] = tk.StringVar(self.master,
                                                         value,
                                                         name=param.option)

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

        holes = stoi(self.tkvars[ckey.HOLES].get())

        if holes > MAX_HOLES:
            print('value too big.')
            return

        widgets = self.udir_frame.winfo_children()
        prev_holes = len(widgets)

        for idx in range(holes, prev_holes):
            widgets[idx].destroy()

        for idx in range(prev_holes + 1, holes + 1):
            tk.Checkbutton(self.udir_frame, text=str(idx),
                           variable=self.tkvars[ckey.UDIR_HOLES][idx - 1]
                           ).pack(side=tk.LEFT)

    def _make_text_entry(self, frame, param):
        """Make a text box entry with scroll bar."""

        tframe = tk.LabelFrame(frame, text=param.text, labelanchor='nw')
        tframe.grid(row=param.row, column=param.col, columnspan=2, rowspan=2)

        text_box = tk.Text(tframe, width=40, height=8)
        self.tktexts[param.option] = text_box

        scroll = tk.Scrollbar(tframe)
        text_box.configure(yscrollcommand=scroll.set)
        text_box.pack(side=tk.LEFT)

        scroll.config(command=text_box.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tframe.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_entry(self, frame, param):
        """Make a single line string entry."""

        length = 5 if param.vtype == INT_TYPE else 20

        lbl = tk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        if param.vtype == INT_TYPE:
            ent = tk.Entry(frame,  width=length,
                           textvariable=self.tkvars[param.option],
                           validate=tk.ALL,
                           validatecommand=(INT_VALID_CMD, '%P'))
        else:
            ent = tk.Entry(frame,  width=length,
                           textvariable=self.tkvars[param.option])

        ent.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self._update_desc, param.option))
        ent.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_checkbox(self, frame, param):
        """Make a labeled checkbox."""

        lbl = tk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        box = tk.Checkbutton(frame, variable=self.tkvars[param.option])
        box.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self._update_desc, param.option))
        box.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_checkbox_list(self, frame, param):
        """Make a list of checkboxes."""

        lbl = tk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        boxes = self._get_boxes_config(param)
        boxes_fr = tk.Frame(frame)
        boxes_fr.grid(row=param.row, column=param.col + 1,
                      columnspan=3, sticky=tk.W)

        if param.option == ckey.UDIR_HOLES:
            self.udir_frame = boxes_fr

        add_in = 1 if param.option == ckey.CAPT_ON else 0
        for nbr in range(boxes):
            tk.Checkbutton(boxes_fr, text=str(nbr + add_in),
                           variable=self.tkvars[param.option][nbr]
                           ).pack(side=tk.LEFT)

        lbl.bind('<Enter>', ft.partial(self._update_desc, param.option))
        boxes_fr.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_entry_list(self, frame, param):
        """Make a list of entries."""

        lbl = tk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        boxes = self._get_boxes_config(param)
        eframe = tk.Frame(frame)
        eframe.grid(row=param.row, column=param.col + 1,
                    columnspan=2, sticky=tk.W)

        if param.option == ckey.UDIR_HOLES:
            self.udir_frame = eframe

        for nbr in range(boxes):
            tk.Entry(eframe, width=5,
                     textvariable=self.tkvars[param.option][nbr],
                     validate=tk.ALL,
                     validatecommand=(INT_VALID_CMD, '%P')
                     ).pack(side=tk.LEFT)

        eframe.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self._update_desc, param.option))
        eframe.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_option_list(self, frame, param):
        """Make an option list corresponding to the enum type."""

        values = list(STRING_DICTS[param.vtype].str_dict.keys())

        lbl = tk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        opmenu = tk.OptionMenu(frame, self.tkvars[param.option], *values)
        opmenu.config(width=2 + max(len(str(val)) for val in values))
        opmenu.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self._update_desc, param.option))
        opmenu.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_ui_param(self, frame, param):
        """Make the ui elements for a single parameter."""

        if param.vtype == MSTR_TYPE:
            self._make_text_entry(frame, param)

        elif param.vtype in (STR_TYPE, INT_TYPE):
            self._make_entry(frame, param)

        elif param.vtype == BOOL_TYPE:
            self._make_checkbox(frame, param)

        elif param.vtype == BLIST_TYPE:
            self._make_checkbox_list(frame, param)

        elif param.vtype == ILIST_TYPE:
            self._make_entry_list(frame, param)

        elif param.vtype in STRING_DICTS:
            self._make_option_list(frame, param)


    def _make_ui_elements(self):
        """Make the UI elements corresponding to the parameter table.
        Make them in order to set 'tab' (selection) order is nice.
        Odd that OptionMenus are not in the tab order."""

        for tname, tab in self.tabs.items():
            tab_params = sorted(
                [p for p in self.params.values() if p.tab == tname],
                key = lambda p: (p.col, p.row))

            for param in tab_params:
                self._make_ui_param(tab, param)


    def _fill_tk_list(self, param, value):
        """Set the values of a list of tkvariables."""

        if not isinstance(value, list):
            print(type(value))
            raise ValueError(
                f"Don't know how to fill {param.option} from {value}.")

        if param.vtype == BLIST_TYPE:
            for var in self.tkvars[param.option]:
                var.set(False)
            sub_out = 1 if param.option == ckey.CAPT_ON else 0
            for val in value:
                self.tkvars[param.option][val - sub_out].set(True)

        else:
            for var in self.tkvars[param.option]:
                var.set('0')
            for idx, val in enumerate(value):
                self.tkvars[param.option][idx].set(str(val))


    def _fill_tk_from_config(self):
        """Set the tk vars (display vars) from the game_config
        dict."""

        for param  in self.params.values():
            value = self._get_config_value(param)

            if param.vtype == MSTR_TYPE:
                self.tktexts[param.option].delete('1.0', tk.END)
                self.tktexts[param.option].insert('1.0', value)

            elif param.vtype in (STR_TYPE, BOOL_TYPE, INT_TYPE):
                self.tkvars[param.option].set(value)

            elif param.vtype == BLIST_TYPE:
                self._fill_tk_list(param, value)

            elif param.vtype == ILIST_TYPE:
                self._fill_tk_list(param, value)

            elif param.vtype in STRING_DICTS:
                inv_dict = STRING_DICTS[param.vtype].int_dict
                self.tkvars[param.option].set(inv_dict[value])


    def _make_config_from_tk(self):
        """Get the values from the tkvars and set them into
        the a game_config dict."""

        self.game_config = {}

        for param in self.params.values():

            if param.vtype == MSTR_TYPE:
                value = self.tktexts[param.option].get('1.0', tk.END)

            elif param.vtype in (STR_TYPE, BOOL_TYPE):
                value = self.tkvars[param.option].get()

            elif param.vtype == INT_TYPE:
                value = stoi(self.tkvars[param.option].get())

            elif param.vtype == BLIST_TYPE:
                add_in = 1 if param.option == ckey.CAPT_ON else 0
                value = [nbr + add_in
                         for nbr, var in enumerate(self.tkvars[param.option])
                         if var.get()]

            elif param.vtype == ILIST_TYPE:
                value = [int(var.get())
                         for nbr, var in enumerate(self.tkvars[param.option])]

            elif param.vtype in STRING_DICTS:
                str_dict = STRING_DICTS[param.vtype].str_dict
                value = self.tkvars[param.option].get()
                value = str_dict[value]

            self._set_gc_value(self.game_config,
                               param.cspec, param.option, value)

        print(self.game_config)


    def _prepare_game(self):
        """Build the two game variables: constants and info
        and then build the game.
        This function should be wrapped with a try because
        exceptions/warnings might be raised."""

        self._make_config_from_tk()
        game_class = self.game_config[ckey.GAME_CLASS]
        gclass = GAME_CLASSES[game_class]

        consts = gc.GameConsts(**self.game_config[ckey.GAME_CONSTANTS])
        info = gi.GameInfo(nbr_holes=consts.holes,
                           rules=gclass.rules,
                           **self.game_config[ckey.GAME_INFO])

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
            self.loaded_config = man_config.read_game(filename)
        except ValueError as error:
            tk.messagebox.showerror('JSON File Error', error)
            return

        self._fill_tk_from_config()
        self._test()


    def _save(self):
        """Save params to file.
        Preserve any tags/comments that were in a loaded config."""

        self._make_config_from_tk()
        if self.loaded_config:
            for tag in self.loaded_config.keys():
                if tag not in self.game_config:
                    self.game_config[tag] = self.loaded_config[tag]

        if not self.filename:
            self.filename = self.game_config[ckey.GAME_INFO][ckey.NAME] \
                + '.txt'

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
            json.dump(self.game_config, file, indent=3)


    def _set_frame_active(self, frame, new_state):
        """Activate or deactivate wigets, recursing through frames."""

        for child in frame.winfo_children():

            if isinstance(child, (tk.Frame, tk.LabelFrame)):
                self._set_frame_active(child, new_state)

            elif isinstance(child, tk.Scrollbar):
                pass

            elif isinstance(child, tk.Text):
                tstate = new_state if new_state == DISABLED else NORMAL
                child.configure(state=tstate)

            else:
                child.configure(state=new_state)


    def _set_active(self, activate):
        """Activate or deactivate main window wingets."""

        new_state = NORMAL if activate else DISABLED

        for tab in self.tabs.values():
            self._set_frame_active(tab, new_state)


    def _play(self):
        """Create and play the game. deactivate param ui and block
        while the game is being played. reactivate when the game
        is exited."""

        self._test()
        if not self.game:
            return

        game_ui = mancala_ui.MancalaUI(self.game,
                                       self.game_config[ckey.PLAYER],
                                       self.master)
        self._set_active(False)
        game_ui.wait_window()
        self._set_active(True)


    def _reset(self):
        """Reset to ui_defaults; clear loaded config dictionary.

        Call this at initialization to fill the text boxes which don't
        have preinitialized variables."""

        self.loaded_config = None

        for param in self.params.values():

            if param.vtype == MSTR_TYPE:
                self.tktexts[param.option].delete('1.0', tk.END)
                self.tktexts[param.option].insert('1.0', param.ui_default)

            elif param.vtype in STRING_DICTS:
                _, inv_dict, enum_dict = STRING_DICTS[param.vtype]
                value = inv_dict[enum_dict[param.ui_default]]
                self.tkvars[param.option].set(value)

            elif param.vtype == BLIST_TYPE:
                for var in self.tkvars[param.option]:
                    var.set(False)

            elif param.vtype == ILIST_TYPE:
                default = param.ui_default
                if (default
                        and isinstance(default, list)
                        and len(default) == self._get_boxes_config(param)):

                    for var, val in zip(self.tkvars[param.option], default):
                        var.set(val)

            else:
                self.tkvars[param.option].set(param.ui_default)


# %%  main

if __name__ == '__main__':

    ROOT = tk.Tk()
    INT_VALID_CMD = ROOT.register(int_validate)

    man_games = MancalaGames(ROOT)
    man_games.mainloop()
