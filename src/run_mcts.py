# -*- coding: utf-8 -*-
"""Use the Monte Carlo Tree Search to play a game.

Created on Sun Aug 13 01:42:21 2023
@author: Ann"""

from game_logger import game_log
import man_config
import mancala_ui


game, pdict = man_config.make_game('../GameProps/XCaptSowOwn.txt')
game.turn = True

game_ui = mancala_ui.MancalaUI(game, pdict)
game_ui.player.set_algorithm('montecarlo_ts')

game_ui.ai_active.set(True)     # enable via ui's tkvar
# game_ui.log_ai.set(True)        # enable via ui's tkvar
game_ui._schedule_ai()

game_log.live = True
game_log.level = game_log.SHOWALL

game_ui.mainloop()
