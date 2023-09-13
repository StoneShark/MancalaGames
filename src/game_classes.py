# -*- coding: utf-8 -*-
"""Define the class names and classes in one spot
for mancala_games, play_mancala and play.

Created on Sun Jul 30 09:41:09 2023
@author: Ann"""

import deka
import gamacha
import mancala
import nam_nam
import qelat

GAME_CLASSES = {'Mancala': mancala.Mancala,
                'Deka': deka.Deka,
                'Gamacha': gamacha.Gamacha,
                'NamNam': nam_nam.NamNam,
                'Qelat': qelat.Qelat}
