# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:14:39 2023
@author: Ann"""

import os

import man_path

def test_get_path():

    epath = os.path.abspath('.') + '\\testpath'
    assert man_path.get_path('testpath') == epath

    # if src isn't the parent dir of __file__ it isn't used
    man_path.__file__ =  os.path.abspath('.') + '\\extra'
    assert man_path.get_path('testpath') == epath
