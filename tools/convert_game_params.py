# -*- coding: utf-8 -*-
"""Convert the excel parameter table to tab separated.

This file is generated as tab separated because of the multiline
descriptions.

Created on Tue Jun 25 12:05:51 2024
@author: Ann"""

import pandas as pd


gparams = pd.read_excel('src/game_params.xlsx')

with open('src/game_params.txt', 'w', newline='') as file:
    gparams.to_csv(file, sep='\t', index=False)
