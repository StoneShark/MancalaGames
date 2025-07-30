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

import man_path

FAV_FILE = 'favorites.csv'


class GameFavorites:
    """A class that manages game ratings."""

    def __init__(self):

        self.favs = {}
        self.pathname = None
        self._load_file()


    def _load_file(self):
        """Load the favorites.csv file into a dictionary.

        File format is:   game_name,rating"""

        self.pathname = man_path.find_gamefile(FAV_FILE, no_error=True)
        if not self.pathname:
            return

        with open(self.pathname, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

        for line in data:
            if len(line) != 2:
                print(f'Skipping {line}')
                continue

            gname, rating = line
            try:
                self.favs[gname] = int(rating)
            except ValueError:
                print(f'Skipping favorite {gname}; rating not int.')


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
