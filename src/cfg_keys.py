# -*- coding: utf-8 -*-
"""All the string keys from the configuration files.

When adding a parameter be sure to include it in the
appropriate tuple below.

Created on Tue Jul 25 07:43:16 2023
@author: Ann"""

ABOUT = 'about'
AI_ACTIVE = 'ai_active'
AI_PARAMS = 'ai_params'
ALGORITHM = 'algorithm'
ALLOW_RULE = 'allow_rule'
BLOCKS = 'blocks'
CAPT_DIR = 'capt_dir'
CAPT_MAX = 'capt_max'
CAPT_MIN = 'capt_min'
CAPT_ON = 'capt_on'
CAPT_RTURN = 'capt_rturn'
CAPT_SIDE = 'capt_side'
CAPT_TYPE = 'capt_type'
CHILD_CVT = 'child_cvt'
CHILD_LOCS = 'child_locs'
CHILD_RULE = 'child_rule'
CHILD_TYPE = 'child_type'
CROSSCAPT = 'crosscapt'
DIFFICULTY = 'difficulty'
END_COND = 'end_cond'
END_PARAM = 'end_param'
EVENS = 'evens'
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
MLAP_CONT = 'mlap_cont'
MLAP_PARAM = 'mlap_param'
MLAPS = 'mlaps'
MLENGTH = 'mlength'
MM_DEPTH = 'mm_depth'
MOVE_ONE = 'move_one'
MOVEUNLOCK = 'moveunlock'
MULTICAPT = 'multicapt'
MUSTPASS = 'mustpass'
MUSTSHARE = 'mustshare'
MX_ACCESS_M = 'mx_access_m'
MX_CHILD_CNT_M = 'mx_child_cnt_m'
MX_EASY_RAND_A = 'mx_easy_rand_a'
MX_EMPTIES_M = 'mx_empties_m'
MX_EVENS_M = 'mx_evens_m'
MX_RTURN_A = 'mx_rturn_a'
MX_SEEDS_M = 'mx_seeds_m'
MX_STORES = 'mx_stores_m'
NAME = 'name'
NBR_START = 'nbr_start'
NO_SIDES = 'no_sides'
NOCAPTMOVES = 'nocaptmoves'
NOSINGLECAPT = 'nosinglecapt'
PICKEXTRA = 'pickextra'
PLAYER = 'player'
PLAY_LOCS = 'play_locs'
PRESCRIBED = 'prescribed'
PRESOWCAPT = 'presowcapt'
QUITTER = 'quitter'
ROUND_FILL = 'round_fill'
ROUND_STARTER = 'round_starter'
ROUNDS = 'rounds'
SCORER = 'scorer'
SKIP_START = 'skip_start'
SOW_DIRECT = 'sow_direct'
SOW_STORES = 'sow_stores'
SOW_PARAM = 'sow_param'
SOW_RULE = 'sow_rule'
SOW_START = 'sow_start'
START_PATTERN = 'start_pattern'
STORES = 'stores'
UDIR_HOLES = 'udir_holes'
UDIRECT = 'udirect'
UNCLAIMED = 'unclaimed'
VARI_PARAMS = 'vari_params'
VARIANTS = 'variants'
XC_SOWN = 'xc_sown'
XCPICKOWN = 'xcpickown'

# a combined dict of extra tags
EXTRA_TOPS = 'extra_tops'


#  Top level elements that are edited via individual parameters
#   - that is they are not collected and edited on the 'tags' tab
#   - they will also not be put into the xml text section of
#     game config files
TOP_LEVELS = (GAME_CLASS,
              GAME_CONSTANTS,
              GAME_INFO,
              PLAYER,
              VARIANTS,
              VARI_PARAMS,
              FILENAME)


GCONST_PARAMS = (HOLES,
                 NBR_START)

# these are the parameters that actually effect game play
# the description parameters are not included
GINFO_PARAMS =  (ALLOW_RULE,
                 BLOCKS,
                 CAPT_DIR,
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
                 END_COND,
                 END_PARAM,
                 EVENS,
                 GOAL,
                 GOAL_PARAM,
                 GRANDSLAM,
                 MIN_MOVE,
                 MLAPS,
                 MLAP_CONT,
                 MLAP_PARAM,
                 MOVE_ONE,
                 MOVEUNLOCK,
                 MULTICAPT,
                 MUSTPASS,
                 MUSTSHARE,
                 NO_SIDES,
                 NOCAPTMOVES,
                 NOSINGLECAPT,
                 PICKEXTRA,
                 PLAY_LOCS,
                 PRESCRIBED,
                 PRESOWCAPT,
                 QUITTER,
                 ROUND_FILL,
                 ROUND_STARTER,
                 ROUNDS,
                 SKIP_START,
                 SOW_DIRECT,
                 SOW_STORES,
                 SOW_PARAM,
                 SOW_RULE,
                 SOW_START,
                 START_PATTERN,
                 STORES,
                 UDIR_HOLES,
                 UNCLAIMED,
                 XC_SOWN,
                 XCPICKOWN,
                 )

# these are the keys allowed in variants
CONFIG_PARAMS = {GAME_CLASS} | set(GCONST_PARAMS) | set(GINFO_PARAMS)

# don't save empty values for these keys
NO_EMPTY = (VARI_PARAMS, VARIANTS)


# the parameters that configure the AI player
PLAYER_PARAMS = (ALGORITHM,
                 DIFFICULTY,
                 AI_ACTIVE,
                 MCTS_BIAS,
                 MCTS_NODES,
                 MCTS_POUTS,
                 MM_DEPTH,
                 MX_STORES,
                 MX_ACCESS_M,
                 MX_SEEDS_M,
                 MX_EMPTIES_M,
                 MX_CHILD_CNT_M,
                 MX_EVENS_M,
                 MX_RTURN_A,
                 MX_EASY_RAND_A,
                )


# options with values that are not hashable (not simple types)
NOT_HASHABLE = (CAPT_ON,
                UDIR_HOLES,
                MCTS_BIAS,
                MCTS_NODES,
                MCTS_POUTS,
                MM_DEPTH)
