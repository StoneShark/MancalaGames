# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 06:16:21 2023
@author: Ann"""

import random
import time

import ai_player
import game_interface as gi
import man_config

from game_log import game_log



# %%  random Players

def test_random_one_game(game_path):

    game_log.active = True
    game_log.level = game_log.DETAIL

    game, _ = man_config.make_game(game_path)

    game_log.turn('Start', game)

    max_turns = 2000 if game.info.rounds else 500
    for _ in range(max_turns):
        moves = game.get_moves()
        assert moves, "Game didn't end right."

        move = random.choice(moves)

        cond = game.move(move)
        if cond in (gi.WinCond.WIN, gi.WinCond.TIE, gi.WinCond.ENDLESS):
            break
        if cond in (gi.WinCond.ROUND_WIN, gi.WinCond.ROUND_TIE):
            game_log.add(f'(rs) ROUND OVER: {cond}')
            if game.new_game(cond, new_round_ok=True):
                game_log.save(game.params_str())
                return

        if game.info.mustpass:
            game.test_pass()

    else:
        game_log.add("(rs) Loop maxed before game ended.")

    if cond == gi.WinCond.ENDLESS:
        game_log.add('(rs) Abandoned due to endless mlaps.')

    elif cond:
        game_log.add(f'(rs) GAME OVER {cond}')

    game_log.save(game.params_str())



# %%  ai players


PLAYER1 = {"algorithm": "minimaxer",
           "difficulty": 0,
           "scorer": {
               "stores_m": 4,
               },
           "ai_params": {
               "mm_depth": [1, 3, 5, 8],
            }
          }


PLAYER2 = {"algorithm": "minimaxer",
           "difficulty": 2,
           "scorer": {
               "stores_m": 4,
               },
           "ai_params": {
               "mm_depth": [1, 3, 5, 8],
            }
          }


def test_ai_one_game(game_path):

    game_log.active = True
    game_log.level = game_log.DETAIL

    game, _ = man_config.make_game(game_path)

    game_log.turn('Start', game)

    tplayer = ai_player.AiPlayer(game, PLAYER1)
    fplayer = ai_player.AiPlayer(game, PLAYER2)

    for _ in range(2000 if game.info.rounds else 500):

        if not game.turn:
            move = fplayer.pick_move()
        else:
            moves = game.get_moves()
            move = random.choice(moves)

        cond = game.move(move)
        if cond in (gi.WinCond.WIN, gi.WinCond.TIE, gi.WinCond.ENDLESS):
            break
        if cond in (gi.WinCond.ROUND_WIN, gi.WinCond.ROUND_TIE):
            if game.new_game(cond, new_round_ok=True):
                game_log.save(game.params_str())
                return cond.value, game.turn

        if game.info.mustpass:
            game.test_pass()

    else:
        game_log.add("(rs) Loop maxed before game ended.")

    if cond == gi.WinCond.ENDLESS:
        game_log.add('(rs) Abandoned due to endless mlaps.')

    elif cond:
        game_log.add(f'(rs) GAME OVER {cond}')

    game_log.save(game.params_str())


# %%  main

if  __name__ == '__main__':

    gpath = "../GameProps/Giuthi.txt"

    # for _ in range(30):
    #     test_random_one_game(gpath)
    #     game_log.new()
    #     time.sleep(1)

    # test_random_one_game(gpath)

    test_ai_one_game(gpath)
