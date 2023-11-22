# -*- coding: utf-8 -*-
"""Direct interface to start a mancala game given a config file.

Created on Tue Jul 18 13:50:32 2023
@author: Ann"""

import argparse
import os.path
import sys

import man_config
import mancala_ui


def find_file(gname):
    """Look in a few logical places for the file."""

    places = [gname,
              './ ' + gname + '.txt',
              './GameProps/' + gname,
              './GameProps/' + gname + '.txt',
              '../GameProps/' + gname,
              '../GameProps/' + gname + '.txt']

    for fname in places:
        if os.path.isfile(fname):
            return fname

    raise ValueError(f"Can't file {gname}.")


def get_gamename():
    """Define the parser and use it."""

    parser = argparse.ArgumentParser()
    parser.add_argument('gamename')

    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    return cargs.gamename


if __name__ == '__main__':

    gamename = get_gamename()
    filename = find_file(gamename)

    game, pdict = man_config.make_game(filename)
    print(game.info.about)

    game_ui = mancala_ui.MancalaUI(game, pdict)
    game_ui.mainloop()
