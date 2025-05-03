# -*- coding: utf-8 -*-
"""Utility operations for tk/ttk and mancala games.

Created on Sun Mar  9 07:04:43 2025
@author: Ann"""

import functools as ft
import re
import textwrap
import tkinter as tk
import tkinter.simpledialog as tksimpledialog
from tkinter import ttk
import webbrowser

import man_path
import version
from game_logger import game_log


# %% cursors


NORMAL = ''
AI_BUSY = 'watch'
ANI_ACTIVE = 'exchange'  #'hand2'
HOLD_SEEDS = 'circle'


# %% common styles

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

    #  on: filled    off:  open as above    don't care: x
    style.map('TriState.TCheckbutton',
                indicatorbackground=[('selected', '!alternate', MY_BLUE),  # on
                                     ('selected', 'alternate', WHITE),  # dc
                                     ('!selected', WHITE)   # off
                                    ],
                indicatorforeground=[('selected', '!alternate', MY_BLUE),
                                     ('alternate', MY_BLUE),
                                     ('!selected', WHITE)
                                    ])

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


# %%  tri-state checkbox


class TriStateCheckbutton(ttk.Checkbutton):
    """A checkbox that cycles through three states: False, None, True.
    """

    def __init__(self, master, text, update_cmd=None):

        super().__init__(master, text=text, command=self.cycle,
                         style='TriState.TCheckbutton')
        self.update_cmd = update_cmd
        self.value = None
        self.update()


    def update(self):
        """Update the widget state for our value."""

        if self.value is False:
            self.state(['!selected'])

        elif self.value is None:
            self.state(['selected', 'alternate'])

        else:   # True
            self.state(['selected', '!alternate'])


    def set(self, value):
        """Set the value (just like we were a tk variable).
        value needs to translated to be one of
        False, True, None"""

        # we mean zero, not falsy
        # pylint: disable=compare-to-zero
        if value == 0:
            self.value = False

        elif value == 1:
            # want to show all, so set don't care
            self.value = None

        else:
            self.value = value
        self.update()


    def get(self):
        """Get the value (just like we were a tk variable)"""

        return self.value


    def cycle(self):
        """Cycle the checkbox state."""

        if self.value is False:
            self.value = None

        elif self.value is None:
            self.value = True

        else:
            self.value = False
        self.update()

        if self.update_cmd:
            self.update_cmd()


# %% popup dialogs

RECOMP = re.compile('\n *')
TEXTFILL = textwrap.TextWrapper(width=50)

def format_message(message):
    """Format any message for a popup.
    message may be a string or list of strings

    If a string, format it.
    Otherwise, format each individual string as a paragraph.
    Join them together with two blank lines."""

    if isinstance(message, list):
        return '\n\n'.join(TEXTFILL.fill(RECOMP.sub(' ', m))
                           for m in message)
    return TEXTFILL.fill(RECOMP.sub(' ', message))


class QuietDialog(tksimpledialog.Dialog):
    """A simple modal quiet dialog box."""

    def __init__(self, master, title, message, fixed_form=False):

        if fixed_form:
            self.msg = message
        else:
            self.msg = format_message(message)
        super().__init__(master, title)


    def body(self, master):
        """Put the message in a label in the master."""

        label = tk.Label(master, text=self.msg,
                         anchor='nw', justify=tk.LEFT, padx=5, pady=5)
        label.pack(side=tk.TOP)
        return label


    def buttonbox(self):
        """Create an ok button and bind the return key."""

        box = tk.Frame(self)
        box.pack()

        tk.Button(box, text="OK", width=10,
                  command=self.ok, default=tk.ACTIVE
                  ).pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


class WinPopup(tksimpledialog.Dialog):
    """Popup the win window with a game dump option."""

    def __init__(self, master, title, message):

        self.mancala_ui = master
        self.msg = format_message(message)
        super().__init__(master, title)


    def body(self, master):
        """Put the message in a label in the master and ring the bell."""

        master.bell()
        label = tk.Label(master, text=self.msg,
                         anchor='nw', justify=tk.LEFT, padx=5, pady=5)
        label.pack(side=tk.TOP)
        return label


    def buttonbox(self):
        """Create Dump Game, Save Game, and Ok buttons.
        Bind return to Ok."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        tk.Button(bframe, text='Dump Game', width=12,
                  command=game_log.dump).pack(side=tk.LEFT)
        tk.Button(bframe, text='Save Game', width=12,
                  command=self.mancala_ui.save_file).pack(side=tk.LEFT)
        tk.Button(bframe, text='Ok', width=12,
                  command=self.ok, default=tk.ACTIVE).pack(side='right')

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


class PassPopup(tksimpledialog.Dialog):
    """A popup for the pass dialog which also provides
    End Round and Game buttons. Need because if the AI doesn't
    make a turn available the user doesn't regain control."""

    def __init__(self, master, title, message):

        self.msg = format_message(message)
        self.mancala_ui = master
        super().__init__(master, title)


    def body(self, master):
        """Put the message in a label in the master."""

        label = tk.Label(master, text=self.msg,
                         anchor='nw', justify=tk.LEFT, padx=5, pady=5)
        label.pack(side=tk.TOP)
        return label


    def buttonbox(self):
        """Create Dump Game, Save Game, and Ok buttons.
        Bind return to Ok."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        tk.Button(bframe, text='End Round', width=12,
                  command=lambda: (self.ok(), self.mancala_ui.end_round())
                  ).pack(side=tk.LEFT)
        tk.Button(bframe, text='End Game', width=12,
                  command=lambda: (self.ok(), self.mancala_ui.end_game())
                  ).pack(side=tk.LEFT)
        tk.Button(bframe, text='Ok', command=self.ok, width=12,
                  default=tk.ACTIVE
                  ).pack(side='right')

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


class GetSeedsPopup(tksimpledialog.Dialog):
    """A popup to get a number of seeds to pick up."""

    def __init__(self, master, title, max_seeds):

        self.mancala_ui = master
        self.value = 0
        self.max_seeds = max_seeds
        super().__init__(master, title)


    def body(self, master):
        """Create an entry box that will validate as integer."""

        self.entry = ttk.Entry(master)
        self.entry.pack(side=tk.TOP)
        return self.entry


    def buttonbox(self):
        """Create Dump Game, Save Game, and Ok buttons.
        Bind return to Ok."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        for nbr in range(10):
            row = 3 - (nbr + 2) // 3
            col = (nbr - 1) % 3 if nbr else 0

            tk.Button(bframe, text=str(nbr), width=3,
                      command=ft.partial(self.digit, nbr)
                      ).grid(row=row, column=col, stick='ew')

        tk.Button(bframe, text='Bsp', command=self.backspace,
                  ).grid(row=3, column=1, stick='ew')

        tk.Button(bframe, text='Ok', command=self.ok
                  ).grid(row=3, column=2, stick='ew')

        bframe.grid_rowconfigure('all', weight=1)
        bframe.grid_columnconfigure('all', weight=1)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


    def apply(self):
        """Get the value from the entry box and validate it."""
        try:
            self.value = int(self.entry.get())
        except ValueError:
            self.value = 0
            self.bell()
            return

        if not 0 < self.value <= self.max_seeds:
            self.value = 0
            self.bell()

        return


    def digit(self, nbr, _=None):
        """Enter a digit into the entry widget."""

        self.entry.insert(tk.END, nbr)


    def backspace(self, _=None):
        """Backspace one character."""

        self.entry.delete(self.entry.index(tk.END) - 1)


def get_nbr_seeds(master, max_seeds):
    """Wrap the GetSeedsPopup so we can return the value entered."""

    obj = GetSeedsPopup(master, 'Number Seeds', max_seeds)
    return obj.value



# values for buttons
OK = 1               # just sayin'
OKCANCEL = 2        # confirm user wants to do requested action
YESNO = 3            # do you want to do action
YESNOCANCEL = 4      # do you want to save ... no, continue wo

# values for icon
INFO = 1
WARN = 2
ERROR = 3

class MessageDialog(tksimpledialog.Dialog):
    """Basic message dialog with standard responses."""

    # pylint: disable=too-many-arguments
    def __init__(self, master, title, message, buttons, icon=None):

        self.msg = format_message(message)
        self.master = master
        self.buttons = buttons
        self.icon = icon
        self.ans = None

        super().__init__(master, title)


    def body(self, master):
        """Put the message in a label in the master."""

        label = tk.Label(master, text=self.msg,
                         anchor='nw', justify=tk.LEFT, padx=5, pady=5)
        label.pack(side=tk.TOP)
        return label


    def buttonbox(self):
        """Create buttons for the MBType.
        If the Ok button is present, it is the default.
        If the Yes buttone is present, it is the default."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        if self.buttons in (OK, OKCANCEL):

            tk.Button(bframe, text='Ok', width=6,
                      command=self.ok_yes, default=tk.ACTIVE
                      ).pack(side=tk.LEFT, padx=5, pady=5)

        if self.buttons in (YESNO, YESNOCANCEL):

            tk.Button(bframe, text='Yes', width=6,
                      command=self.ok_yes, default=tk.ACTIVE
                      ).pack(side=tk.LEFT, padx=5, pady=5)
            tk.Button(bframe, text='No', width=6, command=self.ans_no
                      ).pack(side=tk.LEFT, padx=5, pady=5)

        if self.buttons in (OKCANCEL, YESNOCANCEL):

            tk.Button(bframe, text='Cancel', width=6, command=self.cancel
                      ).pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok_yes)
        self.bind("<Escape>", self.cancel)


    def ok_yes(self, _=None):
        """User clicked ok or yes, record result."""

        self.ans = True
        self.cancel()


    def ans_no(self):
        """User clicked no, record result."""

        self.ans = False
        self.cancel()


def ask_popup(parent, title, message, buttons):
    """Ask a question with predefined buttons groups:
            OK, OKCANCEL, YESNO, YESNOCANCEL

    Return values: Ok or Yes: True,  No: False, Cancel: None"""

    popup = MessageDialog(parent, title, message, buttons)
    return popup.ans


def showinfo(parent, title, message):
    """Show an info message"""
    MessageDialog(parent, title, message, OK, INFO)


def showwarning(parent, title, message):
    """Show a warning message"""
    MessageDialog(parent, title, message, OK, WARN)


def showerror(parent, title, message):
    """Show an error message"""
    MessageDialog(parent, title, message, OK, ERROR)


# %% common help menu

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

    QuietDialog(parent, 'About Manacala Games', version.RELEASE_TEXT,
                fixed_form=True)


# %% Counter

class Counter:
    """A counter that increments every time the count is retrieved.
    Useful for putting UI elements in sequential rows or columns."""

    def __init__(self):
        self.value = -1

    @property
    def count(self):
        """increment round and return it"""
        self.value += 1
        return self.value


    def reset(self):
        """Reset the count."""
        self.value = -1
