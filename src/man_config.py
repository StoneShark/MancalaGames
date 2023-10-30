# -*- coding: utf-8 -*-
"""Read a mancala configuration file and return
the game class, game constants and game info.

Created on Tue Jul 18 12:16:20 2023
@author: Ann"""

import dataclasses as dc
import json

import ai_player
import cfg_keys as ckey
import game_constants as gc
import game_interface as gi

from ai_player import ALGORITHM_DICT
from ai_player import AI_PARAM_DEFAULTS
from game_classes import GAME_CLASSES
from param_consts import INT_TYPE
from param_consts import STR_TYPE
# from param_consts import BOOL_TYPE
from param_consts import MSTR_TYPE
# from param_consts import BLIST_TYPE
# from param_consts import ILIST_TYPE


# %%

MAX_LINES = 150
MAX_CHARS = 3000

NO_CONVERT = [ckey.NAME, ckey.ABOUT, ckey.HELP_FILE,
              ckey.UDIR_HOLES, ckey.CAPT_ON]

OPT_TAG = '_'
GI_TAG = 'game_info _'
AI_TAG = 'player ai_params _'
SCR_TAG = 'player scorer _'


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
    """Return a constructed game from the configuration."""

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

    elif option == ckey.DIFFICULTY:
        rval = 1

    elif vtype in (STR_TYPE, MSTR_TYPE):
        rval = ""

    elif vtype == INT_TYPE:
        rval =  0

    return rval


def get_gc_value(game_config, cspec, option):
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


def set_config_value(game_config, cspec, option, value):
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
