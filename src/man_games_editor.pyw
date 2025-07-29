# -*- coding: utf-8 -*-
"""Launch the Mancala Games Editor.

Created on Thu Mar 30 13:43:39 2023
@author: Ann"""


import tkinter as tk

import game_editor
import game_chooser


if __name__ == '__main__':

    ROOT = tk.Tk()
    man_games = game_editor.MancalaGamesEditor(ROOT, game_chooser.GameChooser)
    man_games.mainloop()
