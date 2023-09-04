# -*- coding: utf-8 -*-
"""Use the Monte Carlo Tree Search to play a game.

Created on Sun Aug 13 01:42:21 2023
@author: Ann
"""

from game_log import game_log
import man_config
import mancala_ui
import montecarlo_ts as mcts


game = man_config.make_game('../GameProps/XCaptSowOwn.txt')
game.turn = True

player = mcts.MonteCarloTS(game)
game.set_player(player)

game_ui = mancala_ui.MancalaUI(game)
game_ui.ai_player.set(True)     # enable via ui's tkvar
# game_ui.log_ai.set(True)        # enable via ui's tkvar
game_ui._schedule_ai()

game_log.live = True
# game_log.level = game_log.SHOWALL

game_ui.mainloop()
