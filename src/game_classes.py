# -*- coding: utf-8 -*-
"""Define the class names and classes in one spot
for mancala_games, play_mancala and play.

Created on Sun Jul 30 09:41:09 2023
@author: Ann"""

import gamacha
import mancala
import nam_nam

GAME_CLASSES = {'Mancala': mancala.Mancala,
                'Gamacha': gamacha.Gamacha,
                'NamNam': nam_nam.NamNam}
