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

# this file contains integration tests
# report warnings as test failures
pytestmark = [pytest.mark.integtest, pytest.mark.filterwarnings("error")]


from context import ai_player
from context import cfg_keys as ckey
from context import game_constants as gconsts
from context import game_info as gi
from context import man_config
from context import round_tally


PATH = './GameProps/'
FILES = os.listdir(PATH)


BAD_CFG = '_all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)

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

    game_dict = man_config.read_game(PATH + filename)

    # status is used for indevelopment files, not releases
    assert "status" not in game_dict.keys()
    assert "Status" not in game_dict.keys()


    vparams = game_dict.get(ckey.VARI_PARAMS, {})
    for key, value in vparams.items():
        # don't comment this print; it's the only way to find an error
        print(f"VARI_PARAM check {key}")

        # all vari_params keys are game options
        assert key in PARAM_DICT

        # lists only contain integers
        if isinstance(value, list):
            assert all(isinstance(val, int) for val in value)

            # the non-variant option is in the list
            if key == ckey.GAME_CLASS:
                assert game_dict[ckey.GAME_CLASS] in value

            elif key in game_dict[ckey.GAME_CONSTANTS]:
                assert game_dict[ckey.GAME_CONSTANTS][key] in value

            elif key in game_dict[ckey.GAME_INFO]:
                assert game_dict[ckey.GAME_INFO][key] in value

            else:
                # this is an assumption of the default value
                # pretty sure all params whose default is not
                # zero are always included in the config file
                assert 0 in value

    # if goal_param would be useful, check to see that it's included
    # this isn't really required but would be nice
    if vparams:
        goal = game_dict[ckey.GAME_INFO].get(ckey.GOAL, gi.Goal.MAX_SEEDS)
        rounds = game_dict[ckey.GAME_INFO].get(ckey.ROUNDS, 0)

        if ((rounds and goal in (gi.Goal.MAX_SEEDS, gi.Goal.TERRITORY))
            or goal in round_tally.RoundTally.GOALS):
            assert ckey.GOAL_PARAM in vparams

    if ckey.VARIANTS in game_dict:
        variants = game_dict[ckey.VARIANTS]

        # one for the default and one more or why have it?
        assert len(variants) >= 2

        # first item has an empty dictionary
        vlist = list(variants.items())
        assert isinstance(vlist[0][1], dict)
        assert vlist[0][1] == {}

        # all spec'ed parameters are game options
        for key, vdict in variants.items():
            # don't comment this print; it's the only way to find an error
            print(f"VARIANT check {key}")
            assert isinstance(vdict, dict)

            for param, value in vdict.items():

                # all parameters keys are game options
                assert param in PARAM_DICT


def test_bad_file():

    with pytest.raises(gconsts.GameConstsError):
        man_config.make_game(PATH + BAD_CFG)
