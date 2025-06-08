
all: clean context params docs pylint tests

final: spotless context params docs pylint all_tests exe


SOURCES = src/*.py src/*.pyw
GAMES = GameProps/*.txt
TESTS = test/*.py
GAME_TESTS = $(wildcard test/test_gm_*.py)

HELPFILES = docs\\mancala_help.html
HELPFILES += docs\\about_games.html
HELPFILES += docs\\game_params.html
HELPFILES += docs\\game_xref.html
HELPFILES += docs\\param_types.html
HELPFILES += docs\\dist_readme.txt
HELPFILES += docs\\Diffusion_rules.pdf

DATAFILES = GameProps/*.txt $(HELPFILES) logs/README.txt

HELPINPUTS = src\\game_params.csv
HELPINPUTS += src\\game_param_descs.txt
HELPINPUTS += src\\man_config.py
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
CONTEXTS += tools\\context.py


# game params
#
# convert xlsx to txt for main programs
# uses pandas which we don't want to use for main programs
# exe can't be built with pandas

params: src\\game_params.csv

src\\game_params.csv: src\\game_params.xlsx tools\\context.py tools\\convert_game_params.py
	python tools/convert_game_params.py


# context files

context: $(CONTEXTS)

test\\context.py: src
	python tools/make_context.py

docs\\context.py: test\\context.py
	copy test\\context.py docs\\context.py
	
analysis\\context.py: test\\context.py
	copy test\\context.py analysis\\context.py
	
tools\\context.py: test\\context.py
	copy test\\context.py tools\\context.py

# docs
#
# generate the html helps files

docs: $(GENEDHELPS) docs\\context.py params

$(GENEDHELPS): $(GAMES) $(HELPINPUTS) docs\\context.py
	cd docs && python build_docs.py


#  tests

unit_tests: $(SOURCES) $(TESTS) $(GAMES) test\\context.py src\\game_params.csv
	-coverage run -m pytest -m unittest
	coverage html


integ_tests: $(SOURCES) $(TESTS) $(GAMES) test\\context.py src\\game_params.csv
	-coverage run -m pytest -m integtest --sim_fails
	coverage html


tests: $(SOURCES) $(TESTS) $(GAMES) test\\context.py src\\game_params.csv
	-coverage run -m pytest --sim_fails
	coverage html

long_tests: stress_tests player_tests cov_unit_tests

all_tests: tests long_tests


# a target to run only the test_gm files
.PHONY: game_tests
game_tests: test\\context.py
	-coverage run -m pytest $(GAME_TESTS)
	coverage html

# a target to run the stress tests with higher iterations
.PHONY: strest_tests	
stress_tests: test\\context.py params
	pytest test\\test_z_simul_game.py --nbr_runs 500 --sim_fails
	
.PHONY: player_tests
player_tests: test\\context.py params
	-pytest test\\test_z_simul_players.py --run_slow 



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

vpath %.cov .\\cov
vpath %.py .\\test

%.cov: test\\context.py src\\game_params.csv $(subst .cov,.py,$@) 
	-mkdir cov
	coverage run -m pytest test\\$(subst .cov,.py,$@)
	coverage json
	python test\\check_unit_cov.py $(subst .cov,,$@) > cov\\$@
	type cov\\$@

.PHONY: %.test
%.test: test\\context.py src\\game_params.csv $(subst .test,.py,$@)
	coverage run -m pytest test\\$(subst .test,.py,$@) --sim_fails
	coverage html

# do a stress test of one game:   make Wari.stress
# does both Wari and Wari GSO
PHONY: %.stress
%.stress: test\\context.py src\\game_params.csv $(subst .stre,.py,$@)
	pytest -k $(subst .stress,,$@) test\\test_z_simul_game.py --sim_fails --nbr_runs 1000


UNIT_TESTS += test_ai_player.cov
UNIT_TESTS += test_allowables.cov
UNIT_TESTS += test_bear_off.cov
UNIT_TESTS += test_capt_ok.cov
UNIT_TESTS += test_captures.cov
UNIT_TESTS += test_claimer.cov
UNIT_TESTS += test_diffusion.cov
UNIT_TESTS += test_drawer.cov
UNIT_TESTS += test_end_move.cov
UNIT_TESTS += test_game_info.cov
UNIT_TESTS += test_game_logger.cov
UNIT_TESTS += test_game_str.cov
# UNIT_TESTS += test_game_tally.cov     doesn't report coverage, likely tk not covered
UNIT_TESTS += test_gconsts.cov
UNIT_TESTS += test_get_direct.cov
UNIT_TESTS += test_get_moves.cov
UNIT_TESTS += test_history.cov
UNIT_TESTS += test_incr.cov
UNIT_TESTS += test_inhibitor.cov
UNIT_TESTS += test_make_child.cov
# test_man_config is last because it sometimes fails to load tkinter
UNIT_TESTS += test_mancala.cov
UNIT_TESTS += test_minimax.cov
UNIT_TESTS += test_montecarlo_ts.cov
UNIT_TESTS += test_mpath.cov
UNIT_TESTS += test_negamax.cov
UNIT_TESTS += test_new_game.cov
UNIT_TESTS += test_patterns.cov
UNIT_TESTS += test_round_tally.cov
UNIT_TESTS += test_rule_tester.cov
UNIT_TESTS += test_same_side.cov
UNIT_TESTS += test_sower.cov
UNIT_TESTS += test_two_cycle.cov
UNIT_TESTS += test_man_config.cov

cov_unit_tests: $(UNIT_TESTS)
	grep -h src cov\\*.cov



#  pylint
#
#  run the pylint on all source files together

pylint: $(SOURCES) .pylint_report makefile

.pylint_report: $(SOURCES) .pylintrc makefile
	-del .pylint_report
	-pylint --output .pylint_report --rcfile .pylintrc src/*py src/*pyw
	type .pylint_report


#  clean/spotless
#
#  clean: remove most of the accumulated stuff from builds
#  but leave things that are stored in configuration management
#  generally causes any other target to be re-run
#  leave the exe too
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
	-del MancalaGames.tgz
	
.PHONY : spotless
spotless: clean
	-rmdir /S /Q MancalaGames
	-del $(GENEDHELPS)
	-del $(CONTEXTS)
	-del src\\game_params.csv

# exe
#
# build stand alone executables with a shared runtime 
# put it into a compressed tar file for github

exe: MancalaGames/mancala_games.exe makefile

MancalaGames/mancala_games.exe: $(SOURCES) $(DATAFILES) $(HELPFILES) mancala_games.spec
	-rmdir /S /Q MancalaGames
	-git stash push mancala.ini -m "save mancala.ini"
	python tools\\update_version.py
	pyinstaller mancala_games.spec --distpath .
	mkdir MancalaGames\\help
	cp $(HELPFILES) MancalaGames\\help
	mkdir MancalaGames\\help\\figs
	copy docs\\figs\\*.jpg MancalaGames\\help\\figs
	copy docs\\styles.css MancalaGames\\help
	copy docs\\dist_readme.txt MancalaGames\\README.txt
	mkdir MancalaGames\\GameProps
	copy GameProps\\* MancalaGames\\GameProps
	mkdir MancalaGames\\logs
	copy logs\\README.txt MancalaGames\\logs
	copy src\\game_params.csv MancalaGames
	copy src\\game_param_descs.txt MancalaGames
	copy mancala.ini MancalaGames
	-git stash pop
	-rmdir /S /Q build
	tar -czf MancalaGames.tgz MancalaGames


.PHONY: list
list:
	@grep -Eo "^[a-zA-Z0-9\\/._]+:" makefile | sed -e "s/://" | sed -e "/PHONY/d" | sort
	
# includes Not a target files	
#	@$(MAKE) -pRrq | grep -Eo "^[a-zA-Z0-9\\/._]+:" | sed -e "s/://" | sed -e "/PHONY/d" | sort

# doesn't work
#	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'
