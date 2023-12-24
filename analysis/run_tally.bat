

set runs=30000

rem  no mlaps, no rounds
python tally_games.py --nbr_runs %runs% --output no_mlaps_rounds --game Cow --game Eson_Xorgol --game Goat --game Kalah --game Mbangbi --game NoCapt --game NoSides --game NoSidesChild --game Oware --game Qelat --game Songo --game Toguz_Xorgol --game Vai_Lun_Thlan --game Wari --game XCaptSowOwn

rem  mlaps but no rounds
python tally_games.py --nbr_runs %runs% --output no_rounds --game Ayoayo --game Bao_Kenyan --game Dabuda --game Deka --game Endodoi --game Enkeshui --game Gamacha --game J_Odu --game Mbothe --game Nambayi --game Ndoto --game Sadeqa --game Tapata --game Valah

rem  rounds
python tally_games.py --nbr_runs %runs% --output mlaps_rounds --game Bao_Tanzanian --game Bechi --game Bosh --game Congklak --game Dakon --game Erherhe --game Gabata --game Giuthi --game Lami --game Lamlameta --game Lam_Waladach --game Longbeu-a-cha --game NamNam --game NumNum --game Pallam_Kuzhi --game Pandi --game Weg

