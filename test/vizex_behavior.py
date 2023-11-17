# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 01:42:21 2023
@author: Ann"""

from context import btn_behaviors as btnb
from context import man_config
from context import mancala_ui


# %%  rndmove

# three cases:
#     f store < t store      - move on f side
#     f store > t store      - move on t side
#     f store == t store     - invalid case, shouldn't get to set_game_mode
#
# test both with True and False turns

def rnd_move_test_one(pathname, board, store, turn):

    game, pdict = man_config.make_game(pathname)
    game.board = board
    game.store =store
    game.turn = turn
    print(game)

    game_ui = mancala_ui.MancalaUI(game, pdict)
    game_ui.set_game_mode(btnb.Behavior.RNDMOVE)
    game_ui.mainloop()


def rnd_move_tests():

    config_file = 'GameProps/Giuthi.txt'
    board = tuple([2] * 16)

    for turn in (True, False):
        for store in [(44, 20), (20, 44)]:
            print(f'RNDMOVE: Giuthi    store={store}  turn={turn} ')
            rnd_move_test_one(config_file, list(board), list(store), turn)


# %%  rnd choose



def rnd_choose_test_one(pathname, board, store, turn):

    game, pdict = man_config.make_game('GameProps/Bechi.txt')

    game.board = board
    game.blocked = [not bool(seeds) for seeds in board]
    game.store = store
    game.turn = True
    print(game)

    game_ui = mancala_ui.MancalaUI(game, pdict)
    game_ui.set_game_mode(btnb.Behavior.RNDCHOOSE)
    game_ui.mainloop()


def rnd_choose_tests():

    config_file = 'GameProps/Bechi.txt'

    lside = (4, 0, 0, 4)
    wside = (4, 4, 4, 4)

    for turn in (True, False):
        for winner in (True, False):

            if winner:
                store = [2, 6]
                board = lside + wside
            else:
                store = [6, 2]
                board = wside + lside

            print(f'RNDCHOOSE: Bechi    store={store}  turn={turn} ')
            rnd_choose_test_one(config_file, list(board), list(store), turn)


# %%

rnd_move_tests()
rnd_choose_tests()
