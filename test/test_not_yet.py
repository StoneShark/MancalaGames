# -*- coding: utf-8 -*-
"""The point of this file to get all of the source files
included in the coverage report (make unit_tests).

Created on Mon Jul 31 14:07:52 2023
@author: Ann
"""

import sys

import pytest

sys.path.extend(['src'])

import hole_button
import mancala_games
import mancala_ui
import play_mancala
import play


def test_files_not():

    assert True
