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

import os

import pytest

from context import game_constants as gconsts

# this file contains integration tests
# report warnings as test failures
pytestmark = [pytest.mark.integtest, pytest.mark.filterwarnings("error")]

from context import ai_player
from context import man_config


PATH = './GameProps/'
FILES = os.listdir(PATH)


BAD_CFG = '_all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)



@pytest.mark.parametrize('game_pdict', FILES, indirect=True)
def test_config_files(game_pdict):

    game, pdict = game_pdict
    ai_player.AiPlayer(game, pdict)


@pytest.mark.parametrize('filename', FILES)
def test_no_status(request, filename):
    """Fail if any game files have a tag of status,
    this is mean for development and testing not release.

    The config.cache checks against the keys created by
    the global fixture game_pdict, in an attempt to only
    generate one failure report for each game file with
    an error."""

    key_name = filename.replace('.', '_') + '_failed'
    if request.config.cache.get(key_name, False):
        pytest.xfail("Game cfg error (again)")

    game_dict = man_config.read_game(PATH + filename)
    assert "status" not in game_dict


def test_bad_file():

    with pytest.raises(gconsts.GameConstsError):
        man_config.make_game(PATH + BAD_CFG)
