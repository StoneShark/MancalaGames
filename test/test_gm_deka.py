# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:23:34 2023

@author: Ann
"""

import pytest
pytestmark = [pytest.mark.integtest]

from context import game_interface as gi
from context import man_config
from context import mancala


class TestDeka:

    @pytest.fixture
    def game_data(self):

        return man_config.make_game('./GameProps/Deka.txt')
