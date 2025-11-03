# -*- coding: utf-8 -*-
"""Direct interface to start a mancala game given a config file and
possibly a variant.

Created on Tue Jul 18 13:50:32 2023
@author: Ann"""

import tkinter as tk

import format_msg
import man_config
import man_path
import mancala_ui
import ui_utils


def print_about(game):
    """Format and print the about game text."""

    text = man_config.remove_tags(game.info.about)
    formatted = format_msg.fmsg(list(format_msg.build_paras(text)),
                                wide=True)
    print(formatted)


def build_game_ui(game_str):
    """Build the game ui."""

    if man_config.VAR_SEP in game_str:
        man_config.read_params_data(need_descs=False)

    gamename, variant = man_config.game_name_to_parts(game_str)

    filename = man_path.find_gamefile(gamename)
    game, pdict = man_config.make_game(filename, variant)
    print_about(game)

    return mancala_ui.MancalaUI(game, pdict)


if __name__ == '__main__':

    man_config.check_disable_animator()

    param = man_path.get_cmd_ln_gamename(optional=True)
    if param:

        game_ui = build_game_ui(param)
        game_ui.mainloop()

    else:

        ROOT = tk.Tk()
        ROOT.bell()
        msg = ["""Game not specified.""",
               """The play script requires a parameter to know
               what game to play. It must be specified via a command
               line argument or via a parameter in a shortcut.""",
               """If you would like to browser through all
               preconfigured games, run play_mancala."""]
        ui_utils.QuietDialog(ROOT, 'Play', msg)
