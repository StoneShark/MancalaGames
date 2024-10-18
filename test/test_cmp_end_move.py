# -*- coding: utf-8 -*-
"""These tests start by verifying the game configurations and
expected end games.  End games don't occur often and this behavior
is  of more concern than finding configurations not tested in the games.

The purpose of the game config tests is two fold:

    1. confirm the ender deco chain has the parameters set as expected
    2. games end as expected per game rules

Created on Tue Oct 15 13:53:14 2024
@author: Ann"""


# %% imports

import collections
import os

import pytest

from context import end_move
from context import game_interface as gi
from context import mancala


pytestmark = [pytest.mark.integtest]


# %% constants

PATH = './GameProps/'
FILES = os.listdir(PATH)


BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


# %% ender config

# these parameters control how the ender works at run-time
# they do not control how the ender deco chain is built

Config = collections.namedtuple('Config',
                                ['win_seeds', 'min_needed', 'rnd_req_seeds'],
                                defaults=[0])

CONFIG_CASES = {
    'Ayoayo': Config(24, 0),       # NoOutcomeChange should not be included
    'Bao_Kenyan': Config(16, 2),
    'Bao_Tanzanian': Config(55, 2, 4),

}


class TestEnderConfig:
    """check the parameters of the ender"""

    @pytest.fixture
    def econfig(self, request):
        """Use with indirect to look up the expected configuration
        from the game config file name.

        We want tests for which there is no expected config to
        be shown as skipped."""
        key = request.param[:-4]
        if key in CONFIG_CASES:
            return CONFIG_CASES[key]

        return None

    @staticmethod
    def find_ender_deco(game, dclass):

        deco = game.deco.ender
        while deco and not isinstance(deco, dclass):
            deco = deco.decorator

        return deco


    @pytest.mark.parametrize('game_pdict, econfig',
                             zip(FILES, FILES),
                             indirect=True)
    def test_game_const(self, game_pdict, econfig):
        """Test that the game and ender are configured/constructed
        as expected. If file wasn't translated to a Config
        named tuple skip the test for (econfig)."""

        if econfig is None:
            pytest.skip('No econfig')

        game, _ = game_pdict

        assert game.deco.ender.win_seeds == econfig.win_seeds

        nooutcome = self.find_ender_deco(game, end_move.NoOutcomeChange)
        if econfig.min_needed:
            assert nooutcome
            assert nooutcome.min_needed == econfig.min_needed
        else:
            assert not nooutcome

        # set to zero for no rounds, find round ender and check req_seeds
        if not econfig.rnd_req_seeds:
            return

        rnd_ender = self.find_ender_deco(game, end_move.RoundWinner)
        assert rnd_ender
        assert rnd_ender.req_seeds == econfig.rnd_req_seeds


# %% end game tests

# don't check the winner result
DONT_CARE = -5


def make_state(board, store, turn=False):
    return mancala.GameState(board=board,
                             store=store,
                             _turn=turn,
                             mcount=25)


#  test case # are counted with in each game

END_CASES = {
    'Ayoayo': [
        # 0:
        [make_state(board=(1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
                    store=(23, 23)),
         None, DONT_CARE],
        # 1:
        [make_state(board=(0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
                    store=(25, 22)),
         gi.WinCond.WIN, False],
        # 2:
        [make_state(board=(2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0),
                    store=(5, 26)),
         gi.WinCond.WIN, True],

        # 3: no moves
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
                    store=(24, 23),
                    turn=True),
         gi.WinCond.TIE, DONT_CARE],

        # 4: next player can't share, game ended
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
                    store=(24, 23),
                    turn=False),
         gi.WinCond.TIE, DONT_CARE],

        # 5: False has no move, True win
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
                    store=(23, 24),
                    turn=True),
         gi.WinCond.WIN, True],

        # 6: False has no move, True win
        # T can share doesn't matter, because they just moved
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                    store=(23, 24),
                    turn=True),
         gi.WinCond.WIN, True],

        # 7:  True has a move but can't share, True win
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
                    store=(23, 24),
                    turn=False),
         gi.WinCond.WIN, True],

        # 8: True can share, game not over
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                    store=(23, 23),
                    turn=False),
         None, DONT_CARE],

        # 9: removing NoOutcomeChange changed the result
        # was TIE which is ultimate outcome (but not for another move)
        [make_state(board=(0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                    store=(24, 23),
                    turn=True),
         None, DONT_CARE],

        # 10: removing NoOutcomeChange changed the result
        # was TIE which is WRONG
        # T should win this game (but not for another move)
        [make_state(board=(0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                    store=(23, 24),
                    turn=True),
         None, DONT_CARE],

    ],

    'Bao_Kenyan': [
        #                  1  2  3  4  5  6  7  8\/
        # 0: not over
        [make_state(board=(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
                    store=(15, 15)),
         None, DONT_CARE],
        # 1: F max seed win
        [make_state(board=(0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(17, 14)),
         gi.WinCond.WIN, False],
        # 2: T max seed win
        [make_state(board=(2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(5, 17)),
         gi.WinCond.WIN, True],

        # 3: Tie game - no moves
        [make_state(board=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                    store=(8, 8)),
         gi.WinCond.TIE, DONT_CARE],

        # 4: true moved, False has a move but NoOutcomeChange gets seed and ties
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(15, 16),
                    turn=True),
         gi.WinCond.TIE, DONT_CARE],

        # 5:  true moved, false has no move, True collects seed
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
                    store=(15, 16),
                    turn=True),
         gi.WinCond.WIN, True],

        # 6: end of F turn but T doesn't have a move, collect seeds F wins
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(16, 15),
                    turn=False),
         gi.WinCond.WIN, False],

        # 7: end of T turn but F doesn't have a move, collect seeds T wins
        [make_state(board=(0, 0, 0, 0, 0, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0),
                    store=(11, 14),
                    turn=True),
         gi.WinCond.WIN, True],
        # 8: even though F doesn't have a move, F still wins after collecting seeds
        [make_state(board=(0, 0, 0, 0, 0, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0),
                    store=(14, 11),
                    turn=True),
         gi.WinCond.WIN, False],

    ],
}


def end_cases(files):
    """Build the applicable test case list based
    on the contents of files and END_CASES."""

    for config_file in files:
        gname = config_file[:-4]
        if gname in END_CASES:
            for test_case in END_CASES[gname]:
                yield [config_file] + test_case


def case_ids(files):
    """Build a list of easy to understand case names.
    Order must exactly match end_cases.
    Count cases w/i each game config and translate the
    win condition and winner to good names."""

    for config_file in files:
        gname = config_file[:-4]
        if gname in END_CASES:
            for idx, (state, cond, winner) in enumerate(END_CASES[gname]):
                cname = cond.name if cond else "None"
                wname = winner if winner > DONT_CARE else "DC"
                yield f"{gname}-case{idx}-{cname}-{wname}"


class TestEndGames:

    def test_end_cases(self):
        """Assure that all END_CASES keys are actual config'ed games.
        Cases for test_end_game are collected by FILES, so if
        any END_CASES keys are not actual files, the tests won't be run."""

        assert all(cfg + '.txt' in FILES for cfg in END_CASES.keys())


    @pytest.mark.usefixtures('logger')
    @pytest.mark.parametrize('game_pdict, gstate, econd, ewinner',
                             end_cases(FILES), indirect=['game_pdict'],
                             ids=case_ids(FILES))
    def test_end_game(self, game_pdict, gstate, econd, ewinner):

        game, _ = game_pdict
        game.state = gstate
        print(game)
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
            "Test Config Error: missing seeds"

        cond, winner = game.deco.ender.game_ended(repeat_turn=False,
                                                  ended=False)
        print(game)

        assert cond == econd
        if ewinner != DONT_CARE:
            assert winner == ewinner
