# -*- coding: utf-8 -*-
"""Define the class names and classes in one spot
for mancala_games, play_mancala and play.

Created on Sun Jul 30 09:41:09 2023
@author: Ann"""

import diffusion
import mancala
import same_side

GAME_CLASSES = {'Mancala': mancala.Mancala,
                'Diffusion': diffusion.Diffusion,
                'DiffusionV2': diffusion.DiffusionV2,
                'SameSide': same_side.SameSide,
                'Ohojichi': same_side.Ohojichi}
