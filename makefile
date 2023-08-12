


MODULES = ai_interface.py
MODULES += allowables.py
MODULES += capt_ok.py
MODULES += capturer.py
MODULES += cfg_keys.py
MODULES += deka.py
MODULES += game_classes.py
MODULES += game_constants.py
MODULES += game_interface.py
MODULES += game_log.py
MODULES += game_str.py
MODULES += get_direction.py
MODULES += get_moves.py
MODULES += incrementer.py
MODULES += man_config.py
MODULES += mancala.py
MODULES += mancala_games.pyw
MODULES += mancala_ui.py
MODULES += montecarlo_ts.py
MODULES += minimax.py
MODULES += new_game.py
MODULES += play.py
MODULES += play_mancala.pyw
MODULES += qelat.py
MODULES += seed_collector.py
MODULES += sow_starter.py
MODULES += sower.py


SOURCES = src/*.py src/*.pyw
GAMES = GameProps/*.txt
TESTS = test/*.py

DATAFILES = GameProps/*.txt

all: unit_tests pylint exe


#  unit_tests
#
#  run all the unit tests and create a coverage report

unit_tests: htmlcov/index.html $(SOURCES) $(TESTS)  $(GAMES)

htmlcov/index.html: $(SOURCES)  $(TESTS) $(GAMES)
	-coverage run --branch -m pytest
	coverage html

.PHONY: vtest
vtest: 
	pytest -v test
	

#  test individual files
#	usage:   make <testfile>.test
#       example: make test_var.test
#  where <testfile> is a file of tests in the 'test' directory
#  this rules cleans all previous coverage data and runs the one
#  files of tests. This can be used to make certain that the
#  code is actually tested and not just run as part of another
#  test.

%.test: clean
	-coverage run --branch -m pytest test\\$(subst .test,.py,$@)
	coverage html


#  pylint
#
#  run the pylint on all source files together

pylint: $(SOURCES) .pylint_report 

.pylint_report: $(SOURCES) .pylintrc
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
# build a stand alone executable
exe: dist/mancala_games.exe

dist/mancala_games.exe: $(SOURCES) $(DATAFILES) mancala_games.spec
	pyinstaller mancala_games.spec
	-rmdir /S /Q build
