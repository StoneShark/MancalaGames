# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:14:39 2023
@author: Ann"""

import os

import pytest
pytestmark = pytest.mark.unittest

from context import man_path


TEST_COVERS = ['src\\man_path.py']


class TestGameFiles:

    def test_game_files(self, mocker):

        mobj = mocker.patch('os.listdir')
        mobj.return_value = ['Game1.txt', 'Game2.txt', 'Game3.txt',
                             '_all_params.txt', 'data.csv']

        assert man_path.game_files() == ['Game1.txt', 'Game2.txt', 'Game3.txt']


class TestGetPath:

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


class TestFindGameFile:

    @pytest.fixture
    def dir_tree(self, tmp_path):

        cwd = os.getcwd()

        dir1 = tmp_path / 'GameProps'
        dir1.mkdir()
        dir2 = tmp_path / 'base'
        dir2.mkdir()
        dir3 = tmp_path / 'base' / 'GameProps'
        dir3.mkdir()

        for gfile in ['base/Game1.txt',
                      'GameProps/Game2.txt',
                      'base/GameProps/Game3.txt']:
            testfile = tmp_path / gfile
            testfile.write_text('text')

        os.chdir(dir2)
        yield

        os.chdir(cwd)


    GAME_FILES = ['Game1', 'Game2', 'Game3',
                  'Game1.txt', 'Game2.txt', 'Game3.txt']

    @pytest.mark.parametrize('game_name', GAME_FILES)
    def test_get_path(self, game_name, dir_tree):

        print(os.listdir('.'))
        for dpath, dirs, files in os.walk('..'):
            for f in files:
                print(dpath, '/', f, sep='')

        assert man_path.find_gamefile(game_name)


    def test_get_path_abs(self, tmp_path):
        """Test calling find_game file with an absolute path."""

        dir2 = tmp_path / 'base'
        dir2.mkdir()
        dir3 = tmp_path / 'base' / 'GameProps'
        dir3.mkdir()

        testfile = tmp_path / 'game3.txt'
        testfile.write_text('text')

        assert man_path.find_gamefile(testfile)


    def test_error(self):

        with pytest.raises(FileNotFoundError):
            man_path.find_gamefile('junk.txt')


    def test_no_error(self, tmp_path):

        assert man_path.find_gamefile('junk.txt', no_error=True) is False
