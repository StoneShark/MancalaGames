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
ginfos = sorted(get_dc_field_names(GameInfo))

for dontcare in ['name', 'help_file', 'about']:
    ginfos.remove(dontcare)

params = gconsts + ginfos


# %%

with open('props_used.csv', 'w') as file:

    print(',', end='', file=file)
    for param in params:
        print(f'{param},', end='', file=file)
    print(file=file)

    for game in files:

        print(f'{game[:-4]},', end='', file=file)

        for param in params:

            gclass, consts, info, pdict = all_games[game]
            vstr = ''

            if param in gconsts:
                vstr = str(getattr(consts, param))

            elif param in ('capt_on', 'udir_holes'):
                vstr = ' '.join(str(val) for val in getattr(info, param))

            elif param in ginfos:
                pval = getattr(info, param)
                if pval is True:
                    vstr = 'x'
                elif pval not in (0, False):
                    vstr = str(getattr(info, param))

            elif param == 'player':
                pass

            else:
                vstr = str(getattr(info, param))

            print(vstr, ',', sep='', end='', file=file)

        print(file=file)
