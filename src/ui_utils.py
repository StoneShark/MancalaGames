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


def setup_styles(root):
    """Define the global styles."""

    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', background='#f0f0f0', padding=4)
    style.map('.',
              background=[('disabled', '#f0f0f0')],
              foreground=[('disabled', 'grey40')])

    style.configure('Title.TLabel', background='grey80', anchor='center')
    style.map('Title.TLabel',
              background=[('disabled', 'grey80')],
              foreground=[('disabled', 'black')])

    style.configure('Play.TButton', background='grey40', anchor='center',
                    borderwidth=5, foreground="#f0f0f0",
                    font=('bold', 12))

    style.configure('TNotebook.Tab', background='grey60')
    style.map('TNotebook.Tab', expand=[('selected', [4, 4, 4, 0])])

    style.map('Treeview',
              background=[('selected', '#00008b')],
              foreground=[('selected', '#ffffff')])

    # set the colors for the only tk object, the text box
    root.option_add("*selectForeground", "#ffffff")
    root.option_add("*selectBackground", "#00008b")


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
