# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 15:21:06 2023
@author: Ann"""

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
        assert glog.level == game_log.MOVES
        assert glog.turn_nbr == -1
        assert not glog.log_records
        assert not glog.move_start
        
        
    def test_add(self, mocker, glog):
        
        glog.add('test line one', game_log.MOVES)
        glog.add('test line two', game_log.MOVES)
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
        
        glog.add('test line one', game_log.MOVES)
        glog.add('test line two', game_log.MOVES)
 
        assert len(glog.log_records) == 2
        assert len(glog.move_start) == 1
       
        glog.mark_turn()
        assert len(glog.move_start) == 2
        
        assert list(glog.move_start) == [0, 2]
        
        glog.reset()
        assert glog.turn_nbr == -1
        assert not glog.log_records
        assert not glog.move_start


    
    

