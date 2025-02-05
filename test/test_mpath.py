# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:14:39 2023
@author: Ann"""

import os

import pytest
pytestmark = pytest.mark.unittest

from context import man_path


TEST_COVERS = ['src\\man_path.py']

class TestMPath:

    @pytest.fixture(params=['testfile.txt',
                            'sub/testfile.txt',
                            'sub/src/testfile.txt'])
    def man_dir(self, request, tmp_path):

        cwd = os.getcwd()

        dir1 = tmp_path / 'sub'
        dir1.mkdir()
        dir2 = tmp_path / 'sub' / 'src'
        dir2.mkdir()
        testfile = tmp_path / request.param
        testfile.write_text('text')

        os.chdir(dir1)
        yield

        os.chdir(cwd)


    def test_get_path(self, man_dir):
        assert man_path.get_path('testfile.txt')


    def test_error(self, tmp_path):

        testfile = tmp_path / 'junk.txt'
        with pytest.raises(FileNotFoundError):
            man_path.get_path(testfile)


    def test_no_error(self, tmp_path):

        testfile = tmp_path / 'junk.txt'
        assert man_path.get_path(testfile, no_error=True) is False
