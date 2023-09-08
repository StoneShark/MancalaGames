# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:24:10 2023

@author: Ann
"""

import os
import random
import sys
import string

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


@pytest.fixture
def config_file2(tmp_path):

    filename = os.path.join(tmp_path,'config.txt')
    with open(filename, 'w', encoding='utf-8') as file:
        print("""{
                   "game_constants": {
                      "holes": 6,
                      "nbr_start": 4
                   },
                   "game_info": {
                       "flags": {
                        }
                   }
                 }
            """, file=file)
    return filename


@pytest.mark.filterwarnings("ignore")
def test_no_dir(config_file2):

    gclass, gconsts, ginfo = man_config.read_game_config(config_file2)

    assert gclass == 'Mancala'

    assert gconsts.holes == 6
    assert gconsts.nbr_start == 4



@pytest.fixture
def junk_file1(tmp_path):

    filename = os.path.join(tmp_path,'config.txt')
    with open(filename, 'w', encoding='utf-8') as file:
        print(''.join(random.choices(string.ascii_lowercase +
                         string.digits, k=3000)),
              file=file)
    return filename


@pytest.fixture
def junk_file2(tmp_path):

    filename = os.path.join(tmp_path,'config.txt')
    with open(filename, 'w', encoding='utf-8') as file:
        for _ in range(200):
            print(''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=80)),
                  file=file)
    return filename


@pytest.mark.parametrize('file', [junk_file1, junk_file2])
def test_big_files(file, request):

    ffixt = request.getfixturevalue(file.__name__)
    with pytest.raises(ValueError):
        man_config.read_game_config(ffixt)
