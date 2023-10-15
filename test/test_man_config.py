# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:24:10 2023
@author: Ann"""


import os
import random
import string

import pytest
pytestmark = pytest.mark.unittest

from context import cfg_keys as ckey
from context import man_config
from context import mancala

from game_interface import Direct


# %%

TEST_COVERS = ['src\\man_config.py']



# %%

class TestBasicConstruction:

    @pytest.fixture
    def config_file1(self, tmp_path):
        """confirm non-default game class and conversion of enums.
        can't use read_game_config because it needs the game
        class to be in GAMES_CLASSES."""

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            print("""{
                       "game_class": "TestGame",
                       "game_constants": {
                          "holes": 6,
                          "nbr_start": 4
                       },
                       "game_info": {
                           "capt_on": [4],
                           "sow_direct": -1
                       },
                       "player": {
                           "mm_depth": [1, 1, 3, 5]
                        }
                     }
                """, file=file)
        return filename

    def test_dir(self, config_file1):

        game_dict = man_config.read_game(config_file1)

        assert game_dict[ckey.GAME_CLASS] == 'TestGame'
        assert game_dict[ckey.GAME_CONSTANTS][ckey.HOLES] == 6
        assert game_dict[ckey.GAME_CONSTANTS][ckey.NBR_START] == 4

        info_dict = game_dict[ckey.GAME_INFO]
        assert isinstance(info_dict[ckey.SOW_DIRECT], Direct)
        assert info_dict[ckey.SOW_DIRECT] == Direct.CW

        assert 'mm_depth' in game_dict[ckey.PLAYER]


    @pytest.fixture
    def config_file2(self, tmp_path):

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            print("""{
                       "game_constants": {
                          "holes": 6,
                          "nbr_start": 4
                       },
                       "game_info": {
                       },
                       "player": {}
                     }
                """, file=file)
        return filename

    @pytest.mark.filterwarnings("ignore")
    def test_basic_file(self, config_file2):

        config = man_config.read_game_config(config_file2)
        gclass, gconsts, ginfo, pdict = config

        assert gclass == 'Mancala'
        assert gconsts.holes == 6
        assert gconsts.nbr_start == 4


    @pytest.fixture
    def config_file3(self, tmp_path):

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            print("""{
                       "game_constants": {
                          "holes": 6,
                          "nbr_start": 4
                       },
                       "game_info": {
                       },
                       "player": {
                           "mm_depth": [1, 1, 3, 5]
                        }
                     }
                """, file=file)
        return filename

    @pytest.mark.filterwarnings("ignore")
    def test_no_dir(self, config_file3):

        config = man_config.read_game_config(config_file3)
        gclass, gconsts, ginfo, pdict = config

        assert gclass == 'Mancala'
        assert gconsts.holes == 6
        assert gconsts.nbr_start == 4
        assert isinstance(ginfo.sow_direct, Direct)
        assert ginfo.sow_direct == Direct.CCW
        assert 'mm_depth' in pdict


    @pytest.fixture
    def config_file4(self, tmp_path):

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            print("""{
                       "game_constants": {
                          "holes": 9,
                          "nbr_start": 2
                       },
                       "game_info": {
                           "capt_on": [2]
                       },
                       "player": {
                           "mm_depth": [1, 1, 3, 5]
                        }
                     }
                """, file=file)
        return filename


    def test_make_game(self, config_file4):

        game, pdict = man_config.make_game(config_file4)

        assert isinstance(game, mancala.Mancala)
        assert game.cts.holes == 9
        assert game.cts.nbr_start == 2
        assert game.info.capt_on == [2]
        assert 'mm_depth' in pdict


class TestRejectFile:

    @pytest.fixture
    def junk_file1(self, tmp_path):

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            print(''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=3000)),
                  file=file)
        return filename


    @pytest.fixture
    def junk_file2(self, tmp_path):

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            for _ in range(200):
                print(''.join(random.choices(string.ascii_lowercase +
                                 string.digits, k=80)),
                      file=file)
        return filename


    @pytest.mark.parametrize('file', [junk_file1, junk_file2])
    def test_big_files(self, file, request):

        ffixt = request.getfixturevalue(file.__name__)
        with pytest.raises(ValueError):
            man_config.read_game_config(ffixt)
