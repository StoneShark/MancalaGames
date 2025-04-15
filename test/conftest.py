# -*- coding: utf-8 -*-
"""Configuration for a pytest run:

1. disable the animator

2. command line option nbr_runs: tests marked stress_test
   are run this many times. Also, make the number of runs
   available as a fixture named nbr_runs

3. command line option run_slow: to run tests marked slow

4. incremental tests:  classes where each method
   is a test step, mark incremental. Only the failed
   step will generate a report.

5. global fixtures:

        logger and logger_sim - to support debugging

        random_seed - make most tests run predictably,
        use no_seed mark to disable

        game_pdict - only report the failure to load a
        game configuration file once per test session

Created on Fri Sep 15 09:07:52 2023
@author: Ann"""

import json
import random
import time

import pytest

from context import animator
from context import game_logger
from context import man_config


# don't let the animator put it's hooks into the Mancala state variables
animator.ENABLED = False


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


# %% incremental test hooks

# for test_gm _* where each test step is a separate method
# in the test class that relies on the previous step passing
# after the first fail all the rest will be marked as xfail
# mark the test class with @pytest.mark.incremental
#
# got these from here:
# https://stackoverflow.com/questions/12411431/how-to-skip-the-rest-of-tests-in-the-class-if-one-has-failed/12579625#12579625


def pytest_runtest_setup(item):
    """If a parent node has a record that a test failed,
    mark this as expected fail."""

    previousfailed = getattr(item.parent, "_previousfailed", None)
    if previousfailed is not None:
        pytest.xfail("previous test failed (%s)" % previousfailed.name)


def pytest_runtest_makereport(item, call):
    """If a test is marked incremental and exception was raised
    record that there was a failure in the parent node."""

    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


# %% global fixtures

@pytest.fixture()
def logger():
    """Include this fixture to activate the logger for the test,
    it will be deactivated after the test."""

    log_level = game_logger.game_log.level
    game_logger.game_log.active = True
    game_logger.game_log.level = game_logger.game_log.DETAIL
    game_logger.game_log.live = True
    yield
    game_logger.game_log.active = False
    game_logger.game_log.level = log_level
    game_logger.game_log.live = False


@pytest.fixture()
def logger_sim():
    """Include this fixture to activate the logger for the test
    and set the logger to show simulated moves,
    it will be deactivated after the test."""

    log_level = game_logger.game_log.level
    game_logger.game_log.active = True
    game_logger.game_log.level = game_logger.game_log.SIMUL
    game_logger.game_log.live = True
    yield
    game_logger.game_log.active = False
    game_logger.game_log.level = log_level
    game_logger.game_log.live = False


@pytest.fixture(autouse=True)
def random_seed(request):
    """Force the random number generator to produce
    consistent random values.

    Tests which intentionally use the random number generator,
    e.g. simulations should be marked with:
        @pytest.mark.no_seed
    These tests will be seeded with the time, otherwise the
    previous instantiation of this fixture will leave the
    random number generator behaving with more consistency
    than desired.
    """

    if 'no_seed' in request.keywords:
        random.seed(time.time())
        return

    random.seed(10)


@pytest.fixture
def game_pdict(request):
    """Parametrize with game config file(s).
    Then use with indirect, to convert the game config file name
    to an actual game and pdict.  As in:
        @pytest.mark.parametrize('game_pdict', FILES, indirect=True)
    or
        @pytest.mark.parametrize('game_pdict ...',
                                 ...FILES...,    # full param lists
                                 indirect=['game_pdict'])


    If the cache contains a failure, mark the test as xfail.
    Otherwise try to make the game, if it fails save the failure
    in the cache and reraise the exception.

    This causes only one failure report to be generated for each
    test session."""

    cfg_filename = request.param
    key_name = cfg_filename.replace('.', '_') + '_failed'

    if request.config.cache.get(key_name, False):
        pytest.xfail("Game cfg error (again)")

    try:
        game_data = man_config.make_game("./GameProps/" + cfg_filename)

    except json.decoder.JSONDecodeError:
        request.config.cache.set(key_name, True)
        raise

    return game_data
