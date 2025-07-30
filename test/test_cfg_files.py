# -*- coding: utf-8 -*-
"""Test the config file by running the contructors
for game_consts and game_info which do the error
checking.

Also, a top level tag named status is flagged as
a failure, game with status are not meant for
release.

Warngings are set to be test failures.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""


import pytest

# this file contains integration tests
# report warnings as test failures
pytestmark = [pytest.mark.integtest, pytest.mark.filterwarnings("error")]


from context import ai_player
from context import cfg_keys as ckey
from context import game_constants as gconsts
from context import man_config
from context import man_path
from context import variants


FILES = man_path.game_files()
PARAM_DICT = man_config.ParamData(no_descs=True)


@pytest.mark.parametrize('game_pdict', FILES, indirect=True)
def test_config_files(game_pdict):

    game, pdict = game_pdict
    ai_player.AiPlayer(game, pdict)


@pytest.mark.parametrize('filename', FILES)
def test_nonrule_checks(request, filename):
    """Check for errors that are not tested by the build
    rules.

    The config.cache checks against the keys created by
    the global fixture game_pdict, in an attempt to only
    generate one failure report for each game file with
    an error."""

    key_name = filename.replace('.', '_') + '_failed'
    if request.config.cache.get(key_name, False):
        pytest.xfail("Game cfg error (again)")

    game_dict = man_config.read_game(man_path.GAMEPATH + filename)

    # status is used for indevelopment files, not releases
    assert "status" not in game_dict.keys()
    assert "Status" not in game_dict.keys()
    assert "status" not in game_dict[ckey.GAME_INFO][ckey.ABOUT].lower()

    # don't raise an exception if there are no variations
    variants.test_variation_config(game_dict, no_var_error=False)


def test_bad_file():

    with pytest.raises(gconsts.GameConstsError):
        man_config.make_game(man_path.GAMEPATH + man_path.EX_GAME)
