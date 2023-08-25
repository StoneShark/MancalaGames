# -*- coding: utf-8 -*-
"""Test the game_log.

For tests which use the global _game_log,
the game_log module is re-imported at the start of
each so that we know we have a consistent starting
point.

Created on Sat Aug 19 15:21:06 2023
@author: Ann"""

import datetime
import importlib
import sys

import pytest

sys.path.extend(['src'])

import game_log


class TestGameLog:

    @pytest.fixture
    def glog(self):
        return game_log.GameLog()


    def test_construct(self, glog):

        assert glog.active == True
        assert glog.live == False
        assert glog.level == game_log.MOVE
        assert glog.turn_nbr == -1
        assert not glog.log_records
        assert not glog.move_start


    def test_add(self, mocker, glog):

        glog.add('test line one', game_log.MOVE)
        glog.add('test line two', game_log.MOVE)
        assert len(glog.log_records) == 2
        assert not glog.move_start

        mopen = mocker.mock_open()
        with mopen('logfile', 'w') as file:
            glog.output(file)

        mopen.assert_called_once_with('logfile', 'w')
        handle = mopen()
        handle.write.has_calls('test line one', 'test line two')


    def test_add_level(self, glog):

        glog.add('test line one', game_log.IMPORT)
        glog.add('test line two', game_log.IMPORT)
        assert len(glog.log_records) == 0
        assert not glog.move_start


    def test_mark_turn(self, glog):

        glog.mark_turn()
        assert len(glog.move_start) == 1

        glog.add('test line one', game_log.MOVE)
        glog.add('test line two', game_log.MOVE)

        assert len(glog.log_records) == 2
        assert len(glog.move_start) == 1

        glog.mark_turn()
        assert len(glog.move_start) == 2

        assert list(glog.move_start) == [0, 2]

        glog.reset()
        assert glog.turn_nbr == -1
        assert not glog.log_records
        assert not glog.move_start


    def test_prev_init(self, glog, capsys):

        glog.prev()

        data = capsys.readouterr().out
        assert 'No moves' in data


    def test_prev_no_data(self, glog, capsys):

        glog.mark_turn()
        glog.prev()

        data = capsys.readouterr().out
        assert 'Previous Turn' in data


    def test_prev_one_rec(self, glog, capsys):

        glog.mark_turn()

        glog.add('turn 1, line 1', game_log.MOVE)
        glog.add('turn 1, line 2', game_log.MOVE)
        glog.add('turn 1, line 3', game_log.MOVE)

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
            glog.mark_turn()
            for line in range(1, lines[turn] + 1):
                glog.add(f'turn {turn} line {line}', game_log.MOVE)

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


class TestGameLogModule:

    @pytest.fixture
    def game(self):

        class GClass:
            def __str__(self):
                return 'game line 1\ngame line 2'

        return GClass()


    def test_active_basic(self, capsys):

        importlib.reload(game_log)
        game_log.add('active one', game_log.MOVE)

        game_log.set_active(False)
        game_log.add('not active one', game_log.MOVE)

        game_log.set_active(True)
        game_log.add('active two', game_log.MOVE)

        game_log.dump()
        data = capsys.readouterr().out.split('\n')

        assert len(data) == 5
        assert '' == data[0]
        assert 'Game history' in data[1]
        assert 'active one' == data[2]
        assert 'active two' == data[3]
        assert '' == data[4]


    def test_active_ops(self, game):

        importlib.reload(game_log)
        game_log.set_level(game_log.STEP)

        game_log.turn(game, 'start')
        game_log.step('step one', game)
        game_log.step('step twp', game)
        game_log.add('active one', game_log.IMPORT)

        assert game_log._game_log.turn_nbr == 0
        assert len(game_log._game_log.move_start) == 1
        assert len(game_log._game_log.log_records) == 7

        game_log.set_active(False)
        game_log.turn(game, 'seconds')
        game_log.step('step two.one', game)
        game_log.step('step two.two', game)
        game_log.add('inactive one', game_log.MOVE)

        assert game_log._game_log.turn_nbr == 0
        assert len(game_log._game_log.move_start) == 1
        assert len(game_log._game_log.log_records) == 7

        game_log.set_active(True)
        game_log.add('active two', game_log.MOVE)

        assert game_log._game_log.turn_nbr == 0
        assert len(game_log._game_log.move_start) == 1
        assert len(game_log._game_log.log_records) == 8


    def test_live(self, capsys):

        importlib.reload(game_log)
        game_log.add('not live one', game_log.MOVE)

        game_log.set_live(True)
        game_log.add('live one', game_log.MOVE)
        game_log.add('live two', game_log.MOVE)

        game_log.set_live(False)
        game_log.add('not live two', game_log.MOVE)

        data = capsys.readouterr().out.split('\n')

        assert len(data) == 3
        assert 'live one' == data[0]
        assert 'live two' == data[1]
        assert '' == data[2]

        assert len(game_log._game_log.log_records) == 4


    def test_level(self):

        importlib.reload(game_log)

        game_log.add('one - MOVE', game_log.MOVE)
        game_log.add('two - import', game_log.IMPORT)
        game_log.add('two - STEP', game_log.STEP)

        assert len(game_log._game_log.log_records) == 1

        game_log._game_log.reset()
        game_log.set_level(game_log.IMPORT)

        game_log.add('one - MOVE', game_log.MOVE)
        game_log.add('two - import', game_log.IMPORT)
        game_log.add('two - STEP', game_log.STEP)

        assert len(game_log._game_log.log_records) == 2

        game_log.set_level(-1)
        assert game_log._game_log.level == game_log.IMPORT


    def test_new(self, game):

        importlib.reload(game_log)

        game_log.set_level(game_log.IMPORT)
        game_log.turn(game, 'start')            # 2 recs
        game_log.add('import', game_log.IMPORT)
        game_log.step('step 1', game)           # not logged
        game_log.step('step 2', game)           # not logged
        game_log.turn(game, 'move 1')           # 2 recs

        assert len(game_log._game_log.move_start) == 2
        assert len(game_log._game_log.log_records) == 5
        assert game_log._game_log.turn_nbr == 1

        game_log.new()
        assert game_log._game_log.turn_nbr == -1
        assert len(game_log._game_log.move_start) == 0
        assert len(game_log._game_log.log_records) == 1


    def test_prev_long(self, game, capsys):

        importlib.reload(game_log)

        lines = [0, 4, 2, 6, 3]
        for turn in range(1, 5):
            game_log.turn(game, f'move {turn}')
            for line in range(1, lines[turn] + 1):
                game_log.add(f'turn {turn} line {line}', game_log.MOVE)

        game_log.prev()
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


    def test_save(self, mocker, game):

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

        importlib.reload(game_log)

        game_log.set_level(game_log.STEP)

        game_log.turn(game, 'start')
        game_log.add('import 1', game_log.IMPORT)
        game_log.step('step 1', game)
        game_log.step('step 2', game)
        game_log.turn(game, 'move 1')
        game_log.add('import 2', game_log.IMPORT)

        game_log.save('parameter string')
