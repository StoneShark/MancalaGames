# -*- coding: utf-8 -*-
"""A UI that allows play of any of the games in the GameProps directory.

Created on Thu Mar 23 08:10:28 2023
@author: Ann"""


import tkinter as tk

import game_editor
import game_chooser


if __name__ == '__main__':

    ROOT = tk.Tk()
    chooser = game_chooser.GameChooser(ROOT, game_editor.MancalaGamesEditor)
    chooser.mainloop()
