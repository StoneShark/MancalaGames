# -*- coding: utf-8 -*-
"""A tester for consistency of parameters of objects,
allowing all of the rules to be in basically one place.
Rules testers can also be chained to support derived
classes.

Created on Fri Jun  6 09:36:28 2025
@author: Ann"""

import warnings

# use this with warn for gentle warnins (only a printed message, no popup)
PRINT_MSG = 'print msg'


class RuleTester:
    """Test the rules on the given obj1 and obj2.

    skip_rules: a set of rule names to skip while testing."""

    def __init__(self, obj1, obj2, skip=None):

        self.obj1 = obj1
        self.obj2 = obj2

        self.skip_rules = skip if skip else set()
        self.tested = set()


    def test_rule(self, name, *, rule, msg,
                  warn=False, excp=None, both_objs=False):
        """Test an individual rule.

        name: name of the rule
              if a duplicate rule name is used and error is printed.

        rule: a function or lambda that takes 1 or 2 params
              should return True if there is an error

        warn: if PRINT_MSG, will print a message to console (too early to
              be put into a game log)
              if True, genearte a warning, else an exception

        excp: if generating an exception, generate this exception

        both_objs: if True, call with obj1 and obj2, otherwise only obj1"""
        # pylint: disable=too-many-arguments

        if name in self.skip_rules:
            return

        # these are programming errors so don't use popup
        if name in self.tested:
            print(f'Duplicate rule name: {name}')
        self.tested |= {name}

        if not warn and not excp:
            print(f'{name} has no effect (missing warn or excp)')

        if warn and excp:
            print(f'{name} has two actions (both warn or excp)')

        if rule(self.obj1, self.obj2) if both_objs else rule(self.obj1):
            msg = msg + f' ({name}).'
            if warn == PRINT_MSG:
                print('\n*** Gentle Warning:  ', msg)
            elif warn:
                warnings.warn(msg)
            else:
                raise excp(msg)
