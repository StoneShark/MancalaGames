# -*- coding: utf-8 -*-
"""Test the config file by running the contructors
for game_consts and game_info which do the error
checking.

Warngings are set to be test failures for all but
_all_params.txt.
One warning is accepted from _all_params.txt:
No capture mechanism provided
any other errors will generate a warning.

Created on Sun Jul 23 11:29:10 2023
@author: Ann
"""

import os

import pytest

from context import game_constants as gc

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


def test_bad_file():

    with pytest.raises(gc.GameConstsError):
        man_config.read_game_config(PATH + BAD_CFG)
