# -*- coding: utf-8 -*-
"""Creation and most handling of the parameter widgets
is done here. This file deals with paramters one at
time. Actual parameters to be managed are controlled
elsewhere.

Created on Tue Jun  3 06:31:43 2025
@author: Ann"""


# %% import

import enum
import functools as ft
import json
import tkinter as tk
from tkinter import ttk

import cfg_keys as ckey
import game_constants as gconsts
import game_info as gi
import man_config
import mg_config
import param_consts as pc
import ui_utils


# %% constants

# given a real value after we have tk root
INT_VALID_CMD = None

MINUS = '-'


# %% helper funcs

def stoi(sval):
    """make, a possibly empty, string a valid int."""

    return int(sval) if sval else 0


def int_validate(value):
    """Only allow empty values, or decimals."""

    if not value or value == MINUS:
        return True

    if ((value[0] != MINUS and not value.isdecimal())
            or (value[0] == MINUS and not value[1:].isdecimal())):
        return False
    return True


def register_int_validate(root):
    """Register the integer validation function so that it can be
    used for int parameter widgets.

    Needs to be called with root after tk.Tk is called."""

    global INT_VALID_CMD

    INT_VALID_CMD = root.register(int_validate)


def goal_param_desc(game_config):
    """Get a descriptive string to use for the label
    on the goal param.

    This might get the label wrong if the goal can be
    changed in the variations; it will be right for
    the base game configuration."""

    rounds = game_config[ckey.GAME_INFO].get('rounds', 0)
    if not rounds:
        return None

    goal = game_config[ckey.GAME_INFO].get('goal', 0)
    desc = None
    if goal == gi.Goal.MAX_SEEDS:
        desc = "Goal: Opp Can't Fill Holes"

    elif goal == gi.Goal.TERRITORY:
        desc = "Goal: Owned Holes"

    elif goal.rnd_win_count():
        desc = "Goal: Round Wins"

    elif goal == gi.Goal.RND_POINTS:
        desc = "Goal: Points Needed"

    elif goal == gi.Goal.RND_SEED_COUNT:
        desc = "Goal: Total Seeds"

    elif goal == gi.Goal.RND_EXTRA_SEEDS:
        desc = "Goal: Extra Seeds"

    return desc


# %%  ParamHelperMixin

class ParamMixin:
    """A mixin to handle the UI elements for game parameters."""


    def update_desc(self, option, event=None):
        """A method to update a possible description box.
        It does nothing by default"""


    @staticmethod
    def _get_boxes_config(param, game_config=None):
        """Return the number items for the list for name."""

        if param.option == ckey.UDIR_HOLES:
            holes_param = man_config.PARAMS[ckey.HOLES]
            if game_config:
                boxes = man_config.get_config_value(game_config,
                                                    holes_param.cspec,
                                                    holes_param.option,
                                                    holes_param.vtype)
            else:
                boxes = holes_param.ui_default

        elif param.option == ckey.CAPT_ON:
            boxes = 6

        elif param.vtype == pc.ILIST_TYPE:
            boxes = gi.DIFF_LEVELS

        else:
            raise gi.DataError(f"Don't know list length for {param.option}.")

        return boxes


    def _get_boxes_vars(self, param, game_config=None):
        """Get the number of variables to make for int or check boxes.
        UDIR_HOLES might change size so make all of the possible variables
        now."""

        if param.option == ckey.UDIR_HOLES:
            return gconsts.MAX_HOLES + 1

        return self._get_boxes_config(param, game_config)


    @staticmethod
    def _text_dict_str(param, config_dict):
        """Return a string representation of the param, which
        should be missing, empty or a dictionary.
        If it was saved as a string, return it to preserve
        the formatting."""

        if param.option not in config_dict:
            return ''

        value = config_dict.get(param.option)
        if isinstance(value, dict):
            value = json.dumps(value, indent=3, cls=mg_config.GameDictEncoder)

        return value


    def _str_dict(self, param, raise_excp=True):
        """Convert the text from the window to a dictionary.
        If raise_excp is True, raise any decoding errors;
        otherwise, return the string representation."""

        text = self.tktexts[param.option].get('1.0', tk.END).strip()

        if not text:
            return {}

        try:
            value = json.loads(text)
        except json.decoder.JSONDecodeError as error:
            if raise_excp:
                raise error
            value = text

        return value


    def _trim_text(self, param):
        """Remove trailing spaces from each line."""

        text = self.tktexts[param.option].get('1.0', tk.END)
        text = [line.strip() + '\n' for line in text.split('\n')]
        return ''.join(text)


    def pm_make_tkvar(self, param, prefix, config_dict=None):
        """Create a tk variable for param."""

        if config_dict:
            value = man_config.get_config_value(
                        config_dict,
                        param.cspec, param.option, param.vtype)

        else:
            value = param.ui_default

        if param.vtype in (pc.STR_TYPE, pc.INT_TYPE):
            self.tkvars[param.option] = tk.StringVar(self.master,
                                                     str(value),
                                                     name=prefix + param.option)
        elif param.vtype == pc.BOOL_TYPE:
            self.tkvars[param.option] = tk.BooleanVar(self.master,
                                                      bool(value),
                                                      name=prefix + param.option)
        elif param.vtype == pc.BLIST_TYPE:
            boxes = self._get_boxes_vars(param, config_dict)
            self.tkvars[param.option] = \
                [tk.BooleanVar(self.master, i in value,
                               name=prefix + f'{param.option}_{i}')
                 for i in range(boxes)]

        elif param.vtype == pc.ILIST_TYPE:
            boxes = self._get_boxes_vars(param, config_dict)
            self.tkvars[param.option] = \
                [tk.StringVar(self.master, i in value,
                              name=prefix + f'{param.option}_{i}')
                 for i in range(boxes)]

        elif param.vtype in pc.STRING_DICTS:
            _, inv_dict, enum_dict = pc.STRING_DICTS[param.vtype]
            if isinstance(value, enum.Enum):
                vstr = inv_dict[value]
            else:
                vstr = inv_dict[enum_dict[value]]
            self.tkvars[param.option] = tk.StringVar(self.master,
                                                     vstr,
                                                     name=prefix + param.option)

        else:
            raise gi.DataError(f"Unexpected parameter type {param.vtype}.")


    def _make_text_entry(self, frame, param, col_span=4):
        """Make a text box entry with scroll bar."""

        tframe = ttk.LabelFrame(frame, text=param.text, labelanchor=tk.NW)
        tframe.grid(row=param.row, column=param.col, columnspan=col_span,
                    sticky=tk.NSEW)

        text_box = tk.Text(tframe, width=50, height=20)
        self.tktexts[param.option] = text_box

        scroll = tk.Scrollbar(tframe)
        text_box.configure(yscrollcommand=scroll.set)
        text_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scroll.config(command=text_box.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tframe.bind('<Enter>', ft.partial(self.update_desc, param.option))


    def _make_entry(self, frame, param, game_config=None):
        """Make a single line string entry."""

        length = 5 if param.vtype == pc.INT_TYPE else 30

        text = param.text
        if game_config and param.option == ckey.GOAL_PARAM:
            gp_text = goal_param_desc(game_config)
            text = gp_text if gp_text else text

        lbl = ttk.Label(frame, text=text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        if param.vtype == pc.INT_TYPE:
            ent = ttk.Entry(frame, width=length,
                            textvariable=self.tkvars[param.option],
                            validate=tk.ALL,
                            validatecommand=(INT_VALID_CMD, '%P'))
        else:
            ent = ttk.Entry(frame, width=length,
                            textvariable=self.tkvars[param.option])

        ent.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self.update_desc, param.option))
        ent.bind('<Enter>', ft.partial(self.update_desc, param.option))


    def _make_checkbox(self, frame, param):
        """Make a labeled checkbox."""

        lbl = ttk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        box = ttk.Checkbutton(frame, variable=self.tkvars[param.option])
        box.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self.update_desc, param.option))
        box.bind('<Enter>', ft.partial(self.update_desc, param.option))


    def _make_checkbox_list(self, frame, param, game_config):
        """Make a list of checkboxes."""

        lbl = ttk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        boxes = self._get_boxes_config(param, game_config)
        boxes_fr = ttk.Frame(frame)
        if param.option == ckey.UDIR_HOLES:
            boxes_fr.grid(row=param.row, column=param.col + 1,
                          columnspan=3, sticky=tk.W)
        else:
            boxes_fr.grid(row=param.row, column=param.col + 1,
                          sticky=tk.W)

        if param.option == ckey.UDIR_HOLES:
            self.udir_frame = boxes_fr

        add_in = 1 if param.option == ckey.CAPT_ON else 0
        for nbr in range(boxes):
            ttk.Checkbutton(boxes_fr, text=str(nbr + add_in),
                            variable=self.tkvars[param.option][nbr]
                            ).pack(side=tk.LEFT)

        lbl.bind('<Enter>', ft.partial(self.update_desc, param.option))
        boxes_fr.bind('<Enter>', ft.partial(self.update_desc, param.option))


    def _make_entry_list(self, frame, param):
        """Make a list of entries."""

        lbl = ttk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col, sticky=tk.E)

        boxes = self._get_boxes_config(param)
        eframe = ttk.Frame(frame)
        eframe.grid(row=param.row, column=param.col, sticky=tk.W)

        if param.option == ckey.UDIR_HOLES:
            self.udir_frame = eframe

        for nbr in range(boxes):
            ttk.Entry(eframe, width=5,
                      textvariable=self.tkvars[param.option][nbr],
                      validate=tk.ALL,
                      validatecommand=(INT_VALID_CMD, '%P')
                      ).pack(side=tk.LEFT)

        eframe.grid(row=param.row, column=param.col + 1, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self.update_desc, param.option))
        eframe.bind('<Enter>', ft.partial(self.update_desc, param.option))


    def _make_option_list(self, frame, param, limits):
        """Make an option list corresponding to the parameter.
        in MancalaGamesUI this is only called with enums, but
        MancalaUI with variations may call with a limited set of
        integers (if so, limits must be a list of numbers)."""

        if param.vtype == pc.INT_TYPE:
            values = [str(val) for val in limits]

        elif limits:
            values = [key for key, value
                              in pc.STRING_DICTS[param.vtype].str_dict.items()
                      if value in limits]
        else:
            values = list(pc.STRING_DICTS[param.vtype].str_dict.keys())

        lbl = ttk.Label(frame, text=param.text)
        lbl.grid(row=param.row, column=param.col,sticky=tk.E)

        opmenu = ttk.OptionMenu(frame, self.tkvars[param.option],
                                self.tkvars[param.option].get(),
                                *values)
        opmenu.config(width=2 + max(len(str(val)) for val in values))
        opmenu.grid(row=param.row, column=param.col + 1, pady=2, sticky=tk.W)

        lbl.bind('<Enter>', ft.partial(self.update_desc, param.option))
        opmenu.bind('<Enter>', ft.partial(self.update_desc, param.option))


    def _make_label_row(self, frame, param):
        """Make label row spanning two columns."""
        _ = self

        lbl = ttk.Label(frame, text=param.text, style='Title.TLabel')
        lbl.grid(row=param.row, column=param.col, columnspan=2,
                 padx=4, pady=2, sticky=tk.EW)
        lbl.configure(anchor='center')  # anchor in style is ignored


    def pm_make_ui_param(self, frame, param, limits=None, game_config=None):
        """Make the ui elements for a single parameter."""

        if param.vtype == pc.MSTR_TYPE:
            self._make_text_entry(frame, param)

        elif param.vtype == pc.TEXTDICT:
            self._make_text_entry(frame, param, col_span=2)

        elif param.vtype == pc.INT_TYPE and limits:
            self._make_option_list(frame, param, limits)

        elif param.vtype in (pc.STR_TYPE, pc.INT_TYPE):
            self._make_entry(frame, param, game_config)

        elif param.vtype == pc.BOOL_TYPE:
            self._make_checkbox(frame, param)

        elif param.vtype == pc.BLIST_TYPE:
            self._make_checkbox_list(frame, param, game_config)

        elif param.vtype == pc.ILIST_TYPE:
            self._make_entry_list(frame, param)

        elif param.vtype in pc.STRING_DICTS:
            self._make_option_list(frame, param, limits)

        elif param.vtype == pc.LABEL_TYPE:
            self._make_label_row(frame, param)


    def _fill_tk_list(self, param, value):
        """Set the values of a list of tkvariables."""

        if not isinstance(value, list):
            raise gi.DataError(
                f"Don't know how to fill {param.option} from {value}.")

        if param.vtype == pc.BLIST_TYPE:
            for var in self.tkvars[param.option]:
                var.set(False)
            sub_out = 1 if param.option == ckey.CAPT_ON else 0
            for val in value:
                self.tkvars[param.option][val - sub_out].set(True)

        else:
            for var in self.tkvars[param.option]:
                var.set('0')
            for idx, val in enumerate(value):
                self.tkvars[param.option][idx].set(str(val))


    def pm_set_tk_var(self, param, value):
        """Set a tk variable based on param and the given value."""

        if param.vtype in (pc.MSTR_TYPE, pc.TEXTDICT):
            self.tktexts[param.option].delete('1.0', tk.END)
            self.tktexts[param.option].insert('1.0', value)

        elif param.vtype in (pc.STR_TYPE, pc.BOOL_TYPE, pc.INT_TYPE):
            self.tkvars[param.option].set(value)

        elif param.vtype == pc.BLIST_TYPE:
            self._fill_tk_list(param, value)

        elif param.vtype == pc.ILIST_TYPE:
            self._fill_tk_list(param, value)

        elif param.vtype in pc.STRING_DICTS:
            inv_dict = pc.STRING_DICTS[param.vtype].int_dict
            self.tkvars[param.option].set(inv_dict[value])


    def pm_copy_config_to_tk(self, param, game_config):
        """Set the tk variable from the game_config dict."""

        if param.vtype == pc.TEXTDICT:
            value = self._text_dict_str(param, game_config)

        else:
            value = man_config.get_config_value(
                        game_config,
                        param.cspec, param.option, param.vtype)

        self.pm_set_tk_var(param, value)


    def pm_copy_tk_to_config(self, param, game_config, *, raise_excp=True):
        """Get the values from a tkvar and set it into
        the a game_config dict.
        From the editor, raise_excp can be set False so that any
        errors in variation dictionaries will be ignored and string
        values set and saved."""

        if param.vtype == pc.MSTR_TYPE:
            value = self._trim_text(param)

        elif param.vtype == pc.TEXTDICT:
            value = self._str_dict(param, raise_excp)

        elif param.vtype in (pc.STR_TYPE, pc.BOOL_TYPE):
            value = self.tkvars[param.option].get()

        elif param.vtype == pc.INT_TYPE:
            value = stoi(self.tkvars[param.option].get())

        elif param.vtype == pc.BLIST_TYPE:
            holes = len(self.tkvars[param.option])
            if param.option == ckey.UDIR_HOLES:
                if ckey.HOLES in self.tkvars:
                    holes = stoi(self.tkvars[ckey.HOLES].get())
                else:
                    holes = game_config[ckey.GAME_CONSTANTS][ckey.HOLES]

            add_in = 1 if param.option == ckey.CAPT_ON else 0
            value = [nbr + add_in
                     for nbr, var in enumerate(self.tkvars[param.option])
                     if var.get() and nbr < holes]

        elif param.vtype == pc.ILIST_TYPE:
            value = [int(var.get()) for var in self.tkvars[param.option]]

        elif param.vtype in pc.STRING_DICTS:
            str_dict = pc.STRING_DICTS[param.vtype].str_dict
            value = self.tkvars[param.option].get()
            value = str_dict[value]

        man_config.set_config_value(
            game_config, param.cspec, param.option, value)


    def pm_resize_udirs(self):
        """Change the number of the checkboxes on the screen,
        limiting it to MAX_HOLES.
        All the variables were built with the tkvars.
        Destroy any extra widgets or make any required new ones."""

        holes = stoi(self.tkvars[ckey.HOLES].get())

        if holes > gconsts.MAX_HOLES:
            self.tkvars[ckey.HOLES].set(str(gconsts.MAX_HOLES))
            holes = gconsts.MAX_HOLES
            message = f'Holes is limited to {gconsts.MAX_HOLES}.'
            ui_utils.showerror(self, 'Out of Range', message)

        widgets = self.udir_frame.winfo_children()
        prev_holes = len(widgets)

        for idx in range(holes, prev_holes):
            widgets[idx].destroy()

        for idx in range(prev_holes + 1, holes + 1):
            ttk.Checkbutton(self.udir_frame, text=str(idx),
                            variable=self.tkvars[ckey.UDIR_HOLES][idx - 1]
                            ).pack(side=tk.LEFT)


    def pm_reset_ui_default(self, param):
        """Reset the tk variables to the user interface defaults"""

        if param.vtype in (pc.MSTR_TYPE, pc.TEXTDICT):
            self.tktexts[param.option].delete('1.0', tk.END)
            self.tktexts[param.option].insert('1.0', param.ui_default)

        elif param.vtype in pc.STRING_DICTS:
            _, inv_dict, enum_dict = pc.STRING_DICTS[param.vtype]
            value = inv_dict[enum_dict[param.ui_default]]
            self.tkvars[param.option].set(value)

        elif param.vtype == pc.BLIST_TYPE:
            for var in self.tkvars[param.option]:
                var.set(False)

        elif param.vtype == pc.ILIST_TYPE:
            default = param.ui_default
            if (default
                    and isinstance(default, list)
                    and len(default) == self._get_boxes_config(param)):

                for var, val in zip(self.tkvars[param.option], default):
                    var.set(val)

        elif param.vtype != pc.LABEL_TYPE:
            self.tkvars[param.option].set(param.ui_default)


    def pm_reset_const_default(self, param):
        """Reset the parameter to the construction default."""

        default = man_config.get_construct_default(
                    param.vtype, param.cspec, param.option)

        if param.vtype in (pc.MSTR_TYPE, pc.TEXTDICT):
            self.tktexts[param.option].delete('1.0', tk.END)
            self.tktexts[param.option].insert('1.0', default)

        elif param.vtype in pc.STRING_DICTS:
            inv_dict = pc.STRING_DICTS[param.vtype][1]
            value = inv_dict[default]
            self.tkvars[param.option].set(value)

        elif param.vtype == pc.BLIST_TYPE:
            for var in self.tkvars[param.option]:
                var.set(False)

        elif param.vtype == pc.ILIST_TYPE:
            if (default
                    and isinstance(default, list)
                    and len(default) == self._get_boxes_config(param)):

                for var, val in zip(self.tkvars[param.option], default):
                    var.set(val)

        elif param.vtype != pc.LABEL_TYPE:
            self.tkvars[param.option].set(default)
