

Test Naming conventions:

    test_gm...     tests full complete games with pre-defined
                   sequences of moves

    test_simul...  heuristic tests of games, seek gross errors.
                   Often slow.

    vizex_...      frameworks to exercise the UI elements.
                   tests are interactive and require the human
                   tester to decide test pass & failure ...


Debugging in Spyder:

- evaluate the file
- put breakpoints in test
- execute something like:

%debug pytest.main(['test_allowables.py::TestAllowables::test_ml3_allowables[case_6]'])


if the file loads a test table run from MancalaGames like this:

%debug pytes
t.main(['test/test_end_move.py::TestTerritory::test_cant_occ_more[case_1]'])
