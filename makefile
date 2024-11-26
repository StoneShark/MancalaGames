
all: clean pylint context params all_tests docs exe

long_tests: stress_tests player_tests cov_unit_tests

# do in this order so that html coverage dir is output from all_tests
final: spotless long_tests all


MODULES = ai_interface.py
MODULES += ai_player.py
MODULES += allowables.py
MODULES += aspect_frame.py
MODULES += behaviors.py
MODULES += btn_behaviors.py
MODULES += capt_ok.py
MODULES += capturer.py
MODULES += cfg_keys.py
MODULES += claimer.py
MODULES += deco_chain_if.py
MODULES += diffusion.py
MODULES += drawer.py
MODULES += end_move.py
MODULES += end_move_decos.py
MODULES += end_move_rounds.py
MODULES += fill_patterns.py
MODULES += game_classes.py
MODULES += game_constants.py
MODULES += game_interface.py
MODULES += game_logger.py
MODULES += game_str.py
MODULES += game_tally.py
MODULES += get_direction.py
MODULES += get_moves.py
MODULES += ginfo_rules.py
MODULES += incrementer.py
MODULES += inhibitor.py
MODULES += make_child.py
MODULES += man_config.py
MODULES += man_path.py
MODULES += mancala_games.pyw
MODULES += mancala_ui.py
MODULES += mancala.py
MODULES += minimax.py
MODULES += montecarlo_ts.py
MODULES += negamax.py
MODULES += new_game.py
MODULES += param_consts.py
MODULES += play_mancala.pyw
MODULES += play.py
MODULES += round_tally.py
MODULES += sower.py

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
CONTEXTS += tools\\context.py


# game params
#
# convert xlsx to txt for main programs
# uses pandas which we don't want to use for main programs
# exe can't be built with pandas

params: src\\game_params.txt

src\\game_params.txt: src\\game_params.xlsx tools\\context.py tools\\convert_game_params.py
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
	-coverage run -m pytest $(GAME_TESTS)
	coverage html

# a target to run the stress tests with higher iterations
.PHONY: strest_tests	
stress_tests: test\\context.py
	pytest test\\test_z_simul_game.py --nbr_runs 500
	
.PHONY: player_tests
player_tests: test\\context.py
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
#
# TODO this isn't running after a "make clean"

vpath %.cov .\\cov
vpath %.py .\\test

%.cov: test\\context.py $(subst .cov,.py,$@)
	coverage run -m pytest test\\$(subst .cov,.py,$@)
	coverage json
	python test\\check_unit_cov.py $(subst .cov,,$@) > cov\\$@
	type cov\\$@

.PHONY: %.test
%.test: test\\context.py $(subst .test,.py,$@)
	coverage run -m pytest test\\$(subst .test,.py,$@)
	coverage html


UNIT_TESTS += test_ai_player.cov
UNIT_TESTS += test_allowables.cov
UNIT_TESTS += test_capt_ok.cov
UNIT_TESTS += test_captures.cov
UNIT_TESTS += test_claimer.cov
UNIT_TESTS += test_diffusion.cov
UNIT_TESTS += test_drawer.cov
UNIT_TESTS += test_end_move.cov
UNIT_TESTS += test_game_if.cov
UNIT_TESTS += test_game_logger.cov
UNIT_TESTS += test_game_str.cov
#  UNIT_TESTS += test_game_tally.cov     TODO doesn't report coverage, don't know why
UNIT_TESTS += test_gconsts.cov
UNIT_TESTS += test_get_direct.cov
UNIT_TESTS += test_get_moves.cov
UNIT_TESTS += test_incr.cov
UNIT_TESTS += test_inhibitor.cov
UNIT_TESTS += test_man_config.cov
UNIT_TESTS += test_mancala.cov
UNIT_TESTS += test_minimax.cov
UNIT_TESTS += test_montecarlo_ts.cov
UNIT_TESTS += test_mpath.cov
UNIT_TESTS += test_negamax.cov
UNIT_TESTS += test_new_game.cov
UNIT_TESTS += test_patterns.cov
UNIT_TESTS += test_round_tally.cov
UNIT_TESTS += test_sower.cov

cov_unit_tests: $(UNIT_TESTS)
	grep -h src cov\\*.cov




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
	-del src\\game_params.txt

# exe
#
# build stand alone executables with a shared runtime 
# put it into a compressed tar file for github

exe: MancalaGames/mancala_games.exe

MancalaGames/mancala_games.exe: $(SOURCES) $(DATAFILES) $(HELPFILES) mancala_games.spec
	-rmdir /S /Q MancalaGames
	pyinstaller mancala_games.spec --distpath .
	mkdir MancalaGames\\help
	cp $(HELPFILES) MancalaGames\\help
	copy docs\\styles.css MancalaGames\\help
	copy docs\\dist_readme.txt MancalaGames\\README.txt
	mkdir MancalaGames\\GameProps
	copy GameProps\\* MancalaGames\\GameProps
	mkdir MancalaGames\\logs
	copy logs\\README.txt MancalaGames\\logs
	copy src\\game_params.txt MancalaGames
	-rmdir /S /Q build
	tar -czf MancalaGames.tgz MancalaGames


.PHONY: list
list:
	@grep -Eo "^[a-zA-Z0-9\\/._]+:" makefile | sed -e "s/://" | sed -e "/PHONY/d" | sort
	
# includes Not a target files	
#	@$(MAKE) -pRrq | grep -Eo "^[a-zA-Z0-9\\/._]+:" | sed -e "s/://" | sed -e "/PHONY/d" | sort

# doesn't work
#	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'
