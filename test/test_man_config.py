# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:24:10 2023
@author: Ann"""

import copy
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



class TestGc:

    def test_gc_get(self):

        gdict  = {
                   "game_constants": {
                      "holes": 9,
                      "nbr_start": 2
                   },
                   "game_info": {
                       "capt_on": [2]
                   },
                   "player": {
                       "ai_params": {
                           "mm_depth": [1, 1, 3, 5]
                       }
                    }
                 }

        assert man_config.get_gc_value(gdict, 'game_constants _', 'holes') == 9
        assert man_config.get_gc_value(gdict, 'game_info _', 'capt_on') == [2]

        assert man_config.get_gc_value(gdict,
                                       'player ai_params _',
                                       'mm_depth')[2] == 3

        assert man_config.get_gc_value(gdict, 'junk', '') is None
        assert man_config.get_gc_value(gdict, 'game_constants junk', '') is None
        assert man_config.get_gc_value(gdict, 'game_constants _', 'junk') is None

        gi_dict = man_config.get_gc_value(gdict, 'game_info', '')
        assert isinstance(gi_dict, dict)
        assert 'capt_on' in gi_dict


    def test_gc_set(self):

        gdict  = {
                    "game_constants": {
                      "holes": 9,
                      "nbr_start": 2
                    },
                    "game_info": {
                        "capt_on": [2]
                    },
                    "player": {
                        "ai_params": {
                            "mm_depth": [1, 1, 3, 5]
                        }
                    }
                  }

        assert man_config.get_gc_value(gdict, 'game_constants _', 'holes') == 9
        man_config.set_config_value(gdict, 'game_constants _', 'holes', 4)
        assert man_config.get_gc_value(gdict, 'game_constants _', 'holes') == 4


        man_config.set_config_value(gdict,
                                    'player ai_params _',
                                    'mm_depth', [5, 7, 9, 11])
        assert man_config.get_gc_value(gdict,
                                        'player ai_params _',
                                        'mm_depth') == [5, 7, 9, 11]

        man_config.set_config_value(gdict, 'junk _', 'param', 5)
        assert 'junk' in gdict
        assert 'param' in gdict['junk']
        assert gdict['junk']['param'] == 5

        man_config.set_config_value(gdict, 'more_junk', 'param', 5)
        assert 'more_junk' in gdict
        assert gdict['more_junk'] == 5


    def test_const_def(self):

        assert man_config.get_construct_default('int',
                                                'game_info _',
                                                'min_move') == 1
        assert man_config.get_construct_default('int',
                                                'player scorer _',
                                                'stores_m') == 0
        assert man_config.get_construct_default('list[int]',
                                                'player ai_params _',
                                                'mm_depth') == [1, 1, 3, 5]
        assert man_config.get_construct_default('str',
                                                'player _',
                                                'algorithm') == 'minimaxer'
        assert man_config.get_construct_default('str',
                                                'player  _',
                                                'difficulty') == 1
        assert man_config.get_construct_default('GameClasses',
                                                '_',
                                                'game_class') == 'Mancala'
        assert man_config.get_construct_default('str',
                                                'junk  _',
                                                'more_junk') == ""
        assert man_config.get_construct_default('int',
                                                'junk  _',
                                                'more_junk') == 0

        assert not man_config.get_construct_default('bool',
                                                    'junk  _',
                                                    'more_junk')


    def test_config_get(self):

        gdict  = {
                   "game_constants": {
                      "holes": 9,
                      "nbr_start": 2
                   },
                   "game_info": {
                       "capt_on": [2]
                   },
                   "player": {
                       "ai_params": {
                           "mm_depth": [1, 1, 3, 5]
                       }
                    }
                 }

        assert man_config.get_config_value(gdict,
                                           'game_constants _',
                                           'holes',
                                           'int') == 9
        assert man_config.get_config_value(gdict,
                                           'game_info _',
                                           'min_move',
                                           'int') == 1




class TestResetDefs:

    @pytest.fixture
    def config_file(self, tmp_path):

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
                           "sow_direct": 1,
                           "evens": false
                       },
                       "player": {
                           "ai_params": {
                               "mcts_bias": [10, 10, 10],
                               "mm_depth": [1, 1, 3, 5]
                           }
                        }
                     }
                """, file=file)
        return filename


    def test_del_default(self, config_file):
        """confirm deletion of construction default but not
        ui defaults."""

        game_dict = man_config.read_game(config_file)

        assert ckey.SOW_DIRECT in game_dict[ckey.GAME_INFO]
        assert ckey.EVENS in game_dict[ckey.GAME_INFO]
        assert ckey.MM_DEPTH in game_dict[ckey.PLAYER][ckey.AI_PARAMS]

        man_config.del_default_config_tag(game_dict,
                                          'list[int',
                                          'game_info _',
                                          ckey.CAPT_ON)   # not default
        man_config.del_default_config_tag(game_dict,
                                          'Direct',
                                          'game_info _',
                                          ckey.SOW_DIRECT)  # default
        man_config.del_default_config_tag(game_dict,
                                          'bool',
                                          'game_info _',
                                          ckey.EVENS)     # not default, but UI default
        man_config.del_default_config_tag(game_dict,
                                          'list[int]',
                                          'player ai_params _',
                                          ckey.MCTS_BIAS) # not default
        man_config.del_default_config_tag(game_dict,
                                          'list[int]',
                                          'player ai_params _',
                                          ckey.MM_DEPTH)   # default


        assert ckey.SOW_DIRECT not in game_dict[ckey.GAME_INFO]
        assert ckey.EVENS not in game_dict[ckey.GAME_INFO]
        assert ckey.MM_DEPTH not in game_dict[ckey.PLAYER][ckey.AI_PARAMS]

        assert ckey.CAPT_ON in game_dict[ckey.GAME_INFO]
        assert ckey.MCTS_BIAS in game_dict[ckey.PLAYER][ckey.AI_PARAMS]


    def test_del_def_nothing(self, config_file):
        """test case where del_def.... does nothing because of
        an invalid tag"""

        game_dict = man_config.read_game(config_file)
        gd_copy = copy.deepcopy(game_dict)

        man_config.del_default_config_tag(game_dict,
                                          'bool',
                                          'player invalid_tag _',
                                          ckey.MM_DEPTH)
        man_config.del_default_config_tag(game_dict,
                                          'bool',
                                          'player ai_params _',
                                          'junk')
        man_config.del_default_config_tag(game_dict,
                                          'bool',
                                          'player ai_params',
                                          'junk')
        assert gd_copy == game_dict
