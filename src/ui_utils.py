# -*- coding: utf-8 -*-
"""Utility operations for tk/ttk and mancala games.

Created on Sun Mar  9 07:04:43 2025
@author: Ann"""

import functools as ft
import webbrowser
import tkinter as tk
from tkinter import ttk

import man_path
import version


MY_BLUE = '#00008b'
DK_BLUE = '#00006b'
LT_BLUE = '#8080cb'

WHITE = '#ffffff'
BLACK = '#000000'

BGROUND = '#f0f0f0'
DK_BGROUND = '#e8e8e8'

ARROW = 'grey20'
DIS_FG = 'grey40'
UNSEL_TAB = 'grey60'
LABEL = 'grey70'
BTN_HLIGHT = 'grey80'


def setup_styles(root):
    """Define the global styles used for MancalaGames (mancala_games)
    and GameChooser (play_mancala).

    Using clam because it supports more options than default.
    This is 'styling' both tk and ttk widgets."""

    style = ttk.Style()
    style.theme_use('clam')

    style.configure('.', background=BGROUND)
    style.map('.',
              background=[('disabled', BGROUND)],
              foreground=[('disabled', DIS_FG)])

    style.map('TButton', background=[('active',  BTN_HLIGHT)])

    style.configure('Filt.TButton', width=-9, padding=1)

    style.configure('Play.TButton',
                    background=MY_BLUE,
                    foreground=WHITE,
                    borderwidth=5,
                    font=('bold', 12))
    style.map('Play.TButton', background=[('active',  DK_BLUE)])

    # clam theme shows an x in the boxes, this fills them in
    style.map('TCheckbutton',
               indicatorbackground=[('selected', '!disabled', MY_BLUE),
                                    ('selected', 'disabled',  LT_BLUE)],
               indicatorforeground=[('selected', '!disabled', MY_BLUE),
                                    ('selected', 'disabled',  LT_BLUE)])

    style.configure('TEntry',
                    padding=2,
                    selectbackground=MY_BLUE,
                    selectforeground=WHITE)
    style.map('TEntry', bordercolor=[('focus', MY_BLUE)])

    style.configure('Title.TLabel', background=LABEL, anchor='center')
    style.map('Title.TLabel',
              background=[('disabled', LABEL)],
              foreground=[('disabled', BLACK)])

    # for ttk.OptionMenu
    style.configure('TMenubutton', padding=1, arrowcolor=ARROW)
    style.map('TMenubutton', arrowcolor=[('disabled', DIS_FG)])

    style.configure('TNotebook', background=DK_BGROUND, padding=4)
    style.map('TNotebook.Tab',
              expand=[('selected', [0, 4, 4, 0])],
              background=[('selected', BGROUND),
                          ('!selected', UNSEL_TAB)])

    style.configure('TScrollbar',
                    arrowcolor=ARROW,
                    lightcolor=WHITE,
                    darkcolor='grey20',
                    bordercolor='grey50',
                    troughcolor='grey80')

    style.map('Treeview',
              background=[('selected', MY_BLUE)],
              foreground=[('selected', WHITE)])

    # set the colors for the text box
    root.option_add("*selectForeground", WHITE)
    root.option_add("*selectBackground", MY_BLUE)

    # set the color for menu and optionmenu highlighting
    root.option_add("*activeForeground", WHITE)
    root.option_add("*activeBackground", MY_BLUE)


def quiet_dialog(parent, title, text):
    """Popup a quiet dialog message.

    The messagebox methods all make a warning tone."""

    xpos = parent.winfo_rootx() + 100
    ypos = parent.winfo_rooty() + 50

    top = tk.Toplevel(parent)
    top.resizable(False, False)
    top.lift(aboveThis=parent)
    top.title(title)
    top.wm_geometry(f'+{xpos}+{ypos}')
    top.minsize(200, 100)
    top.grab_set()

    frame = tk.Frame(top, borderwidth=10)
    frame.pack(side='top', expand=True)

    tk.Label(frame, anchor='nw', justify='left', text=text
             ).pack(side='top')
    tk.Button(frame, text='Ok', command=top.destroy).pack(side='bottom')


def add_help_menu(menubar, master):
    """Add the help menu bar."""

    helpmenu = tk.Menu(menubar)
    helpmenu.add_command(label='Help...', command=show_main_help)
    helpmenu.add_command(label='Parameters...', command=show_param_help)
    helpmenu.add_command(label='Games...', command=show_game_help)
    helpmenu.add_separator()

    helpmenu.add_command(label='About...',
                         command=ft.partial(show_release, master))
    menubar.add_cascade(label='Help', menu=helpmenu)


def show_main_help():
    """Have the os pop open the help file in a browser."""

    webbrowser.open(man_path.get_path('mancala_help.html'))


def show_param_help():
    """Have the os pop open the help file in a browser."""

    webbrowser.open(man_path.get_path('game_params.html'))


def show_game_help():
    """Have the os pop open the help file in a browser."""

    webbrowser.open(man_path.get_path('about_games.html'))


def show_release(parent):
    """Show the Release text."""

    quiet_dialog(parent, 'About Manacala Games', version.RELEASE_TEXT)
