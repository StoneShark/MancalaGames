# -*- coding: utf-8 -*-
"""Generate a log of the specified game, with either the ai players
or random play. Useful for trying to find games with particular
conditions or moves.

The ai move logs might be in a different place than in logs generated
by Mancala UI.

Created on Wed Sep 13 06:16:21 2023
@author: Ann"""

import argparse
import random
import sys

from context import ai_player
from context import game_interface as gi
from context import man_config
from context import game_logger as gl

cargs = None

# %% play a game

def ai_pick_move(player):
    """Have player pick a move, but turn off logging first
    and restore after."""

    gl.game_log.active = False
    move = player.pick_move()
    gl.game_log.active = True
    gl.game_log.add(player.get_move_desc(), gl.game_log.MOVE)

    return move


def play_a_game(fplayer, tplayer):
    """Generate a log with fplayer (or random) and tplayer (or random)."""

    gl.game_log.turn(0, 'Start', game)

    for _ in range(2000 if game.info.rounds else 500):
        moves = game.get_moves()
        assert moves, "Game didn't end right."

        if game.turn and tplayer:
            move = ai_pick_move(tplayer)
        elif not game.turn and fplayer:
            move = ai_pick_move(fplayer)
        else:
            move = random.choice(moves)

        cond = game.move(move)
        if cond in (gi.WinCond.WIN, gi.WinCond.TIE, gi.WinCond.ENDLESS):
            break
        if cond in (gi.WinCond.ROUND_WIN, gi.WinCond.ROUND_TIE):
            gl.game_log.add(f'(ggl) ROUND OVER: {cond}')
            if game.new_game(cond, new_round_ok=True):
                gl.game_log.save(game.params_str())
                return
            else:
                gl.game_log.turn(0, 'Start', game)

        if game.info.mustpass:
            game.test_pass()

    else:
        gl.game_log.add("(ggl) Loop maxed before game ended.")

    if cond == gi.WinCond.ENDLESS:
        gl.game_log.add('(ggl) Abandoned due to endless mlaps.')

    elif cond:
        gl.game_log.add(f'(ggl) GAME OVER {cond}')

    gl.game_log.save(game.params_str())



# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('game')

    parser.add_argument('--log_level', action='store',
                        choices=['MOVE', 'IMPORT', 'STEP', 'INFO', 'DETAIL'],
                        default='DETAIL',
                        help="""Set the log level to collect.
                        Default: %(default)s""")

    parser.add_argument('--ai_tplayer', action='store_true',
                        help="""Use the minimaxer for player true; moves
                        are made randomly otherwise.
                        Default: %(default)s""")

    parser.add_argument('--ai_fplayer', action='store_true',
                        help="""Use the minimaxer for player false; moves
                        are made randomly otherwise.
                        Default: %(default)s""")

    return parser


def process_command_line():
    """Process the command line arguements."""

    global cargs

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    print(cargs)


# %%  main

if  __name__ == '__main__':

    process_command_line()

    gl.game_log.active = True
    gl.game_log.level = getattr(gl.game_log, cargs.log_level)

    game, gdict = man_config.make_game('../GameProps/' + cargs.game + '.txt')

    fplayer = tplayer = None
    if cargs.ai_tplayer:
        tplayer = ai_player.AiPlayer(game, gdict)
    if cargs.ai_fplayer:
        fplayer = ai_player.AiPlayer(game, gdict)

    play_a_game(fplayer, tplayer)
