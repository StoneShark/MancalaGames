# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 15:14:27 2023
@author: Ann
"""

# %% imports

import dataclasses as dc
import os
import sys

sys.path.extend(['../src'])

from game_interface import GameFlags
from game_interface import GameInfo
import man_config


# %% read the game config files

PATH = '../GameProps/'
files = os.listdir(PATH)

files.remove('all_params.txt')

all_games = {}
for game in files:
    all_games[game] = man_config.read_game_config(PATH + game)

del game

# %% get params we want

def get_dc_field_names(dc_cls):
    return [field.name for  field in dc.fields(dc_cls)]

gconsts  = ['holes', 'nbr_start']
gflags = sorted(get_dc_field_names(GameFlags))
ginfos = get_dc_field_names(GameInfo)

for dontcare in ['flags', 'scorer', 'name', 'nbr_holes',
                 'difficulty', 'help_file', 'about']:
    ginfos.remove(dontcare)

gflags.remove('udirect')

del dontcare

params = gconsts + gflags + ginfos


# %%

with open('props_used.csv', 'w') as file:

    print(',', end='', file=file)
    for name in params:
        print(f'{name},', end='', file=file)
    print(file=file)

    for game in files:

        print(f'{game[:-4]},', end='', file=file)

        for param in params:

            _, consts, info = all_games[game]
            vstr = ''

            if param in gconsts:
                vstr = str(getattr(consts, param))

            elif param in gflags:
                vstr = str(getattr(info.flags, param))

            elif param in ('capt_on', 'udir_holes', 'mm_depth'):
                vstr = ' '.join(str(val) for val in getattr(info, param))
            else:
                vstr = str(getattr(info, param))

            print(vstr, ',', sep='', end='', file=file)

        print(file=file)
