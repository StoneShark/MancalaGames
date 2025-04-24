# -*- coding: utf-8 -*-
"""Mancala doesn't know whose playing it. Minimax doesn't know
what game it's playing. This module ties the two together.

Created on Fri Oct 13 14:40:46 2023
@author: Ann"""

import dataclasses as dc
import functools as ft
import random

import ai_interface
import cfg_keys as ckey
import game_interface as gi
import ginfo_rules
import minimax
import montecarlo_ts as mcts
import negamax

from game_logger import game_log


# XXXX ai player data should be in algo files
# will this work:
#   define the variables in the ai_interface
#   add to them in the player files
#   use them here

ALGORITHM_DICT = {'minimaxer': minimax.MiniMaxer,
                  'negamaxer': negamax.NegaMaxer,
                  'montecarlo_ts': mcts.MonteCarloTS}

AI_PARAM_DEFAULTS = {ckey.MM_DEPTH: [1, 1, 3, 5],
                     ckey.MCTS_BIAS: [300, 200, 100, 100],
                     ckey.MCTS_NODES: [100, 300, 500, 800],
                     ckey.MCTS_POUTS: [1, 1, 1, 1]}

NEGAMAXER = 'negamaxer'
MCTS = 'montecarlo_ts'

# a divider for the bias so that we can store ints in the config file
MCTS_BIAS_DIV = 1000


@dc.dataclass(kw_only=True)
class ScoreParams:
    """Multipliers for the different scorers, 0 turns it off.
    easy_rand is the +- error introduced on easy difficulty.
    access_m if positive, is only used on Hard or Expert."""

    stores_m: int = 0
    access_m: int = 0
    seeds_m: int = 0
    empties_m: int = 0
    child_cnt_m: int = 0
    evens_m: int = 0
    easy_rand: int = 0
    repeat_turn: int = 0

    @classmethod
    def get_default(cls, fname):
        """Lookup the default value for the field."""

        for field in dc.fields(cls):
            if field.name == fname:
                return field.default
        return 0


# %%

class AiPlayer(ai_interface.AiPlayerIf):
    """The wrapper for the configuration and the algorithm."""

    def __init__(self, game, player_dict):

        super().__init__(game, player_dict)
        player_dict_rules().test(player_dict, game.info)

        if ckey.ALGORITHM in player_dict:
            self.set_algorithm(player_dict[ckey.ALGORITHM])
        else:
            self.algo = minimax.MiniMaxer(game, self)

        self.dbl_holes = self.game.cts.dbl_holes
        self.holes = self.game.cts.holes

        if ckey.SCORER in player_dict:
            self.sc_params = ScoreParams(**(player_dict[ckey.SCORER]))
        else:
            self.sc_params = ScoreParams()

        if ckey.AI_PARAMS not in player_dict:
            player_dict[ckey.AI_PARAMS] = {}
        self.ai_params = AI_PARAM_DEFAULTS | player_dict[ckey.AI_PARAMS]

        self._diff = 0
        self.difficulty = player_dict.get(ckey.DIFFICULTY, 1)

        self.scorers = []
        self.collect_scorers()


    def __str__(self):

        rstr = 'AiPlayer:\n'
        rstr += '   Algorithm: ' + str(self.algo) + '\n'
        rstr += '   Difficulty: ' + str(self._diff) + '\n'
        rstr += '   ' + str(self.sc_params) + '\n'
        return rstr


    @property
    def difficulty(self):
        return self._diff


    @difficulty.setter
    def difficulty(self, value):
        """Set the difficulty after checking the algo type"""

        self._diff = value

        if isinstance(self.algo, (minimax.MiniMaxer, negamax.NegaMaxer)):
            max_depth = self.ai_params[ckey.MM_DEPTH][value]
            self.algo.set_params(max_depth)

        elif isinstance(self.algo, mcts.MonteCarloTS):
            mcts_bias = self.ai_params[ckey.MCTS_BIAS][value] / MCTS_BIAS_DIV
            mcts_nodes = self.ai_params[ckey.MCTS_NODES][value]
            mcts_pouts = self.ai_params[ckey.MCTS_POUTS][value]
            self.algo.set_params(mcts_bias, mcts_nodes, mcts_pouts)

        else:
            raise ValueError("Don't know how to set the algo difficulty.")


    def set_algorithm(self, algo_name):
        """Change the algorithm by name"""

        if algo_name in ALGORITHM_DICT:
            self.algo = ALGORITHM_DICT[algo_name](self.game, self)
        else:
            raise KeyError(f'Unknown ai player algorithm: {algo_name}.')


    def pick_move(self):
        """Have the algorithm pick the move."""
        return self.algo.pick_move()


    def get_move_desc(self):
        """Get the description from the algorithm."""
        return self.algo.get_move_desc()


    def collect_scorers(self):
        """Collect the list of scorers.
        This must be called if any of the multipliers are enabled/disabled."""
        # pylint: disable=too-complex
        # pylint: disable=too-many-branches

        self.scorers = []

        if self.sc_params.repeat_turn:
            self.scorers += [self._score_repeat_turn]

        if self.sc_params.stores_m:
            if self.game.info.child_cvt:
                self.scorers += [self._score_child_stores]
            else:
                self.scorers += [self._score_stores]

        if self.game.info.child_cvt and self.sc_params.child_cnt_m:
            self.scorers += [self._score_children]

        if self.sc_params.easy_rand:
            self.scorers += [self._score_easy]

        if self.sc_params.access_m:
            self.scorers += [self._score_access]

        scorers = [('evens_m',
                     self._score_cnt_evens,
                     self._score_diff_evens),
                    ('seeds_m',
                     self._score_cnt_seeds,
                     self._score_diff_seeds),
                    ('empties_m',
                     self._score_cnt_empties,
                     self._score_diff_empties)]

        if self.game.info.goal == gi.Goal.TERRITORY:
            # pylint: disable=unnecessary-lambda-assignment
            who_func = lambda loc: self.game.owner[loc]
        else:
            who_func = self.game.cts.board_side

        for param, cnt_func, diff_func in scorers:
            if getattr(self.sc_params, param):

                # if board_side(0) is True, it's an EAST/WEST game
                if self.game.info.no_sides and not self.game.cts.board_side(0):
                    self.scorers += [cnt_func]
                else:
                    self.scorers += [ft.partial(diff_func, who_func)]


    def clear_history(self):
        """Tell the algorithm to reset/clear any history or
        saved game states."""
        self.algo.clear_history()


    def is_max_player(self):
        """Return True if 'score' maximizes for the current player."""
        return self.game.turn is False


    def score(self, end_cond):
        """Statically evaluate the playing position in terms of the bottom
        player (i.e. False).
        end_cond is the result of the last move."""

        sval = self._score_endgame(end_cond)
        if sval is not None:
            return sval

        return sum(scorer(end_cond) for scorer in self.scorers)


    def _score_endgame(self, end_cond):
        """Score the end game conditions.
        return None if not scored."""

        if end_cond in (gi.WinCond.ROUND_WIN, gi.WinCond.WIN):
            return -1000 if self.game.turn else 1000

        if end_cond in (gi.WinCond.ROUND_TIE, gi.WinCond.TIE):
            return -5 if self.game.turn else 5

        if end_cond == gi.WinCond.ENDLESS:
            return 0

        return None


    def _score_repeat_turn(self, end_cond):
        """Score a repeat turn."""

        if end_cond == gi.WinCond.REPEAT_TURN:
            mult = -1 if self.game.turn else 1
            return mult * self.sc_params.repeat_turn

        return 0

    def _score_stores(self, _):
        """Score the stores and children."""

        store_f = self.game.store[False]
        store_t = self.game.store[True]

        return (store_f - store_t) * self.sc_params.stores_m


    def _score_child_stores(self, _):
        """Score the stores and children."""

        store_f = self.game.store[False]
        store_t = self.game.store[True]

        for loc in range(self.dbl_holes):
            if self.game.child[loc] is False:
                store_f += self.game.board[loc]
            elif self.game.child[loc] is True:
                store_t += self.game.board[loc]

        return (store_f - store_t) * self.sc_params.stores_m


    def _score_children(self, _):
        """Score children on each side of the board.
        More children, more places to capture."""

        child_f = self.game.child.count(False)
        child_t = self.game.child.count(True)
        return (child_f - child_t) * self.sc_params.child_cnt_m


    def _score_diff_evens(self, who_func, _):
        """Score evens on each side of the board.
        If capturing on evens, having evens prevents captures."""

        even_t = even_f = 0
        for loc in range(self.game.cts.dbl_holes):

            if (self.game.child[loc] is None
                    and self.game.board[loc]
                    and not self.game.board[loc] % 2):

                who = who_func(loc)
                if who is True:
                    even_t += 1
                elif who is False:
                    even_f += 1

        return (even_f - even_t) * self.sc_params.evens_m


    def _score_cnt_evens(self, _):
        """Score count of evens on the whole board.
        To make min values best for true, mult by -1.
        If capturing on evens, having evens prevents captures."""

        even_cnt = sum(1 for loc in range(self.game.cts.dbl_holes)
                       if self.game.child[loc] is None
                             and self.game.board[loc] > 0
                             and not self.game.board[loc] % 2)
        tmult = -1 if self.game.turn else 1

        return even_cnt * self.sc_params.evens_m * tmult


    def _score_diff_seeds(self, who_func, _):
        """Score the seeds on each side of the board.
        Sometimes hoarding seeds is a good strategy."""

        sum_t = sum_f = 0
        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is None:

                who = who_func(loc)
                if who is True:
                    sum_t += self.game.board[loc]
                elif who is False:
                    sum_f += self.game.board[loc]

        return (sum_f - sum_t) * self.sc_params.seeds_m


    def _score_cnt_seeds(self, _):
        """Score count of seeds remaining on the board.
        To make min values best for true, mult by -1."""

        tmult = -1 if self.game.turn else 1
        seeds_sum = sum(self.game.board[loc]
                        for loc in range(self.game.cts.dbl_holes)
                        if self.game.child[loc] is None)
        return seeds_sum * self.sc_params.seeds_m * tmult


    def _score_diff_empties(self, who_func, _):
        """Score the number of empties on each side of the board.
        Without empties, cross captures cannot occur."""

        empty_t = empty_f = 0
        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is None and not self.game.board[loc]:

                who = who_func(loc)
                if who is True:
                    empty_t += 1
                elif who is False:
                    empty_f += 1

        return (empty_f - empty_t) * self.sc_params.empties_m


    def _score_cnt_empties(self, _):
        """Score the count of empties on the board.
        To make min values best for true, mult by -1."""

        empties = sum(1 for loc in range(self.game.cts.dbl_holes)
                      if not self.game.board[loc])
        tmult = -1 if self.game.turn else 1
        return empties * self.sc_params.empties_m * tmult


    def _score_easy(self, _):
        """When the difficulty is easy,
        add a small random value to the score, i.e. introduce
        a scoring error."""

        if not self._diff:
            easy = self.sc_params.easy_rand
            return random.randrange(-easy, easy)

        return 0


    def _score_access(self, _):
        """Score the difference between the number opponents cells that
        false and true can access. Only do this on higher difficulties.

        Do not support games that take too long to simulate, e.g.
        multi-lap, udirect, no_sides. Rules enforce these conditions."""

        if self._diff <= 1:
            return 0

        access = [set(), set()]
        saved_state = self.game.state

        for pos in range(self.holes):
            for turn in (True, False):

                self.game.turn = turn
                with game_log.simulate():
                    mdata = self.game.do_sow(pos)

                if self.game.cts.opp_side(self.game.turn, mdata.capt_loc):
                    access[turn] |= set([mdata.capt_loc])

                self.game.state = saved_state

        return ((len(access[False]) - len(access[True]))
                * self.sc_params.access_m)


# %%  rule dict

DIFF_LEVELS = 4
MAX_MINIMAX_DEPTH = 15


def player_dict_rules():
    """Create the rules to check the consistency of the player dict.
    pdict will always be passed, game.info is the second optional
    object."""

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'def_diff',
        rule=lambda pdict: (ckey.DIFFICULTY in pdict
                            and pdict[ckey.DIFFICULTY]
                                not in range(DIFF_LEVELS)),
        msg='Difficulty not 0, 1, 2 or 3',
        excp=gi.GameInfoError)

    rules.add_rule(
        'scorer_vals',
        rule=lambda pdict: ((ckey.ALGORITHM not in pdict
                             or (ckey.ALGORITHM in pdict
                                 and pdict[ckey.ALGORITHM] in {'minimaxer',
                                                               'negamaxer'}))
                             and ckey.SCORER in pdict
                             and not sum(pdict[ckey.SCORER].values())),
        msg='At least one scorer value should be non-zero '
            'to prevent random play for Minimaxer or Negamaxer',
        warn=True)

    rules.add_rule(
        'params_four_diff',
        rule=lambda pdict: (ckey.AI_PARAMS in pdict
                            and any(len(values) != DIFF_LEVELS
                                    for values in
                                        pdict[ckey.AI_PARAMS].values())),
        msg=f'Exactly {DIFF_LEVELS} param values are expected '
            'for each ai parameter',
        excp=gi.GameInfoError)

    rules.add_rule(
        'stores_scorer',
        rule=lambda pdict, ginfo: (not ginfo.stores
                                   and not ginfo.child_cvt
                                   and ckey.SCORER in pdict
                                   and ckey.STORES_M in pdict[ckey.SCORER]
                                   and pdict[ckey.SCORER][ckey.STORES_M]),
        both_objs=True,
        msg='Stores scorer is not supported without stores or children.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'stores_scorer_inv',
        rule=lambda pdict, ginfo: (ginfo.goal in (gi.Goal.CLEAR,
                                                  gi.Goal.DEPRIVE,
                                                  gi.Goal.RND_WIN_COUNT_CLR,
                                                  gi.Goal.RND_WIN_COUNT_DEP)
                                   and ckey.SCORER in pdict
                                   and ckey.STORES_M in pdict[ckey.SCORER]
                                   and pdict[ckey.SCORER][ckey.STORES_M]),
        both_objs=True,
        msg='Stores scorer is not supported for CLEAR or DEPRIVE games.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'mlaps_access_prohibit',
        rule=lambda pdict, ginfo: (ginfo.mlaps
                                   and ckey.SCORER in pdict
                                   and ckey.ACCESS_M in pdict[ckey.SCORER]
                                   and pdict[ckey.SCORER][ckey.ACCESS_M]),
        both_objs=True,
        msg='Access scorer not supported for multilap games',
        excp=gi.GameInfoError)

    rules.add_rule(
        'udirect_access_prohibit',
        rule=lambda pdict, ginfo: (ginfo.udirect
                                   and ckey.SCORER in pdict
                                   and ckey.ACCESS_M in pdict[ckey.SCORER]
                                   and pdict[ckey.SCORER][ckey.ACCESS_M]),
        both_objs=True,
        msg='Access scorer not supported with UDIR_HOLES',
        excp=gi.GameInfoError)

    rules.add_rule(
        'no_side_access',
        rule=lambda pdict, ginfo: (ginfo.mlength == 3
                                   and ckey.SCORER in pdict
                                   and ckey.ACCESS_M in pdict[ckey.SCORER]
                                   and pdict[ckey.SCORER][ckey.ACCESS_M]),
        both_objs=True,
        msg='Scorer ACCESS_M multiplier is incompatible with'
        'NO_SIDES and TERRITORY',
        excp=gi.GameInfoError)

    rules.add_rule(
        'child_scorer',
        rule=lambda pdict, ginfo: (not ginfo.child_cvt
                                   and ckey.SCORER in pdict
                                   and ckey.CHILD_CNT_M in pdict[ckey.SCORER]
                                   and pdict[ckey.SCORER][ckey.CHILD_CNT_M]),
        both_objs=True,
        msg='Child count scorer not supported without CHILD',
        excp=gi.GameInfoError)

    rules.add_rule(
        'no_repeat_scorer',
        rule=lambda pdict, ginfo: (not (ginfo.sow_own_store
                                        or ginfo.capt_rturn
                                        or ginfo.xc_sown)
                                   and ckey.SCORER in pdict
                                   and ckey.REPEAT_TURN in pdict[ckey.SCORER]
                                   and pdict[ckey.SCORER][ckey.REPEAT_TURN]),
        both_objs=True,
        msg="Repeat turn scorer not supported without repeat turns "
            "(SOW_OWN_STORE | CAPT_RTURN | XC_SOWN)",
        excp=gi.GameInfoError)

    rules.add_rule(
        'nmax_no_repeat',
        rule=lambda pdict, ginfo: ((ginfo.sow_own_store
                                    or ginfo.capt_rturn
                                    or ginfo.xc_sown)
                                   and ckey.ALGORITHM in pdict
                                   and pdict[ckey.ALGORITHM] == NEGAMAXER),
        both_objs=True,
        msg="NegaMax not compatible with repeat turns "
            "(SOW_OWN_STORE | CAPT_RTURN | XC_SOWN)",
        excp=gi.GameInfoError)

    # rules.add_rule(
    #     'mcts_move_nbrs',
    #     rule=lambda pdict, ginfo: ((ginfo.prescribed
    #                                 or ginfo.nocaptmoves
    #                                 or ginfo.allow_rule in
    #                                     {gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
    #                                      gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO}
    #                                 )
    #                                and ckey.ALGORITHM in pdict
    #                                and pdict[ckey.ALGORITHM] == MCTS),
    #     both_objs=True,
    #     msg="Monte Carlo Tree Search might not work well with options that "
    #         "vary behavior with move number (prescribed openings, allow "
    #         "rules that only apply to some moves, no first move captures).",
    #     warn=True)
    #     # this might really only be an issue after the first move

    return rules
