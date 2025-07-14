# -*- coding: utf-8 -*-
"""Allow the game to be reconfigured to a small number of
variations that are defined in the game config file.

Created on Tue Jun  3 04:35:08 2025
@author: Ann"""

# %% imports

import collections
import enum
import tkinter as tk
import tkinter.simpledialog as tksimpledialog
from tkinter import ttk
import warnings

import ai_player
import cfg_keys as ckey
import format_msg
import game_info as gi
import man_config
import param_mixin
import param_consts as pc
import round_tally
import ui_utils


# %%  classes

class GameVariantError(Exception):
    """Error in GameInfo."""


class GameVariations:
    """Collect the data used for game variations."""

    def __init__(self, game_ui, game_file):

        self.failed = True
        self.game_ui = game_ui
        self.game_file = game_file
        self.game_config = man_config.read_game(game_file)

        try:
            test_variation_config(self.game_config)

        except GameVariantError as error:
            message = error.__class__.__name__ + ':  ' + str(error)
            ui_utils.showerror(self.game_ui, 'Variations Error', message)
            return

        self.ptable = man_config.ParamData(no_descs=True)

        self.vari_params = self.game_config.get(ckey.VARI_PARAMS, {})
        self.variants = self.game_config.get(ckey.VARIANTS, {})

        # collect the list of all params that can be changed
        options = set(self.vari_params.keys())
        if self.variants:
            for vdict in self.variants.values():
                options |= set(vdict.keys())

        self.my_params = options
        self.failed = False


    def _make_consistent(self):
        """If we can adjust the size of the board for games with
        udir holes, try to  update the udir_holes based on
        orginal game configuration. Either set all holes to udir
        or set just the center hole to udir."""

        game = self.game_ui.game
        if (not game.info.udirect
                or ckey.HOLES not in self.my_params
                or ckey.UDIR_HOLES in self.my_params):
            return

        new_holes = self.game_config[ckey.GAME_CONSTANTS][ckey.HOLES]
        if game.cts.holes == new_holes:
            return

        nbr_old_udir = len(game.info.udir_holes)

        if nbr_old_udir == game.cts.holes:
            self.game_config[ckey.GAME_INFO][ckey.UDIR_HOLES] = \
                list(range(new_holes))

        elif nbr_old_udir == 1:
            quot, odd = divmod(new_holes, 2)
            self.game_config[ckey.GAME_INFO][ckey.UDIR_HOLES] = [quot + odd]

        else:   # pragma: no coverage
            assert False, "Variations tests should have precluded this."


    def rebuild_variant(self):
        """Rebuild the game based on game_config."""

        self._make_consistent()
        new_game = man_config.game_from_config(self.game_config)
        player_dict = self.game_config[ckey.PLAYER]
        player = ai_player.AiPlayer(new_game, player_dict)

        new_game.filename = self.game_file

        return new_game, player_dict, player


    def reconfigure(self):
        """Reconfigure the game base on user selected variation
        values from the var_dict.

        If there was an error reread the game configuration file
        to reset it."""

        title = self.game_config[ckey.GAME_INFO][ckey.NAME] + ' Variations'

        popup = AdjustPopup(self.game_ui, title, self)
        if not popup.do_it:
            return False

        build_context = ui_utils.ReportError(self.game_ui)
        with build_context:
            ret_vals = self.rebuild_variant()

        if build_context.error:
            self.game_config = man_config.read_game(self.game_file)
            return False

        return ret_vals


    def settings(self):
        """Popup a window with all the parameters settings that can be
        changed via variations."""

        text = ''
        for key in self.my_params:
            param = self.ptable[key]
            value = man_config.get_game_value(self.game_ui.game,
                                              param.cspec, key)

            title = param.text
            if key == ckey.GOAL_PARAM:
                goal = self.game_ui.game.info.goal
                rounds = self.game_ui.game.info.rounds
                blocks = self.game_ui.game.info.blocks

                rtally = round_tally.RoundTally.PSTR.get(goal, False)
                if rtally:
                    title = f'Goal: {rtally}'

                elif goal == gi.Goal.MAX_SEEDS and rounds and blocks:
                    title = "Goal: Opp Can't Fill Holes"

            text += f'{title}:    '

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
        self.game_name = self.game_config[ckey.GAME_INFO][ckey.NAME]
        self.tkvars = {}

        self.do_it = False

        if self.variants:
            gamename, vname = man_config.game_name_to_parts(
                                                 vari.game_ui.game.info.name)
            vname = vname if vname else gamename

            self.tkvars[ckey.VARIANTS] = tk.StringVar(self.master,
                                                      vname,
                                                      name='varaints')
        for vname in self.vari_params.keys():
            param = self.params[vname]
            self.pm_make_tkvar(param, self.game_config)
            self.pm_copy_config_to_tk(param, self.game_config)

        self.update_tkvars_for_game(vari.game_ui.game)

        super().__init__(master, title)


    def body(self, master):
        """Build widgets for parameter variations."""

        self.resizable(False, False)
        rcnt = ui_utils.Counter()

        if self.variants:
            lbl = ttk.Label(master, text='Variant')
            lbl.grid(row=0, column=0,sticky=tk.E)

            keys = list(self.variants.keys())
            opmenu = ttk.OptionMenu(master, self.tkvars[ckey.VARIANTS],
                                    self.tkvars[ckey.VARIANTS].get(), *keys,
                                    command=self.update_tkvars_for_variant)
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
                  command=self.revert,
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

        self.game_config[ckey.GAME_INFO][ckey.NAME] = self.game_name


    def revert(self):
        """Reset the ui to base game config values"""

        if self.variants:
            key_list = list(self.variants.keys())
            self.tkvars[ckey.VARIANTS].set(key_list[0])

        for vname in self.vari_params.keys():
            param = self.params[vname]
            self.pm_copy_config_to_tk(param, self.game_config)


    def update_tkvars_for_game(self, game):
        """Load the tk variables with the values corresponding
        to the game.  Variant is already set."""

        for vname in self.vari_params.keys():
            param = self.params[vname]
            value = man_config.get_game_value(game, param.cspec, vname)
            self.pm_set_tk_var(param, value)


    def update_tkvars_for_variant(self, _=None):
        """When a variant is selected, update any duplicate vari_params
        to match it.
        If the variants dict is empty, reset to the game_config."""

        # revert to the base game options
        self.game_name = self.game_config[ckey.GAME_INFO][ckey.NAME]

        for vname in self.vari_params.keys():
            param = self.params[vname]
            self.pm_copy_config_to_tk(param, self.game_config)

        # if we've selected the base game, stop
        vari_name = self.tkvars[ckey.VARIANTS].get()
        if not self.variants[vari_name]:
            return

        # configure for the selected varaint (not the base game)
        self.game_name = man_config.qual_game_name(self.game_config, vari_name)
        vkeys = self.vari_params.keys()
        for vname, fvalue in self.variants[vari_name].items():

            if vname not in vkeys:
                continue

            param = self.params[vname]
            value = man_config.convert_from_file(vname, fvalue)
            self.pm_set_tk_var(param, value)


# %% variant tests


def possible_values(vparam, variants):
    """Create a dictionary where the keys are options that may be
    changed and the values are sets of all possible values they
    can take.

    If the value is True (not truthy) the parameter, can take on
    any value.

    Don't collect values for any options that are do not have
    hashable values."""

    params = collections.defaultdict(set)

    for pname, pvalues in vparam.items():
        if pname in ckey.NOT_HASHABLE:
            continue

        if isinstance(pvalues, list):
            params[pname] = set(pvalues)

        else:
            params[pname] = True

    for vdict in variants.values():
        for pname, pvalue in vdict.items():
            if  pname in ckey.NOT_HASHABLE or params[pname] is True:
                continue

            params[pname] |= {pvalue}

    return params


def test_algo_ok(game_dict, vparam, variants):
    """Test if the algorithm might prevent one of the options
    from being used.

    This is a heurstic test, it might have false positives and
    true negatives (its always safe to configure the minimaxer)."""

    pdict = game_dict[ckey.PLAYER]
    if (ckey.ALGORITHM not in pdict
        or pdict[ckey.ALGORITHM] == ai_player.MINIMAXER):
        return

    # cannot test params in ckey.NOT_HASHABLE
    bad_opts = {ckey.SOW_OWN_STORE: {True, },
                ckey.XC_SOWN: {True, },
                ckey.PRESCRIBED: {gi.SowPrescribed, },
                ckey.NOCAPTMOVES: {1, 2, 3, 4, 5, 6, },   # any value > 0 is bad
                ckey.ALLOW_RULE: {gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                  gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO},
                ckey.UNCLAIMED: {gi.EndGameSeeds.LAST_MOVER, },
                ckey.CAPT_RTURN: {gi.CaptRTurn.ONCE, gi.CaptRTurn.ALWAYS},
                ckey.SOW_DIRECT: {gi.Direct.PLAYALTDIR, },
                ckey.ROUND_FILL: {gi.RoundFill.SHORTEN,
                                  gi.RoundFill.SHORTEN_ALL},
                }

    value_dict = possible_values(vparam, variants)

    for opt, bad_values in bad_opts.items():

        error = False
        if opt in value_dict:
            pos_values = value_dict[opt]

            if pos_values is True:
                error = True
            else:
                error = bad_values & pos_values

        if error:
            msg=f"""{pdict[ckey.ALGORITHM]} might preclude use of
                {opt.upper()} in variations."""
            warnings.warn(format_msg.fmsg(msg))


def test_include_goal_param(game_dict, vparams):
    """Test to see if it would be a good idea to include goal_param"""

    if not vparams:
        return

    goal = game_dict[ckey.GAME_INFO].get(ckey.GOAL, gi.Goal.MAX_SEEDS)
    rounds = game_dict[ckey.GAME_INFO].get(ckey.ROUNDS, 0)

    if (((rounds and goal in (gi.Goal.MAX_SEEDS, gi.Goal.TERRITORY))
             or goal in round_tally.RoundTally.GOALS)
            and ckey.GOAL_PARAM not in vparams):
        msg="GOAL_PARAM might be useful in VARI_PARAM."
        warnings.warn(msg)


def test_vari_params(game_dict, vparams):
    """Test the VARI_PARAMS section."""
    # pylint: disable=too-complex

    for key, vlist in vparams.items():

        if key not in ckey.CONFIG_PARAMS:
            msg=f"{key} in VARI_PARAM is not a valid game parameter."
            raise GameVariantError(msg)


        if key == ckey.GAME_CLASS:
            if (not isinstance(vlist, list)
                    and game_dict[ckey.GAME_CLASS] not in vlist):

                msg="Configured GAME_CLASS not in VARI_PARAMS value list."
                raise GameVariantError(msg)

        elif isinstance(vlist, list):
            if not all(isinstance(val, int) for val in vlist):
                msg=f"{key} value list contains non-integers."
                raise GameVariantError(msg)

            if (key in game_dict[ckey.GAME_CONSTANTS]
                    and game_dict[ckey.GAME_CONSTANTS][key] not in vlist):
                msg=f"Configured {key.upper()} not in VARI_PARAMS value list."
                raise GameVariantError(msg)

            if key in game_dict[ckey.GAME_INFO]:

                cval = game_dict[ckey.GAME_INFO][key]
                if isinstance(cval, enum.Enum):
                    cval = cval.value

                if cval not in vlist:
                    msg=f"Configured {key.upper()} not in VARI_PARAMS value list."
                    raise GameVariantError(msg)

    test_include_goal_param(game_dict, vparams)


def test_variants_param(game_dict, variants):
    """Test the variants section."""

    if not variants:
        return

    if len(variants) < 2:
        msg="""Game variants aren't useful if there aren't 2 or more.
            Is the base game variant missing?"""
        raise GameVariantError(msg)

    # first item has game name key and an empty dictionary
    vlist = list(variants.items())
    if vlist[0][0] != game_dict[ckey.GAME_INFO][ckey.NAME]:
        msg="""The first variant should have the base game name"""
        raise GameVariantError(msg)

    if not (isinstance(vlist[0][1], dict) and vlist[0][1] == {}):
        msg="""The first variant should be for the base game
            and have a value of empty dictionary"""
        raise GameVariantError(msg)

    for key, vdict in variants.items():

        if not isinstance(vdict, dict):
            msg = f"Variant value for {key} is not a dict."
            raise GameVariantError(msg)

        for param in vdict.keys():

            if param not in ckey.CONFIG_PARAMS:
                msg=f"{param} in VARIANT[{key}] is not a valid game parameter."
                raise GameVariantError(msg)


def test_udir_hole_changes(game_dict, var_options):
    """Test if we know what to do if the user can change the
    number of holes in the presence of udir_holes.

    var_options is a set of all parameter names in vari_param
    and in the variant dicts."""

    # game isn't udirect, nothing to be checked
    if not game_dict[ckey.GAME_INFO].get(ckey.UDIRECT, False):
        return

    # variants don't allow board size to be changed, all good
    if ckey.HOLES not in var_options:
        return

    if ckey.UDIR_HOLES in var_options:
        msg = """Variations that allow changing HOLES and UDIR_HOLES are
              are not supported."""
        raise GameVariantError(msg)

    udirs = game_dict[ckey.GAME_INFO].get(ckey.UDIR_HOLES, [])
    nbr_udir = len(udirs)
    holes = game_dict[ckey.GAME_CONSTANTS][ckey.HOLES]

    # we'll make all holes udir holes
    if nbr_udir == holes:
        return

    # we'll make the odd center hole udir
    quot, odd = divmod(holes, 2)
    if nbr_udir == 1 and odd and udirs[quot + odd]:
        return

    # we don't know what to do
    msg = """Game has user directed holes and
          variations allow changing the number of holes,
          but it cannot be infered
          how to adjust udir_holes (all holes or center)."""
    raise GameVariantError(msg)


def test_variation_config(game_dict, no_var_error=True):
    """Test the consistency of the variation configuration
    in the game dictionary.

    Using the tester overly complicates this code because the tests
    are inside loops. Don't think classes derived from Mancala will
    ever want to skip these tests."""

    if not (ckey.VARI_PARAMS in game_dict or ckey.VARIANTS in game_dict):
        if no_var_error:
            msg="Cannot create GameVariations without variations."
            raise GameVariantError(msg)

        return

    vari_params = game_dict.get(ckey.VARI_PARAMS, {})
    if not isinstance(vari_params, dict):
        msg = "VARI PARAMS value is not a dictionary."
        raise GameVariantError(msg)

    variants = game_dict.get(ckey.VARIANTS, {})
    if not isinstance(variants, dict):
        msg = "VARIANTS value is not a dictionary."
        raise GameVariantError(msg)

    options = set(vari_params.keys())
    if variants:
        for vdict in variants.values():
            options |= set(vdict.keys())

    test_vari_params(game_dict, vari_params)
    test_variants_param(game_dict, variants)
    test_udir_hole_changes(game_dict, options)
    test_algo_ok(game_dict, vari_params, variants)
