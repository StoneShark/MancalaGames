# -*- coding: utf-8 -*-
"""Handles the configuration files for mancala games:

Read a specified game configuration file and return
the game class, game constants, game info, and
player dictionary.

Utilities to get default values and retrieve or set
game configuration value via the 'cspec' from
the game_params file.

Read the parameters data files game_params and
game_param_descs, return a dictionary of
    param_name: Param

Reads (or creates) the ini for UI options.

Created on Tue Jul 18 12:16:20 2023
@author: Ann"""

import configparser
import csv
import dataclasses as dc
import json
import re
import os
from tkinter import font

import ai_player
import cfg_keys as ckey
import game_constants as gc
import game_interface as gi
import man_path
import param_consts as pc

from ai_player import ALGORITHM_DICT
from ai_player import AI_PARAM_DEFAULTS
from game_classes import GAME_CLASSES


# %%  constants

MAX_LINES = 150
MAX_CHARS = 3000

NO_CONVERT = [ckey.NAME, ckey.ABOUT, ckey.HELP_FILE,
              ckey.UDIR_HOLES, ckey.CAPT_ON]

SP = ' '
OPT_TAG = '_'
GI_TAG = ckey.GAME_INFO + SP + OPT_TAG
AI_TAG = ckey.PLAYER + SP + ckey.AI_PARAMS + SP + OPT_TAG
SCR_TAG = ckey.PLAYER + SP + ckey.SCORER + SP + OPT_TAG

MINUS = '-'
INT_LIST_CHARS = '0123456789, '
ELIST_STR = '[]'

SKIP_TAB = 'skip'

PARAM = re.compile('^<param ([a-z0-9_]+)>')


# %% read config files

def read_game(filename):
    """Read a mancala configuration returning the
    game dictionary.  The main UI uses this to load tk widgets,
    then calls test to report any errors making it easier on the
    human to correct any errors.

    Convert the type of all of the flags to those expected by
    the dataclass. This validates enum values and provides access
    to methods on the enums."""

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text = ''.join(lines)
    if len(lines) > MAX_LINES or len(text) > MAX_CHARS:
        raise ValueError('Input file problem.')

    game_dict = json.loads(text)

    info_dict = game_dict[ckey.GAME_INFO]
    for fdesc in dc.fields(gi.GameInfo):
        if fdesc.name in info_dict and fdesc.name not in NO_CONVERT:
            ftype = type(fdesc.default)
            info_dict[fdesc.name] = ftype(info_dict[fdesc.name])

    return game_dict


def read_game_config(filename):
    """Read a mancala configuration file and return
    the game class, constants, info and player_dict."""

    game_dict = read_game(filename)
    game_class = game_dict[ckey.GAME_CLASS] \
        if ckey.GAME_CLASS in game_dict else 'Mancala'

    game_consts = gc.GameConsts(**game_dict[ckey.GAME_CONSTANTS])
    info_dict = game_dict[ckey.GAME_INFO]

    gclass = GAME_CLASSES[game_class]
    game_info = gi.GameInfo(**info_dict,
                            nbr_holes=game_consts.holes,
                            rules=gclass.rules)

    return game_class, game_consts, game_info, game_dict[ckey.PLAYER]


def make_game(filename):
    """Return a constructed game from the configuration
    and the player dictionary."""

    class_name, consts, info, player_dict = read_game_config(filename)

    gclass = GAME_CLASSES[class_name]
    return gclass(consts, info), player_dict


# %% access config data and defaults

def get_config_value(game_config, config_spec, option, vtype):
    """Get the value from the configuration, if it's not there
    use the constructor default."""

    value = get_gc_value(game_config, config_spec, option)
    if value is None:
        value = get_construct_default(vtype, config_spec, option)
    return value


def get_construct_default(vtype, cspec, option):
    """The defaults in the UI parameter table yield a playable game,
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

    elif option == ckey.GAME_CLASS:
        rval = list(GAME_CLASSES.keys())[0]

    elif option == ckey.DIFFICULTY:
        rval = 1

    elif vtype in (pc.STR_TYPE, pc.MSTR_TYPE):
        rval = ""

    elif vtype == pc.INT_TYPE:
        rval = 0

    return rval


def get_gc_value(game_config, cspec, option):
    """Game_config_spec format is one of
        word+  or  word* _
    where option is substituted for _

    Lookup and return the value in a series of nested dictionaries."""

    tags = cspec.split(SP)

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


def set_config_value(game_config, cspec, option, value):
    """Set the value in a series of nested dictionaries;
    create empty dictionaries as required."""

    tags = cspec.split(SP)

    vdict = game_config
    for tag in tags[:-1]:
        if tag not in vdict:
            vdict[tag] = {}
        vdict = vdict[tag]

    if tags[-1] == OPT_TAG:
        vdict[option] = value
    else:
        vdict[tags[-1]] = value


def del_default_config_tag(game_config, vtype, cspec, option):
    """If the option has the default value,
    delete it from it's parent dictionary."""

    tags = cspec.split(SP)

    vdict = game_config
    for tag in tags:
        if tag == OPT_TAG:
            if option in vdict:
                default = get_construct_default(vtype, cspec, option)
                if vdict[option] == default:
                    vdict.pop(option, None)
                return

        if tag in vdict:
            vdict = vdict[tag]
        else:
            return


# %% parameters files

def convert_default_value(value):
    """Convert the ui_defaults to appropriate python values.

    NONE is an enumeration value (usually 0) not the value None."""

    convert_dict = {'true': True,
                    'false': False,
                    }
    value = value.strip()

    if (key := value.lower()) in convert_dict:
        return convert_dict[key]

    if value.isdigit() or (value[0] == MINUS and value[1:].isdigit()):
        return int(value)

    if value == ELIST_STR:
        return []

    if (value[0] == ELIST_STR[0]
            and value[-1] == ELIST_STR[-1]
            and all(c in INT_LIST_CHARS for c in value[1:-1])):
        substrs = value[1:-1].split(',')
        return [int(val.strip()) for val in substrs]

    return value


@dc.dataclass
class Param:
    """A single parameter description.
    These must be in the same order that they are in the spead sheet
    (or Params shouldn't be created with positional args)."""

    tab: str
    option: str
    text: str
    cspec: str
    order: int
    vtype: str
    ui_default: object
    row: int
    col: int
    description: str = dc.field(repr=False, default='')


TAB_IDX = 0
OPTION_IDX = 1
UI_DEFAULT_IDX = 6
INT_IDXS = [4, 7, 8]


class ParamData(dict):
    """A dictionary of the parameter data. Keys are the 'option'
    column (parameter name); values are Param dataclass objects."""

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self._read_params_table()
        self._read_param_descriptions()


    def _read_param_descriptions(self):
        """Read the parameter descriptions file.
        static method because read_params_file is used outside
        mancala_games."""

        with open(man_path.get_path('game_param_descs.txt'), 'r',
                  encoding='us-ascii') as file:
            data = file.readlines()

        text = ''
        param = ''
        for line in data:

            # skip blank lines
            if not line.strip():
                continue

            pmatch = PARAM.match(line)

            if pmatch:
                # if we have a param name, save the accumulated data
                if param:
                    self[param].description = text

                param = pmatch.groups()[0]
                text = ''

                if param not in self:
                    msg = f"Description without game_params data {param}"
                    raise ValueError(msg)

            else:
                text += line

        # add the last parameter
        self[param].description = text


    def _read_params_table(self):
        """Read the game parameters file.
        static method because used outside mancala_games."""

        with open(man_path.get_path('game_params.txt'), 'r',
                  encoding='us-ascii') as file:
            reader = csv.reader(file, delimiter='\t')
            data = list(reader)

        fields = data[0]
        if not all(fname == pfield.name
                   for fname, pfield in zip(fields, dc.fields(Param))):
            raise ValueError("game_params columns are not as expected")

        for rec in data[1:]:
            if rec[TAB_IDX] == SKIP_TAB:
                continue

            opt_name = rec[OPTION_IDX]
            if opt_name in self:
                msg = f"Duplicate option in game_params {opt_name}."
                raise ValueError(msg)

            for idx in INT_IDXS:
                if not rec[idx].isdigit():
                    raise ValueError("Expected int for {opt_name} col {idx}.")
                rec[idx] = int(rec[idx])

            rec[UI_DEFAULT_IDX] = convert_default_value(rec[UI_DEFAULT_IDX])
            self[opt_name] = Param(*rec)


# %% read and process config ini

INI_FILENAME = 'mancala.ini'

DEFAULTS = {
    'button_size': '100',

    'system_color': 'SystemButtonFace',
    'turn_color': 'LightBlue2',
    'turn_dark_color': 'LightBlue4',
    'inactive_color': 'grey60',

    'choose_color': 'pink2',
    'seed_color': 'goldenrod',
    'move_color': 'sandy brown',

    'font_family' : 'Helvetica',
    'font_size' : '14',
    'font_weight' : 'bold',

    'show_tally': 'no',
    'touch_screen': 'no',
    'facing_players': 'no',
    'ownership_arrows': 'no',

    'ai_active': 'no',
    'ai_delay': '1',
    'difficulty': '1',

    'log_live': 'no',
    'log_level': 'move',
    }

DEFAULT = 'default'


class ConfigData:
    """Read/create configuration data."""

    def __init__(self):

        pathname = man_path.get_path(INI_FILENAME, no_error=True)
        if not pathname:
            self.create_ini_file()
            return

        self._config = configparser.ConfigParser()
        self._config.read(pathname)

        if DEFAULT not in self._config.sections():
            self.create_ini_file()


    def __getitem__(self, key):
        """Get the item from the default dicitonary"""

        return self._config[DEFAULT].get(key, DEFAULTS[key])


    def create_ini_file(self):
        """Create a default ini file.
        Make an attempt to put the ini file at the project root."""

        directory = os.getcwd()
        pdir, bdir = os.path.split(directory)
        if bdir in {'GameProps', 'GamePropsNoRelease', 'src'}:
            directory = pdir
        fullpath = os.path.join(directory, INI_FILENAME)

        self._config = configparser.ConfigParser()
        self._config[DEFAULT] = DEFAULTS

        with open(fullpath, 'w', encoding='UTF-8') as configfile:
            self._config.write(configfile)


    def get_int(self, key, default=0):
        """Attempt to get an int from the config.
        If it is missing or invalid return the default."""

        if key not in self._config[DEFAULT]:
            return default

        try:
            int_val = int(self._config[DEFAULT][key])
        except ValueError:
            int_val = int(DEFAULTS[key])

        return max(0, int_val)


    def get_bool(self, key):
        """Interpret the value as an affirmative or not.
        If the key is not there return False"""

        if key in self._config[DEFAULT]:
            return self._config[DEFAULT][key].lower() in {'yes', 'true'}

        return False


    def get_font(self):
        """Attempt to get a font from the config.
        If it is missing return the default.
        If it invalid, 'font.Font' will pick the best match."""

        ftuple = (self['font_family'],
                  self.get_int('font_size'),
                  self['font_weight'])
        return font.Font(font=ftuple)


CONFIG = ConfigData()
