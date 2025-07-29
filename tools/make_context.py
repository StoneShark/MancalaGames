# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 10:10:39 2023
@author: Ann"""


import datetime
import os
import re


PATH = './src/'
PYFILE = '\\.py$'
BAD_FILE_RE = ['pycache', 'Copy']


def get_module_names():

    files = os.listdir(PATH)
    modules = []

    for file in files:

        match = re.search(PYFILE, file)
        if not match:
            continue
        file = file[:match.span()[0]]

        if not any(re.search(regex, file) for regex in BAD_FILE_RE):
            modules += [file]

    return modules


def create_context(modules):

    with open('test/context.py', 'w', encoding='utf-8') as file:

        print("# -*- coding: utf-8 -*-", file=file)
        print('"""Auto-generated context file.', file=file)
        now = datetime.datetime.now()
        print('Created on', now.strftime('%c'), file=file)
        print('"""\n', file=file)

        print('import os', file=file)
        print('import sys\n', file=file)

        print("PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))",
              file=file)
        print('sys.path.append(PATH)', file=file)
        print(file=file)

        for mod in modules:
            print(f'import {mod}', file=file)

        print(file=file)
        print('sys.path.remove(PATH)', file=file)


create_context(get_module_names())
