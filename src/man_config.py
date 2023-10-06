# -*- coding: utf-8 -*-
"""Read a mancala configuration file and return
the game class, game constants and game info.

Created on Tue Jul 18 12:16:20 2023
@author: Ann"""

import dataclasses as dc
import json

import cfg_keys as ckey
import game_constants as gc
import game_interface as gi

from game_classes import GAME_CLASSES


MAX_LINES = 150
MAX_CHARS = 2000

NO_CONVERT = [ckey.AI_PARAMS, ckey.SCORER, ckey.HELP_FILE,
              ckey.ABOUT, ckey.UDIR_HOLES, ckey.NAME, ckey.CAPT_ON]


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
    the game class, constants and info."""

    game_dict = read_game(filename)
    game_class = game_dict[ckey.GAME_CLASS] \
        if ckey.GAME_CLASS in game_dict else 'Mancala'

    game_consts = gc.GameConsts(**game_dict[ckey.GAME_CONSTANTS])
    info_dict = game_dict[ckey.GAME_INFO]

    if ckey.SCORER in info_dict:
        info_dict[ckey.SCORER] = gi.Scorer(**info_dict[ckey.SCORER])
    else:
        info_dict[ckey.SCORER] = gi.Scorer()

    gclass = GAME_CLASSES[game_class]
    game_info = gi.GameInfo(**info_dict,
                            nbr_holes=game_consts.holes,
                            rules=gclass.rules)

    return game_class, game_consts, game_info


def make_game(filename):
    """Return a constructed game from the configuration."""

    class_name, consts, info = read_game_config(filename)

    gclass = GAME_CLASSES[class_name]
    return gclass(consts, info)
