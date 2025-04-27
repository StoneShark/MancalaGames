# -*- coding: utf-8 -*-
"""Handling of the game configuration and file input / output.

Created on Tue Jan 28 11:07:30 2025
@author: Ann"""

import json
import os.path
import tkinter.filedialog as tkfile

import cfg_keys as ckey
import man_config
import man_path
import ui_utils


ALL_PARAMS = '_all_params.txt'


class GameDictEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small lists and tuples on single lines.

    Adapted from code originally written by Jannis Mainczyk
    (https://gist.github.com/jannismain)."""

    CONTAINER_TYPES = (list, tuple, dict)
    MAX_WIDTH = 65
    MAX_ITEMS = 15

    # pylint: disable=arguments-renamed
    # its either going to whine about renaming the arg (o) or
    # that o doesn't form to snake_case naming!?

    def __init__(self, *args, **kwargs):

        if kwargs.get("indent") is None:
            kwargs["indent"] = 4

        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def iterencode(self, obj, _one_shot=False):
        """Required to also work with `json.dump`."""

        return self.encode(obj)

    def encode(self, obj):
        """Encode JSON object obj with respect to single line lists."""

        if isinstance(obj, (list, tuple)):
            return self._encode_list(obj)

        if isinstance(obj, dict):
            return self._encode_dict(obj)

        return json.dumps(
            obj,
            skipkeys=self.skipkeys,
            ensure_ascii=self.ensure_ascii,
            check_circular=self.check_circular,
            allow_nan=self.allow_nan,
            sort_keys=self.sort_keys,
            indent=self.indent,
            separators=(self.item_separator, self.key_separator),
            default=self.default if hasattr(self, "default") else None,
        )

    def _encode_list(self, obj):

        if self._put_on_single_line(obj):
            return "[ " + ", ".join(self.encode(elem) for elem in obj) + " ]"

        self.indentation_level += 1
        output = [self.indent_str + self.encode(elem) for elem in obj]
        self.indentation_level -= 1

        return "[\n" + ",\n".join(output) + "\n" + self.indent_str + "]"

    def _encode_dict(self, obj):
        """Encode a dictionary object.
        This is needed to call self.encode for values in
        the dictionaries."""

        if not obj:
            return "{}"

        # ensure keys are converted to strings
        obj = {str(k) if k is not None else "null": v for k, v in obj.items()}

        if self.sort_keys:
            obj = dict(sorted(obj.items(), key=lambda x: x[0]))

        # never put dicts on one line (well maybe game_constants??)
        # if self._put_on_single_line(obj):
        #     return ("{ "
        #             + ", ".join(f"{json.dumps(k)}: {self.encode(elem)}"
        #                         for k, elem in obj.items())
        #             + " }")

        self.indentation_level += 1
        output = [f"{self.indent_str}{json.dumps(k)}: {self.encode(v)}"
                  for k, v in obj.items()]
        self.indentation_level -= 1

        return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"

    def _put_on_single_line(self, obj):
        """Determine if obj can be put on a single line."""

        return (self._primitives_only(obj)
                and len(obj) <= self.MAX_ITEMS
                and len(str(obj)) <= self.MAX_WIDTH)

    def _primitives_only(self, obj):
        """Determine if the object only contains primitive objects."""

        if isinstance(obj, (list, tuple)):
            return not any(isinstance(elem, self.CONTAINER_TYPES)
                           for elem in obj)

        if isinstance(obj, dict):
            return not any(isinstance(elem, self.CONTAINER_TYPES)
                            for elem in obj.values())

        return False

    @property
    def indent_str(self):
        """Return an indent string or int."""

        if isinstance(self.indent, int):
            return ' ' * (self.indentation_level * self.indent)

        if isinstance(self.indent, str):
            return self.indentation_level * self.indent

        raise ValueError("indent must either be of type int or str "
                          + f"(is: {type(self.indent)})")


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
            ui_utils.showerror(self._master, 'JSON File Error', error)
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
            json.dump(self.game_config, file, indent=3,
                      cls=GameDictEncoder)

        self.edited = False
        self._known = True


    def check_save_cancel(self):
        """If the game params are edited and not saved,
        ask to save them.

        Return True to cancel the operation."""

        if self.edited:
            message = f'Save changes to {self.filename}?'
            do_it = ui_utils.ask_popup(self._master,
                                       'Save Changes', message,
                                       ui_utils.YESNOCANCEL)
            if do_it is None:
                return True

            if do_it is True:
                self.save()

        return False


    def revert(self):
        """If the file is known and the data edited,
        then reload from the file."""

        message = f'Revert changes to {self.filename}?'
        do_it = ui_utils.ask_popup(self._master,
                                   'Revert Changes', message,
                                   ui_utils.YESNO)
        if do_it:
            self._load_file()
            return True

        return False
