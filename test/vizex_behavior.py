# -*- coding: utf-8 -*-
"""

pytest -s test\vizex_behavior.py


Created on Sun Aug 13 01:42:21 2023
@author: Ann"""

import pytest

from context import btn_behaviors as btnb
from context import game_interface as gi
from context import man_config
from context import mancala_ui


def rnd_move_test_one(pathname, board, store, turn):

    game, pdict = man_config.make_game(pathname)
    print("Constructed game:")
    print(game)

    game_ui = mancala_ui.MancalaUI(game, pdict)

    game.board = board
    game.store = store
    game.turn = turn
    print("Test setup:")
    print(game)

    game.new_game(win_cond=gi.WinCond.WIN, new_round_ok=True)
    print("New game:")
    print(game)

    game_ui.set_game_mode(btnb.Behavior.RNDMOVE)
    game_ui.mainloop()


@pytest.mark.parametrize('turn', (False, True))
@pytest.mark.parametrize('store', ((52, 28), (28, 52)))
def test_rnd_move(turn, store):

    config_file = 'GameProps/Giuthi.txt'
    board = tuple([0] * 16)

    print(f'RNDMOVE: Giuthi    store={store}  turn={turn} ')
    rnd_move_test_one(config_file, list(board), list(store), turn)

    assert input('Pass? ') == 'y'



def rnd_choose_test_one(pathname, board, store, turn):

    game, pdict = man_config.make_game(pathname)
    game_ui = mancala_ui.MancalaUI(game, pdict)
    print("Constructed game:")
    print(game)

    game.board = board
    game.blocked = [not bool(seeds) for seeds in board]
    game.store = store
    game.turn = turn
    print("Test setup:")
    print(game)

    game.new_game(win_cond=gi.WinCond.WIN, new_round_ok=True)
    print("New game:")
    print(game)

    game_ui.set_game_mode(btnb.Behavior.RNDCHOOSE)
    game_ui.mainloop()


@pytest.mark.parametrize('turn', (False, True))
@pytest.mark.parametrize('winner', (False, True))
def test_rnd_choose(turn, winner):

    config_file = 'GameProps/Bechi.txt'

    lside = (4, 0, 0, 4)
    wside = (4, 4, 4, 4)

    if winner:
        store = [2, 6]
        board = lside + wside
    else:
        store = [6, 2]
        board = wside + lside

    print(f'RNDCHOOSE: Bechi    store={store}  turn={turn} ')
    rnd_choose_test_one(config_file, list(board), list(store), turn)

    assert input('Pass? ') == 'y'
