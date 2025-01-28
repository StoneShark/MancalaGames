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
        self._filename = None

        self.edited = False           # is there an edit that hasn't been saved
        self.loaded_config = None     # keep for persistent comment entries
        self.game_config = None       # constructed config for playing


    def reset(self):
        """Reset data to initial values"""

        self._dir = man_path.get_path('GameProps')
        self._filename = None

        self.edited = False
        self.loaded_config = None
        self.game_config = None


    def init_fname(self, game_name):
        """If we don't have a filename yet,
        initialize it with the game name."""

        if not self._filename and game_name:
            self._filename = game_name + '.txt'


    def load(self):
        """Load the game configuration from a file.
        Set the working dir to the selected dir.
        json.JSONDecodeError is dervied from ValueError."""

        if self.check_save_cancel():
            return

        filename = tkfile.askopenfilename(
            parent=self._master,
            title='Load Parameters',
            initialdir=self._dir)
        if not filename:
            return

        self._dir, self._filename = os.path.split(filename)
        os.chdir(self._dir)
        self.edited = False

        try:
            self.loaded_config = man_config.read_game(filename)
        except ValueError as error:
            tk.messagebox.showerror('JSON File Error', error,
                                    parent=self._master)
            return


    def _del_defaults(self):
        """Delete most tags that have the default value."""

        for param in self._params.values():

            if param.option not in (ckey.GAME_CLASS,
                                    ckey.HOLES, ckey.NBR_START,
                                    ckey.NAME, ckey.ABOUT, ckey.SOW_DIRECT):

                man_config.del_default_config_tag(self.game_config,
                                                  param.vtype,
                                                  param.cspec,
                                                  param.option)

    def save(self):
        """Save the game configuration to a file.
        Preserve any tags/comments that were in a loaded config.
        Set the working dir to the selected dir."""

        if self.loaded_config:
            for tag in self.loaded_config.keys():
                if tag not in self.game_config:
                    self.game_config[tag] = self.loaded_config[tag]

        if not self._filename:
            game_name = self.game_config[ckey.GAME_INFO].get([ckey.NAME],
                                                             'Mancala')
            self._filename =  game_name + '.txt'

        filename = tkfile.asksaveasfilename(
            parent=self._master,
            title='Save Parameters',
            confirmoverwrite=True,
            initialdir=self._dir,
            initialfile=self._filename,
            filetypes=[('text file', '.txt')],
            defaultextension='.txt')
        if not filename:
            return

        if not filename.endswith(ALL_PARAMS):
            self._del_defaults()

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.game_config, file, indent=3)

        self._dir, self._filename = os.path.split(filename)
        os.chdir(self._dir)
        self.edited = False


    def check_save_cancel(self):
        """If the game params are edited and not saved,
        ask to save them.

        Return True to cancel the operation."""

        if self.edited:
            message = f'Save changes to {self._filename}?'
            do_it = tk.messagebox.askyesnocancel(title='Save Changes',
                                                 message=message,
                                                 parent=self._master)
            if do_it is None:
                return True

            if do_it is True:
                self.save()

        return False
