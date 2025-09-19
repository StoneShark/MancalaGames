# -*- coding: utf-8 -*-
"""A script to convert pure json game files into
json+xml-lite format.

The strings for the about text and any top level tag
not in ckey.TOP_LEVELS maybe moved to a text_section,
which is written after the json part.

The xml-lite is not pure and proper xml because the data
is read as character data even though the CDATA designator
is not included.

The text in the text_section may have html and other tags
in it (e.g. <nolink>).

Created on Fri Sep 19 04:56:30 2025
@author: Ann"""

import json
import os
import os.path
import textwrap

from context import cfg_keys as ckey
from context import man_config
from context import man_path
from context import mg_config


def reformat(text):
    """Wrap the paragraphs; then rebuild the string."""

    return '\n\n'.join(textwrap.fill(para) for para in text.split('\n\n'))


def write_text_section(text_sec, file):
    """Write the values for the text section out to file."""

    print('', file=file)
    print(man_config.TEXT_SEC_KEY, file=file)

    for tag, value in text_sec.items():
        print('<' + tag + '>', file=file)
        print(reformat(value), file=file)
        print('</' + tag + '>', file=file)

    print(man_config.TEXT_SEC_END, file=file)


def check_save_text_sec(game_dict, text_sec, tag):
    """If there are any new lines in the text,
    move it to the test_section dict."""

    if tag == ckey.ABOUT:
        pdict = game_dict[ckey.GAME_INFO]
    else:
        pdict = game_dict

    text = pdict[tag]

    # make any single new-line, a double
    text = text.replace('\n\n', '@@@@')
    text = text.replace('\n', '\n\n')
    text = text.replace('@@@@', '\n\n')

    if '\n' in text:
        text_sec[tag] = text.rstrip()
        pdict[tag] = man_config.TEXT_SEC_KEY

    else:
        pdict[tag] = text


def move_long_tags(game_dict):
    """Go through the candidates for the text section
    and check them."""

    text_sec = {}

    if ckey.ABOUT in game_dict[ckey.GAME_INFO]:
        check_save_text_sec(game_dict, text_sec, ckey.ABOUT)

    for key in game_dict.keys():

        if key in ckey.TOP_LEVELS:
            continue

        check_save_text_sec(game_dict, text_sec, key)

    return text_sec


def restructure_file(pathname):
    """Restructure one file."""

    game_dict = man_config.read_game(pathname)
    del game_dict[ckey.FILENAME]
    text_sec = move_long_tags(game_dict)

    if not text_sec:
        return

    with open(pathname, 'w', encoding='utf-8') as file:
        json.dump(game_dict, file, indent=3,
                  cls=mg_config.GameDictEncoder)
        write_text_section(text_sec, file)


def convert_all_games():
    """Convert all games in the GameProps dir"""

    path = man_path.get_path(man_path.GAMEPATH)
    files = os.listdir(path)

    for idx, game in enumerate(files):

        if man_path.is_game_file(game):
            print(game)
            restructure_file(os.path.join(path, game))


def convert_one(gamename):
    """Convert the specified game."""

    path = man_path.get_path(man_path.GAMEPATH)
    restructure_file(os.path.join(path, gamename))



if __name__ == '__main__':

    param = man_path.get_cmd_ln_gamename(optional=True)

    if param == 'all':
        convert_all_games()
    else:
        convert_one(param)
