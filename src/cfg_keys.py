# -*- coding: utf-8 -*-
"""All the string keys from the configuration files.

When adding a parameter be sure to include it in the
appropriate tuple below.

Created on Tue Jul 25 07:43:16 2023
@author: Ann"""

ABOUT = 'about'
ACCESS_M = 'access_m'
AI_ACTIVE = 'ai_active'
AI_PARAMS = 'ai_params'
ALGORITHM = 'algorithm'
ALLOW_RULE = 'allow_rule'
BLOCKS = 'blocks'
CAPSAMEDIR = 'capsamedir'
CAPT_MAX = 'capt_max'
CAPT_MIN = 'capt_min'
CAPT_ON = 'capt_on'
CAPT_RTURN = 'capt_rturn'
CAPT_SIDE = 'capt_side'
CAPT_TYPE = 'capt_type'
CHILD_CNT_M = 'child_cnt_m'
CHILD_CVT = 'child_cvt'
CHILD_LOCS = 'child_locs'
CHILD_RULE = 'child_rule'
CHILD_TYPE = 'child_type'
CROSSCAPT = 'crosscapt'
DIFFICULTY = 'difficulty'
EASY_RAND = 'easy_rand'
EMPTIES_M = 'empties_m'
EVENS = 'evens'
EVENS_M = 'evens_m'
FILENAME = 'filename'
GAME_CLASS = 'game_class'
GAME_CONSTANTS = 'game_constants'
GAME_INFO = 'game_info'
GOAL = 'goal'
GOAL_PARAM = 'goal_param'
GRANDSLAM = 'grandslam'
HELP_FILE = 'help_file'
HOLES = 'holes'
MCTS_BIAS = 'mcts_bias'
MCTS_NODES = 'mcts_nodes'
MCTS_POUTS = 'mcts_pouts'
MIN_MOVE = 'min_move'
MLAPS = 'mlaps'
MLENGTH = 'mlength'
MM_DEPTH = 'mm_depth'
MOVE_ONE = 'move_one'
MOVEUNLOCK = 'moveunlock'
MULTICAPT = 'multicapt'
MUSTPASS = 'mustpass'
MUSTSHARE = 'mustshare'
NAME = 'name'
NBR_START = 'nbr_start'
NO_SIDES = 'no_sides'
NOCAPTMOVES = 'nocaptmoves'
NOSINGLECAPT = 'nosinglecapt'
PICKEXTRA = 'pickextra'
PLAYER = 'player'
PRESCRIBED = 'prescribed'
PRESOWCAPT = 'presowcapt'
QUITTER = 'quitter'
REPEAT_TURN = 'repeat_turn'
ROUND_FILL = 'round_fill'
ROUND_STARTER = 'round_starter'
ROUNDS = 'rounds'
SCORER = 'scorer'
SEEDS_M = 'seeds_m'
SKIP_START = 'skip_start'
SOW_DIRECT = 'sow_direct'
SOW_OWN_STORE = 'sow_own_store'
SOW_PARAM = 'sow_param'
SOW_RULE = 'sow_rule'
SOW_START = 'sow_start'
START_PATTERN = 'start_pattern'
STORES = 'stores'
STORES_M = 'stores_m'
UDIR_HOLES = 'udir_holes'
UDIRECT = 'udirect'
UNCLAIMED = 'unclaimed'
VARI_PARAMS = 'vari_params'
VISIT_OPP = 'visit_opp'
XC_SOWN = 'xc_sown'
XCPICKOWN = 'xcpickown'


GCONST_PARAMS = (HOLES,
                 NBR_START)

# these are the parameters that actually effect game play
# the description parameters are not included
GINFO_PARAMS =  (ALLOW_RULE,
                 BLOCKS,
                 CAPSAMEDIR,
                 CAPT_MAX,
                 CAPT_MIN,
                 CAPT_ON,
                 CAPT_RTURN,
                 CAPT_SIDE,
                 CAPT_TYPE,
                 CHILD_CVT,
                 CHILD_LOCS,
                 CHILD_RULE,
                 CHILD_TYPE,
                 CROSSCAPT,
                 EVENS,
                 GOAL,
                 GOAL_PARAM,
                 GRANDSLAM,
                 MIN_MOVE,
                 MLAPS,
                 MOVE_ONE,
                 MOVEUNLOCK,
                 MULTICAPT,
                 MUSTPASS,
                 MUSTSHARE,
                 NO_SIDES,
                 NOCAPTMOVES,
                 NOSINGLECAPT,
                 PICKEXTRA,
                 PRESCRIBED,
                 PRESOWCAPT,
                 QUITTER,
                 ROUND_FILL,
                 ROUND_STARTER,
                 ROUNDS,
                 SKIP_START,
                 SOW_DIRECT,
                 SOW_OWN_STORE,
                 SOW_PARAM,
                 SOW_RULE,
                 SOW_START,
                 START_PATTERN,
                 STORES,
                 UDIR_HOLES,
                 UNCLAIMED,
                 VISIT_OPP,
                 XC_SOWN,
                 XCPICKOWN,
                 )

# the parameters that configure the AI player
PLAYER_PARAMS = (ALGORITHM,
                 DIFFICULTY,
                 AI_ACTIVE,
                 MCTS_BIAS,
                 MCTS_NODES,
                 MCTS_POUTS,
                 MM_DEPTH,
                 STORES_M,
                 ACCESS_M,
                 SEEDS_M,
                 EMPTIES_M,
                 CHILD_CNT_M,
                 EVENS_M,
                 EASY_RAND,
                )
