# -*- coding: utf-8 -*-
"""Test the config file by running the contructors
for game_consts and game_info which do the error
checking.

Warngings are set to be test failures for all but
all_params.txt.
One warning is accepted from all_params.txt:
No capture mechanism provided
any other errors will generate a warning.

Created on Sun Jul 23 11:29:10 2023
@author: Ann
"""

import os

import pytest

# this file contains integration tests
# report warnings as test failures
pytestmark = [pytest.mark.integtest, pytest.mark.filterwarnings("error")]

from context import ai_player
from context import man_config


PATH = './GameProps/'
FILES = os.listdir(PATH)


BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)

@pytest.mark.parametrize('file', FILES)
def test_config_files(file):

    game, pdict = man_config.make_game(PATH + file)
    ai_player.AiPlayer(game, pdict)


def test_bad_file():

    with pytest.warns(UserWarning) as record:
        man_config.read_game_config(PATH + BAD_CFG)

    assert len(record) == 1
    assert 'No capture mechanism provided' in record[0].message.args[0]
