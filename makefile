
all: clean pylint context all_tests docs exe


MODULES = ai_interface.py
MODULES += ai_player.py
MODULES += allowables.py
MODULES += btn_behaviors.py
MODULES += capt_ok.py
MODULES += capturer.py
MODULES += cfg_keys.py
MODULES += deco_chain_if.py
MODULES += end_move.py
MODULES += fill_patterns.py
MODULES += game_classes.py
MODULES += game_constants.py
MODULES += game_interface.py
MODULES += game_log.py
MODULES += game_str.py
MODULES += game_tally.py
MODULES += get_direction.py
MODULES += get_moves.py
MODULES += ginfo_rules.py
MODULES += incrementer.py
MODULES += inhibitor.py
MODULES += man_config.py
MODULES += man_path.py
MODULES += mancala_games.pyw
MODULES += mancala_ui.py
MODULES += mancala.py
MODULES += minimax.py
MODULES += montecarlo_ts.py
MODULES += new_game.py
MODULES += param_consts.py
MODULES += play_mancala.pyw
MODULES += play.py
MODULES += sow_starter.py
MODULES += sower.py

SOURCES = src/*.py src/*.pyw
GAMES = GameProps/*.txt
TESTS = test/*.py
GAME_TESTS = $(wildcard test/test_gm_*.py)

HELPFILES = docs\\mancala_help.html
HELPFILES += docs\\about_games.html
HELPFILES += docs\\game_params.html
HELPFILES += docs\\game_xref.html
HELPFILES += docs\param_types.html

DATAFILES = GameProps/*.txt $(HELPFILES) logs/README.txt

HELPINPUTS = src\\game_params.txt 
HELPINPUTS += src\\mancala_games.pyw 
HELPINPUTS += src\\game_classes.py 
HELPINPUTS += src\\ai_player.py
HELPINPUTS += docs\\build_docs.py 
HELPINPUTS += docs\\context.py 

GENEDHELPS = docs\\about_games.html 
GENEDHELPS += docs\\game_params.html 
GENEDHELPS += docs\\game_xref.html 
GENEDHELPS += docs\\param_types.html

CONTEXTS = test\\context.py
CONTEXTS += docs\\context.py
CONTEXTS += analysis\\context.py


# game params
#
# convert xlsx to txt for main programs
# uses pandas which we don't want to use for main programs
# exe can't be built with pandas

src\\game_params.txt: src\\game_params.xlsx
	python tools/convert_game_params.py

# context files

context: $(CONTEXTS)

test\\context.py: src
	python tools/make_context.py

docs\\context.py: test\\context.py
	copy test\\context.py docs\\context.py
	
analysis\\context.py: test\\context.py
	copy test\\context.py analysis\\context.py
	
	
# docs
#
# generate the html helps files

docs: $(GENEDHELPS)

$(GENEDHELPS): $(GAMES) $(HELPINPUTS)
	cd docs && python build_docs.py


#  tests

unit_tests: $(SOURCES) $(TESTS) $(GAMES) test\\context.py
	-coverage run -m pytest -m unittest
	coverage html


integ_tests: $(SOURCES) $(TESTS) $(GAMES) test\\context.py
	-coverage run -m pytest -m integtest
	coverage html


all_tests: $(SOURCES) $(TESTS) $(GAMES) test\\context.py
	-coverage run -m pytest
	coverage html

# run the tests with the verbose flag
# mostly a reminder on how to do this
.PHONY: vtest
vtest: 
	pytest -v test

# a target to run only the test_gm files
.PHONY: game_tests
game_tests: test\\context.py
	-coverage run --branch -m pytest $(GAME_TESTS)
	coverage html

# a target to run the stress tests with higher iterations
.PHONY: strest_tests	
stress_tests: test\\context.py
	pytest test\\test_simul_game.py --nbr_runs 500
	pytest test\\test_simul_players.py --nbr_runs 50


# cov_unit_tests
#
# determine coverage each of unit test for the code it should cover
#
#	usage:   make <testfile>.cov
#       example: make test_var.cov
#  where <testfile> is a file of tests in the 'test' directory
#  this rule cleans all previous coverage data and runs the one
#  file from test. It reports the coverage of the files that
#  are expected to be covered (via TEST_COVERS in the test file).
#
# TODO this isn't running after a "make clean"

vpath %.cov .\\cov
vpath %.py .\\test

%.cov: test\\context.py $(subst .cov,.py,$@)
	coverage run --branch -m pytest test\\$(subst .cov,.py,$@)
	coverage json
	python test\\check_unit_cov.py $(subst .cov,,$@) > cov\\$@
	type cov\\$@

UNIT_TESTS += test_ai_player.cov
UNIT_TESTS += test_allowables.cov
UNIT_TESTS += test_capt_ok.cov
UNIT_TESTS += test_captures.cov
UNIT_TESTS += test_end_move.cov
UNIT_TESTS += test_game_if.cov
UNIT_TESTS += test_game_log.cov
UNIT_TESTS += test_game_str.cov
UNIT_TESTS += test_gconsts.cov
UNIT_TESTS += test_get_direct.cov
UNIT_TESTS += test_get_moves.cov
UNIT_TESTS += test_incr.cov
UNIT_TESTS += test_man_config.cov
UNIT_TESTS += test_mancala.cov
UNIT_TESTS += test_minimax.cov
UNIT_TESTS += test_mpath.cov
UNIT_TESTS += test_new_game.cov
UNIT_TESTS += test_patterns.cov
UNIT_TESTS += test_sow_starter.cov
UNIT_TESTS += test_sower.cov

cov_unit_tests: $(UNIT_TESTS)
	grep src cov\\*.cov


#  pylint
#
#  run the pylint on all source files together

pylint: $(SOURCES) .pylint_report makefile

.pylint_report: $(SOURCES) .pylintrc makefile
	-del .pylint_report
	-cd src && pylint --output ..\\.pylint_report --rcfile ..\\.pylintrc $(MODULES)
	type .pylint_report


#  clean/spotless
#
#  clean: remove most of the accumulated stuff from builds
#  but leave things that are stored in configuration management
#  generally causes any other target to be re-run
#
#  spotless: remove everything including the exes and generated files

.PHONY : clean
clean:
	-rmdir /S /Q __pycache__
	-rmdir /S /Q analysis\\__pycache__
	-rmdir /S /Q doc\\__pycache__
	-rmdir /S /Q src\\__pycache__
	-rmdir /S /Q test\\__pycache__
	-rmdir /S /Q .pytest_cache
	-rmdir /S /Q build
	-del .pylint_report
	-rmdir /S /Q htmlcov
	-del .coverage
	-del coverage.json
	-del src\\.coverage
	-del test\\context.py
	-del cov\\*.cov
	
.PHONY : spotless
spotless: clean
	-rmdir /S /Q MancalaGames
	-del $(GENEDHELPS)
	-del $(CONTEXTS)
	-del src\\game_params.txt

# exe
#
# build stand alone executables with a shared runtime 
#
# cannot find a way in windows to make relative sym links or short cuts

exe: MancalaGames/mancala_games.exe

MancalaGames/mancala_games.exe: $(SOURCES) $(DATAFILES) $(HELPFILES) mancala_games.spec
	-rmdir /S /Q MancalaGames
	pyinstaller mancala_games.spec --distpath MancalaGames
	copy docs\\*.html MancalaGames
	copy docs\\styles.css MancalaGames
	mkdir MancalaGames\\GameProps
	copy GameProps\\* MancalaGames\\GameProps
	mkdir MancalaGames\\logs
	copy logs\\README.txt MancalaGames\\logs
	copy src\\game_params.txt MancalaGames
	ln -s .\\MancalaGames\\runtime\\play .\\MancalaGames\\play.exe
	ln -s .\\MancalaGames\\runtime\\play_mancala .\\MancalaGames\\play_mancala.exe
	ln -s .\\MancalaGames\\runtime\\mancala_games .\\MancalaGames\\mancala_games.exe
	-rmdir /S /Q build
