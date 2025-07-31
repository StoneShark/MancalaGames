# -*- coding: utf-8 -*-
"""Allow games to be rated in the GameChooser.

The ratings are kept in a separate file favorites.csv along
side the game property files.

The GameChooser can filter games based on ratings.

Created on Wed Jul 30 07:35:43 2025
@author: Ann
"""

import csv
import os.path
import shutil

import man_path
import ui_utils

FAV_FILE = 'favorites.csv'


class GameFavorites:
    """A class that manages game ratings."""

    def __init__(self, master):

        self.master = master
        self.favs = {}
        self.pathname = None
        self._load_file()


    def _read_favs(self):
        """Read the data file."""

        with open(self.pathname, 'r', encoding='utf-8') as file:
            data = list(csv.reader(file))

        return data


    def _backup_favs(self):
        """Move the favorites file to a backup file, but
        don't overwrite an existing file (unless there are
        already 20 backups).

        Return the name of the back up file."""

        for cnt in range(20):

            backup = self.pathname + '.bak'
            if cnt:
                backup += str(cnt)

            if not os.path.isfile(backup):
                break

        shutil.move(self.pathname, backup)
        return backup


    def _load_file_int(self):
        """Load the favorites.csv file into a dictionary.

        File format is:   game_name,rating"""

        self.pathname = man_path.find_gamefile(FAV_FILE, no_error=True)
        if not self.pathname:
            return

        data = self._read_favs()

        for nbr, line in enumerate(data):
            if len(line) != 2:
                raise ValueError(f"Line length wrong at line {nbr + 1}:\n{line}")

            gname, rating = line
            try:
                self.favs[gname] = int(rating)
            except ValueError:
                msg = f'Favorite {gname}; rating not integer.'
                raise ValueError(msg) from None


    def _load_file(self):

        try:
            self._load_file_int()

        except ValueError as exp:
            backup = self._backup_favs()
            ui_utils.showerror(self.master, 'Corrupt favorites.csv',
                               [f"""Corrupt favorites file found.
                                 It was moved to {backup}""",
                                str(exp)])


    def _save_file(self):
        """Write the favorites.csv file."""

        if not self.pathname:
            path = man_path.get_path(man_path.GAMEPATH)
            if path:
                self.pathname = os.path.join(path, FAV_FILE)
            else:
                self.pathname = FAV_FILE

        with open(self.pathname, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            for key, val in self.favs.items():
                writer.writerow([key, val])


    def rate_game(self, gamename, rating):
        """Record the game rating."""

        if rating:
            self.favs[gamename] = rating
        else:
            self.favs.pop(gamename, None)

        self._save_file()


    def rating(self, gamename):
        """Return the rating of the game, return None
        if the game is not rated."""

        return self.favs.get(gamename, 0)
