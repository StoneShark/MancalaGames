# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 10:00:41 2025

@author: Ann
"""

import pytest

# unit test
# report warnings as errrors
pytestmark = [pytest.mark.unittest, pytest.mark.filterwarnings("error")]

from context import rule_tester


TEST_COVERS = ['src\\rule_tester.py']

class TestRuleTester:

    def test_useless_rule(self, capsys):

        tester = rule_tester.RuleTester(None, None)

        tester.test_rule(name='rule_name',
                         msg='something bad',
                         rule= lambda ginfo : ginfo)

        data = capsys.readouterr().out
        assert 'rule_name' in data
        assert 'has no effect' in data


    def test_excess_rule(self, capsys):

        tester = rule_tester.RuleTester(None, None)

        tester.test_rule(name='rule_name',
                         msg='something bad',
                         rule= lambda ginfo : ginfo,
                         warn=True,
                         excp=NotImplementedError)

        data = capsys.readouterr().out
        assert 'rule_name' in data
        assert 'has two actions' in data


    def test_dupl_rule(self, capsys):

        tester = rule_tester.RuleTester(None, None)

        tester.test_rule(name='dupl_rule',
                         msg='something bad',
                         rule= lambda obj1 : obj1,
                         warn=True)
        tester.test_rule(name='dupl_rule',
                         msg='more of bad stuff',
                         rule= lambda obj1 : obj1,
                         warn=True)

        data = capsys.readouterr().out
        assert 'dupl_rule' in data
        assert 'Duplicate' in data


    def test_both_rule(self, capsys):

        tester = rule_tester.RuleTester(False, True)

        # test expecting both objects without requesting them
        with pytest.raises(TypeError):
            tester.test_rule(name='only_one',
                             msg='got both objects',
                             rule=lambda obj1, obj2 : obj1 or obj2,
                             warn=True)

        # test getting both objects
        tester.test_rule(name='both_rule',
                         msg='got both objects',
                         both_objs=True,
                         rule= lambda obj1, obj2 : obj1 or obj2,
                         warn=rule_tester.PRINT_MSG)

        data = capsys.readouterr().out
        assert 'got both objects' in data


    def test_rules(self, capsys):

        tester = rule_tester.RuleTester(None, None, skip={'dont_test'})

        tester.test_rule(name='dont_test',
                         msg='exception occurred',
                         rule=lambda obj1: True,
                         excp=TypeError)

        # test raising an exception
        with pytest.raises(ValueError):
            tester.test_rule(name='excp_rule',
                             msg='exception occurred',
                             rule=lambda obj1: True,
                             excp=ValueError)

        # test a warning
        with pytest.warns(UserWarning) as record:
            tester.test_rule(name='warn_rule',
                             msg='got a warning',
                             rule=lambda obj1: True,
                             warn=True)

        assert len(record) == 1
        assert 'got a warning' in record[0].message.args[0]

        # test a gentle warning
        tester.test_rule(name='gentle warning',
                         msg='bad things could happen',
                         rule=lambda obj1: True,
                         warn=rule_tester.PRINT_MSG)
        data = capsys.readouterr().out
        assert 'Gentle Warning' in data
        assert 'bad things' in data
