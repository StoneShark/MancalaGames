# -*- coding: utf-8 -*-
"""Goal: for given game(s), test two players against eachother.
See --help or exper_config for how to configure the players.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

import logging

import ana_logger
import exper_config
import play_game


logger = logging.getLogger()
game_players_gen, config = exper_config.get_configuration()


for game, fplayer, tplayer, gname in game_players_gen:

    logger.info(gname)
    logger.info('True %s', tplayer if tplayer else 'Random')
    logger.info('False %s', fplayer if fplayer else 'Random')

    gstats = play_game.play_games(game, fplayer, tplayer,
                                  config.nbr_runs,
                                  save_logs=config.save_logs,
                                  end_all=config.end_all,
                                  move_limit=config.max_moves)
    logger.info(gstats)

    win_pct = gstats.wins[True] / gstats.total
    logger.info('\n%s True win %%=%10.2f%%', gname, win_pct)

ana_logger.close(logger)
