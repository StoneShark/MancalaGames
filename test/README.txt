

Test Naming conventions:

    test_gm...     tests full complete games with pre-defined
                   sequences of moves

    test_simul...  heuristic tests of games, seek gross errors.
                   Often slow.


Debugging in Spyder:

- evaluate the file
- put breakpoints in test
- execute something like:

%debug pytest.main(['test_allowables.py::TestAllowables::test_allowables'])
