# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 06:16:21 2023
@author: Ann"""


import random

from game_log import game_log
import man_config

from game_interface import WinCond


def test_one_game():

    game_log.active = True
    game_log.level = game_log.SHOWALL

    game, _ = man_config.make_game("../GameProps/NamNam.txt")
    game_log.turn('Start', game)

    max_turns = 1000 if game.inforounds else 500
    for _ in range(max_turns):
        moves = game.get_moves()
        assert moves, "Game didn't end right."

        move = random.choice(moves)

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE, WinCond.ENDLESS):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            game_log.add(f'ROUND OVER: {cond}')
            if game.new_game(cond, new_round_ok=True):
                game_log.save(game.params_str())
                return

        if game.infomustpass:
            game.test_pass()

    else:
        game_log.add("Loop maxed before game ended.")

    if cond == WinCond.ENDLESS:
        game_log.add('Abandoned due to endless mlaps.')

    elif cond:
        game_log.add(f'Game Over {cond}')

    game_log.save(game.params_str())

test_one_game()
