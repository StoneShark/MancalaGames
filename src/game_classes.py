# -*- coding: utf-8 -*-
"""Define the class names and classes in one spot
for mancala_games, play_mancala and play.

Created on Sun Jul 30 09:41:09 2023
@author: Ann"""

import bear_off
import diffusion
import mancala
import same_side
import two_cycle

GAME_CLASSES = {'Mancala': mancala.Mancala,
                'North/South Cycles': two_cycle.NorthSouthCycle,
                'East/West Cycles': two_cycle.EastWestCycle,
                'Diffusion': diffusion.Diffusion,
                'DiffusionV2': diffusion.DiffusionV2,
                'SameSide': same_side.SameSide,
                'Ohojichi': same_side.Ohojichi,
                'BearOff': bear_off.BearOff}
