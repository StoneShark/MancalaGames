# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:24:10 2023
@author: Ann"""


import os
import random
import string

import pytest
pytestmark = pytest.mark.unittest


from context import game_interface as gi
from context import man_config
from context import mancala

from game_interface import Direct


# %%

TEST_COVERS = ['src\\man_config.py']

class TestBasicConstruction:

    @pytest.fixture
    def config_file(self, tmp_path):

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
    def test_basic_file(self, config_file):

        gclass, gconsts, ginfo = man_config.read_game_config(config_file)

        assert gclass == 'Mancala'
        assert gconsts.holes == 6
        assert gconsts.nbr_start == 4


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
                       }
                     }
                """, file=file)
        return filename

    @pytest.mark.filterwarnings("ignore")
    def test_no_dir(self, config_file2):

        gclass, gconsts, ginfo = man_config.read_game_config(config_file2)

        assert gclass == 'Mancala'
        assert gconsts.holes == 6
        assert gconsts.nbr_start == 4
        assert isinstance(ginfo.sow_direct, Direct)
        assert ginfo.sow_direct == Direct.CCW


    @pytest.fixture
    def config_file3(self, tmp_path):

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            print("""{
                       "game_class": "Mancala",
                       "game_constants": {
                          "holes": 6,
                          "nbr_start": 4
                       },
                       "game_info": {
                           "capt_on": [4],
                           "sow_direct": -1
                       }
                     }
                """, file=file)
        return filename

    def test_dir(self, config_file3):

        gclass, gconsts, ginfo = man_config.read_game_config(config_file3)

        assert gclass == 'Mancala'
        assert gconsts.holes == 6
        assert gconsts.nbr_start == 4
        assert isinstance(ginfo.sow_direct, Direct)
        assert ginfo.sow_direct == Direct.CW


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
                           "capt_on": [2],
                           "scorer": {
                               "stores_m": 10
                            }
                       }
                     }
                """, file=file)
        return filename

    def test_scorer(self, config_file4):

        gclass, gconsts, ginfo = man_config.read_game_config(config_file4)

        assert gclass == 'Mancala'
        assert gconsts.holes == 9
        assert gconsts.nbr_start == 2
        assert isinstance(ginfo.scorer, gi.Scorer)
        assert ginfo.scorer.stores_m == 10


    @pytest.fixture
    def config_file5(self, tmp_path):

        filename = os.path.join(tmp_path,'config.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            print("""{
                       "game_constants": {
                          "holes": 9,
                          "nbr_start": 2
                       },
                       "game_info": {
                           "capt_on": [2],
                           "scorer": {
                               "stores_m": 10
                            }
                       }
                     }
                """, file=file)
        return filename

    def test_make_game(self, config_file4):

        game = man_config.make_game(config_file4)

        assert isinstance(game, mancala.Mancala)
        assert game.cts.holes == 9
        assert game.cts.nbr_start == 2
        assert game.info.capt_on == [2]
        assert game.info.scorer.stores_m == 10


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
