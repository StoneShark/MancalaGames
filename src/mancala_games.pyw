# -*- coding: utf-8 -*-
"""Create a window that collects the mancala parameters
and then plays the game. Saving and loading parameter
sets to files is supported.

The file game_info.txt drives much of what happens here.

Labels can be included in the table:
    - the option must be unique, as it is used as a key
      for the param dict
    - the order and ui_default fields must be 0
      to keep read_csv interpretting the col as ints

Created on Thu Mar 30 13:43:39 2023
@author: Ann"""


# %% import

import functools as ft
import textwrap
import traceback
import tkinter as tk
from tkinter import ttk
import warnings
import webbrowser

import ai_player
import cfg_keys as ckey
import game_constants as gc
import game_interface as gi
import mancala_ui
import man_config
import man_path
import mg_config
import param_consts as pc
import version

from game_classes import GAME_CLASSES


# %%  Constants

# how many variables to make for lists
# if the option for a 'list[int]' isn't here, 4 variables will be made
MAKE_LVARS = {ckey.CAPT_ON: 6,
              ckey.UDIR_HOLES: gc.MAX_HOLES + 1}

DESC_WIDTH = 60
DASH_BULLET = '- '

# these are the expected tabs, put them in this order (add any extras)
PARAM_TABS = ('Game', 'Dynamics', 'Sow', 'Capture', 'Player')

SKIP_TAB = 'skip'

WTITLE = 'Mancala Options'


OPTIONS = 0
PARAMS = 1
GAMES = 2
ABOUT = 4


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


# %%  game params UI


class MancalaGames(tk.Frame):
    """Main interface to select game parameters, save & load games,
    and play Mancala games."""

    def __init__(self, master):

        self.master = master
        self.tkvars = {}
        self.tktexts = {}
        self.udir_frame = None
        self.param_changed = False
        self.tabs = {}
        self.but_frame = None
        self.desc = None
        self.prev_option = None
        self.menubar = None

        self.params = man_config.ParamData()
        self.config = mg_config.GameConfig(self.master, self.params)
        self.game = None

        super().__init__(self.master)
        self.master.title(WTITLE)
        self.master.resizable(False, False)
        self.master.wm_geometry('+100+100')
        self.pack()

        self.master.report_callback_exception = self._exception_callback
        warnings.showwarning = self._warning
        warnings.simplefilter('always', UserWarning)

        self._create_menus()
        self._add_commands_ui()
        self._add_tabs()
        self._create_desc_pane()
        self._make_tkvars()
        self._make_ui_elements()
        self._reset()


    def destroy(self):
        """Remove the traces from the tk variables.
        Don't change the name, we're overriding Frame method."""

        self.config.edited |= \
            any(field.edit_modified() for field in self.tktexts.values())
        if self.config.check_save_cancel():
            return

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


    def _help(self, what=OPTIONS):
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


    def _update_title(self):
        """Update the window title with the filename and
        edited status."""

        self.master.title((self.config.filename or WTITLE)
                          + ('*' if self.config.edited else ''))


    def _create_menus(self):
        """Create the game control menus."""

        self.master.option_add('*tearOff', False)

        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        gamemenu = tk.Menu(self.menubar)
        gamemenu.add_command(label='Load...', command=self._load)
        gamemenu.add_command(label='Save', command=self._save)
        gamemenu.add_command(label='Save As...',
                             command=ft.partial(self._save, True))
        gamemenu.add_separator()
        gamemenu.add_command(label='Play', command=self._play)
        gamemenu.add_command(label='Test', command=self._test)
        self.menubar.add_cascade(label='Game', menu=gamemenu)

        mguimenu = tk.Menu(self.menubar)
        mguimenu.add_command(label='Set UI Defaults', command=self._reset)
        mguimenu.add_command(label='Set Defaults', command=self._reset_const)
        self.menubar.add_cascade(label='Controls', menu=mguimenu)

        helpmenu = tk.Menu(self.menubar)
        helpmenu.add_command(label='Help...',
                             command=ft.partial(self._help, OPTIONS))
        helpmenu.add_command(label='Parameters...',
                             command=ft.partial(self._help, PARAMS))
        helpmenu.add_command(label='Games...',
                             command=ft.partial(self._help, GAMES))
        helpmenu.add_separator()
        helpmenu.add_command(label='About...',
                             command=ft.partial(self._help, ABOUT))
        self.menubar.add_cascade(label='Help', menu=helpmenu)


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


    def _add_tabs(self):
        """Determine what tabs are needed and add them."""

        tab_set = set(r.tab for r in self.params.values())
        extra_tabs = tab_set - set(PARAM_TABS)
        tabs = PARAM_TABS + tuple(extra_tabs)

        tab_control = ttk.Notebook(self)
        for tab_name in tabs:

            tab = ttk.Frame(tab_control, padding=3)
            self.tabs[tab_name] = tab
            tab_control.add(tab, text=tab_name, padding=5)
        tab_control.pack(expand=1, fill=tk.BOTH)


    def _create_desc_pane(self):
        """Build the label desc pane."""

        dframe = tk.LabelFrame(self, text='Param Description',
                               labelanchor='nw')
        dframe.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        self.desc = tk.Text(dframe, width=DESC_WIDTH, height=12)

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


    def _get_boxes_config(self, param):
        """Return the number items for the list for name."""

        if param.option == ckey.UDIR_HOLES:
            boxes = self.params[ckey.HOLES].ui_default

        elif param.option in MAKE_LVARS:
            boxes = MAKE_LVARS[param.option]

        elif param.vtype == pc.ILIST_TYPE:
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
            if param.vtype in (pc.MSTR_TYPE, pc.LABEL_TYPE):
                continue

            if param.vtype in (pc.STR_TYPE, pc.INT_TYPE):
                self.tkvars[param.option] = tk.StringVar(self.master,
                                                         param.ui_default,
                                                         name=param.option)
            elif param.vtype == pc.BOOL_TYPE:
                self.tkvars[param.option] = tk.BooleanVar(self.master,
                                                          param.ui_default,
                                                          name=param.option)
            elif param.vtype == pc.BLIST_TYPE:
                boxes = MAKE_LVARS[param.option]
                self.tkvars[param.option] = \
                    [tk.BooleanVar(self.master, False,
                                   name=f'{param.option}_{i}')
                     for i in range(boxes)]

            elif param.vtype == pc.ILIST_TYPE:
                boxes = self._get_boxes_config(param)
                self.tkvars[param.option] = \
                    [tk.StringVar(self.master, 0,
                                  name=f'{param.option}_{i}')
                     for i in range(boxes)]

            elif param.vtype in pc.STRING_DICTS:
                _, inv_dict, enum_dict = pc.STRING_DICTS[param.vtype]
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
        self.config.edited = True
        self._update_title()

        if var == ckey.HOLES:
            self._resize_udirs()


    def _resize_udirs(self):
        """Change the number of the checkboxes on the screen.
        All the variables were built with the tkvars.
        Destroy any extra widgets or make any required new ones."""

        holes = stoi(self.tkvars[ckey.HOLES].get())

        if holes > gc.MAX_HOLES:
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
        tframe.grid(row=param.row, column=param.col, columnspan=4,
                    sticky='nsew')

        text_box = tk.Text(tframe, width=50, height=12)
        self.tktexts[param.option] = text_box

        scroll = tk.Scrollbar(tframe)
        text_box.configure(yscrollcommand=scroll.set)
        text_box.pack(side=tk.LEFT, expand=True, fill='both')

        scroll.config(command=text_box.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tframe.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_entry(self, frame, param):
        """Make a single line string entry."""

        length = 5 if param.vtype == pc.INT_TYPE else 30

        lbl = tk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        if param.vtype == pc.INT_TYPE:
            ent = tk.Entry(frame, width=length,
                           textvariable=self.tkvars[param.option],
                           validate=tk.ALL,
                           validatecommand=(INT_VALID_CMD, '%P'))
        else:
            ent = tk.Entry(frame, width=length,
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
        if param.option == ckey.UDIR_HOLES:
            boxes_fr.grid(row=param.row, column=param.col + 1,
                          columnspan=3, sticky=tk.W)
        else:
            boxes_fr.grid(row=param.row, column=param.col + 1,
                          sticky=tk.W)

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
        eframe.grid(row=param.row, column=param.col, sticky=tk.W)

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

        values = list(pc.STRING_DICTS[param.vtype].str_dict.keys())

        lbl = tk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col,sticky=tk.E)

        opmenu = tk.OptionMenu(frame, self.tkvars[param.option], *values)
        opmenu.config(width=2 + max(len(str(val)) for val in values))
        opmenu.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self._update_desc, param.option))
        opmenu.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_label_row(self, frame, param):
        """Make label row spanning two columns."""
        _ = self

        lbl = tk.Label(frame, text=param.text, bg='darkgrey')
        lbl.grid(row=param.row, column=param.col, columnspan=2,
                 padx=4, sticky='ew')

        # lbl.bind('<Enter>', ft.partial(self._update_desc, param.option))


    def _make_ui_param(self, frame, param):
        """Make the ui elements for a single parameter."""

        if param.vtype == pc.MSTR_TYPE:
            self._make_text_entry(frame, param)

        elif param.vtype in (pc.STR_TYPE, pc.INT_TYPE):
            self._make_entry(frame, param)

        elif param.vtype == pc.BOOL_TYPE:
            self._make_checkbox(frame, param)

        elif param.vtype == pc.BLIST_TYPE:
            self._make_checkbox_list(frame, param)

        elif param.vtype == pc.ILIST_TYPE:
            self._make_entry_list(frame, param)

        elif param.vtype in pc.STRING_DICTS:
            self._make_option_list(frame, param)

        elif param.vtype == pc.LABEL_TYPE:
            self._make_label_row(frame, param)


    def _make_ui_elements(self):
        """Make the UI elements corresponding to the parameter table.
        Make them in order to set 'tab' (selection) order is nice.
        Odd that OptionMenus are not in the tab order."""

        for tname, tab in self.tabs.items():
            tab_params = sorted(
                [p for p in self.params.values() if p.tab == tname],
                key=lambda p: (p.col, p.row))

            for param in tab_params:
                self._make_ui_param(tab, param)

        for tab in self.tabs.values():
            tab.grid_rowconfigure('all', weight=1)
            tab.grid_columnconfigure('all', weight=1)


    def _fill_tk_list(self, param, value):
        """Set the values of a list of tkvariables."""

        if not isinstance(value, list):
            raise ValueError(
                f"Don't know how to fill {param.option} from {value}.")

        if param.vtype == pc.BLIST_TYPE:
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

        for param in self.params.values():
            value = man_config.get_config_value(
                self.config.loaded_config,
                param.cspec, param.option, param.vtype)

            if param.vtype == pc.MSTR_TYPE:
                self.tktexts[param.option].delete('1.0', tk.END)
                self.tktexts[param.option].insert('1.0', value)

            elif param.vtype in (pc.STR_TYPE, pc.BOOL_TYPE, pc.INT_TYPE):
                self.tkvars[param.option].set(value)

            elif param.vtype == pc.BLIST_TYPE:
                self._fill_tk_list(param, value)

            elif param.vtype == pc.ILIST_TYPE:
                self._fill_tk_list(param, value)

            elif param.vtype in pc.STRING_DICTS:
                inv_dict = pc.STRING_DICTS[param.vtype].int_dict
                self.tkvars[param.option].set(inv_dict[value])


    def _make_config_from_tk(self):
        """Get the values from the tkvars and set them into
        the a game_config dict."""

        self.config.game_config = {}

        for param in sorted(self.params.values(), key=lambda v: v.order):

            if param.vtype == pc.LABEL_TYPE:
                continue

            if param.vtype == pc.MSTR_TYPE:
                value = self.tktexts[param.option].get('1.0', tk.END)

            elif param.vtype in (pc.STR_TYPE, pc.BOOL_TYPE):
                value = self.tkvars[param.option].get()

            elif param.vtype == pc.INT_TYPE:
                value = stoi(self.tkvars[param.option].get())

            elif param.vtype == pc.BLIST_TYPE:
                holes = len(self.tkvars[param.option])
                if param.option == ckey.UDIR_HOLES:
                    holes = stoi(self.tkvars[ckey.HOLES].get())

                add_in = 1 if param.option == ckey.CAPT_ON else 0
                value = [nbr + add_in
                         for nbr, var in enumerate(self.tkvars[param.option])
                         if var.get() and nbr < holes]

            elif param.vtype == pc.ILIST_TYPE:
                value = [int(var.get()) for var in self.tkvars[param.option]]

            elif param.vtype in pc.STRING_DICTS:
                str_dict = pc.STRING_DICTS[param.vtype].str_dict
                value = self.tkvars[param.option].get()
                value = str_dict[value]

            man_config.set_config_value(
                self.config.game_config, param.cspec, param.option, value)


    def _prepare_game(self):
        """Build the two game variables: constants and info
        and then build the game.
        This function should be wrapped with a try because
        exceptions/warnings might be raised."""

        self._make_config_from_tk()
        game_class = self.config.game_config[ckey.GAME_CLASS]
        gclass = GAME_CLASSES[game_class]

        consts = gc.GameConsts(**self.config.game_config[ckey.GAME_CONSTANTS])
        info = gi.GameInfo(nbr_holes=consts.holes,
                           rules=gclass.rules,
                           **self.config.game_config[ckey.GAME_INFO])

        self.game = gclass(consts, info)
        ai_player.AiPlayer(self.game, self.config.game_config[ckey.PLAYER])
        self.param_changed = False


    def _test(self):
        """Try to build the game params and game,
        trap any exceptions, report to user."""

        self.param_changed |= \
            any(field.edit_modified() for field in self.tktexts.values())
        if self.game and not self.param_changed:
            return

        self._update_title()

        try:
            self._prepare_game()

        except (gc.GameConstsError, gi.GameInfoError, NotImplementedError
                ) as error:
            message = error.__class__.__name__ + ':  ' + str(error)
            tk.messagebox.showerror('Parameter Error', message)

            self.game = None


    def _load(self):
        """Load params from file.
        Translate the json string. Convert non-primitive types.
        Build game_consts and game_info."""

        self.config.edited |= \
            any(field.edit_modified() for field in self.tktexts.values())
        if not self.config.load():
            return

        self._fill_tk_from_config()
        self._test()
        self.config.edited = False

        self._update_title()
        for field in self.tktexts.values():
            field.edit_modified(False)


    def _save(self, askfile=False):
        """Save params to file."""

        self.config.init_fname(self.tkvars[ckey.NAME].get())
        self._make_config_from_tk()
        self.config.save(askfile)
        self._update_title()
        for field in self.tktexts.values():
            field.edit_modified(False)


    def _set_frame_active(self, frame, new_state):
        """Activate or deactivate wigets, recursing through frames."""

        for child in frame.winfo_children():

            if isinstance(child, (tk.Frame, tk.LabelFrame)):
                self._set_frame_active(child, new_state)

            elif isinstance(child, tk.Scrollbar):
                pass

            elif isinstance(child, tk.Text):
                tstate = new_state if new_state == tk.DISABLED else tk.NORMAL
                child.configure(state=tstate)

            else:
                child.configure(state=new_state)


    def _set_active(self, activate):
        """Activate or deactivate main window wingets."""

        new_state = tk.NORMAL if activate else tk.DISABLED

        for tab in self.tabs.values():
            self._set_frame_active(tab, new_state)
        self._set_frame_active(self.but_frame, new_state)

        self.menubar.entryconfig('Game', state=new_state)
        self.menubar.entryconfig('Controls', state=new_state)


    def _play(self):
        """Create and play the game. deactivate param ui and block
        while the game is being played. reactivate when the game
        is exited."""

        self._test()
        if not self.game:
            return

        game_ui = mancala_ui.MancalaUI(self.game,
                                       self.config.game_config[ckey.PLAYER],
                                       self.master)
        self._set_active(False)
        game_ui.wait_window()
        self._set_active(True)


    def _reset_edited(self):
        """Clear the edited flags and config data."""

        self.config.reset()
        for field in self.tktexts.values():
            field.edit_modified(False)
        self._update_title()


    def _reset(self):
        """Reset to ui_defaults; clear loaded config dictionary.

        Call this at initialization to fill the text boxes which don't
        have preinitialized variables."""

        for param in self.params.values():

            if param.vtype == pc.MSTR_TYPE:
                self.tktexts[param.option].delete('1.0', tk.END)
                self.tktexts[param.option].insert('1.0', param.ui_default)

            elif param.vtype in pc.STRING_DICTS:
                _, inv_dict, enum_dict = pc.STRING_DICTS[param.vtype]
                value = inv_dict[enum_dict[param.ui_default]]
                self.tkvars[param.option].set(value)

            elif param.vtype == pc.BLIST_TYPE:
                for var in self.tkvars[param.option]:
                    var.set(False)

            elif param.vtype == pc.ILIST_TYPE:
                default = param.ui_default
                if (default
                        and isinstance(default, list)
                        and len(default) == self._get_boxes_config(param)):

                    for var, val in zip(self.tkvars[param.option], default):
                        var.set(val)

            elif param.vtype != pc.LABEL_TYPE:
                self.tkvars[param.option].set(param.ui_default)

        self._reset_edited()


    def _reset_const(self):
        """Reset to defaults; clear loaded config dictionary."""

        for param in self.params.values():

            default = man_config.get_construct_default(
                        param.vtype, param.cspec, param.option)

            if param.vtype == pc.MSTR_TYPE:
                self.tktexts[param.option].delete('1.0', tk.END)
                self.tktexts[param.option].insert('1.0', default)

            elif param.vtype in pc.STRING_DICTS:
                inv_dict = pc.STRING_DICTS[param.vtype][1]
                value = inv_dict[default]
                self.tkvars[param.option].set(value)

            elif param.vtype == pc.BLIST_TYPE:
                for var in self.tkvars[param.option]:
                    var.set(False)

            elif param.vtype == pc.ILIST_TYPE:
                if (default
                        and isinstance(default, list)
                        and len(default) == self._get_boxes_config(param)):

                    for var, val in zip(self.tkvars[param.option], default):
                        var.set(val)

            elif param.vtype != pc.LABEL_TYPE:
                self.tkvars[param.option].set(default)

        self._reset_edited()


# %%  main

if __name__ == '__main__':

    ROOT = tk.Tk()
    INT_VALID_CMD = ROOT.register(int_validate)

    man_games = MancalaGames(ROOT)
    man_games.mainloop()
