
check_doc_classes.bash          bash script to see what classes are missing from 
                                GameClasses.odg, but it must be saved as a flat 
                                file (GameClasses.fodg).

context.py                      support imports of src modules

convert_game_params.py          converts the src/game_params.xlsx file to 
                                src/game_params.csv (which is used by mancala_games.pyw)

game_prop_csv_to_xlsx.txt       an Excel macro which will convert game_prop.csv to a 
                                formatted and filterable game_prop.xlsx file.
                                Must be installed in 'personal' workbook.

gen_game_log.py                 an outdated game log generator. 
                                analysis/challenge.py provides more options.
                    
log_to_script.py                a script to convert a game log into a series of 
                                methods to test each successive move in the log.
                                See any test/test_gm for an example of extra code
                                needed to make it a proper integratino test.

                                Use with care while it will generate the test sequence,
                                if the log has an error, the test will confirm the
                                bad behavior.

make_context.py                 creates the test/context.py which is copied any
                                where else it is needed by the main makefile

update_version.py               updates the build date, time and branch name for
                                the about popups. Run by makefile with exe target.
