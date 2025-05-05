# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:24:10 2023
@author: Ann"""

import copy
import os
import random
import string
import tkinter as tk

import pytest
pytestmark = pytest.mark.unittest

from context import animator
from context import cfg_keys as ckey
from context import man_config
from context import man_path
from context import mancala

from game_interface import Direct


# %%

TEST_COVERS = ['src\\man_config.py']


# %%

class TestRemoveTags:

    CASES = [('<a alkjsdf;lskfj>', ''),
             ('</a>', ''),
             ('<img alksjf;aslk lkj;laskjdfalksdf>\n', ''),
             ('<b a;lksjdflakjsfdals>', ''),
             ('</b>', ''),
             ('<nolink>', ''),
             ('<b class=aald>BOLD WORDS</b>', 'BOLD WORDS'),
             ('<nolink>word', 'word'),
             ('<a', '<a'),
             ]

    @pytest.mark.parametrize('text, eresult', CASES)
    def test_remove_tags(self, text, eresult):

        assert man_config.remove_tags(text) == eresult


# %%  test game config files

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
                           "sow_direct": -1,
                           "stores": true
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
                           "capt_on": [2],
                           "stores": true
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
                        "capt_on": [2],
                        "stores": True
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
                           "evens": false,
                           "stores": true
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


# %%  test reading params

class TestParamDict:

    def test_param_dict(self):

        param_dict = man_config.ParamData()
        assert len(param_dict) > 50
        assert '</a>' not in param_dict['mlaps'].description


    def test_param_dict_tags(self):

        param_dict = man_config.ParamData(del_tags=False)
        assert len(param_dict) > 50
        assert '</a>' in param_dict['mlaps'].description


    @pytest.mark.parametrize(
        'columns',
        ["tab,option,text,order,vtype,ui_default,row,col",
         "tab,option,text,order,vtype,cspecui_default,row,col",
         "tab,option,text,order,vtype,ui_default,row",
         ])
    def test_bad_cols(self, mocker, tmp_path, columns):

        params = os.path.join(tmp_path,'game_params.csv')
        with open(params, 'w', encoding='utf-8') as file:
            print(columns, file=file)

        descs = os.path.join(tmp_path,'game_param_descs.csv')
        with open(descs, 'w', encoding='utf-8') as file:
            print("""
                """, file=file)

        def test_files(fname):
            if fname == 'game_params.csv':
                return params

            if fname == 'game_param_descs.txt':
                return descs

            pytest.fail(reason='Unknown file read')

        mocker.patch.object(man_path, 'get_path', test_files)


        with pytest.raises(ValueError):
            man_config.ParamData()


    def test_dupl_param(self, mocker, tmp_path):

        params = os.path.join(tmp_path,'game_params.csv')
        with open(params, 'w', encoding='utf-8') as file:
            print("""tab,option,text,cspec,order,vtype,ui_default,row,col
Capture,evens,Basic Capture,,0,label,0,0,0
skip,evens,Capture Evens,game_info _,114,bool,True,1,0
Capture,evens,Capture Max,game_info _,104,int,0,2,0
                """, file=file)

        descs = os.path.join(tmp_path,'game_param_descs.txt')
        with open(descs, 'w', encoding='utf-8') as file:
            print("""
                """, file=file)

        def test_files(fname):
            if fname == 'game_params.csv':
                return params

            if fname == 'game_param_descs.txt':
                return descs

            pytest.fail(reason='Unknown file read')

        mocker.patch.object(man_path, 'get_path', test_files)


        with pytest.raises(ValueError):
            man_config.ParamData()


    def test_bad_int_param(self, mocker, tmp_path):

        params = os.path.join(tmp_path,'game_params.csv')
        with open(params, 'w', encoding='utf-8') as file:
            print("""tab,option,text,cspec,order,vtype,ui_default,row,col
Capture,evens,Basic Capture,,0,label,0,0,notint

                """, file=file)

        descs = os.path.join(tmp_path,'game_param_descs.txt')
        with open(descs, 'w', encoding='utf-8') as file:
            print("""
                """, file=file)

        def test_files(fname):
            if fname == 'game_params.csv':
                return params

            if fname == 'game_param_descs.txt':
                return descs

            pytest.fail(reason='Unknown file read')

        mocker.patch.object(man_path, 'get_path', test_files)


        with pytest.raises(ValueError):
            man_config.ParamData()


    def test_bad_desc_param(self, mocker, tmp_path):

        descs = os.path.join(tmp_path,'game_param_descs.txt')
        with open(descs, 'w', encoding='utf-8') as file:
            print("""<param missing>
                  mydata
                """, file=file)

        oget_path = man_path.get_path

        def test_files(fname):
            if fname == 'game_params.csv':
                return oget_path('game_params.csv')

            if fname == 'game_param_descs.txt':
                return descs

            pytest.fail(reason='Unknown file read')

        mocker.patch.object(man_path, 'get_path', test_files)

        with pytest.raises(ValueError):
            man_config.ParamData()


    def test_no_desc(self):

        param_data = man_config.ParamData(del_tags=False, no_descs=True)
        assert len(param_data) > 50
        assert ckey.NBR_START in param_data
        assert ckey.SOW_DIRECT in param_data
        assert ckey.UNCLAIMED in param_data

        assert not param_data[ckey.UNCLAIMED].description



# %%  test config data


class TestConfig:

    def test_config(self):

        man_config.read_ini_file()

        assert man_config.CONFIG
        assert man_config.CONFIG['button_size']


    def test_get_filename(self, mocker):

        man_config.read_ini_file()

        mcwd = mocker.patch.object(os, 'getcwd')
        mcwd.side_effect = ['.\\',
                            '.\\GameProps',
                            '.\\src']

        assert man_config.CONFIG._get_filename() == '.\\mancala.ini'
        assert man_config.CONFIG._get_filename() == '.\\mancala.ini'
        assert man_config.CONFIG._get_filename() == '.\\mancala.ini'


    def test_no_file(self, mocker, tmp_path):

        # man_path doesn't find the file
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = None

        # patch this so we don't overwrite the proper ini file
        mdata = mocker.patch.object(man_config.ConfigData, '_get_filename')
        mdata.return_value = os.path.join(tmp_path, 'mancala.ini')

        config = man_config.ConfigData()

        assert config._config['default'] == man_config.DEFAULTS
        assert 'difficulty' not in config._config['default']


    def test_junk_file(self, mocker, tmp_path):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""junk in the file""", file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        # patch this so we don't overwrite the proper ini file
        mdata = mocker.patch.object(man_config.ConfigData, '_get_filename')
        mdata.return_value = path

        config = man_config.ConfigData()

        assert config._config['default'] == man_config.DEFAULTS


    def test_no_default(self, mocker, tmp_path):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""[section]
                  keyword""", file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        # patch this so we don't overwrite the proper ini file
        mdata = mocker.patch.object(man_config.ConfigData, '_get_filename')
        mdata.return_value = path

        config = man_config.ConfigData()

        assert config._config['default'] == man_config.DEFAULTS


    def test_bad_values(self, mocker, tmp_path):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""[default]
                  button_size = 20
                  difficulty = 2
                  grid_density = 33
                  ai_delay = 10
                  log_level = ten""", file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        config = man_config.ConfigData()
        # print(list(config._config['default'].items()))

        # good values
        assert config['button_size'] == '20'

        # diff is not in default dict, must use get_int
        with pytest.raises(KeyError):
            config._config['difficulty']
        assert config.get_int('difficulty', 0) == 2

        # bad values
        assert config['grid_density'] == man_config.DEFAULTS['grid_density']
        assert config['ai_delay'] == man_config.DEFAULTS['ai_delay']
        assert config['log_level'] == man_config.DEFAULTS['log_level']


    def test_bad_difficulty(self, mocker, tmp_path):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""[default]
                  button_size = 20
                  difficulty = 33
                  """, file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        config = man_config.ConfigData()

        assert config['button_size'] == '20'
        assert 'difficulty' not in config._config


    def test_get_int(self, mocker, tmp_path):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""[default]
                  button_size = astring
                  font_size = -5
                  """, file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        config = man_config.ConfigData()

        # difficult is not in the default dictionary
        with pytest.raises(KeyError):
            config.get_int('difficulty')
        assert config.get_int('difficulty', 0) == 0

        # missing key, get_int handled differently with default or not
        assert config.get_int('grid_density', 20) == 20
        assert config.get_int('grid_density') \
            == int(man_config.DEFAULTS['grid_density'])

        # bad values reverted to defaults
        assert config.get_int('button_size') \
            == int(man_config.DEFAULTS['button_size'])

        assert config.get_int('font_size') \
            == int(man_config.DEFAULTS['font_size'])


    def test_get_bool(self, mocker, tmp_path):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""[default]
                  log_live = astring
                  show_tally = -5
                  ai_active = yes
                  touch_screen = true
                  true_value = TRUE
                  """, file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        config = man_config.ConfigData()

        # missing or bad values revert to False
        assert not config.get_bool('log_live')
        assert not config.get_bool('show_tally')
        assert not config.get_bool('junk_key')

        assert config.get_bool('ai_active')
        assert config.get_bool('touch_screen')
        assert config.get_bool('true_value')


    @pytest.fixture
    def tk_root(self):
        """Create a tk app and then clean up after it.
        This will pop a window up on the screen.
        This will occationally report that tcl is not
        installed properly!"""

        root = tk.Tk()
        yield root

        root.after(20, root.destroy)
        root.mainloop()
        root.update()


    @pytest.mark.parametrize('family, size, weight',
                              [('', '', ''),
                              ('Serif', '', ''),
                              ('Times', '20', 'bold'),
                              ])
    def test_get_font(self, mocker, tmp_path, family, size, weight, tk_root):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print(f"""[default]
                  font_family = {family}
                  size = {size}
                  weight = {weight}
                  """, file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        config = man_config.ConfigData(tk_root)

        assert isinstance(config.get_font(), tk.font.Font)


    def test_colors(self, mocker, tmp_path, tk_root):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""[default]
                  system_color = SystemButtonFace
                  turn_color = #303030
                  turn_dark_color = not_a_color
                  inactive_color = #1234567890
                  """, file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        config = man_config.ConfigData(tk_root)

        assert config['system_color'] == 'SystemButtonFace'
        assert config['turn_color'] == '#303030'

        assert config['turn_dark_color'] == \
            man_config.DEFAULTS['turn_dark_color']
        assert config['inactive_color'] == \
            man_config.DEFAULTS['inactive_color']


    def test_game_overrides(self, mocker, tmp_path):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print("""[default]
                  button_size = 20
                  grid_density = 25
                  [my_game]
                  button_size=40""", file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        config = man_config.ConfigData(None, 'diff game')
        assert config['button_size'] == '20'
        assert config['grid_density'] == '25'

        config = man_config.ConfigData(None, 'my game')
        assert config['button_size'] == '40'
        assert config['grid_density'] == '25'


@pytest.mark.animator
class TestPreloadCfg:

    @pytest.mark.parametrize('contents, eres',
                             [("""[default]
                                   button_size = 80
                                   """, True),
                              ("""[default]
                                   disable_animator = no
                                   """, True),
                              ("""[default]
                                  disable_animator = yes
                                  """, False),
                             ], ids=['case0', 'case1', 'case2'])
    def test_dis_animator(self, mocker, tmp_path, contents, eres):

        path = os.path.join(tmp_path, 'mancala.ini')
        with open(path, 'w', encoding='utf-8') as file:
            print(contents, file=file)

        # man_path finds the file where we just put it
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = path

        man_config.check_disable_animator()
        assert animator.ENABLED == eres


    def test_dis_ani_no_file(self, mocker, tmp_path):

        # man_path doesn't find the file
        mpath = mocker.patch.object(man_path, 'get_path')
        mpath.return_value = None

        # patch this so we don't overwrite the proper ini file
        mdata = mocker.patch.object(man_config.ConfigData, '_get_filename')
        mdata.return_value = os.path.join(tmp_path, 'mancala.ini')

        man_config.check_disable_animator()
        assert animator.ENABLED
