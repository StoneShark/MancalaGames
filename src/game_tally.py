# -*- coding: utf-8 -*-
"""Create a game tally class to display the
wins/loses/ties (from false's perspective).

Created on Sun Nov 12 20:33:14 2023
@author: Ann"""


import tkinter as tk

from game_interface import WinCond


class GameTally:
    """Class to collect game data across multiple games."""

    def __init__(self, frame):
        """Set the counts to 0."""

        self.games = 0
        self.game_wins = [0, 0]
        self.game_ties = 0

        self.rounds = 0
        self.round_wins = [0, 0]
        self.round_ties = 0

        self.games_str = tk.StringVar(frame, '  0')
        self.gtwins_str = tk.StringVar(frame, '  0')
        self.gfwins_str = tk.StringVar(frame, '  0')
        self.gties_str = tk.StringVar(frame, '  0')

        self.rounds_str = tk.StringVar(frame, '  0')
        self.rtwins_str = tk.StringVar(frame, '  0')
        self.rfwins_str = tk.StringVar(frame, '  0')
        self.rties_str = tk.StringVar(frame, '  0')

        tk.Label(frame, text='Games Played:'
                 ).grid(row=0, column=0, columnspan=2)
        tk.Label(frame, textvariable=self.games_str).grid(row=0, column=2)

        tk.Label(frame, text='Wins:').grid(row=1, column=0)
        tk.Label(frame, textvariable=self.gfwins_str).grid(row=1, column=1)
        tk.Label(frame, text='Loses:').grid(row=1, column=2)
        tk.Label(frame, textvariable=self.gtwins_str).grid(row=1, column=3)
        tk.Label(frame, text='Ties:').grid(row=1, column=4)
        tk.Label(frame, textvariable=self.gties_str).grid(row=1, column=5)

        tk.Label(frame, text=' ').grid(row=2, column=0)

        tk.Label(frame, text='Rounds Played:', anchor=tk.W
                 ).grid(row=3, column=0, columnspan=2)
        tk.Label(frame, textvariable=self.rounds_str).grid(row=3, column=2)

        tk.Label(frame, text='Wins:').grid(row=4, column=0)
        tk.Label(frame, textvariable=self.rfwins_str).grid(row=4, column=1)
        tk.Label(frame, text='Loses:').grid(row=4, column=2)
        tk.Label(frame, textvariable=self.rtwins_str).grid(row=4, column=3)
        tk.Label(frame, text='Ties:').grid(row=4, column=4)
        tk.Label(frame, textvariable=self.rties_str).grid(row=4, column=5)


    def tally_game(self, winner, win_cond):
        """Ignore the odd outcomes.

        If we get round results tally them, but a game result
        ends the rounds (so reset the round numbers).

        winner: boolean - player that won if win.
        win_cond: WinCond - outcome of the game."""

        if win_cond in [WinCond.REPEAT_TURN, WinCond.ENDLESS]:
            return

        if win_cond is WinCond.ROUND_WIN:
            self.rounds += 1
            self.round_wins[winner] += 1

        if win_cond is WinCond.ROUND_TIE:
            self.rounds += 1
            self.round_ties += 1

        if win_cond is WinCond.WIN:
            self.games += 1
            self.game_wins[winner] += 1

        if win_cond is WinCond.TIE:
            self.games += 1
            self.game_ties += 1

        if win_cond in [WinCond.WIN, WinCond.TIE]:
            self.rounds = 0
            self.round_wins = [0, 0]
            self.round_ties = 0

        self.games_str.set(f'{self.games:3}')
        self.gtwins_str.set(f'{self.game_wins[1]:3}')
        self.gfwins_str.set(f'{self.game_wins[0]:3}')
        self.gties_str.set(f'{self.game_ties:3}')

        self.rounds_str.set(f'{self.rounds:3}')
        self.rtwins_str.set(f'{self.round_wins[1]:3}')
        self.rfwins_str.set(f'{self.round_wins[0]:3}')
        self.rties_str.set(f'{self.round_ties:3}')
