# -*- coding: utf-8 -*-
"""Allow the game to be reconfigured to a small number of
variations that are defined in the game config file.

Created on Tue Jun  3 04:35:08 2025
@author: Ann"""

# %% imports

import dataclasses as dc
import tkinter as tk
import tkinter.simpledialog as tksimpledialog
from tkinter import ttk

import ai_player
import cfg_keys as ckey
import game_constants as gconsts
import game_interface as gi
import man_config
import param_mixin
import param_consts as pc
import round_tally
import ui_utils


class GameVariations:
    """Collect the data used for game variations."""

    def __init__(self, game_ui, game_file):

        self.game_ui = game_ui
        self.game_file = game_file
        self.game_config = man_config.read_game(game_file)

        if (ckey.VARI_PARAMS not in self.game_config
                and ckey.VARIANTS not in self.game_config):
            raise TypeError("Cannot create GameVariations without variations.")

        self.ptable = man_config.ParamData(no_descs=True)

        self.vari_params = self.game_config.get(ckey.VARI_PARAMS, {})
        self.variants = self.game_config.get(ckey.VARIANTS, {})

        # collect the list of all params that can be changed
        params = set(self.vari_params.keys())
        options = set()
        if self.variants:
            for vdict in self.variants.values():
                options |= set(vdict.keys())

        if params & options:
            print("VARI_PARAMS and VARIANTS have overlapping parameters"
                  "VARI_PARAMS settings will override VARIATIONS")
        self.my_params = params | options


    def _update_config(self):
        """Make the config read from the file match the current
        game.  Cannot assume that all keys that have been changed
        are in the game configuration."""

        # not used because we don't know what variant to set

        for param in ckey.GCONST_PARAMS:
            value = getattr(self.game_ui.game.cts, param)
            self.game_config[ckey.GAME_CONSTANTS][param] = value

        for fdesc in dc.fields(gi.GameInfo):
            value = getattr(self.game_ui.game.info, fdesc.name)
            self.game_config[ckey.GAME_INFO][fdesc.name] = value


    def rebuild(self):
        """Rebuild the game based on game_config."""

        new_game = man_config.game_from_config(self.game_config)
        player_dict = self.game_config[ckey.PLAYER]
        player = ai_player.AiPlayer(new_game, player_dict)

        new_game.filename = self.game_file

        return new_game, player_dict, player


    def reconfigure(self):
        """Reconfigure the game base on user selected variation
        values from the var_dict."""

        title = self.game_config[ckey.GAME_INFO][ckey.NAME] + ' Variations'

        popup = AdjustPopup(self.game_ui, title, self)
        if not popup.do_it:
            return False

        try:
            ret_vals = self.rebuild()

        except (gconsts.GameConstsError, gi.GameInfoError, NotImplementedError
                ) as error:
            message = error.__class__.__name__ + ':  ' + str(error)
            ui_utils.showerror(self.game_ui, 'Parameter Error', message)
            return False

        return ret_vals


    def settings(self):
        """Popup a window with all the parameters settings that can be
        changed via variations."""

        text = ""
        for key in self.my_params:
            param = self.ptable[key]
            value = man_config.get_game_value(self.game_ui.game,
                                              param.cspec, key)

            goal = self.game_ui.game.info.goal
            if key == ckey.GOAL_PARAM and goal in round_tally.RoundTally.PSTR:
                text += round_tally.RoundTally.PSTR[goal]
                text += ' (' + key + '):    '
            else:
                text += f"{param.text}:    "

            if param.vtype in pc.STRING_DICTS:
                text += pc.STRING_DICTS[param.vtype].int_dict[value]
            else:
                text += str(value)
            text += "\n"

        ui_utils.QuietDialog(self.game_ui,
                             'Variant Settings', text,
                             fixed_form=True)


class AdjustPopup(param_mixin.ParamMixin, tksimpledialog.Dialog):
    """Do a popup to allow adjustment of the parameters in the
    GameVariations (parameter vari).

    The param mixin does most of the work, so the simple dialog
    template works fine."""

    def __init__(self, master, title, vari):

        self.master = master

        self.vari = vari
        self.game_config = vari.game_config
        self.vari_params = vari.vari_params
        self.variants = vari.variants
        self.params = vari.ptable

        self.do_it = False

        if self.variants:
            keys = list(self.variants.keys())
            self.tkvars[ckey.VARIANTS] = tk.StringVar(self.master,
                                                        keys[0],
                                                        name='varaints')
        for vname in self.vari_params.keys():
            param = self.params[vname]
            self.pm_make_tkvar(param, self.game_config)
            self.pm_copy_config_to_tk(param, self.game_config)

        super().__init__(master, title)


    def body(self, master):
        """Build widgets for parameter variations."""

        self.resizable(False, False)
        rcnt = ui_utils.Counter()

        if self.variants:
            lbl = ttk.Label(master, text='Variant Sets')
            lbl.grid(row=0, column=0,sticky=tk.E)

            keys = list(self.variants.keys())
            opmenu = ttk.OptionMenu(master, self.tkvars[ckey.VARIANTS],
                                    keys[0], *keys)
            opmenu.config(width=2 + max(len(str(val)) for val in keys))
            opmenu.grid(row=0, column=1, pady=2, sticky=tk.W)
            rcnt.increment()

        for vname, pdata in self.vari_params.items():
            param = self.params[vname]
            param.row = rcnt.count
            param.col = 0
            lims = pdata if isinstance(pdata, list) else None
            self.pm_make_ui_param(master, param, lims, self.game_config)


    def buttonbox(self):
        """Only Ok, Revert and Cancel."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        tk.Button(bframe, text='Ok', width=6,
                  command=self.ok, default=tk.ACTIVE
                  ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(bframe, text='Revert', width=6,
                  command=self.revert, default=tk.ACTIVE
                  ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(bframe, text='Cancel', width=6, command=self.cancel
                  ).pack(side=tk.LEFT, padx=5, pady=5)


    def apply(self):
        """Copy the tk variables values into the game config."""

        self.do_it = True

        if self.variants:
            vari_name = self.tkvars[ckey.VARIANTS].get()
            for vname, value in self.variants[vari_name].items():

                param = self.params[vname]
                man_config.set_config_value(
                    self.game_config, param.cspec, param.option,
                    man_config.convert_from_file(vname, value))

        for vname in self.vari_params.keys():
            param = self.params[vname]
            self.pm_copy_tk_to_config(param, self.game_config)

            # value = man_config.get_config_value(
            #             self.game_config,
            #             param.cspec, param.option, param.vtype)
            # print(vname, value)


    def revert(self):
        """Ignore the settings on the popup and revert to the game file
        configure, which is already loaded into game config."""

        self.do_it = True
        self.cancel()
