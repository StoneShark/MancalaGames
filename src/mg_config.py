# -*- coding: utf-8 -*-
"""Handling of the game configuration and file input / output.

Created on Tue Jan 28 11:07:30 2025
@author: Ann"""

import json
import os.path
import tkinter as tk
import tkinter.filedialog as tkfile

import cfg_keys as ckey
import man_config
import man_path


ALL_PARAMS = '_all_params.txt'


class GameConfig:
    """Encapsulate the file handling and game config dictionaries."""

    def __init__(self, master, params):

        self._master = master    # parent for dialog boxes
        self._params = params    # link to parameter dict

        self._dir = man_path.get_path('GameProps')
        self._known = False      # what this previously loaded or saved

        self.filename = None
        self.edited = False           # is there an edit that hasn't been saved
        self.loaded_config = None     # keep for persistent comment entries
        self.game_config = None       # constructed config for playing


    def reset(self):
        """Reset data to initial values"""

        self._dir = man_path.get_path('GameProps')
        self.filename = None
        self._known = False

        self.edited = False
        self.loaded_config = None
        self.game_config = None


    def init_fname(self, game_name):
        """If we don't have a filename yet,
        initialize it with the game name."""

        if not self.filename and game_name:
            self.filename = game_name.replace(' ', '_') + '.txt'


    def load(self):
        """Load the game configuration from a file.
        Set the working dir to the selected dir.
        json.JSONDecodeError is dervied from ValueError.

        Return False if there is an error in file.
        Return True if the file was successfully loaded."""

        filename = tkfile.askopenfilename(parent=self._master,
                                          title='Load Parameters',
                                          initialdir=self._dir)
        if not filename:
            return False

        self._dir, self.filename = os.path.split(filename)
        os.chdir(self._dir)

        return self._load_file()


    def _load_file(self):
        """Load from the saved filename."""

        try:
            self.loaded_config = man_config.read_game(self.filename)
        except ValueError as error:
            tk.messagebox.showerror('JSON File Error', error,
                                    parent=self._master)
            return False

        self.edited = False
        self._known = True
        return True


    def _del_defaults(self):
        """Delete most tags that have the default value.
        The help generator only lists the values kept in the file
        (it doesn't build the games), so some defaults are kept.

        Do the inclusion tests before we delete any keys.
        Game config can be written even if it is inconsistent or
        there are errors."""

        capt_keys = [ckey.CAPSAMEDIR, ckey.CAPT_MAX, ckey.CAPT_MIN,
                     ckey.CAPT_ON, ckey.CAPT_TYPE, ckey.EVENS]
        capts_config = any(self.game_config[ckey.GAME_INFO][key]
                           for key in capt_keys)

        rounds_config = self.game_config[ckey.GAME_INFO][ckey.ROUNDS]

        for param in self._params.values():

            if param.option == ckey.CAPT_SIDE and capts_config:
                # if captures, keep capt_side
                continue

            if param.option == ckey.ROUND_STARTER and rounds_config:
                # if played in rounds, keep round_starter
                continue

            if param.option in (ckey.GAME_CLASS,
                                ckey.HOLES, ckey.NBR_START,
                                ckey.NAME, ckey.ABOUT, ckey.SOW_DIRECT):
                continue

            man_config.del_default_config_tag(self.game_config,
                                              param.vtype,
                                              param.cspec,
                                              param.option)

    def save(self, askfile=False):
        """Save the game configuration to a file.
        Preserve any tags/comments that were in a loaded config.
        Set the working dir to the selected dir."""

        if self.loaded_config:
            for tag in self.loaded_config.keys():
                if tag not in self.game_config:
                    self.game_config[tag] = self.loaded_config[tag]

        if not self.filename:
            game_name = 'Mancala'
            if (ckey.GAME_INFO in self.game_config
                    and ckey.NAME in self.game_config[ckey.GAME_INFO]):
                game_name = (self.game_config[ckey.GAME_INFO][ckey.NAME]
                             or 'Mancala')
            self.filename =  game_name + '.txt'

        if askfile or not self._known:
            filename = tkfile.asksaveasfilename(
                                    parent=self._master,
                                    title='Save Parameters',
                                    confirmoverwrite=True,
                                    initialdir=self._dir,
                                    initialfile=self.filename,
                                    filetypes=[('text file', '.txt')],
                                    defaultextension='.txt')
            if not filename:
                return

            self._dir, self.filename = os.path.split(filename)
            os.chdir(self._dir)

        if not self.filename.endswith(ALL_PARAMS):
            self._del_defaults()

        if ckey.ABOUT in self.game_config[ckey.GAME_INFO]:
            # remove all trailing whitespace, but add 1 newline
            text = self.game_config[ckey.GAME_INFO][ckey.ABOUT]
            self.game_config[ckey.GAME_INFO][ckey.ABOUT] = text.rstrip() + '\n'

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.game_config, file, indent=3)

        self.edited = False
        self._known = True


    def check_save_cancel(self):
        """If the game params are edited and not saved,
        ask to save them.

        Return True to cancel the operation."""

        if self.edited:
            message = f'Save changes to {self.filename}?'
            do_it = tk.messagebox.askyesnocancel(title='Save Changes',
                                                 message=message,
                                                 parent=self._master)
            if do_it is None:
                return True

            if do_it is True:
                self.save()

        return False


    def revert(self):
        """If the file is known and the data edited,
        then reload from the file."""

        if self.edited and self._known:

            message = f'Revert changes to {self.filename}?'
            do_it = tk.messagebox.askyesno(title='Revert Changes',
                                           message=message,
                                           parent=self._master)
            if do_it:
                self._load_file()
                return True

        else:
            self._master.bell()

        return False
