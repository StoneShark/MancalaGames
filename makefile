


MODULES = ai_interface.py
MODULES += allowables.py
MODULES += capt_ok.py
MODULES += capturer.py
MODULES += cfg_keys.py
MODULES += deka.py
MODULES += end_move.py
MODULES += gamacha.py
MODULES += game_classes.py
MODULES += game_constants.py
MODULES += game_interface.py
MODULES += game_log.py
MODULES += game_str.py
MODULES += ginfo_rules.py
MODULES += get_direction.py
MODULES += get_moves.py
MODULES += hole_button.py
MODULES += incrementer.py
MODULES += man_config.py
MODULES += man_path.py
MODULES += mancala.py
MODULES += mancala_games.pyw
MODULES += mancala_ui.py
MODULES += montecarlo_ts.py
MODULES += minimax.py
MODULES += nam_nam.py
MODULES += new_game.py
MODULES += no_sides.py
MODULES += no_seed_goal.py
MODULES += play.py
MODULES += play_mancala.pyw
MODULES += qelat.py
MODULES += sow_starter.py
MODULES += sower.py


SOURCES = src/*.py src/*.pyw
GAMES = GameProps/*.txt
TESTS = test/*.py
GAME_TESTS = $(wildcard test/test_gm_*.py)

DATAFILES = GameProps/*.txt ./mancala_help.html logs/README.txt

all: all_tests pylint exe


#  tests

test/context.py: src
	python tools/make_context.py


unit_tests: $(SOURCES) $(TESTS) $(GAMES) test/context.py
	-coverage run -m pytest -m unittest
	coverage html


integ_tests: $(SOURCES) $(TESTS) $(GAMES) test/context.py
	-coverage run -m pytest -m integtest
	coverage html


all_tests: $(SOURCES) $(TESTS) $(GAMES) test/context.py
	-coverage run -m pytest
	coverage html


.PHONY: vtest
vtest: 
	pytest -v test

.PHONY: game_tests
game_tests: test/context.py
	-coverage run --branch -m pytest $(GAME_TESTS)
	coverage html
	
.PHONY: strest_tests	
stress_tests: test/context.py
	pytest test\\test_simul_game.py --nbr_runs 500
	pytest test\\test_simul_players.py --nbr_runs 50

	
#  test individual files
#	usage:   make <testfile>.test
#       example: make test_var.test
#  where <testfile> is a file of tests in the 'test' directory
#  this rule cleans all previous coverage data and runs the one
#  file from test. It reports the coverage of the files that
#  are expected to be covered (via TEST_COVERS in the test file).

%.test: test/context.py
	coverage run --branch -m pytest test\\$(subst .test,.py,$@)
	coverage json
	python test\\check_unit_cov.py $(subst .test,,$@)


UNIT_TESTS = test_allowables.test
UNIT_TESTS += test_capt_ok.test
UNIT_TESTS += test_captures.test
UNIT_TESTS += test_end_move.test
UNIT_TESTS += test_game_if.test
UNIT_TESTS += test_game_log.test
UNIT_TESTS += test_game_str.test
UNIT_TESTS += test_gconsts.test
UNIT_TESTS += test_get_direct.test
UNIT_TESTS += test_get_moves.test
UNIT_TESTS += test_gm_deka.test
UNIT_TESTS += test_gm_qelat.test
UNIT_TESTS += test_incr.test
UNIT_TESTS += test_man_config.test
UNIT_TESTS += test_mancala.test
UNIT_TESTS += test_minimax.test
UNIT_TESTS += test_mpath.test
UNIT_TESTS += test_sow_starter.test
UNIT_TESTS += test_sower.test

cov_unit_tests: $(UNIT_TESTS)


#  pylint
#
#  run the pylint on all source files together

pylint: $(SOURCES) .pylint_report makefile

.pylint_report: $(SOURCES) .pylintrc makefile
	-del .pylint_report
	-cd src && pylint --output ..\\.pylint_report --rcfile ..\\.pylintrc $(MODULES)
	type .pylint_report


#  clean
#
#  remove most of the accumulated stuff from builds
#  generally causes any other target to re-run

.PHONY : clean
clean:
	-rmdir /S /Q __pycache__
	-rmdir /S /Q src\\__pycache__
	-rmdir /S /Q test\\__pycache__
	-rmdir /S /Q doc\\__pycache__
	-rmdir /S /Q .pytest_cache
	-del .pylint_report
	-rmdir /S /Q htmlcov
	-del .coverage
	-del coverage.json
	-del src\\.coverage


# exe
#
# build stand alone executables with a shared runtime 

# cannot find a way in windows to make relative sym links or short cuts

exe: MancalaGames/mancala_games.exe

MancalaGames/mancala_games.exe: $(SOURCES) $(DATAFILES) mancala_games.spec
	-rmdir /S /Q MancalaGames
	pyinstaller mancala_games.spec --distpath MancalaGames
	copy mancala_help.html MancalaGames
	mkdir MancalaGames\\GameProps
	copy GameProps\\* MancalaGames\\GameProps
	mkdir MancalaGames\\logs
	copy logs\\README.txt MancalaGames\\logs
	ln -s .\\MancalaGames\\runtime\\play .\\MancalaGames\\play.exe
	ln -s .\\MancalaGames\\runtime\\play_mancala .\\MancalaGames\\play_mancala.exe
	ln -s .\\MancalaGames\\runtime\\mancala_games .\\MancalaGames\\mancala_games.exe
	-rmdir /S /Q build


