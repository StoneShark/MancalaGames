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
import json
import tkinter as tk
from tkinter import ttk

import ai_player
import animator
import cfg_keys as ckey
import format_msg
import mancala_ui
import man_config
import man_path
import mg_config
import param_consts as pc
import param_mixin
import ui_utils
import variants


# %%  Constants

DESC_WIDTH = 72

# these are the expected tabs, put them in this order (add any extras)
PARAM_TABS = ('Game', 'Dynamics', 'Sow', 'Capture',
              'Variants', 'Tags', 'Player')

SKIP_TAB = 'skip'

WTITLE = 'Mancala Games Editor'

NL = '\n'

# prefix for the tk variable names
# names must be distinct from variants popup
PREFIX = 'edit_'
HOLES_VAR = PREFIX + ckey.HOLES

# %%  game params UI


class MancalaGamesEditor(param_mixin.ParamMixin, ttk.Frame):
    """Main interface to select game parameters, save & load games,
    and play Mancala games."""

    def __init__(self, master, chooser_class):

        self.master = master
        self.chooser_class = chooser_class
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

        param_mixin.register_int_validate(self.master)
        man_config.read_params_data(need_descs=True)
        self.config = mg_config.GameConfig(self.master)
        self.game = None
        self.ai_player = None

        super().__init__(self.master)
        self.master.title(WTITLE)
        self.master.resizable(False, True)
        self.master.protocol("WM_DELETE_WINDOW", self._check_destroy)
        self.pack(expand=True, fill=tk.BOTH)

        ui_utils.do_error_popups(self.master)

        ui_utils.setup_styles(master)
        self._create_menus()
        self._key_bindings()

        self._add_content_frames()
        self._add_commands_ui()

        self._make_tkvars()
        self._make_ui_elements()
        self._reset(check_save=False)

        man_config.check_disable_animator()


    def _check_save_cancel(self):
        """Check to see if a save is needed, if so then do
        or not at user choice.
        Any parse errors in variant parameters are ignored,
        the values are silently saved as strings.
        If cancel, then return True."""

        self.config.edited |= \
            any(field.edit_modified() for field in self.tktexts.values())

        if self.config.edited:
            self.config.init_fname(self.tkvars[ckey.NAME].get())
            self._make_config_from_tk(raise_excp=False)

        if self.config.check_save_cancel():
            return True

        return False


    def _cleanup(self):
        """Do the pre-destroy cleanup operations.

        Set the quiting flag so we don't try to reactivate
        when wait_window of game_ui returns.
        Remove the traces from the tk variables."""

        self.quitting = True

        for var in self.tkvars.values():
            if isinstance(var, list):
                for cvar in var:
                    cvar.trace_remove(*cvar.trace_info()[0])
            else:
                var.trace_remove(*var.trace_info()[0])


    def _check_destroy(self):
        """On destory window, do our own clean up.
        Bind to WM_DELETE_WINDOW instead of overriding destory,
        so that the cancel operation will work.

        Check for save, allowing cancel.
        Call cleanup.
        Call destroy on master."""

        if self._check_save_cancel():
            return

        self._cleanup()
        self.master.destroy()


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
        gamemenu.add_command(label='Play...', command=self._play,
                             accelerator='Ctrl-p')
        gamemenu.add_command(label='Test', command=self._test,
                             accelerator='Ctrl-t')

        gamemenu.add_separator()
        gamemenu.add_command(label='Launch Chooser...',
                             command=self._launch_chooser)
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

        self.but_frame = ttk.Frame(self, borderwidth=3)
        self.but_frame.grid(row=1, column=0, sticky=tk.EW)

        ttk.Button(self.but_frame, text='Test', command=self._test,
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(self.but_frame, text='Load', command=self._load
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(self.but_frame, text='Save', command=self._save
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(self.but_frame, text='Play', command=self._play
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X)


    def _add_content_frames(self):
        """Add the two content frames in a paned window to support
        the user chaning their relative sizes."""

        panes = ttk.PanedWindow(self, orient=tk.VERTICAL)
        panes.grid(row=0, column=0, sticky=tk.NSEW)

        frame = ttk.Frame(panes, relief=tk.SUNKEN, borderwidth=3)
        self._add_tabs(frame)
        panes.add(frame)

        frame = ttk.Frame(panes, relief=tk.SUNKEN, borderwidth=3)
        self._create_desc_pane(frame)
        panes.add(frame)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(tk.ALL, weight=1)


    def _add_tabs(self, frame):
        """Determine what tabs are needed and add them."""

        tab_set = set(r.tab for r in man_config.PARAMS.values())
        extra_tabs = tab_set - set(PARAM_TABS)
        tabs = PARAM_TABS + tuple(extra_tabs)

        tab_control = ttk.Notebook(frame)
        tab_control.pack(expand=True, fill=tk.BOTH)

        for tab_name in tabs:

            tab = ttk.Frame(tab_control, padding=3)
            self.tabs[tab_name] = tab
            tab_control.add(tab, text=tab_name, padding=5, sticky=tk.NSEW)


    def _create_desc_pane(self, frame):
        """Build the label desc pane."""

        dframe = ttk.LabelFrame(frame, text='Param Description',
                               labelanchor=tk.NW)
        dframe.pack(expand=True, fill=tk.BOTH)

        self.desc = tk.Text(dframe, width=DESC_WIDTH, height=8)
        scroll = tk.Scrollbar(dframe)
        self.desc.configure(yscrollcommand=scroll.set)
        self.desc.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scroll.config(command=self.desc.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.BOTH)


    def update_desc(self, option, event=None):
        """We've enter a new widget, update desc text.
        Don't let the user edit the description."""
        _ = event

        if self.prev_option == option:
            return
        self.prev_option = option

        text = man_config.PARAMS[option].text
        rdesc = man_config.PARAMS[option].description

        desc = ''.join(format_msg.build_paras(rdesc))
        full_text = f'{text} ({option}):\n\n{desc}'

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

        for param in man_config.PARAMS.values():
            if param.vtype in (pc.MSTR_TYPE, pc.LABEL_TYPE, pc.TEXTDICT):
                continue

            self.pm_make_tkvar(param, PREFIX)

        # don't add the traces until all the variables are made
        self._add_watchers()


    def _tkvalue_changed(self, var, index, mode):
        """Called-back whenever any tkvar is changed."""

        _ = (index, mode)
        self.config.edited = True
        self._update_title()
        self.game = None

        if var == HOLES_VAR:
            self.pm_resize_udirs()


    def _make_ui_elements(self):
        """Make the UI elements corresponding to the parameter table.
        Make them in order to set 'tab' (selection) order is nice.
        Odd that OptionMenus are not in the tab order."""

        for tname, tab in self.tabs.items():
            tab_params = sorted(
                [p for p in man_config.PARAMS.values() if p.tab == tname],
                 key=lambda p: (p.col, p.row))

            expand = set()
            for param in tab_params:
                if param.vtype in (pc.MSTR_TYPE, pc.TEXTDICT):
                    expand |= {param.row}

                self.pm_make_ui_param(tab, param)

            if expand:
                tab.grid_rowconfigure(list(expand), weight=1)
            tab.grid_columnconfigure(tk.ALL, weight=1)


    def _fill_tk_from_config(self):
        """Set the tk vars (display vars) from the game_config
        dict."""

        for param in man_config.PARAMS.values():
            self.pm_copy_config_to_tk(param, self.config.loaded_config)


    def _make_config_from_tk(self, raise_excp=True):
        """Get the values from the tkvars and set them into
        the a game_config dict."""

        self.config.game_config = {}

        for param in sorted(man_config.PARAMS.values(), key=lambda v: v.order):

            if param.vtype == pc.LABEL_TYPE:
                continue

            self.pm_copy_tk_to_config(param, self.config.game_config,
                                      raise_excp=raise_excp)


    def _prepare_game(self):
        """Build the two game variables: constants and info
        and then build the game.
        This function should be wrapped with a try because
        exceptions/warnings might be raised."""

        self._make_config_from_tk()

        self.game = man_config.game_from_config(self.config.game_config)
        variants.test_variation_config(self.config.game_config,
                                       no_var_error=False)
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

        with ui_utils.ReportError(self) as build_context:
            self._prepare_game()

        if build_context.error:
            self.game = None
            return

        if positive:
            ui_utils.showinfo(
                self,
                'Game Config',
                'No errors detected in the game configuration.')


    def load_game(self, gamename):
        """Load the specified game name, used when switching
        from the chooser."""

        filename = man_path.find_gamefile(gamename)
        if not filename:
            return

        if not self.config.load(filename):
            return

        self._load_update()


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


    def _check_jsons(self):
        """Check the Text dictionary entries to see if they can be
        parsed. If there is an error in the variation entries ask
        the user if they want to save anyway."""

        for key in (ckey.VARI_PARAMS, ckey.VARIANTS):

            text = self.tktexts[key].get('1.0', tk.END).strip()
            if not text:
                continue

            try:
                json.loads(text)

            except json.decoder.JSONDecodeError as error:

                message = [f"""JSON Encode Error in {key} it cannot be
                           converted to a proper dictionary:""",
                           str(error),
                           """Would you like to save the values
                           as strings?""",
                           """It cannot be used,
                           but will preserve your work."""]

                return  ui_utils.ask_popup(self,
                                           'JSON Encode Error', message,
                                           ui_utils.OKCANCEL)

        return True


    def _save(self, _=None, *, askfile=False):
        """Save params to file."""

        if not self._check_jsons():
            return

        self.config.init_fname(self.tkvars[ckey.NAME].get())
        self._make_config_from_tk(raise_excp=False)
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
        while the game is being played."""

        self._test(positive=False)
        if not self.game:
            return

        # if the game matches a saved file, allow variants to be used
        if self.config.edited or not self.config.filename:
            if hasattr(self.game, 'filename'):
                del self.game.filename
        else:
            self.game.filename = self.config.pathname

        mancala_ui.MancalaUI(self.game,
                             self.config.game_config[ckey.PLAYER],
                             player=self.ai_player,
                             root_ui=self.master,
                             pcleanup=self.reactivate_editor)
        self._set_active(False)


    def reactivate_editor(self):
        """Reactivate the editor controls."""

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

        for param in man_config.PARAMS.values():
            self.pm_reset_ui_default(param)

        self._reset_edited()


    def _reset_const(self, _=None):
        """Reset to defaults; clear loaded config dictionary."""

        if self._check_save_cancel():
            return

        for param in man_config.PARAMS.values():
            self.pm_reset_const_default(param)

        self._reset_edited()


    def _launch_chooser(self, _=None):
        """Delete ourself (but not the master) and create the game chooser."""

        message = ['Do you wish to switch to Game Chooser?',
                   'The editor will be closed.']
        do_it = ui_utils.ask_popup(self.master,
                                   'Swap to Game Chooser', message,
                                   ui_utils.YESNO)

        if not do_it or self._check_save_cancel():
            return

        gamename = None
        if self.config.loaded_config:
            gamename = self.config.loaded_config[ckey.GAME_INFO][ckey.NAME]

        self._cleanup()
        self.destroy()
        animator.reset()
        self._key_bindings(active=False)
        self.master.protocol('WM_DELETE_WINDOW', '')

        chooser = self.chooser_class(self.master, MancalaGamesEditor)
        if gamename:
            chooser.do_select(gamename)
