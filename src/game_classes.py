# -*- coding: utf-8 -*-
"""Define the class names and classes in one spot
for mancala_games, play_mancala and play.

Created on Sun Jul 30 09:41:09 2023
@author: Ann"""

import bear_off
import diffusion
import gratuitous
import mancala
import share_one
import two_cycle
import zigzag

GAME_CLASSES = {'Mancala': mancala.Mancala,
                'NorthSouthCycle': two_cycle.NorthSouthCycle,
                'EastWestCycle': two_cycle.EastWestCycle,
                'Diffusion': diffusion.Diffusion,
                'DiffusionV2': diffusion.DiffusionV2,
                'NSGratuitous': gratuitous.NSGratuitous,
                'EWGratuitous': gratuitous.EWGratuitous,
                'BearOff': bear_off.BearOff,
                'ShareOne': share_one.ShareOne,
                'ZigZag': zigzag.ZigZag}
