Tests which are use game configuration from GameProps
should (if possible) use the global game_pdict fixture.
This will report a configure file error only once.


Test Naming conventions:

    test_cmp_...     tests composistions of deco chains
                     a black box test of the each deco chain
    
    test_gm...       tests full complete games with pre-defined
                     sequences of moves
                     these tests cannot use the game_pdict
                     fixture because most generate the game in
                     a class scope fixture (game_pdict is a 
                     function scope fixture).

    test_z_simul...  heuristic tests of games, seek gross errors.
                     Often slow. z forces to be tested last.


Debugging in Spyder:

- put breakpoints in test
- execute something like:

%debug pytest.main(['test_allowables.py::TestAllowables::test_ml3_allowables[case_6]'])


if the file loads a test table run from MancalaGames like this:

%debug pytest.main(['test/test_end_move.py::TestTerritory::test_cant_occ_more[case_1]'])


To run a verbose test from the command line:

pytest -v test\\test_end_move.py::TestClaimers

To capture output:

pytest -vs test\\test_end_move.py::TestClaimers::test_claimer[case2-DivvySeedsChildOnly]
