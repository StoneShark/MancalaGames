# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:14:39 2023
@author: Ann"""

import os
import sys

import pytest
pytestmark = pytest.mark.unittest

sys.path.extend(['src'])

import man_path



TEST_COVERS = ['src\\man_path.py']

def test_get_path():

    epath = os.path.abspath('.') + '\\testpath'
    assert man_path.get_path('testpath') == epath

    # if src isn't the parent dir of __file__ it isn't used
    man_path.__file__ =  os.path.abspath('.') + '\\extra'
    assert man_path.get_path('testpath') == epath
