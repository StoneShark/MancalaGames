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

import ai_player
import cfg_keys as ckey
import game_constants as gconsts
import game_interface as gi
import mancala_ui
import man_config
import mg_config
import param_consts as pc
import param_mixin
import ui_utils


# %%  Constants

DESC_WIDTH = 60
DASH_BULLET = '- '

# these are the expected tabs, put them in this order (add any extras)
PARAM_TABS = ('Game', 'Dynamics', 'Sow', 'Capture', 'Player')

SKIP_TAB = 'skip'

WTITLE = 'Mancala Game Editor'


# %%  game params UI


class MancalaGames(param_mixin.ParamMixin, ttk.Frame):
    """Main interface to select game parameters, save & load games,
    and play Mancala games."""

    def __init__(self, master):

        self.master = master
        self.tkvars = {}
        self.tktexts = {}
        self.udir_frame = None
        self.tabs = {}
        self.but_frame = None
        self.desc = None
        self.prev_option = None
        self.menubar = None
        self.bind_ids = None
        self.quitting = False

        self.params = man_config.ParamData()
        self.config = mg_config.GameConfig(self.master, self.params)
        self.game = None
        self.ai_player = None

        super().__init__(self.master)
        self.master.title(WTITLE)
        self.master.resizable(False, False)
        self.master.wm_geometry('+100+100')
        self.master.protocol("WM_DELETE_WINDOW", self._check_destroy)
        self.pack()

        self.master.report_callback_exception = self._exception_callback
        warnings.showwarning = ft.partial(self._warning, self)
        warnings.simplefilter('always', UserWarning)

        ui_utils.setup_styles(master)
        self._create_menus()
        self._key_bindings()
        self._add_commands_ui()
        self._add_tabs()
        self._create_desc_pane()
        self._make_tkvars()
        self._make_ui_elements()
        self._reset(check_save=False)

        man_config.check_disable_animator()


    def _check_save_cancel(self):
        """Check to see if a save is needed, if so then do
        or not at user choice.
        If cancel, then return True."""

        self.config.edited |= \
            any(field.edit_modified() for field in self.tktexts.values())

        if self.config.edited:
            self.config.init_fname(self.tkvars[ckey.NAME].get())
            self._make_config_from_tk()

        if self.config.check_save_cancel():
            return True

        return False


    def _check_destroy(self):
        """On destory window, do our own clean up.
        Bind to WM_DELETE_WINDOW instead of overriding destory,
        so that the cancel operation will work.

        Check for save, allowing cancel.
        Set the quiting flag so we don't try to reactivate
        when wait_window of game_ui returns.
        Remove the traces from the tk variables.
        Call destroy on self."""

        if self._check_save_cancel():
            return

        self.quitting = True

        for var in self.tkvars.values():
            if isinstance(var, list):
                for cvar in var:
                    cvar.trace_remove(*cvar.trace_info()[0])
            else:
                var.trace_remove(*var.trace_info()[0])

        self.master.destroy()


    @staticmethod
    def _exception_callback(*args):
        """Support debugging by printing the play_log and the traceback."""

        traceback.print_exception(args[0], args[1], args[2])


    @staticmethod
    def _warning(parent, message, *_):
        """Notify user of warnings during parameter test."""

        ui_utils.showwarning(parent, 'Parameter Warning', str(message))


    def _update_title(self):
        """Update the window title with the filename and
        edited status."""

        self.master.title((self.config.filename or WTITLE)
                          + ('*' if self.config.edited else ''))


    def _create_menus(self):
        """Create the game control menus"""

        self.master.option_add('*tearOff', False)

        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        gamemenu = tk.Menu(self.menubar)
        gamemenu.add_command(label='Load...', command=self._load,
                             accelerator='Ctrl-l')
        gamemenu.add_command(label='Save', command=self._save,
                             accelerator='Ctrl-s')
        gamemenu.add_command(label='Save As...',
                             command=ft.partial(self._save, askfile=True),
                             accelerator='Ctrl-Shift-s')
        gamemenu.add_command(label='Revert', command=self._revert)
        gamemenu.add_separator()
        gamemenu.add_command(label='Play', command=self._play,
                             accelerator='Ctrl-p')
        gamemenu.add_command(label='Test', command=self._test,
                             accelerator='Ctrl-t')
        self.menubar.add_cascade(label='Game', menu=gamemenu)

        mguimenu = tk.Menu(self.menubar)
        mguimenu.add_command(label='Set UI Defaults', command=self._reset)
        mguimenu.add_command(label='Set Defaults', command=self._reset_const,
                             accelerator='Ctrl-n')
        self.menubar.add_cascade(label='Controls', menu=mguimenu)

        ui_utils.add_help_menu(self.menubar, self)


    def _key_bindings(self, active=True):
        """Bind or unbind the keys."""

        bindings = [('<Control-l>', self._load),
                    ('<Control-s>', self._save),
                    ('<Control-S>', ft.partial(self._save, askfile=True)),
                    ('<Control-p>', self._play),
                    ('<Control-t>', self._test),
                    ('<Control-n>', self._reset_const),
                    ]
        ui_utils.key_bindings(self, bindings, active)


    def _add_commands_ui(self):
        """Add buttons for commands."""

        self.but_frame = ttk.Frame(self.master, borderwidth=3)
        self.but_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        ttk.Button(self.but_frame, text='Test', command=self._test,
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(self.but_frame, text='Load', command=self._load
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(self.but_frame, text='Save', command=self._save
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(self.but_frame, text='Play', command=self._play
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

        dframe = ttk.LabelFrame(self, text='Param Description',
                               labelanchor='nw')
        dframe.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        self.desc = tk.Text(dframe, width=DESC_WIDTH, height=12)

        scroll = tk.Scrollbar(dframe)
        self.desc.configure(yscrollcommand=scroll.set)
        self.desc.pack(side=tk.LEFT)

        scroll.config(command=self.desc.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.desc.pack(expand=True, fill=tk.BOTH)


    def update_desc(self, option, event=None):
        """We've enter a new widget, update desc text.
        Don't let the user edit the description."""
        _ = event

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

        for param in self.params.values():
            if param.vtype in (pc.MSTR_TYPE, pc.LABEL_TYPE):
                continue

            self.pm_make_tkvar(param)

        # don't add the traces until all the variables are made
        self._add_watchers()


    def _tkvalue_changed(self, var, index, mode):
        """Called-back whenever any tkvar is changed."""

        _ = (index, mode)
        self.config.edited = True
        self._update_title()
        self.game = None

        if var == ckey.HOLES:
            self.pm_resize_udirs()


    def _make_ui_elements(self):
        """Make the UI elements corresponding to the parameter table.
        Make them in order to set 'tab' (selection) order is nice.
        Odd that OptionMenus are not in the tab order."""

        for tname, tab in self.tabs.items():
            tab_params = sorted(
                [p for p in self.params.values() if p.tab == tname],
                key=lambda p: (p.col, p.row))

            for param in tab_params:
                self.pm_make_ui_param(tab, param)

        for tab in self.tabs.values():
            tab.grid_rowconfigure('all', weight=1)
            tab.grid_columnconfigure('all', weight=1)


    def _fill_tk_from_config(self):
        """Set the tk vars (display vars) from the game_config
        dict."""

        for param in self.params.values():
            self.pm_copy_config_to_tk(param, self.config.loaded_config)


    def _make_config_from_tk(self):
        """Get the values from the tkvars and set them into
        the a game_config dict."""

        self.config.game_config = {}

        for param in sorted(self.params.values(), key=lambda v: v.order):

            if param.vtype == pc.LABEL_TYPE:
                continue

            self.pm_copy_tk_to_config(param, self.config.game_config)


    def _prepare_game(self):
        """Build the two game variables: constants and info
        and then build the game.
        This function should be wrapped with a try because
        exceptions/warnings might be raised."""

        self._make_config_from_tk()

        self.game = man_config.game_from_config(self.config.game_config)
        self.ai_player = ai_player.AiPlayer(self.game,
                                            self.config.game_config[ckey.PLAYER])


    def _test(self, _=None, *, positive=True):
        """Try to build the game params and game,
        trap any exceptions, report to user."""

        self.config.edited |= \
            any(field.edit_modified() for field in self.tktexts.values())
        if self.game and not self.config.edited and not positive:
            return

        self._update_title()

        try:
            self._prepare_game()

        except (gconsts.GameConstsError, gi.GameInfoError, NotImplementedError
                ) as error:
            message = error.__class__.__name__ + ':  ' + str(error)
            ui_utils.showerror(self, 'Parameter Error', message)

            self.game = None
            return

        if positive:
            ui_utils.showinfo(
                self,
                'Game Config',
                'No errors detected in the game configuration.')


    def _load(self, _=None):
        """Load params from file.
        Translate the json string. Convert non-primitive types.
        Build game_consts and game_info."""

        if self._check_save_cancel():
            return

        if not self.config.load():
            return

        self._load_update()


    def _load_update(self):
        """Update the UI with the loaded game."""

        self._fill_tk_from_config()
        self._test(positive=False)
        self.config.edited = False

        self._update_title()
        for field in self.tktexts.values():
            field.edit_modified(False)


    def _save(self, _=None, *, askfile=False):
        """Save params to file."""

        self.config.init_fname(self.tkvars[ckey.NAME].get())
        self._make_config_from_tk()
        self.config.save(askfile)
        self._update_title()
        for field in self.tktexts.values():
            field.edit_modified(False)


    def _revert(self):
        """Revert changes to a previously loaded game."""

        self.config.edited |= \
            any(field.edit_modified() for field in self.tktexts.values())

        if self.config.revert():
            self._load_update()


    def _set_frame_active(self, frame, new_state):
        """Activate or deactivate wigets, recursing through frames."""

        for child in frame.winfo_children():

            if isinstance(child, (ttk.Frame, ttk.LabelFrame)):
                self._set_frame_active(child, new_state)

            elif isinstance(child, tk.Scrollbar):
                pass

            elif isinstance(child, tk.Text):
                tstate = new_state if new_state == tk.DISABLED else tk.NORMAL
                child.configure(state=tstate)

            else:
                child.configure(state=new_state)


    def _set_active(self, activate):
        """Activate or deactivate main window widgets."""

        new_state = tk.NORMAL if activate else tk.DISABLED

        for tab in self.tabs.values():
            self._set_frame_active(tab, new_state)
        self._set_frame_active(self.but_frame, new_state)

        self.menubar.entryconfig('Game', state=new_state)
        self.menubar.entryconfig('Controls', state=new_state)

        self._key_bindings(activate)


    def _play(self, _=None):
        """Create and play the game. deactivate param ui and block
        while the game is being played. reactivate when the game
        is exited.

        If quitting is set, wait_window returned because we are
        quiting, so don't try to reactivate."""

        self._test(positive=False)
        if not self.game:
            return

        game_ui = mancala_ui.MancalaUI(self.game,
                                       self.config.game_config[ckey.PLAYER],
                                       player=self.ai_player,
                                       root_ui=self.master)
        self._set_active(False)
        game_ui.wait_window()

        if not self.quitting:
            self._set_active(True)


    def _reset_edited(self):
        """Clear the edited flags and config data."""

        self.config.reset()
        for field in self.tktexts.values():
            field.edit_modified(False)
        self._update_title()


    def _reset(self, check_save=True):
        """Reset to ui_defaults; clear loaded config dictionary.

        Call this at initialization to fill the text boxes which don't
        have preinitialized variables."""

        if check_save and self._check_save_cancel():
            return

        for param in self.params.values():
            self.pm_reset_ui_default(param)

        self._reset_edited()


    def _reset_const(self, _=None):
        """Reset to defaults; clear loaded config dictionary."""

        if self._check_save_cancel():
            return

        for param in self.params.values():
            self.pm_reset_const_default(param)

        self._reset_edited()


# %%  main

if __name__ == '__main__':

    ROOT = tk.Tk()
    param_mixin.register_int_validate(ROOT)

    man_games = MancalaGames(ROOT)
    man_games.mainloop()
