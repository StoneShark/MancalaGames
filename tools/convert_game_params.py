# -*- coding: utf-8 -*-
"""Convert the excel parameter table csv.

Created on Tue Jun 25 12:05:51 2024
@author: Ann"""

import pandas as pd


gparams = pd.read_excel('src/game_params.xlsx',
                        dtype={'order': str, 'row': str, 'col': str})

with open('src/game_params.csv', 'w', newline='') as file:
    gparams.to_csv(file, index=False)
