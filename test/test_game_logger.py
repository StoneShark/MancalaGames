# -*- coding: utf-8 -*-
"""Test the game_log.

For tests which use the global game_logger,
the game_logger module is re-imported at the start of
each so that we know we have a consistent starting
point.

Created on Sat Aug 19 15:21:06 2023
@author: Ann"""

import datetime

import pytest
pytestmark = pytest.mark.unittest

from context import game_logger


TEST_COVERS = ['src\\game_logger.py']


class TestGameLog:

    @pytest.fixture
    def glog(self):
        return game_logger.GameLog()


    def test_construct(self, glog):

        assert glog._active
        assert not glog._live
        assert glog._level == glog.MOVE
        assert not glog._simulate
        assert glog.active
        assert not glog.live
        assert glog.level == glog.MOVE
        assert not glog._log_records
        assert not glog._move_start


    def test_add(self, mocker, glog):

        glog.add('test line one', glog.MOVE)
        glog.add('test line two', glog.MOVE)
        assert len(glog._log_records) == 2
        assert not glog._move_start

        mopen = mocker.mock_open()
        with mopen('logfile', 'w') as file:
            glog._output(file)

        mopen.assert_called_once_with('logfile', 'w')
        handle = mopen()
        handle.write.has_calls('test line one', 'test line two')


    def test_add_level(self, glog):

        glog.add('test line one', glog.IMPORT)
        glog.add('test line two', glog.IMPORT)
        assert len(glog._log_records) == 0
        assert not glog._move_start


    def test_mark_turn(self, glog):

        glog._mark_turn()
        assert len(glog._move_start) == 1

        glog.add('test line one', glog.MOVE)
        glog.add('test line two', glog.MOVE)

        assert len(glog._log_records) == 2
        assert len(glog._move_start) == 1

        glog._mark_turn()
        assert len(glog._move_start) == 2

        assert list(glog._move_start) == [0, 2]

        glog.new()                         # adds a record
        assert len(glog._log_records) == 1
        assert not glog._move_start


    def test_prev_init(self, glog, capsys):

        glog.prev()

        data = capsys.readouterr().out
        assert 'No moves' in data


    def test_prev_no_data(self, glog, capsys):

        glog._mark_turn()
        glog.prev()

        data = capsys.readouterr().out
        assert 'Previous Turn' in data


    def test_prev_one_rec(self, glog, capsys):

        glog._mark_turn()

        glog.add('turn 1, line 1', glog.MOVE)
        glog.add('turn 1, line 2', glog.MOVE)
        glog.add('turn 1, line 3', glog.MOVE)

        glog.prev()

        data = capsys.readouterr().out.split('\n')
        assert len(data) == 6
        assert '' == data[0]
        assert 'Previous Turn' in data[1]
        assert 'turn 1, line 1' == data[2]
        assert 'turn 1, line 2' == data[3]
        assert 'turn 1, line 3' == data[4]
        assert '' == data[5]


    def test_prev_long(self, glog, capsys):

        lines = [0, 4, 2, 6, 3]
        for turn in range(1, 5):
            glog._mark_turn()
            for line in range(1, lines[turn] + 1):
                glog.add(f'turn {turn} line {line}', glog.MOVE)

        glog.prev()

        data = capsys.readouterr().out.split('\n')

        assert len(data) == 12
        assert '' == data[0]
        assert 'Previous Turn' in data[1]
        assert 'turn 3 line 1' == data[2]
        assert 'turn 3 line 2' == data[3]
        assert 'turn 3 line 3' == data[4]
        assert 'turn 3 line 4' == data[5]
        assert 'turn 3 line 5' == data[6]
        assert 'turn 3 line 6' == data[7]
        assert 'turn 4 line 1' == data[8]
        assert 'turn 4 line 2' == data[9]
        assert 'turn 4 line 3' == data[10]
        assert '' == data[11]



    @pytest.fixture
    def game(self):

        class GClass:
            def __str__(self):
                return 'game line 1\ngame line 2'

        return GClass()


    def test_active_basic(self, glog, capsys):

        glog.add('active one', glog.MOVE)

        glog.active = False
        glog.add('not active one', glog.MOVE)

        glog.active = True
        glog.add('active two', glog.MOVE)

        glog.dump()
        data = capsys.readouterr().out.split('\n')

        assert len(data) == 5
        assert '' == data[0]
        assert 'Game history' in data[1]
        assert 'active one' == data[2]
        assert 'active two' == data[3]
        assert '' == data[4]


    def test_active_ops(self, glog, game):

        glog.level = glog.STEP

        glog.turn(0, 'start', game)
        glog.step('step one', game)
        glog.step('step twp (no game print)', game, glog.DETAIL)
        glog.step('step three without game')
        glog.add('active one', glog.IMPORT)

        assert len(glog._move_start) == 1
        assert len(glog._log_records) == 7

        glog.active = False
        glog.turn(1, 'seconds', game)
        glog.step('step two.one', game)
        glog.step('step two.two', game)
        glog.add('inactive one', glog.MOVE)

        assert len(glog._move_start) == 1
        assert len(glog._log_records) == 7

        glog.active = True
        glog.add('active two', glog.MOVE)

        assert len(glog._move_start) == 1
        assert len(glog._log_records) == 8


    def test_live(self, glog, capsys):

        glog.add('not live one', glog.MOVE)

        glog.live = True
        glog.add('live one', glog.MOVE)
        glog.add('live two', glog.MOVE)

        glog.live = False
        glog.add('not live two', glog.MOVE)

        data = capsys.readouterr().out.split('\n')

        assert len(data) == 3
        assert 'live one' == data[0]
        assert 'live two' == data[1]
        assert '' == data[2]

        assert len(glog._log_records) == 4


    def test_level(self, glog):

        glog.add('one - MOVE', glog.MOVE)
        glog.add('two - import', glog.IMPORT)
        glog.add('two - STEP', glog.STEP)

        assert len(glog._log_records) == 1

        glog.new()                 # adds a record
        glog.level = glog.IMPORT

        glog.add('one - MOVE', glog.MOVE)
        glog.add('two - import', glog.IMPORT)
        glog.add('two - STEP', glog.STEP)

        assert len(glog._log_records) == 3

        glog.level = -1
        assert glog._level == glog.IMPORT


    def test_new(self, glog, game):


        glog.level = glog.IMPORT
        glog.turn(0, 'start', game)            # 2 recs
        glog.add('import', glog.IMPORT)
        glog.step('step 1', game)           # not logged
        glog.step('step 2', game)           # not logged
        glog.turn(1, 'move 1', game)           # 2 recs

        assert len(glog._move_start) == 2
        assert len(glog._log_records) == 5

        glog.new()
        assert len(glog._move_start) == 0
        assert len(glog._log_records) == 1


    def test_prev_log(self, glog, game, capsys):

        lines = [0, 4, 2, 6, 3]
        for turn in range(1, 5):
            glog.turn(turn - 1, f'move {turn}', game)
            for line in range(1, lines[turn] + 1):
                glog.add(f'turn {turn} line {line}', glog.MOVE)

        glog.prev()
        data = capsys.readouterr().out.split('\n')

        assert len(data) == 20
        assert '' == data[0]
        assert 'Previous Turn' in data[1]
        assert '' == data[2]
        assert '2:' in data[3]
        assert 'game line 1' == data[4]
        assert 'game line 2' == data[5]
        assert 'turn 3 line 1' == data[6]
        assert 'turn 3 line 2' == data[7]
        assert 'turn 3 line 3' == data[8]
        assert 'turn 3 line 4' == data[9]
        assert 'turn 3 line 5' == data[10]
        assert 'turn 3 line 6' == data[11]
        assert '' == data[12]
        assert '3:' in data[13]
        assert 'game line 1' == data[14]
        assert 'game line 2' == data[15]
        assert 'turn 4 line 1' == data[16]
        assert 'turn 4 line 2' == data[17]
        assert 'turn 4 line 3' == data[18]
        assert '' == data[19]


    def test_save(self, glog, mocker, game):

        """don't know how to test this"""

        # TODO patch these:
        # datetime.datetime.now
        # man_path.get_path
        # open
        # print

        # don't know why the output is to the console
        # capsys doesn't capture it
        # filename ends up being a MagicMock

        mock_now = mocker.patch('datetime.datetime')
        mock_now.now.return_value = datetime.datetime(2023, 1, 2, 12, 30, 15)
        mocker.patch('man_path.get_path', side_effect=lambda x: x)

        glog.level = glog.STEP

        glog.turn(0, 'start', game)
        glog.add('import 1', glog.IMPORT)
        glog.step('step 1', game)
        glog.step('step 2', game)
        glog.turn(1, 'move 1', game)
        glog.add('import 2', glog.IMPORT)

        glog.save('parameter string')


    def test_simulate(self, glog):

        glog.add('test line one', glog.MOVE)
        assert len(glog._log_records) == 1

        glog.set_simulate()
        assert glog._simulate

        # not added, logged as SIMUL but log level is MOVE
        glog.add('test line two', glog.MOVE)
        assert len(glog._log_records) == 1

        # now logged
        glog.level = glog.SIMUL
        glog.add('test line two', glog.MOVE)
        assert len(glog._log_records) == 2


    def test_clear_simulate(self, glog):

        glog.add('test line one', glog.MOVE)
        assert len(glog._log_records) == 1

        glog.set_simulate()
        assert glog._simulate

        # not added, logged as SIMUL but log level is MOVE
        glog.add('test line two', glog.MOVE)
        assert len(glog._log_records) == 1

        glog.clear_simulate()
        assert not glog._simulate

        # now logged with MOVE
        glog.add('test line two', glog.MOVE)
        assert len(glog._log_records) == 2
