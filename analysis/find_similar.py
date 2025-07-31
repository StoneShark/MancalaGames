# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 10:45:03 2025
@author: Ann"""

# %% imports

import collections
import csv
import itertools as it
import os

from context import cfg_keys as ckey
from context import game_info as gi
from context import man_config
from context import man_path


# %% constants

DIR = 'GameProps'
PATH = '../GameProps/'

TXTPART = '.txt'
EXFILE = '_all_params.txt'

TAB_IDX = 0
OPTION_IDX = 1
SKIP_TAB = 'skip'
LBL_OPT = 'lbl'

GCONSTS = ckey.GAME_CONSTANTS
GINFO = ckey.GAME_INFO


# %% unused routines

def get_params():
    """Read the game parameters file and return a list params."""

    with open(man_path.get_path('../src/game_params.csv'), 'r',
              encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

    return [rec[OPTION_IDX] for rec in data[1:]
            if rec[TAB_IDX] != SKIP_TAB
                and LBL_OPT not in rec[OPTION_IDX]]


# %% neighbors class

class Neighbors:
    """A class to support comparing and contrasting game
    parameters."""


    def __init__(self):

        self.all_games = self.load_game_files()
        self.neighs = self.find_similar()

        self.print_summary()


    def load_game_files(self):
        """Get a list of the game files, read the game_dict,
        create a dictionary."""

        all_games = {}
        for file in os.listdir(PATH):

            if file[-4:] != TXTPART or file == EXFILE:
                continue

            game_dict = man_config.read_game(PATH + file)

            game_name = game_dict[ckey.GAME_INFO][ckey.NAME]
            all_games[game_name] = game_dict

        return all_games


    def find_similar(self):
        """Create a dictionary where the keys are the number of
        differences and the values are a list of game pairs with
        those differences.  Sort it by number of differences."""

        gname_list = list(self.all_games.keys())
        diff_dict = collections.defaultdict(list)

        for gname1, gname2 in it.combinations(gname_list, 2):

            diffs = self.count_diffs(self.all_games[gname1],
                                     self.all_games[gname2])
            diff_dict[diffs] += [(gname1, gname2)]

        return diff_dict


    @staticmethod
    def list_diffs(gdict1, gdict2):
        """Create a list of the game parameters that are different
        between the two games."""

        dlist = []

        if gdict1[ckey.GAME_CLASS] != gdict2[ckey.GAME_CLASS]:
            dlist += [ckey.GAME_CLASS]

        for param in ckey.GCONST_PARAMS:
            if gdict1[GCONSTS][param] != gdict2[GCONSTS][param]:
                dlist += [param]

        for param in ckey.GINFO_PARAMS:

            default = gi.GameInfo.get_default(param)
            val1 = gdict1[GINFO].get(param, default)
            val2 = gdict2[GINFO].get(param, default)
            if val1 != val2:
                dlist += [param]

        return dlist


    @staticmethod
    def count_diffs(gdict1, gdict2):
        """Count the number of differences between the two game
        configurations.  Keys are not required in ginfo so need
        to look up the default if it is not in the dictionary.
        game class and both constansts are required."""

        pdiffs = 0
        for param in ckey.GINFO_PARAMS:

            default = gi.GameInfo.get_default(param)
            val1 = gdict1[GINFO].get(param, default)
            val2 = gdict2[GINFO].get(param, default)
            if val1 != val2:
                pdiffs += 1

        return sum([pdiffs,

            1 if gdict1[ckey.GAME_CLASS] != gdict2[ckey.GAME_CLASS] else 0,

            sum(1 for param in ckey.GCONST_PARAMS
                   if gdict1[GCONSTS][param] != gdict2[GCONSTS][param]),
            ])


    def list_diffs_names(self, game1, game2):
        """List the differences but start with the game names"""

        return self.list_diffs(self.all_games[game1], self.all_games[game2])


    def sorted_items(self):
        """Return the sorted items"""

        return sorted(self.neighs.items(), key=lambda item: item[0])


    def print_summary(self):
        """Print a summary of the results."""

        print("Diff  Count")
        for nbr_diff, pairs in self.sorted_items():

            print(f"{nbr_diff:3}: {len(pairs):4}")

        for d in range(1, 3):
            print(f"Pairs differing by {d} param(s):")
            for g1, g2 in self.neighs[d]:
                print(f'   {g1:20}  {g2:20}')
            print()


    def one_game(self, game, max_diffs=5):
        """Print the distances of all games from the one provided."""

        print(game)
        for nbr_diff, pairs in self.sorted_items():

            if nbr_diff > max_diffs:
                return

            title = f"  {nbr_diff}:"
            for game1, game2 in pairs:

                match1 = game == game1
                match2 = game == game2
                if title and (match1 or match2):
                    if title:
                        print(title)
                        title = None

                if match1:
                    print(f"     {game2}")
                if match2:
                    print(f"     {game1}")


    @staticmethod
    def print_line(values):
        """Print a list of values in columns."""

        print("".join(f"{str(val):20}" for val in values))


    def print_option_line(self, gname_list, option, key=None):
        """Prepare and print one line for option for each game."""

        pvalues = [option]

        for game in gname_list:
            default = gi.GameInfo.get_default(option)

            if key:
                pvalues += [self.all_games[game][key].get(option, default)]
            else:
                pvalues += [self.all_games[game].get(option, default)]

        self.print_line(pvalues)


    def print_diff_table(self, gname_list):
        """Print a table of the values that differ."""

        # gname_list = sorted(gname_list)

        options = set()
        for g1, g2 in it.combinations(gname_list, 2):
            options |= set(self.list_diffs(self.all_games[g1],
                                           self.all_games[g2]))

        self.print_line(["Option"] + gname_list)

        if ckey.GAME_CLASS in options:
            self.print_option_line(gname_list, ckey.GAME_CLASS)

        starters = [ckey.HOLES, ckey.NBR_START]
        for opt in starters:
            if opt in options:
                self.print_option_line(gname_list, opt, GCONSTS)

        starters += [ckey.GAME_CLASS]
        for opt in sorted(options):
            if opt not in starters:
                self.print_option_line(gname_list, opt, GINFO)


    def uniquer(self, max_diffs):
        """Return a list of games that do not have any other game within
        max_diffs of it.

        This is a bit flawed; for example, a unique game like Diffusion has
        DiffusionV2 1 parameter away from it."""

        games = set(self.all_games.keys())

        for nbr_diff, pairs in self.sorted_items():

            if nbr_diff > max_diffs:
                break

            for pair in pairs:
                games -= set(pair)

        return games


# %%

neighs = Neighbors()
