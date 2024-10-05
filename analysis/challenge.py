# -*- coding: utf-8 -*-
"""Goal: for given game(s), test two players against eachother.
See --help or exper_config for how to configure the players.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

import logging

import ana_logger
import play_game
import exper_config


logger = logging.getLogger('challenge')


game_players_gen, config = exper_config.get_configuration()
ana_logger.config(logger, config.output)

logger.info('Challenge:\n %s', config)

for game, fplayer, tplayer, gname in game_players_gen:

    logger.info(gname)
    logger.info('True %s', tplayer if tplayer else 'Random')
    logger.info('False %s', fplayer if fplayer else 'Random')

    gstats = play_game.play_games(game, fplayer, tplayer,
                                  config.nbr_runs, config.save_logs)

    logger.info(game.info.name)
    logger.info('True %s', tplayer if tplayer else 'Random')
    logger.info('False %s', fplayer if fplayer else 'Random')
    logger.info(gstats)

    win_pct = gstats.wins[True] / gstats.total
    logger.info(f'\n{gname:20} True win %={win_pct:10.2%}')

ana_logger.close(logger)
