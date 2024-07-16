# -*- coding: utf-8 -*-
"""Allow the number of runs of tests marked with 'stresstest'
to be set via the command line, as in:

    pytest -k simul --nbr_runs 500

Make the number of runs available as a fixture named: nbr_runs

Created on Fri Sep 15 09:07:52 2023
@author: Ann"""

import pytest

def pytest_addoption(parser):
    parser.addoption("--nbr_runs", action="store", default="10")
    parser.addoption("--run_slow", action="store_true", default=False)


def pytest_collection_modifyitems(config, items):

    if not config.getoption("--run_slow"):
        skipper = pytest.mark.skip(reason="Only run when --run_slow is given")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skipper)


def pytest_generate_tests(metafunc):

    if metafunc.config.option.nbr_runs is not None:
        count = int(metafunc.config.option.nbr_runs)

    if 'stresstest' in [m.name for m in metafunc.definition.own_markers]:
        metafunc.fixturenames.append('run_cnt')
        metafunc.parametrize('run_cnt', range(count))

    # add this fixture for the test_game_stats (and maybe others)
    if 'nbr_runs' in metafunc.fixturenames:
        metafunc.parametrize('nbr_runs', [count])
