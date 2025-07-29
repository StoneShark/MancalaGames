# -*- coding: utf-8 -*-
"""Direct interface to start a mancala game given a config file and
possibly a variant.

Created on Tue Jul 18 13:50:32 2023
@author: Ann"""

import argparse
import sys

import man_config
import man_path
import mancala_ui


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

    man_config.check_disable_animator()

    gamename, variant = man_config.game_name_to_parts(get_gamename())

    filename = man_path.find_gamefile(gamename)
    game, pdict = man_config.make_game(filename, variant)
    print(game.info.about)

    game_ui = mancala_ui.MancalaUI(game, pdict)
    game_ui.mainloop()
