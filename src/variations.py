# -*- coding: utf-8 -*-
"""Allow the game to be reconfigures to a small number of
variations that are defined in the game config file.

Created on Tue Jun  3 04:35:08 2025
@author: Ann"""

# %% imports

import tkinter as tk
import tkinter.simpledialog as tksimpledialog
from tkinter import ttk

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

    if (ckey.VARI_PARAMS not in game_config
            and ckey.VARIATIONS not in game_config):
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
        self.vari_params = game_config.get(ckey.VARI_PARAMS, {})
        self.variations = game_config.get(ckey.VARIATIONS, {})

        self.params = man_config.ParamData()
        self.do_it = False

        if self.variations:
            keys = list(self.variations.keys())
            self.tkvars[ckey.VARIATIONS] = tk.StringVar(self.master,
                                                        keys[0],
                                                        name='variations')
        for vname in self.vari_params.keys():
            param = self.params[vname]
            self.make_tkvar(param)
            self.copy_config_to_tk(param, game_config)

        super().__init__(master, title)


    def body(self, master):
        """Build widgets for parameter variations."""

        self.resizable(False, False)
        rcnt = ui_utils.Counter()

        if self.variations:
            lbl = ttk.Label(master, text='Varations')
            lbl.grid(row=0, column=0,sticky=tk.E)

            keys = list(self.variations.keys())
            opmenu = ttk.OptionMenu(master, self.tkvars[ckey.VARIATIONS],
                                    keys[0], *keys)
            opmenu.config(width=2 + max(len(str(val)) for val in keys))
            opmenu.grid(row=0, column=1, pady=2, sticky=tk.W)
            rcnt.increment()

        for vname, pdata in self.vari_params.items():
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

        # TODO address variations parameter overlap with vari_params
        #  for now assume that the params set in the name variations
        #  are distinct from the vari_params

        if self.variations:
            vari_name = self.tkvars[ckey.VARIATIONS].get()
            for vname, value in self.variations[vari_name].items():

                param = self.params[vname]
                man_config.set_config_value(
                    self.game_config, param.cspec, param.option, value)

        for vname in self.vari_params.keys():
            param = self.params[vname]
            self.copy_tk_to_config(param, self.game_config)

            # value = man_config.get_config_value(
            #             self.game_config,
            #             param.cspec, param.option, param.vtype)
            # print(vname, value)
