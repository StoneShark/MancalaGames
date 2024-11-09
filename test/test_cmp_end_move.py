# -*- coding: utf-8 -*-
"""These tests start by verifying the game configurations and
expected end games.  End games don't occur often and this behavior
is of more concern than finding configurations not tested in the games.

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


N = None
T = True
F = False

REPEAT_TURN = True
ENDED = True


# %% ender config

"""
These parameters control how the ender works at run-time
they do not control how the ender deco chain is built

  win_seeds is in base class, > win_seeds wins the game

  min_needed is in NoOutcomeChange, if seeds <  min_needed for either player
  the game outcome cannot change, end it

  rnd_req_seeds is req_seeds in RoundWinner, number of seeds required by
  either player to start a new round (otherwise a new game is started)

"""

Config = collections.namedtuple('Config',
                                ['win_seeds', 'min_needed', 'rnd_req_seeds'],
                                defaults=[0, 0])

CONFIG_CASES = {
    'Ayoayo': Config(24),       # mustshare no NoOutcomeChange
    'Bao_Kenyan': Config(16, 2),
    'Bao_Tanzanian': Config(55, 2, 4),  # child but capt also
    'Bechi': Config(4*6*2 - 1, 0, 6),  # NoOutcomeChange dupl EndGameNotPlayable  (NOC dupl EGNP)
    'Bosh': Config(5*4*2 - 1, 2, 4),
    'Cow': Config(5*5),   # NOC dupl EGNP
    'Dabuda': Config(10*4, 2),
    'Dakon': Config(7*7*2 - 1, 0, 7*4),
    'Deka': Config(-1),   # DEPRIVE games no win_seeds, rounds or NoOutcomeChange
    'Depouiller': Config(-1),   # DEPRIVE

    'Diffusion': Config(-1),  # Diffusion class
    'DiffusionV2': Config(-1),  # DiffusionV2 class

    'Endodoi': Config(8*4, 2),
    'Enkeshui': Config(24, 2),   # start pattern
    'Enlightenment': Config(-1),
    'Erherhe': Config(6*4, 0, 8) ,  # mustshare
    'Eson_Xorgol': Config(5*9, 3),
    'Gabata': Config(4*6*2 - 1, 0, 11),   # only children
    'Gamacha': Config(-1),
    'Giuthi': Config(8*6*2 - 1, 0, 9),  # NOC dupl EGNP; UMOVE: 1 seed in 7 holes, 2 in 1 hole
    'Goat': Config(3*3),
    'J_Odu': Config(8*4, 2),
    'Kalah': Config(6*4),

    'Lagerung': Config(7*7*2 - 1, 0, 7*4),
    'Lami': Config(10*2*2 - 1, 2, 2),
    'Lamlameta': Config(12*2*2 - 1, 2, 2*4),
    'Lam_Waladach': Config(6*3*2 - 1, 0, 11),  # pick2xlastseeds no NoOutcomeChange
    'Leyla-Gobale': Config(8*4, 2),
    'Longbeu-a-cha': Config(5*5, 2),
    'Mbangbi': Config(5*8),  # NOC dupl EGNP
    'Mbothe': Config(10*2, 2),
    'Nambayi': Config(-1),
    'NamNam': Config(6*4*2 - 1, 0, 11),  # picklastseeds no NoOutcomeChange

    'Ndoto': Config(8*2, 2),
    'NoCapt': Config(6*4),   # sow_own_store
    'NoSides': Config(5*2, 2),
    'NoSidesChild': Config(7*2, 2),
    'NumNum': Config(6*4*2 - 1, 0, 11),  # picklastseeds no NoOutcomeChange
    'Olinda': Config(7*4*2 - 1, 0, 4),   # picklastseeds no NoOutcomeChange
    'Ot-tjin': Config(10*3, 3),
    'Oware': Config(6*4),   # mustshare
    'Pallam_Kuzhi': Config(7*4*2 - 1, 2, 4),
    'Pandi': Config(7*5*2 - 1, 2, 5),

    'Qelat': Config(6*4),  # WALDA seeds in play or waldas, don't need NoOutcomeChange
    'Sadeqa': Config(-1),
    'Songo': Config(7*5),  # mustshare
    'SowOpDirs': Config(5*4, 2),
    'Tapata': Config(-1),
    'Toguz_Xorgol': Config(9*9, 4),  # min capt = 4
    'Vai_Lun_Thlan': Config(6*5),  # capt on 1s
    'Valah': Config(5*3),  # sow_own_store
    'Wari': Config(6*4),  # mustshare
    'Weg': Config(6*4*2 - 1, 0, 11),

    'XCaptSowOwn': Config(6*4),
}


class TestEnderConfig:
    """check the parameters of the ender"""

    @pytest.fixture
    def econfig(self, request):
        """Use with indirect to look up the expected configuration
        from the game config file name."""
        key = request.param[:-4]
        if key in CONFIG_CASES:
            return CONFIG_CASES[key]

        return None


    @staticmethod
    def find_ender_deco(game, dclass):
        """Find the deco of the specified class, return None
        if there is no deco of the specified type"""

        deco = game.deco.ender
        while deco and not isinstance(deco, dclass):
            deco = deco.decorator

        return deco


    @pytest.mark.parametrize('game_pdict, econfig',
                             zip(FILES, FILES),
                             ids=[f[:-4] for f in FILES],
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

        rnd_ender = self.find_ender_deco(game, end_move.RoundWinner)
        if econfig.rnd_req_seeds:
            assert rnd_ender
            assert rnd_ender.req_seeds == econfig.rnd_req_seeds
        else:
            assert not rnd_ender


# %% end move tests

# don't check the winner result
DONT_CARE = -5


def make_state(board, store, turn=False, **kwargs):
    """Helper function to make game states.
    Don't care about mcount, const > 1 is fine."""

    return mancala.GameState(board=board,
                             store=store,
                             _turn=turn,
                             mcount=25,
                             **kwargs)


#  test case ids are counted within each game (see make_cases)
#  test case element order:
#      gstate, econd, ewinner, [repeat_turn, ended]


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

    ],  # end Ayoayo

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

    ],  # end Bao_Kenyan

    'Bao_Tanzanian': [
        #                  1  2  3  4  5  6  7\/7  6  5  4  3  2  1
        # 0: start game
        [make_state(board=(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
                    store=(0, 0),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         None, DONT_CARE],

        # 1: four seeds still in play
        [make_state(board=(0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0),
                    store=(0, 52),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         None, DONT_CARE],

        # 2: four seeds still in play
        [make_state(board=(0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0),
                    store=(52, 0),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         None, DONT_CARE],

        # 3: true collected all seeds, no children
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(0, 56),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.WIN, True],

        # 4: false collected all seeds, no children
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(56, 0),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.WIN, False],

        # 5: not enough seeds to do a cross capt
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
                    store=(0, 55),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.WIN, True],

        # 6: not enough seeds to do a cross capt
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
                    store=(55, 0),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.WIN, False],

        # 7: pure tie round
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(28, 28),
                    child=(N, N, N, N, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.ROUND_TIE, DONT_CARE],

        # 8: tie in children
        [make_state(board=(14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14),
                    store=(0, 0),
                    child=(T, F, N, N, N, N, N, N, N, N, N, N, T, F),
                    istate=(F, F, F, F)),
         gi.WinCond.ROUND_TIE, DONT_CARE],

        # 9: T has most seeds in children, but no moves on next turn
        # F has enough seeds to fill a few holes
        [make_state(board=(0, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(16, 0),
                    turn=False,
                    child=(N, T, T, T, T, T, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.ROUND_WIN, True],

        # 10: T has most seeds in children, but no moves on next turn
        # playable seeds all on F side
        [make_state(board=(8, 10, 10, 10, 10, 8, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(0, 0),
                    turn=False,
                    child=(N, T, T, T, T, T, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.ROUND_WIN, True],

        # 11: F just enough seeds to fill one hole
        [make_state(board=(12, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(4, 0),
                    turn=False,
                    child=(T, T, T, T, T, T, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.ROUND_WIN, True],

        # 12: T not enough holes to fill a hole
        [make_state(board=(13, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(0, 3),
                    turn=False,
                    child=(F, F, F, F, F, F, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         gi.WinCond.WIN, False],

        # 13: (case 5 but child) not enough seeds to do a cross capt, game continues
        [make_state(board=(0, 0, 0, 20, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
                    store=(0, 35),
                    child=
                          (N, N, N, T, N, N, N, N, N, N, N, N, N, N),
                    istate=(F, F, F, F)),
         None, DONT_CARE],

    ],  # end Bao_Tanzanian

    'Bechi': [
        #                  1  2  3  4\/4  3  2  1
        # 0: start game
        [make_state(board=(6, 6, 6, 6, 6, 6, 6, 6),
                    store=(0, 0),
                    unlocked=(F, F, F, F, F, F, F, F)),  # is not used in the ender
         None, DONT_CARE],

        # 1: tie game
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0),
                    store=(24, 24)),
         gi.WinCond.ROUND_TIE, DONT_CARE],

        # 2: T all seeds, ClearWinner ends
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0),
                    store=(0, 48)),
         gi.WinCond.WIN, True],

        # 3: F all seeds, ClearWinner ends
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0),
                    store=(48, 0)),
         gi.WinCond.WIN, False],

        # 4: not playable, EndTurnNotPlayable ends
        [make_state(board=(0, 0, 1, 0, 0, 1, 0, 0),
                    store=(6, 40),
                    turn=True),
         gi.WinCond.ROUND_WIN, True],

        # 5: not playable, EndTurnNotPlayable ends
        [make_state(board=(0, 1, 0, 0, 0, 0, 1, 0),
                    store=(40, 6),
                    turn=False),
         gi.WinCond.ROUND_WIN, False],

        # 6: playable by False but not True (False's turn)
        [make_state(board=(0, 0, 2, 0, 0, 1, 0, 0),
                    store=(6, 39),
                    turn=True),
         None, DONT_CARE],

        # 7: playable by False but not True, True would pass
        [make_state(board=(0, 0, 2, 0, 0, 1, 0, 0),
                    store=(39, 6),
                    turn=False),
         None, DONT_CARE],

    ],  # end Bechi

    'Cow': [
        #                  1  2  3  4  5\/5  4  3  2  1
        # 0: start game
        [make_state(board=(5, 5, 5, 5, 5, 5, 5, 5, 5, 5),
                    store=(0, 0)),
         None, DONT_CARE],

        # 1: no moves, TIE
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(25, 25)),
         gi.WinCond.TIE, DONT_CARE],

         # 2: no win
         [make_state(board=(0, 2, 2, 0, 0, 0, 0, 2, 2, 0),
                     store=(25, 17)),
          None, DONT_CARE],

         # 3: WIN by F
         [make_state(board=(0, 2, 2, 0, 0, 0, 0, 2, 2, 0),
                     store=(26, 16)),
          gi.WinCond.WIN, False],

        # 5: no moves for T, WIN by T
        [make_state(board=(0, 0, 2, 0, 0, 0, 0, 0, 0, 0),
                    store=(10, 38),
                    turn=False),
         gi.WinCond.WIN, True],

        ],   # end Cow

    'Dakon': [
        #                  1  2  3  4  5  6  7\/7  6  5  4  3  2  1
        # 0: start game
        [make_state(board=(7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7),
                    store=(0, 0)),
         None, DONT_CARE],

        # 1: TIE game, no moves
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(49, 49)),
         gi.WinCond.ROUND_TIE, DONT_CARE],

        # 2: T all seeds, ClearWinner ends, RoundWinner leaves
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(0, 98)),
         gi.WinCond.WIN, True],

        # 3: F all seeds, ClearWinner ends, RoundWinner leaves
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(98, 0)),
         gi.WinCond.WIN, False],

        # 4: not playable, EndTurnNotPlayable ends, 5 holes so RoundWinner changes
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(58, 40)),
         gi.WinCond.ROUND_WIN, False],

        # 5: not playable, EndTurnNotPlayable ends,
        #    RoundWinner leaves, not enough seeds for 4 holes
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(27, 71)),
         gi.WinCond.WIN, True],

        # 6: not playable, EndTurnNotPlayable ends,
        #    RoundWinner leaves, exactly enough seeds for 4 holes
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(28, 70)),
         gi.WinCond.ROUND_WIN, True],

        # 7: playable by False but not True (False's turn)
        [make_state(board=(2, 2, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(45, 39),
                    turn=True),
         None, DONT_CARE],

        # 8: playable by False but not True, True would pass
        [make_state(board=(2, 2, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(39, 45),
                    turn=False),
         None, DONT_CARE],

        ],   # end Dakon

    'Deka': [    # deprive game
        #                  1  2  3  4  5  6\/6  5  4  3  2  1
        # 0: start game
        [make_state(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                    store=(0, 0),
                    blocked=(F, F, F, F, F, F, F, F, F, F, F, F)), # not used in ender
         None, DONT_CARE],

        # 1: False gave away their seeds, but it will be True's turn
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0),
                    store=(17, 0),   # seeds out of play
                    turn=False),
         None, DONT_CARE],

        # 2: False has no seeds, True captured them
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0),
                    store=(17, 0),
                    turn=True),
         gi.WinCond.WIN, True],

        ],  # end Deka

    'Depouiller': [    # deprive game
        #                  1  2  3  4  5\/5  4  3  2  1
        # 0: start game
        [make_state(board=(2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                    store=(0, 0)),
         None, DONT_CARE],

        # 1: False gave away their seeds, but it will be True's turn
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0),
                    store=(13, 0),   # seeds out of play
                    turn=False),
         None, DONT_CARE],

        # 3: False has no seeds, True captured them
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0),
                    store=(13, 0),
                    turn=True),
         gi.WinCond.WIN, True],

        ],  # end Depouiller

    'Kalah': [
        #                  1  2  3  4  5  6\/6  5  4  3  2  1
        # 0: start game
        [make_state(board=(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
                    store=(0, 0)),
         None, DONT_CARE],

        # 1: False has no moves, TIE after collecting seeds
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 4, 0),
                    store=(24, 13),
                    turn=True),
         gi.WinCond.TIE, DONT_CARE],

        # 2: True has no moves, False wins by collecting own seeds
        [make_state(board=(0, 4, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0),
                    store=(24, 13),
                    turn=False),
         gi.WinCond.WIN, False],

        # next two cases are same as prev two but turn changed and repeat turn set

        # 3: False sowed final seed into their own store, TIE after collecting seeds
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 4, 0),
                    store=(24, 13),
                    turn=False),
         gi.WinCond.TIE, DONT_CARE, REPEAT_TURN, False],

        # 4: True sowed final seed into their own store,
        #    False wins by collecting own seeds
        [make_state(board=(0, 4, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0),
                    store=(24, 13),
                    turn=True),
         gi.WinCond.WIN, False, REPEAT_TURN, False],

        ],   # end kalah

    'Qelat': [
        #                  1  2  3  4  5  6\/6  5  4  3  2  1
        # 0: start game
        [make_state(board=(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
                    store=(0, 0),
                    child=[N, N, N, N, N, N, N, N, N, N, N, N]),
         None, DONT_CARE],

        # 1: not enough seeds for win
        [make_state(board=(20, 4, 2, 2, 2, 2, 2, 2, 2, 0, 5, 5),
                    store=(0, 0),
                    child=[T, T, N, N, N, N, N, N, N, N, F, F]),
         None, DONT_CARE],

        # 2: just enough seeds for win
        [make_state(board=(20, 5, 2, 2, 2, 2, 2, 2, 2, 0, 4, 5),
                    store=(0, 0),
                    child=[T, T, N, N, N, N, N, N, N, N, F, F]),
         gi.WinCond.WIN, True],

        # 3: force walda collection, ClearWinner but seeds in store
        #      these force conditions are not possible in game play
        [make_state(board=(20, 5, 2, 2, 2, 2, 2, 0, 0, 0, 4, 5),
                    store=(2, 2),
                    child=[T, T, N, N, N, N, N, N, N, N, F, F]),
         gi.WinCond.WIN, True],

        # 4: force walda collection, both
        [make_state(board=(10, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4),
                    store=(20, 6),
                    child=[T, T, N, N, N, N, N, N, N, N, F, F]),
         gi.WinCond.WIN, False],

        # 5: force walda collection, only T has walda's
        [make_state(board=(15, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3),
                    store=(20, 6),
                    child=[T, T, N, N, N, N, N, N, N, N, N, N]),
         gi.WinCond.WIN, True],

        # 6: force walda collection, only F has walda's
        [make_state(board=(15, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3),
                    store=(20, 6),
                    child=[F, F, N, N, N, N, N, N, N, N, N, N]),
         gi.WinCond.WIN, False],

        # 7: force walda collection, no waldas (not a real condition)
        #    EndGameWinner collects seeds and decides TIE,
        #    WaldaEndMove puts them back on the board
        [make_state(board=(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
                    store=(0, 0),
                    child=[N, N, N, N, N, N, N, N, N, N, N, N]),
         gi.WinCond.TIE, DONT_CARE, False, ENDED],

        # 8: Not playable, TIE
        [make_state(board=(20, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 20),
                    store=(0, 0),
                    child=[T, T, N, N, N, N, N, N, N, N, F, F]),
         gi.WinCond.TIE, DONT_CARE],

        # 9: Not playable, but ClearWinner detects F win
        [make_state(board=(20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 20),
                    store=(0, 0),
                    child=[T, T, N, N, N, N, N, N, N, N, F, F]),
         gi.WinCond.WIN, False],

        # 10: Not playable, but ClearWinner detects T win
        [make_state(board=(20, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20),
                    store=(0, 0),
                    child=[T, T, N, N, N, N, N, N, N, N, F, F]),
         gi.WinCond.WIN, True],


        ],  # end Qelat

    'Weg': [
        #                  1  2  3  4  5  6\/6  5  4  3  2  1
        # 0: start game
        [make_state(board=(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
                    store=(0, 0),
                    child=[N, N, N, N, N, N, N, N, N, N, N, N],
                    owner=[F, F, F, F, F, F, T, T, T, T, T, T]),
         None, DONT_CARE],

        # 1: end a new game (not the quitter)
        [make_state(board=(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
                    store=(0, 0),
                    child=[N, N, N, N, N, N, N, N, N, N, N, N],
                    owner=[F, F, F, F, F, F, T, T, T, T, T, T]),
         gi.WinCond.TIE, DONT_CARE, False, ENDED],

        # 2: clear winner
        [make_state(board=(0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(44, 0),
                    child=[N, F, N, N, N, N, N, N, N, N, N, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.WIN, False],

        # 3: not playable
        [make_state(board=(2, 2, 2, 0, 0, 0, 6, 0, 2, 0, 6, 0),
                    store=(14, 14),
                    child=[F, F, F, N, N, N, T, N, T, N, T, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.ROUND_WIN, True],

        # 4: not playable - no seeds in stores
        [make_state(board=(9, 9, 9, 0, 0, 0, 6, 0, 9, 0, 6, 0),
                    store=(0, 0),
                    child=[F, F, F, N, N, N, T, N, T, N, T, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.ROUND_WIN, False],

        # 5: Round Win - based on rounding, False
        [make_state(board=(10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(7, 11),
                    child=[F, F, F, N, N, N, T, N, T, N, T, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.ROUND_WIN, False],

        # 6: Round Win - based on rounding, True
        [make_state(board=(0, 0, 0, 0, 0, 0, 10, 0, 10, 0, 10, 0),
                    store=(11, 7),
                    child=[F, F, F, N, N, N, T, N, T, N, T, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.ROUND_WIN, True],

        # 7: game Win - can't round up, True
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(10, 38),
                    child=[F, F, F, N, N, N, T, N, T, N, T, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.WIN, True],

        # 8: game Win - can't round up, False
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(38, 10),
                    child=[F, F, F, N, N, N, T, N, T, N, T, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.WIN, False],

        # 9: round tie
        [make_state(board=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    store=(24, 24),
                    child=[F, F, F, N, N, N, T, N, T, N, T, N],
                    owner=[T, T, T, T, F, F, F, F, F, F, F, F]),
         gi.WinCond.ROUND_TIE, DONT_CARE],

    ] # end Weg
}


def make_cases():
    """Build the applicable test case list based
    on the contents of files and END_CASES.
    Give each an easy to understand case name:
    Count cases w/i each game config and translate the
    win condition and winner to good names."""

    for config_file in FILES:
        gname = config_file[:-4]
        if gname in END_CASES:

            for idx, test_case in enumerate(END_CASES[gname]):
                cond = test_case[1]
                winner = test_case[2]
                cname = cond.name if cond else "None"
                wname = winner if winner > DONT_CARE else "DC"

                yield pytest.param(config_file, test_case,
                                   id=f"{gname}-case{idx}-{cname}-{wname}")
        else:
            yield pytest.param(config_file, None,
                               id=f"{gname}")


class TestEndGames:

    def test_end_cases(self):
        """Assure that all END_CASES keys are actual config'ed games.
        Cases for test_end_game are collected by FILES, so if
        any END_CASES keys are not actual files, the tests won't be run."""

        assert all(cfg + '.txt' in FILES for cfg in END_CASES.keys())


    # @pytest.mark.usefixtures('logger')
    @pytest.mark.parametrize('game_pdict, test_case',
                             make_cases(), indirect=['game_pdict'])
    def test_end_game(self, game_pdict, test_case):


        if test_case is None:
            pytest.skip("no end game test cases")
            return

        gstate, econd, ewinner, *rest = test_case
        if rest:
            repeat_turn, ended = rest
        else:
            repeat_turn = False
            ended = False

        game, _ = game_pdict
        game.state = gstate
        # print(test_case)
        # print(game)
        assert sum(game.store) + sum(game.board) == game.cts.total_seeds, \
            "Test Config Error: seed count wrong"

        cond, winner = game.deco.ender.game_ended(repeat_turn=repeat_turn,
                                                  ended=ended)
        # print(game)

        assert cond == econd
        if ewinner != DONT_CARE:
            assert winner == ewinner
