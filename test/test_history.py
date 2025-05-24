# -*- coding: utf-8 -*-
"""Test the history class.

Created on Thu May 15 07:59:13 2025
@author: Ann
"""

# %% imports

import pytest
pytestmark = pytest.mark.unittest


from context import man_history


TEST_COVERS = ['src\\man_history.py']


# %%

class TestHistory:

    @pytest.mark.parametrize('size', [3, 7])
    def test_create(self, size):

        hist = man_history.HistoryManager(size)

        assert hist.size == size
        assert hist.history.maxlen == size
        assert hist.rotated == 0
        assert hist.active == True


    @pytest.mark.parametrize('size', [3, 7])
    def test_record_len(self, size):

        hist = man_history.HistoryManager(size)

        # assure the history is full for both tests
        for state in range(10):
            hist.record(state)
        # print(hist)

        assert len(hist.history) == size

        assert hist.history[0] == 9
        assert hist.history[1] == 8
        assert hist.history[2] == 7

        assert hist.undo() == 8


    @pytest.fixture
    def hist(self):
        return man_history.HistoryManager(5)


    def test_record_inact(self, hist):

        hist.record(11)

        with hist.off():
            hist.record(12)

        assert len(hist.history) == 1
        assert hist.history[0] == 11


    def test_record_rotated(self, hist):

        for i in range(10):
            hist.record(i)

        assert hist.undo() == 8
        assert hist.undo() == 7
        assert hist.undo() == 6
        # print(hist)

        assert len(hist.history) == 5
        assert hist.rotated == 3

        hist.record(12)
        # print(hist)

        # 5 on, 3 rotate, 3 pop, add 1 = 3
        assert len(hist.history) == 3

        assert hist.history[0] == 12
        assert hist.history[1] == 6
        assert hist.history[2] == 5


    def test_clear(self, hist):

        for i in range(10):
            hist.record(i)

        assert hist.undo() == 8
        assert hist.undo() == 7

        assert len(hist.history) == 5
        assert hist.rotated == 2

        assert '7\n6\n5\n9\n8' in str(hist)

        hist.clear()

        assert not hist.history
        assert hist.rotated == 0


    def test_context(self, hist):

        hist.record(11)

        with hist.off():
            hist.active = None   # bad, bad code!!

        assert hist.active is True


    def test_undo_empty(self, hist):

        assert not hist.undo()


    def test_undo_part(self, hist):

        hist.record(1)
        hist.record(2)
        hist.record(3)

        assert hist.undo() == 2
        assert hist.undo() == 1

        assert not hist.undo()


    def test_undo_full(self, hist):

        for i in range(6):
            hist.record(i)

        assert hist.undo() == 4
        assert hist.undo() == 3
        assert hist.undo() == 2
        assert hist.undo() == 1

        assert not hist.undo()


    def test_redo_empty(self, hist):

        assert hist.rotated == 0
        assert not hist.redo()


    def test_redo_full_no_undos(self, hist):

        for i in range(6):
            hist.record(i)

        assert hist.rotated == 0
        assert not hist.redo()


    def test_redo_part(self, hist):

        for i in range(6):
            hist.record(i)
        for i in range(3):
            hist.undo()

        # print(hist)
        assert hist.rotated == 3
        assert hist.redo() == 3
        assert hist.redo() == 4
        assert hist.redo() == 5
        assert not hist.redo()


    def test_redo_full(self, hist):

        for i in range(6):
            hist.record(i)
        for i in range(6):
            hist.undo()

        # print(hist)
        assert hist.rotated == 4
        assert hist.redo() == 2
        assert hist.redo() == 3
        assert hist.redo() == 4
        assert hist.redo() == 5
        assert not hist.redo()
