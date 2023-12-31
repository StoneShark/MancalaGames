# -*- coding: utf-8 -*-
"""Report the unittest coverage for the files are expected to be covered.
Usage:

check_unit_cov testname

Assumptions:
    1. Every source code file is covered by ony file.
    2. Each test file might cover multiple source code files.
       Only do this when they work closely together.

Created on Mon Sep 18 10:15:43 2023
@author: Ann"""

import argparse
import importlib
import json
import sys


def get_cov_data():
    with open('coverage.json', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return json.loads(''.join(lines))


def get_params():
    """Define the parser and use it."""

    parser = argparse.ArgumentParser()
    parser.add_argument('testname')

    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        print('Parser error')
        parser.print_help()
        sys.exit()

    return cargs.testname


def check_unit_cov():

    testname = get_params()

    test_module = importlib.import_module(testname)
    if 'TEST_COVERS' not in dir(test_module):
        print(f'\nTEST_COVERS not in {testname}.')
        return

    jcov = get_cov_data()
    jcov_files = jcov['files']

    error = False

    print(f'\nModules covered by {testname}:')
    for file in test_module.TEST_COVERS:

        print(f'  {file:.<25}', end=' ')
        if file in jcov_files:
            pct = jcov_files[file]['summary']['percent_covered']
            print(f'{pct:.1f}%')
        else:
            print('no reported coverage')
            error = True

    if error:
        print('\n', jcov_files.keys())
        print(test_module.TEST_COVERS)

if __name__ == '__main__':
    check_unit_cov()
