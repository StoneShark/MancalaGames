# -*- coding: utf-8 -*-
"""Utility operations for tk/ttk and mancala games.

Created on Sun Mar  9 07:04:43 2025
@author: Ann"""

import functools as ft
import json
import traceback
import tkinter as tk
import tkinter.simpledialog as tksimpledialog
from tkinter import ttk
import warnings
import webbrowser

import game_constants as gconsts
import game_info as gi
import format_msg as fmt
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

    style.configure('Filt.TButton', width=-5, padding=0,
                    font=('Helvetica', 8))

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

    # the sash for the panedwindow in the editor
    style.configure('Sash',
                    gripcount=30,
                    lightcolor=MY_BLUE)

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

        # pylint: disable=use-implicit-booleaness-not-comparison-to-zero
        # we mean zero, not falsy

        if isinstance(value, bool):
            self.value = value

        elif value == 0:
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

class QuietDialog(tksimpledialog.Dialog):
    """A simple modal quiet dialog box."""

    def __init__(self, master, title, message,
                 *, fixed_form=False, wide=False):

        if fixed_form:
            self.msg = message
        else:
            self.msg = fmt.fmsg(message, wide)
        super().__init__(master, title)


    def body(self, master):
        """Put the message in a label in the master."""

        self.resizable(False, False)
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

    def __init__(self, master, title, message, is_round):

        self.mancala_ui = master
        self.msg = fmt.fmsg(message)
        self.is_round = is_round

        self.new_game = False              # the return value
        super().__init__(master, title)


    def body(self, master):
        """Put the message in a label in the master and ring the bell."""

        self.resizable(False, False)
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
                  command=self.mancala_ui.glog_save_log).pack(side=tk.LEFT)
        tk.Button(bframe, text='Wait', width=12,
                  command=self.cancel).pack(side=tk.LEFT)

        btn_lbl = 'New Round' if self.is_round else 'New Game'
        tk.Button(bframe, text=btn_lbl, width=12,
                  command=self.ok, default=tk.ACTIVE).pack(side=tk.RIGHT)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


    def apply(self):
        """Start a new game."""
        self.new_game = True


def win_popup_new_game(master, title, message, is_round):
    """Wrap the WinPopup so we can return if a new round/game was
    requested."""

    obj = WinPopup(master, title, message, is_round)
    return obj.new_game


class PassPopup(tksimpledialog.Dialog):
    """A popup for the pass dialog which also provides
    End Round and Game buttons. Need because if the AI doesn't
    make a turn available the user doesn't regain control."""

    def __init__(self, master, title, message, quit_round):

        self.msg = fmt.fmsg(message)
        self.mancala_ui = master
        self.quit_round = quit_round
        super().__init__(master, title)


    def body(self, master):
        """Put the message in a label in the master."""

        self.resizable(False, False)
        label = tk.Label(master, text=self.msg,
                         anchor='nw', justify=tk.LEFT, padx=5, pady=5)
        label.pack(side=tk.TOP)
        return label


    def buttonbox(self):
        """Add end round and quit game buttons.
        Bind return to Ok and escape to Cancel."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        if self.quit_round:
            tk.Button(bframe, text='End Round', width=12,
                      command=lambda: (self.ok(),
                                       self.mancala_ui.end_game(quitter=True,
                                                                game=False))
                      ).pack(side=tk.LEFT)
        else:
            tk.Button(bframe, text='End Game', width=12,
                      command=lambda: (self.ok(),
                                       self.mancala_ui.end_game(quitter=True,
                                                                game=True))
                      ).pack(side=tk.LEFT)
        tk.Button(bframe, text='Ok', command=self.ok, width=12,
                  default=tk.ACTIVE
                  ).pack(side='right')

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


class GetSeedsPopup(tksimpledialog.Dialog):
    """A popup to get a number of seeds to pick up."""

    def __init__(self, master, title, max_seeds, font):

        self.mancala_ui = master
        self.value = 0
        self.max_seeds = max_seeds
        self.font = font

        super().__init__(master, title)


    def body(self, master):
        """Create an entry box that will validate as integer."""

        self.resizable(False, False)
        self.entry = ttk.Entry(master, font=self.font)
        self.entry.pack(side=tk.TOP, expand=True, fill=tk.Y)

        return self.entry


    def buttonbox(self):
        """Create Dump Game, Save Game, and Ok buttons.
        Bind return to Ok."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack(expand=True, fill=tk.BOTH)


        tk.Button(bframe, text='All', command=self.pick_all,
                  font=self.font,
                  ).grid(row=0, column=0, stick='nsew')

        tk.Button(bframe, text='One', command=self.pick_one,
                  font=self.font,
                  ).grid(row=0, column=1, stick='nsew')

        tk.Button(bframe, text='',
                  font=self.font,
                  ).grid(row=0, column=2, stick='nsew')

        for nbr in range(10):
            row = 3 - (nbr + 2) // 3 + 1
            col = (nbr - 1) % 3 if nbr else 0

            tk.Button(bframe, text=str(nbr), width=3,
                      font=self.font,
                      command=ft.partial(self.digit, nbr)
                      ).grid(row=row, column=col, stick='nsew')

        tk.Button(bframe, text='Bsp', command=self.backspace,
                  font=self.font,
                  ).grid(row=4, column=1, stick='nsew')

        tk.Button(bframe, text='Ok', command=self.ok,
                  font=self.font,
                  ).grid(row=4, column=2, stick='nsew')

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


    def digit(self, nbr, _=None):
        """Enter a digit into the entry widget."""

        self.entry.insert(tk.END, nbr)


    def backspace(self, _=None):
        """Backspace one character."""

        self.entry.delete(self.entry.index(tk.END) - 1)


    def pick_all(self):
        """Pick all the seeds and return."""

        self.entry.delete('1', tk.END)
        self.entry.insert('1', str(self.max_seeds))
        self.ok()


    def pick_one(self):
        """Pick one seed and return."""

        self.entry.delete('1', tk.END)
        self.entry.insert('1', '1')
        self.ok()


def get_nbr_seeds(master, max_seeds, font):
    """Wrap the GetSeedsPopup so we can return the value entered."""

    obj = GetSeedsPopup(master, 'Number Seeds', max_seeds, font)
    return obj.value


class ExceptPopup(tksimpledialog.Dialog):
    """Popup the exception window with options to
        1. save the game log (if logsave)
        2. copy the error data to the clip board"""

    def __init__(self, root, title, message, trace, copy_data, param_data):

        self.root = root
        self.msg = fmt.fmsg(message, wide=True)
        self.trace = trace
        self.copy_data = copy_data
        self.param_data = param_data

        super().__init__(root, title)


    def body(self, master):
        """Put the message in a label in the master and ring the bell."""

        self.resizable(False, False)
        master.bell()
        label = tk.Label(master, text=self.msg,
                         anchor='nw', justify=tk.LEFT, padx=5, pady=5)
        label.pack(side=tk.TOP)

        tk.Label(master, text=self.trace, font='TkFixedFont',
                 anchor='nw', justify=tk.LEFT, padx=5, pady=5
                 ).pack(side=tk.TOP)

        return label


    def buttonbox(self):
        """Create save log, copy error, and Ok buttons.
        Bind return to Ok."""

        bframe = tk.Frame(self, borderwidth=20)
        bframe.pack()

        tk.Button(bframe, text='Copy Error Data', width=12,
                  command=self.load_clipboard
                  ).pack(side=tk.LEFT, padx=5, pady=5)

        if self.param_data:
            tk.Button(bframe, text='Save Game Log', width=12,
                      command=self.save_log
                      ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(bframe, text='Ok', width=12,
                  command=self.ok, default=tk.ACTIVE
                  ).pack(side=tk.RIGHT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


    def save_log(self):
        """Save the game log."""

        game_log.save(self.param_data)


    def load_clipboard(self):
        """Put the copy data onto the clipboard."""

        self.master.clipboard_clear()
        self.master.clipboard_append(self.copy_data)


# %%  MessageDialogs

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

    def __init__(self, master, title, message, buttons, icon=None):

        self.msg = fmt.fmsg(message)
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
        self.resizable(False, False)
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


# %% key bindings

def key_bindings(window, bindings, active):
    """Do or undo key bindings.

    window: the main ui app frame which must have
    master and bind_ids attributes.

    bindings: key sequence, command pairs"""

    if active:
        window.bind_ids = [window.master.bind(key_seq, op)
                           for key_seq, op in bindings]

    elif window.bind_ids:
        for(key_seq, _), bid in zip(bindings, window.bind_ids):
            window.master.unbind(key_seq, bid)
        window.bind_ids = None


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

    def increment(self):
        """Increment the value w/o using it."""

        self.value += 1


# %%   ReportError

class ReportError:
    """A context manager that traps game build errors and
    reports them via a popup. The context can be interrogated
    after use to see if an error was suppressed."""

    def __init__(self, frame):

        self.error = False
        self.frame = frame

    def __enter__(self):
        """Required interface for a context manager."""

        return None

    def __exit__(self, exc_type, exc_value, _):
        """Return True if there was no error or if it should
        be suppressed."""

        if exc_type is None:
            return True

        wtitle = 'Mancala Games Error'
        if exc_type in (NotImplementedError,
                        gconsts.GameConstsError,
                        gi.GameInfoError,
                        gi.UInputError):
            wtitle = 'Parameter Error'

        elif exc_type == FileNotFoundError:
            wtitle = 'File Not Found'

        elif exc_type == json.decoder.JSONDecodeError:
            wtitle = 'JSON Format Error'

        elif exc_type == gi.GameVariantError:
            wtitle = 'Variations Error'

        else:
            # the exception should be propagated
            return False

        self.error = True
        message = exc_type.__name__ + ':  ' + str(exc_value)
        showerror(self.frame, wtitle, message)
        return True


# %% trap warnings/excpetions outside ReportError


GITHUBLINK = 'https://github.com/StoneShark/MancalaGames/issues'

APP_FRAME = None
GAME_UI = None


def exception_callback(*args):
    """Support debugging by printing the play_log and the traceback."""

    etype, evalue, trace, *_ = args
    tb_lst = traceback.format_exception(etype, evalue, trace)

    # dump game for unknown errors
    if etype != gi.DataError and GAME_UI:
        game_log.dump()

    # output to console, though it might not be there
    for line in tb_lst:
        print(line, end='')

    if not APP_FRAME:
        return

    if etype == gi.DataError:
        title = 'Data Error'
        message = ["""A data error was detected in a file that should
                   not be edited by players.""",
                   f"""If you have not edited the parameter configuration
                   files, this might be a software bug; consider reporting
                   it at {GITHUBLINK}"""]

    else:
        title = 'Internal Error'
        message = ["An internal error occurred.",
                   f"""Reporting this error at {GITHUBLINK}
                   would help improve Mancala Games.
                   Include a screen shot of this popup and
                   any other information you think would be valuable.""",
                   """This error could lead to unstable behavior,
                   you may wish to save any work and restart."""]

    trace = ''.join(tb_lst)
    copy_data = ''.join([GITHUBLINK, '\n\n'] + tb_lst)
    param_data = GAME_UI.game.params_str() if GAME_UI else None

    ExceptPopup(APP_FRAME, title, message, trace, copy_data, param_data)


def warning_callback(message, *_):
    """Notify user of warnings during parameter test."""

    showwarning(APP_FRAME, 'Parameter Warning', str(message))


def do_error_popups(root, game_ui_in=None):
    """Save the app_frame and record the warning and exception call backs"""

    global APP_FRAME
    global GAME_UI

    APP_FRAME = root
    GAME_UI = game_ui_in

    APP_FRAME.report_callback_exception = exception_callback

    warnings.showwarning = warning_callback
    warnings.simplefilter('always', UserWarning)
