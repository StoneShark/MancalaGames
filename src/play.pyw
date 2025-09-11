# -*- coding: utf-8 -*-
"""Direct interface to start a mancala game given a config file and
possibly a variant.

Created on Tue Jul 18 13:50:32 2023
@author: Ann"""


import man_config
import man_path
import mancala_ui



if __name__ == '__main__':

    man_config.check_disable_animator()

    param = man_path.get_cmd_ln_gamename()
    if man_config.VAR_SEP in param:
        man_config.read_params_data(need_descs=False)

    gamename, variant = man_config.game_name_to_parts(param)

    filename = man_path.find_gamefile(gamename)
    game, pdict = man_config.make_game(filename, variant)
    print(game.info.about)

    game_ui = mancala_ui.MancalaUI(game, pdict)
    game_ui.mainloop()
