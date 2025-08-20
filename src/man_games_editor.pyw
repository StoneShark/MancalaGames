# -*- coding: utf-8 -*-
"""Launch the Mancala Games Editor.
Accept an optional parameter that is the game or file to
load on startup.

Created on Thu Mar 30 13:43:39 2023
@author: Ann"""


import tkinter as tk

import game_editor
import game_chooser
import man_path


if __name__ == '__main__':

    param = man_path.get_cmd_ln_gamename(optional=True)

    ROOT = tk.Tk()
    man_games = game_editor.MancalaGamesEditor(ROOT, game_chooser.GameChooser)

    if param:
        man_games.load_game(param)

    man_games.mainloop()
