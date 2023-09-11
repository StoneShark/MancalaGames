


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
MODULES += new_game.py
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

all: unit_tests pylint exe


#  unit_tests
#
#  run all the unit tests and create a coverage report

unit_tests: htmlcov/index.html $(SOURCES) $(TESTS) $(GAMES)

htmlcov/index.html: $(SOURCES)  $(TESTS) $(GAMES)
	-coverage run -m pytest --cache-clear --color=no
	coverage html

.PHONY: vtest
vtest: 
	pytest -v test


.PHONY: game_tests
game_tests:
	-coverage run --branch -m pytest $(GAME_TESTS)
	coverage html

	
#  test individual files
#	usage:   make <testfile>.test
#       example: make test_var.test
#  where <testfile> is a file of tests in the 'test' directory
#  this rule cleans all previous coverage data and runs the one
#  files of tests. This can be used to make certain that the
#  code is actually tested and not just run as part of another
#  test suite.

%.test:
	-coverage run --branch -m pytest test\\$(subst .test,.py,$@)
	coverage html


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
	-rmdir /S /Q .pytest_cache
	-del .pylint_report
	-rmdir /S /Q htmlcov
	-del .coverage
	-del src\\.coverage


# exe
#
# build stand alone executables with a shared runtime 

exe: MancalaGames/mancala_games.exe

MancalaGames/mancala_games.exe: $(SOURCES) $(DATAFILES) mancala_games.spec
	-rmdir /S /Q MancalaGames
	pyinstaller mancala_games.spec --distpath MancalaGames
	copy mancala_help.html MancalaGames
	mkdir MancalaGames\\GameProps
	copy GameProps\\* MancalaGames\\GameProps
	mkdir MancalaGames\\logs
	copy logs\\README.txt MancalaGames\\logs
	ln -s .\\MancalaGames\\runtime\\play.exe .\\MancalaGames\\play.exe
	ln -s .\\MancalaGames\\runtime\\play_mancala.exe .\\MancalaGames\\play_mancala.exe
	ln -s .\\MancalaGames\\runtime\\mancala_games.exe .\\MancalaGames\\mancala_games.exe
	-rmdir /S /Q build
