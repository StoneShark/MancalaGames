# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:24:10 2023

@author: Ann
"""

import os
import sys

import pytest

sys.path.extend(['src'])

import man_config

@pytest.fixture
def config_file(tmp_path):

    filename = os.path.join(tmp_path,'config.txt')
    with open(filename, 'w', encoding='utf-8') as file:
        print("""{
                   "game_constants": {
                      "holes": 6,
                      "nbr_start": 4
                   },
                   "game_info": {
                   }
                 }
            """, file=file)
    return filename


@pytest.mark.filterwarnings("ignore")
def test_basic_file(config_file):

    gclass, gconsts, ginfo = man_config.read_game_config(config_file)

    assert gclass == 'Mancala'

    assert gconsts.holes == 6
    assert gconsts.nbr_start == 4
