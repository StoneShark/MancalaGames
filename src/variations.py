# -*- coding: utf-8 -*-
"""Allow the game to be reconfigures to a small number of
variations that are defined in the game config file.

Created on Tue Jun  3 04:35:08 2025
@author: Ann"""

# %% imports

import tkinter as tk
import tkinter.simpledialog as tksimpledialog

import ai_player
import cfg_keys as ckey
import game_constants as gconsts
import game_interface as gi
import man_config
import param_mixin
import ui_utils


def reconfig_game(game_ui, game_file):
    """Reconfigure the game base on user selected variation
    values from the var_dict."""

    game_config = man_config.read_game(game_file)

    if ckey.VARI_PARAMS not in game_config:
        ui_utils.showerror(game_ui, "No Variations",
                           """There are not any preconfigured variation
                           in the game configuration file.""")
        return False

    title = game_config[ckey.GAME_INFO][ckey.NAME] + ' Variations'
    AdjustPopup(game_ui, title , game_config)

    # pylint: disable=too-many-try-statements
    try:
        new_game, player_dict = man_config.game_from_config(game_config)
        player = ai_player.AiPlayer(new_game, player_dict)

    except (gconsts.GameConstsError, gi.GameInfoError, NotImplementedError
            ) as error:
        message = error.__class__.__name__ + ':  ' + str(error)
        ui_utils.showerror(game_ui, 'Parameter Error', message)
        return False

    return new_game, player_dict, player


class AdjustPopup(param_mixin.ParamMixin, tksimpledialog.Dialog):
    """an adjustment popup but um, this isn't a 'simple' dialog"""

    def __init__(self, master, title, game_config):

        self.master = master

        self.game_config = game_config
        self.vari_dict = game_config[ckey.VARI_PARAMS]

        self.params = man_config.ParamData()
        self.do_it = False

        for vname in self.vari_dict.keys():
            param = self.params[vname]
            self.make_tkvar(param)
            self.copy_config_to_tk(param, game_config)

        super().__init__(master, title)


    def body(self, master):
        """Build widgets for parameter variations."""

        self.resizable(False, False)
        rcnt = ui_utils.Counter()

        for vname, pdata in self.vari_dict.items():
            param = self.params[vname]
            param.row = rcnt.count
            param.col = 0
            lims = pdata if isinstance(pdata, list) else None
            self.make_ui_param(master, param, limits=lims)


    def buttonbox(self):
        """Only include Ok and Cancel."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        tk.Button(bframe, text='Ok', width=6,
                  command=self.ok, default=tk.ACTIVE
                  ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(bframe, text='Cancel', width=6, command=self.cancel
                  ).pack(side=tk.LEFT, padx=5, pady=5)


    def apply(self):
        """Copy the tk variables values into the game config."""

        for vname in self.vari_dict.keys():
            param = self.params[vname]
            self.copy_tk_to_config(param, self.game_config)

            # value = man_config.get_config_value(
            #             self.game_config,
            #             param.cspec, param.option, param.vtype)
            # print(vname, value)
