# -*- coding: utf-8 -*-
"""The rules that check GameInfo.

Created on Mon Aug 21 06:54:24 2023
@author: Ann"""

import game_info as gi
import round_tally
import rule_tester

from fill_patterns import PCLASSES

# %% constants

DIFF_LEVELS = 4
MAX_MIN_MOVES = 5
MAX_MINIMAX_DEPTH = 15


# %% grouped rules

def test_creation_rules(tester):
    """Basic rules to make sure that everything that should exist does."""

    tester.test_rule('invalid_holes',
        both_objs=True,
        rule=lambda ginfo, holes: (not holes or not isinstance(holes, int)),
        msg='Holes must > 0',
        excp=gi.GameInfoError)

    tester.test_rule('missing_name',
        rule=lambda ginfo: not ginfo.name,
        msg='Mising Name',
        excp=gi.GameInfoError)

    tester.test_rule('sow_dir_type',
        rule=lambda ginfo: not isinstance(ginfo.sow_direct, gi.Direct),
        msg='SOW_DIRECT not valid type, expected gi.Direct',
        excp=gi.GameInfoError)

    tester.test_rule('high_min_moves',
        both_objs=True,
        rule=lambda ginfo, holes: not 1 <= ginfo.min_move <= min(holes, MAX_MIN_MOVES),
        msg=f'Min_move seems wrong (1<= convention <= min(holes, {MAX_MIN_MOVES}))',
        excp=gi.GameInfoError)
        # First, convenstion. Second, the even fill round ender
        # assumes that min move is <= holes


def test_pattern_rules(tester):
    """Add a rule for each pattern to check the number of holes."""

    def test_pattern(index, pattern):
        """Return a function that tests that the pattern is index
        and tests the size_ok function."""

        def _pattern(ginfo, holes):
            return ginfo.start_pattern == index and not pattern.size_ok(holes)

        return _pattern

    for idx, pat in enumerate(PCLASSES):
        if not pat:
            continue

        tester.test_rule(f'pattern_{idx}_req_size',
            both_objs=True,
            rule=test_pattern(idx, pat),
            msg=pat.err_msg,
            excp=gi.GameInfoError)

    tester.test_rule('move_rmost_mlength',
        rule=lambda ginfo: (ginfo.start_pattern ==
                                gi.StartPattern.MOVE_RIGHTMOST
                            and ginfo.mlength > 1),
        msg="""START_PATTERN of MOVE_RIGHTMOST is incompatible with
            territory GOAL, NO_SIDES, or user directed sow direction
            (mlength > 1)""",
        excp=gi.GameInfoError)
        # territory - rightmost hole might not belong to starter
        # no way to choose direction for generated move


def test_eliminate_goal_rules(tester):
    """Add rules for the game eliminating our own or opponents seeds."""

    def _elimnate_and(flag_name):
        """Return a function that tests that goal is divert
        and the specified flag, based only on a ginfo parameter."""

        def _elimnate_and(ginfo):
            return (ginfo.goal.eliminate() and getattr(ginfo, flag_name))

        return _elimnate_and


    tester.test_rule('elseed_gs_legal',
        rule=lambda ginfo: (ginfo.goal.eliminate()
                            and ginfo.grandslam != gi.GrandSlam.LEGAL),
        msg="""CLEAR, DEPRIVE and IMMOBILIZE games require
        that GRANDSLAM be Legal""",
        excp=gi.GameInfoError)

    bad_flags = ['child_type', 'child_cvt', 'child_rule',
                 'moveunlock', 'mustshare', 'mustpass']
    for flag in bad_flags:
        tester.test_rule(f'elseed_bad_{flag}',
            rule=_elimnate_and(flag),
            msg=f"""CLEAR, DEPRIVE and IMMOBILIZE games cannot be used
                  with {flag.upper()}""",
            excp=gi.GameInfoError)

    tester.test_rule('elseed_no_rounds',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.CLEAR,
                                           gi.Goal.DEPRIVE,
                                           gi.Goal.IMMOBILIZE)
                            and ginfo.rounds),
        msg="""Goals CLEAR, DEPRIVE and IMMOBILIZE cannot be played in rounds
            that are not the Round Tally goals""",
            excp=gi.GameInfoError)

    tester.test_rule('elseed_no_moves',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.RND_WIN_COUNT_CLR,
                                           gi.Goal.RND_WIN_COUNT_DEP,
                                           gi.Goal.RND_WIN_COUNT_IMB)
                            and ginfo.rounds != gi.Rounds.NO_MOVES),
        msg="""Round tally games for CLEAR, DEPRIVE and IMMOBILIZE
            require ROUNDS to be NO_MOVES""",
            excp=gi.GameInfoError)

    tester.test_rule('elseed_ec_no_clear',
        rule=lambda ginfo: (ginfo.goal.eliminate()
                            and ginfo.end_cond in (gi.EndGameCond.CLEARED_OWN,
                                                   gi.EndGameCond.CLEARED_OPP)),
        msg="""CLEAR, DEPRIVE and IMMOBILIZE games are incompatible with
        CLEARED OWN/END end conditions""",
        excp=gi.GameInfoError)

    tester.test_rule('immob_no_rturn',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.IMMOBILIZE,
                                           gi.Goal.RND_WIN_COUNT_IMB)
                            and ginfo.repeat_turn),
        msg='Immobilize cannot use repeat turn',
        excp=gi.GameInfoError)
        # repeat turn in immobilize game -- could immobilize self

    tester.test_rule('clear_no_min_move',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.CLEAR,
                                           gi.Goal.RND_WIN_COUNT_CLR)
                            and ginfo.min_move != 1),
        msg='CLEAR games require that MIN_MOVE be 1',
        excp=gi.GameInfoError)
        # clear game, if there are seeds they must be playable

    tester.test_rule('clear_no_prevent',
        rule=lambda ginfo: (
            ginfo.goal in (gi.Goal.CLEAR, gi.Goal.RND_WIN_COUNT_CLR)
            and ginfo.allow_rule.no_moves()),
        msg="""CLEAR games prohibit the selected allow rule.
            If a player has seeds, they must be able to play""",
        excp=gi.GameInfoError)
        # clear game, if there are seeds they must be playable


def test_territory_rules(tester):
    """Add the rules for games with a goal of territory."""

    tester.test_rule('terr_only_rfill',
        rule=lambda ginfo: (ginfo.goal != gi.Goal.TERRITORY
                            and ginfo.round_fill in
                                (gi.RoundFill.TERR_EX_RANDOM,
                                 gi.RoundFill.TERR_EX_EMPTY,
                                 gi.RoundFill.TERR_EX_LOSER)),
        msg='Selected round fill is only supported Territory goal',
        excp=gi.GameInfoError)
        # don't let other's play in our sandbox

    tester.test_rule('terr_goal_param',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.goal == gi.Goal.TERRITORY
                                   and (ginfo.goal_param <= holes
                                        or ginfo.goal_param > 2 * holes)),
        msg='Territory Goal requires GOAL_PARAM between holes and 2 * holes',
        excp=gi.GameInfoError)

    tester.test_rule('terr_need_stores',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and not ginfo.stores),
        msg='Territory goal requires stores',
        excp=gi.GameInfoError)

    tester.test_rule('terr_no_sides_incomp',
        rule=lambda ginfo: ginfo.goal == gi.Goal.TERRITORY and ginfo.no_sides,
        msg='Territory goal is incompatible with NO_SIDES',
        excp=gi.GameInfoError)

    tester.test_rule('terr_alleq',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.round_fill == gi.RoundFill.TERR_EX_EMPTY
                            and ginfo.start_pattern != gi.StartPattern.ALL_EQUAL),
        msg='Round fill TERR_EX_EMPTY requires the ALL_EQUAL start patterns',
        excp=gi.GameInfoError)
        #  the deco TerrEmtpyNewRound is written with this assumption

    tester.test_rule('terr_capt_side',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.capt_side in (gi.CaptSide.OPP_SIDE,
                                                    gi.CaptSide.OWN_SIDE,
                                                    gi.CaptSide.OPP_CONT,
                                                    gi.CaptSide.OWN_CONT)),
        msg='CAPT_SIDE based on board location is odd for Territory games',
        warn=True)

    tester.test_rule('capt_terr',
        rule=lambda ginfo: (ginfo.goal != gi.Goal.TERRITORY
                            and ginfo.capt_side in (gi.CaptSide.OPP_TERR,
                                                    gi.CaptSide.OWN_TERR)),
        msg='CAPT_SIDE based on hole ownership is only valid for Territory games',
        excp=gi.GameInfoError)

    tester.test_rule('terr_blocks',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.blocks),
        msg='Territory games are incompatible with blocks',
        excp=gi.GameInfoError)
        #  what would blocks mean, hole ownership is allocated based on seed count

    tester.test_rule('terr_no_rfill',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.round_fill not in
                                (gi.RoundFill.NOT_APPLICABLE,
                                 gi.RoundFill.UCHOWN,
                                 gi.RoundFill.TERR_EX_LOSER,
                                 gi.RoundFill.TERR_EX_EMPTY,
                                 gi.RoundFill.TERR_EX_RANDOM)),
        msg='Selected round fill is ignored for Territory goal',
        warn=True)

    tester.test_rule('terr_no_end',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.goal == gi.Goal.TERRITORY
                                   and ginfo.round_fill in
                                       (gi.RoundFill.TERR_EX_LOSER,
                                        gi.RoundFill.TERR_EX_EMPTY)
                                   and ginfo.goal_param == 2 * holes),
        msg="""For territory games with TERR_EX_LOSER or TERR_EX_EMPTY
            round fill, GOAL_PARAM should be less than the total number
            of holes, otherwise a win would require capturing all the seeds""",
        warn=True)

    tester.test_rule('uchown_terr_only',
        rule=lambda ginfo: (ginfo.goal != gi.Goal.TERRITORY
                            and ginfo.round_fill == gi.RoundFill.UCHOWN),
        msg='Round Fill UCHOWN is only supported for Territory goal',
        excp=gi.GameInfoError)

    tester.test_rule('terr_gs_not',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.grandslam == gi.GrandSlam.NOT_LEGAL),
        msg='Territory goal and GRANDLAM=Not Legal are currently incompatible',
        excp=NotImplementedError)
        # territory requires move triples, GS allowables doesn't support

    tester.test_rule('terr_no_fchild',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.child_locs == gi.ChildLocs.FIXED_ONE_RIGHT),
        msg='Territory goal and fixed children are incompatible',
        excp=NotImplementedError)
        # player might not own the child hole

    tester.test_rule('terr_half_rounds',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.rounds == gi.Rounds.HALF_SEEDS),
        msg='Territory goal is incompatible with ROUNDS.HALF_SEEDS',
        excp=gi.GameInfoError)
        # half seeds would lead to endless territory games
        # most seeds must be moved out of play for territory games

    tester.test_rule('terr_gparam_high',
        both_objs=True,
        rule=lambda ginfo, nbr_holes: (
            ginfo.goal == gi.Goal.TERRITORY
            and ginfo.unclaimed == gi.EndGameSeeds.DONT_SCORE
            and ((ginfo.rounds == gi.Rounds.END_S_SEEDS
                  and ginfo.goal_param > (nbr_holes * 2) - 1)
                 or (ginfo.rounds == gi.Rounds.END_2S_SEEDS
                     and ginfo.goal_param > (nbr_holes * 2) - 2))),
        msg='Territory goal param is too high for ROUNDS of DONT_SCORE, '
            'a game winner is unlikely',
        excp=gi.GameInfoError)


def sow_blkd_div(ginfo):
    """Test if either of the sow_blkd_div rules."""
    return (ginfo.sow_rule in
            (gi.SowRule.SOW_BLKD_DIV, gi.SowRule.SOW_BLKD_DIV_NR))


def test_block_and_divert_rules(tester):
    """sow_blkd_div is implemented primarily by the sower and the
    capturer is not used (capt mechanisms not supported). Add rules
    to ensure the right corresponding flags are used (or not used)."""

    def divert_and(flag_name):
        """Return a function that the divert option and the specified
        flag, based only on a ginfo parameter."""

        def _divert_and(ginfo):
            return (sow_blkd_div(ginfo)
                    and getattr(ginfo, flag_name))

        return _divert_and

    tester.test_rule('next_ml_no_bdiv',
        rule=lambda ginfo: (ginfo.mlaps == gi.LapSower.LAPPER_NEXT
                            and sow_blkd_div(ginfo)),
        msg='MLAPS of LAPPER_NEXT is not supported with SOW_BLKD_DIV(_NR)',
        excp=NotImplementedError)

    tester.test_rule('bdiv_need_gparam',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and not ginfo.sow_param),
        msg='SOW_BLKD_DIV(_NR) requires SOW_PARAM for closing holes',
        excp=gi.GameInfoError)

    tester.test_rule('bdiv_need_blocks',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and not ginfo.blocks),
        msg='SOW_BLKD_DIV(_NR) requires BLOCKS for closing holes',
        excp=gi.GameInfoError)

    tester.test_rule('bdiv_req_goal',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and ginfo.goal not in (gi.Goal.DEPRIVE,
                                                   gi.Goal.IMMOBILIZE,
                                                   gi.Goal.RND_WIN_COUNT_DEP,
                                                   gi.Goal.RND_WIN_COUNT_IMB)),
        msg='SOW_BLKD_DIV(_NR) requires a DEPRIVE or IMMOBILIZE goal',
        excp=gi.GameInfoError)

    capt_flags = ['capt_dir', 'capt_max', 'capt_min', 'capt_type',
                  'capt_on', 'capt_rturn', 'crosscapt',
                  'evens', 'multicapt',
                  'nosinglecapt', 'capt_side', 'pickextra', 'xcpickown']
    for flag in capt_flags:
        tester.test_rule(f'bdiv_nocapt_{flag}',
            rule=divert_and(flag),
            msg='SOW_BLKD_DIV(_NR) closes holes to remove seeds from play, '
                f'no other capture mechanisms are allowed [{flag.upper()}]',
        excp=gi.GameInfoError)

    tester.test_rule('bdiv_no_capt_on',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and any(ginfo.capt_on)),
        msg='SOW_BLKD_DIV(_NR) closes holes to remove seeds from play, ' + \
            'no other capture mechanisms are allowed [CAPT_ON]',
        excp=gi.GameInfoError)

    bad_flags = ['allow_rule', 'sow_start']
    for flag in bad_flags:
        tester.test_rule(f'bdiv_bad_{flag}',
            rule=divert_and(flag),
            msg=f'sow_blkd_div is incompatible with {flag.upper()}',
            excp=gi.GameInfoError)

    bad_flags = ['skip_start']
    for flag in bad_flags:
        tester.test_rule(f'bdiv_not_{flag}',
            rule=divert_and(flag),
            msg=f'sow_blkd_div is not supported with {flag.upper()}',
            excp=NotImplementedError)
    # sower doesn't use incrementer which implements skip_start


def test_child_rules(tester):
    """Add rules specific to having children."""

    tester.test_rule('child_need_cvt',
        rule=lambda ginfo: (ginfo.child_type.child_but_not_ram()
                            and ginfo.child_locs
                                    != gi.ChildLocs.FIXED_ONE_RIGHT
                            and not ginfo.child_cvt),
        msg='Selected child type requires CHILD_CVT',
        excp=gi.GameInfoError)

    tester.test_rule('dont_need_cvt',
        rule=lambda ginfo: (ginfo.child_type
                            and ginfo.child_locs
                                    == gi.ChildLocs.FIXED_ONE_RIGHT
                            and ginfo.child_cvt),
        msg='CHILD_CVT is ignored with Child Locs of FIXED_ONE_RIGHT',
        warn=True)

    tester.test_rule('child_cvt_need_type',
        rule=lambda ginfo: not ginfo.child_type and ginfo.child_cvt,
        msg='CHILD_CVT requires a CHILD_TYPE != NOCHILD',
        excp=gi.GameInfoError)

    tester.test_rule('child_no_gs',
        rule=lambda ginfo: (ginfo.child_type
                            and ginfo.grandslam not in (gi.GrandSlam.LEGAL,
                                                        gi.GrandSlam.NOT_LEGAL)),
        msg='Children requires that GRANDSLAM be LEGAL or NOT_LEGAL',
        excp=NotImplementedError)
        # children are not checked in GrandSlamCapt.is_grandslam

    tester.test_rule('ch_rule_own_incom',
        rule=lambda ginfo: (ginfo.goal != gi.Goal.TERRITORY
                            and ginfo.child_rule in (gi.ChildRule.OPP_OWNER_ONLY,
                                                     gi.ChildRule.OWN_OWNER_ONLY)),
        msg='CHILD_RULE: *_OWNER_ONLY requires territory GOAL',
        excp=gi.GameInfoError)

    tester.test_rule('no_sow_child_req',
        rule=lambda ginfo: (not ginfo.child_type
                            and ginfo.sow_rule in (gi.SowRule.NO_OPP_CHILD,
                                                   gi.SowRule.NO_CHILDREN)),
        msg='Sow rule requires children',
        excp=gi.GameInfoError)

    tester.test_rule('not1st_static',
        rule=lambda ginfo: (ginfo.child_rule == gi.ChildRule.NOT_1ST_OPP
                            and (ginfo.blocks
                                 or ginfo.goal == gi.Goal.TERRITORY)),
        msg='ChildRule NOT_1ST_OPP not supported with blocks or territory games',
        excp=NotImplementedError)
        # code assumes 1st's are specific holes
        # complexity of 'current' 1st opposite hole is not implemented
        # for reference: sow own store does have this complexity

    tester.test_rule('ram_no_blocks',
        rule=lambda ginfo: (ginfo.child_type == gi.ChildType.RAM
                            and ginfo.blocks),
        msg='BLOCKS are not supported with ChildType RAM',
        excp=NotImplementedError)
        # would require simulating the moves

    tester.test_rule('ram_basic_sow',
        rule=lambda ginfo: (ginfo.child_type == gi.ChildType.RAM
                            and ginfo.sow_direct not in (gi.Direct.CW,
                                                         gi.Direct.CCW)),
        msg='Only SOW_DIRECT CW and CCW are supported with ChildType RAM',
        excp=NotImplementedError)

    tester.test_rule('ram_stores',
        rule=lambda ginfo: (ginfo.child_type == gi.ChildType.RAM
                            and not ginfo.stores),
        msg='ChildType RAM requires STORES',
        excp=gi.GameInfoError)
        # do not want collect captures into RAMs


def test_no_sides_rules(tester):
    """Add the no_sides rules."""

    def no_sides_and(flag_name):
        """Return a function that tests no_sides and the specified
        flag, based only on a ginfo parameter."""

        def _no_sides_and(ginfo):
            return ginfo.no_sides and getattr(ginfo, flag_name)

        return _no_sides_and

    tester.test_rule('no_sides_need_place',
        rule=lambda ginfo: (not ginfo.goal.eliminate()
                            and ginfo.no_sides
                            and not (ginfo.stores or ginfo.child_type)),
        msg='MAX_SEEDS game with NO_SIDES requires STORES or CHILDREN',
        excp=gi.GameInfoError)

    bad_flags = ['grandslam', 'mustpass', 'mustshare', 'blocks',
                 'round_fill']
    for flag in bad_flags:
        tester.test_rule(f'no_sides_bad_{flag}',
            rule=no_sides_and(flag),
            msg=f'NO_SIDES cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)

    tester.test_rule('no_sides_rtally_only',
        rule=lambda ginfo: (ginfo.no_sides
                            and ginfo.rounds
                            and ginfo.goal not in round_tally.RoundTally.GOALS),
        msg="The specified goal cannot be used with NO_SIDES and ROUNDS.",
        excp=gi.GameInfoError)
        # rounds that hole allocations are incompatible with no_sides

    # generate some warnings of things that might go bad

    tester.test_rule('no_sides_no_stores_warn',
        rule=lambda ginfo: ginfo.no_sides and not ginfo.stores,
        msg="NO_SIDES without STORES should have different colors " \
            + "configured for each player (mancala.ini cannot be checked yet)",
        warn=rule_tester.PRINT_MSG)
        # there is no other way to know whose turn it is
        # cannot test the config file (get circular dependencies)

    tester.test_rule('no_sides_side_warn',
        rule=lambda ginfo: ginfo.no_sides and ginfo.capt_side,
        msg="CAPT_SIDES with NO_SIDES might behave unexpectedly " \
            + "in non-north/south games",
        warn=rule_tester.PRINT_MSG)
        # there is no other way to know whose turn it is


def test_sower_rules(tester):
    """Test the sower rules."""

    tester.test_rule('srule_lapper',
        rule=lambda ginfo: (ginfo.sow_rule in (gi.SowRule.CHANGE_DIR_LAP,
                                               gi.SowRule.LAP_CAPT,
                                               gi.SowRule.LAP_CAPT_OPP_GETS,
                                               gi.SowRule.LAP_CAPT_SEEDS)
                            and not ginfo.mlaps),
        msg="""Selected sow rule requires multi-lap sowing""",
        excp=gi.GameInfoError)

    tester.test_rule('mlap_cont',
        rule=lambda ginfo: ginfo.mlap_cont and not ginfo.mlaps,
        msg="""Lap continue reasons requires multi-lap sowing""",
        excp=gi.GameInfoError)

    tester.test_rule('mlap_param',
        rule=lambda ginfo: (ginfo.mlap_cont in (gi.SowLapCont.ON_PARAM,
                                                gi.SowLapCont.GREQ_PARAM)
                                and not ginfo.mlap_param),
        msg="""Selected MLAP_CONT requires MLAP_PARAM""",
        excp=gi.GameInfoError)

    tester.test_rule('mlap_sown',
        rule=lambda ginfo: (ginfo.mlap_cont in (gi.SowLapCont.STOP_STORE,
                                                gi.SowLapCont.NOT_FROM_STORE)
                                and not ginfo.sow_stores),
        msg="""Selected MLAP_CONT requires SOW_STORES""",
        excp=gi.GameInfoError)


    tester.test_rule('sow_own_not_rules',
        rule=lambda ginfo: (ginfo.sow_stores
                            and ginfo.sow_rule not in
                                (gi.SowRule.NONE,
                                 gi.SowRule.NO_SOW_OPP_NS,
                                 gi.SowRule.CHANGE_DIR_LAP,
                                 gi.SowRule.MAX_SOW,
                                 gi.SowRule.LAP_CAPT,
                                 gi.SowRule.NO_OPP_CHILD,
                                 gi.SowRule.LAP_CAPT_SEEDS,
                                 gi.SowRule.NO_CHILDREN)),
        msg='SOW_STORES is not supported with the selected sow rule',
        excp=NotImplementedError)

    tester.test_rule('sow_own_prescribed',
        rule=lambda ginfo: (ginfo.sow_stores
                            and ginfo.prescribed in
                                (gi.SowPrescribed.BASIC_SOWER,
                                 gi.SowPrescribed.MLAPS_SOWER,
                                 gi.SowPrescribed.SOW1OPP,
                                 gi.SowPrescribed.PLUS1MINUS1)
                            ),
        msg='SOW_STORES is ignored for the selected first prescribed sow',
        warn=True)

    tester.test_rule('nu1st_cw_ccw',
        rule=lambda ginfo: (ginfo.prescribed == gi.SowPrescribed.NO_UDIR_FIRSTS
                            and ginfo.sow_direct not in (gi.Direct.CCW,
                                                         gi.Direct.CW)),
        msg="""Prescribed sow of NO_UDIR_FIRSTS requires SOW_DIRECT
        be CW or CCW""",
        warn=gi.GameInfoError)



def test_capture_rules(tester):
    """Most of the capture rules are added here."""

    tester.test_rule('warn_no_capt',
        rule=lambda ginfo: not any([sow_blkd_div(ginfo),
                                    ginfo.child_type,
                                    ginfo.capt_type,
                                    ginfo.evens,
                                    ginfo.crosscapt,
                                    ginfo.sow_stores,
                                    ginfo.capt_max,
                                    ginfo.capt_min,
                                    ginfo.capt_on,
                                    ginfo.presowcapt]),
        msg='No capture mechanism provided',
        warn=True)

    tester.test_rule('capt_no_place',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.MAX_SEEDS, gi.Goal.TERRITORY)
                            and not (ginfo.stores
                                     or ginfo.child_type.child_but_not_ram())
                            and any([ginfo.capt_type,
                                     ginfo.evens,
                                     ginfo.crosscapt,
                                     ginfo.capt_max,
                                     ginfo.capt_min,
                                     ginfo.capt_on,
                                     ginfo.presowcapt])),
        msg="""The game has captures configured but there is no place
            to put captured seeds. Suggest stores or children be used""",
        warn=True)

    tester.test_rule('capt_conflict',
        rule=lambda ginfo: any(
            [(ginfo.capt_min and ginfo.capt_max
                  and ginfo.capt_min > ginfo.capt_max),
             (ginfo.capt_on and ginfo.evens
                  and all(cval % 2 == 1 for cval in ginfo.capt_on)),
             (ginfo.capt_min and ginfo.capt_on
                  and max(ginfo.capt_on) < ginfo.capt_min),
             (ginfo.capt_max and ginfo.capt_on
                  and min(ginfo.capt_on) > ginfo.capt_max),
              ]),
        msg='Selected capture mechanisms conflict (no captures)',
        warn=True)
        # this doesn't catch all conflicts :(

    tester.test_rule('xcapt_multi_same',
        rule=lambda ginfo: (ginfo.crosscapt == gi.XCaptType.ONE_ZEROS
                            and ginfo.multicapt
                            and ginfo.capt_dir != gi.CaptDir.SOW),
        msg="""CROSSCAPT ONE_ZEROS with MULTICAPT requires CAPT_DIR
            be SOW""",
        excp=gi.GameInfoError)
        # capturing the opp dir (as usual) wont capture because
        # the preceeding holes were just sown, that is, not empty

    tester.test_rule('xcapt_any_uncond',
        rule=lambda ginfo: (ginfo.crosscapt == gi.XCaptType.ANY
                            and ginfo.multicapt
                            and not ginfo.basic_capt),
        msg="""Unconstrained cross capture type of ANY use basic capture""",
        excp=gi.GameInfoError)
        # all seeds on the opposite side from the final hole will be captured

    tester.test_rule('capt2out_needs_samedir',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.TWO_OUT
                            and ginfo.capt_dir != gi.CaptDir.SOW),
        msg="""Capture type TWO_OUT requires CAPT_DIR of SOW because
            the preceeding holes were just sown (not empty)""",
        excp=gi.GameInfoError)

    tester.test_rule('cdir_both_multicapt',
        rule=lambda ginfo: (ginfo.capt_dir == gi.CaptDir.BOTH
                            and not ginfo.multicapt),
        msg="""CAPT_DIR of BOTH requires MULTICAPT""",
        excp=gi.GameInfoError)
        # CaptBothDir needs to decorate CaptMultiple

    tester.test_rule('cdir_both_ctypes',
        rule=lambda ginfo: (
            ginfo.capt_dir == gi.CaptDir.BOTH
            and not (ginfo.capt_type in (gi.CaptType.NEXT,
                                         gi.CaptType.MATCH_OPP)
                     or (ginfo.basic_capt and not ginfo.crosscapt))),
        msg="""CAPT_DIR of BOTH is only supported for basic captures,
            NEXT and match opposite types.""",
        excp=gi.GameInfoError)

    tester.test_rule('both_mlaps_next',
        rule=lambda ginfo: (ginfo.capt_dir == gi.CaptDir.BOTH
                            and ginfo.multicapt
                            and ginfo.capt_type == gi.CaptType.NEXT
                            and ginfo.mlaps),
        msg="""CAPT_DIR of BOTH is not supported with MLAPS sowing
            and capture type NEXT.""",
        excp=gi.GameInfoError)
        # the capture behavior is odd because any basic capture
        # criteria are used to stop the mlap sowing, but wo basic
        # capture criteria all holes would be captured

    tester.test_rule('lcapt_no_ctype',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT
                            and ginfo.capt_type not in (gi.CaptType.NONE,
                                                        gi.CaptType.TWO_OUT,
                                                        gi.CaptType.NEXT)),
        msg="""LAP_CAPT is only supported for basic captures,
            cross capture, capt two out, and capt next""",
        excp=NotImplementedError)
        # currently only MATCH_OPP is not supported

    tester.test_rule('ogol_no_ctype',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_OPP_GETS
                            and ginfo.capt_type not in (gi.CaptType.NONE,
                                                        gi.CaptType.TWO_OUT,
                                                        gi.CaptType.NEXT)),
        msg="""LAP_CAPT_OPP_GETS is only supported for basic captures,
            cross capture, capt two out, and capt next""",
        excp=NotImplementedError)
        # see lcapt_no_ctype

    tester.test_rule('opp1ccw_noterr',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.CAPT_OPP_1CCW
                            and ginfo.goal == gi.Goal.TERRITORY),
        msg="CAPT_TYPE of CAPT_OPP_1CWW is not supported for TERRITORY games",
        excp=NotImplementedError)

    tester.test_rule('opp1ccw_noblcks',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.CAPT_OPP_1CCW
                            and ginfo.blocks),
        msg="CAPT_TYPE of CAPT_OPP_1CWW does not adjust for blocked holes",
        warn=True)

    tester.test_rule('lcs_presow_capt',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_SEEDS
                            and ginfo.presowcapt),
        msg="LAP_CAPT_SEEDS with PRESOWCAPT isn't supported",
        excp=NotImplementedError)
        # presow capture could be supported, but ContWithCaptSeeds
        # would need to only move the newly captured seeds into play
        # it currently moves all captured seeds into play

    tester.test_rule('lcs_stores',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_SEEDS
                            and ginfo.stores),
        msg="""LAP_CAPT_SEEDS with STORES isn't supported""",
        excp=NotImplementedError)
        # any seeds put into the stores are moved back into play
        # on the next capture and lap

    tester.test_rule('lcs_collect',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_SEEDS
                            and not (ginfo.capt_type or ginfo.crosscapt)),
        msg="""LAP_CAPT_SEEDS is only supported when seeds are
            captured from holes in addition to final hole sown""",
        excp=gi.GameInfoError)
        # don't lap_capt_seeds if we are not capturing seeds from some
        # place other than the end hole, it does nothing useful

    tester.test_rule('lcs_ctype_warn',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_SEEDS
                            and ginfo.capt_type
                            and ginfo.capt_type in (gi.CaptType.NEXT,
                                                    gi.CaptType.SINGLETONS)),
        msg="""LAP_CAPT_SEEDS with selected capture type will generally
            end result in an ENDLESS sows. Suggest turning on Disallow
            Endless Sow. Using a start pattern, prescribed sow, or other
            option could prevent this.""",
        warn=True)

    tester.test_rule('sca_gs_not',
        rule=lambda ginfo: (ginfo.sow_rule in (gi.SowRule.OWN_SOW_CAPT_ALL,
                                               gi.SowRule.SOW_CAPT_ALL)
                            and ginfo.grandslam != gi.GrandSlam.LEGAL),
        msg='(OWN_)SOW_CAPT_ALL requires that GRANDLAM be LEGAL',
        excp=gi.GameInfoError)

    tester.test_rule('xpick_requires_cross',
        rule=lambda ginfo: ginfo.xcpickown and not ginfo.crosscapt,
        msg="XCPICKOWN without CROSSCAPT doesn't do anything",
        excp=gi.GameInfoError)

    tester.test_rule('xc_const_pickextra',
        rule=lambda ginfo: (ginfo.crosscapt
                            and ginfo.basic_capt
                            and ginfo.pickextra == gi.CaptExtraPick.PICKCROSS),
        msg="""A constrainted CROSSCAPT with PICKEXTRA=PICKCROSS will
            ingnore the constraint""",
        excp=gi.GameInfoError)

    tester.test_rule('xpick_pickcross',
        rule=lambda ginfo: (ginfo.crosscapt
                            and ginfo.pickextra == gi.CaptExtraPick.PICKCROSS),
        msg="PICKEXTRA=PICKCROSS with CROSSCAPT is redundant",
        warn=True)

    tester.test_rule('xcross_all_nlaps',
        rule=lambda ginfo: (ginfo.crosscapt == gi.XCaptType.ANY
                            and ginfo.mlaps),
        msg="MLAPS sowing is not supported CROSSCAPT of ANY",
        excp=NotImplementedError)
        # the stop on capture (lap continuer) decos were not written

    tester.test_rule('moveall_no_locks',
        rule=lambda ginfo: (ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST
                            and ginfo.moveunlock),
        msg="""Do not set MOVEUNLOCK with MOVE_ALL_HOLES_FIRST.
            Locks are automatically used to limit first moves but not captures""",
        excp=gi.GameInfoError)
        # we do not want CaptUnlocked added to the capt_basic deco
        # which causes captures to be limited by locks

    tester.test_rule('moveall_no_capttype',
        rule=lambda ginfo: (ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST
                            and ginfo.capt_type == gi.CaptType.TWO_OUT),
        msg='MOVE_ALL_HOLES_FIRST is incompatible with CAPT_TYPE TWO_OUT',
        excp=gi.GameInfoError)
        # decos use capt_check and not capt_basic

    tester.test_rule('moveall_no_picker',
        rule=lambda ginfo: (ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST
                            and (ginfo.xcpickown or ginfo.pickextra)),
        msg='MOVE_ALL_HOLES_FIRST is incompatible with all pickers',
        excp=gi.GameInfoError)
        # the pickers check the locks directly
        # an alternate approach could be to not check any locks on pickers
        # locks are rarely used

    tester.test_rule('pcm_multi',
        rule=lambda ginfo: (ginfo.pickextra == gi.CaptExtraPick.PICKCROSSMULT
                            and not ginfo.multicapt),
        msg='PICKCROSSMULT does nothing without MULICAPT',
        excp=gi.GameInfoError)

    tester.test_rule('scont_mcapt',
        rule=lambda ginfo: (ginfo.capt_side in (gi.CaptSide.OWN_CONT,
                                                gi.CaptSide.OPP_CONT)
                            and not ginfo.multicapt),
        msg='CAPT_SIDE *_CONT requires multicapt',
        excp=gi.GameInfoError)

    tester.test_rule('capt2out_cside',
        rule=lambda ginfo: (ginfo.capt_side
                            and ginfo.capt_type == gi.CaptType.TWO_OUT),
        msg='Capture TWO_OUT cannot be used with CAPT_SIDE other than BOTH',
        excp=gi.GameInfoError)

    tester.test_rule('singles_no_mult',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.SINGLETONS
                            and ginfo.multicapt),
        msg='Multiple captures with capture SINGLETONS is not supported',
        excp=gi.GameInfoError)

    tester.test_rule('str_capt_stores',
        rule=lambda ginfo: (ginfo.capt_type in (gi.CaptType.PASS_STORE_CAPT,
                                                gi.CaptType.END_OPP_STORE_CAPT)
                            and not ginfo.stores),
        msg='Store capturing (selected CAPT_TYPE) requires stores',
        excp=gi.GameInfoError)

    tester.test_rule('str_capt_single',
        rule=lambda ginfo: (ginfo.capt_type in (gi.CaptType.PASS_STORE_CAPT,
                                                gi.CaptType.END_OPP_STORE_CAPT)
                            and ginfo.multicapt),
        msg="""Multiple captures is incompatible with store captures
            (selected CAPT_TYPE)""",
        excp=gi.GameInfoError)
        # this could potentially be supported for the basic/xcapt, but
        # the supporting capt deco would need to be above CaptMultiple

    tester.test_rule('pacross_same_dir',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.PULL_ACROSS
                            and ginfo.multicapt
                            and ginfo.capt_dir != gi.CaptDir.SOW),
        msg='PULL_ACROSS with multiple capture requires CAPT_DIR be SOW',
        excp=gi.GameInfoError)

    tester.test_rule('end_opp_both',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.END_OPP_STORE_CAPT
                            and ginfo.sow_stores not in (gi.SowStores.BOTH_NR,
                                                         gi.SowStores.BOTH_NR_OPP)),
        msg="""END_OPP_STORE_CAPT requires that both stores be sown
            and there is no repeat turn when ending in opposite store""",
        excp=gi.GameInfoError)


def test_basic_rules(tester):
    """Test the basic set fo rules"""

    tester.test_rule('allowrule_mlen3',
        rule=lambda ginfo: (ginfo.mlength == 3
                            and ginfo.allow_rule in
                                {gi.AllowRule.TWO_ONLY_ALL_RIGHT,
                                 gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                 gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO,
                                 gi.AllowRule.NOT_XFROM_1S,
                                 gi.AllowRule.RIGHT_HALF_FIRSTS,
                                 gi.AllowRule.RIGHT_HALF_1ST_OPE}),
        msg='Selected allow rule not supported for MLENGTH 3 games',
        excp=gi.GameInfoError)

    tester.test_rule('opp_empty_no_tuples',
        rule=lambda ginfo: (ginfo.allow_rule in (gi.AllowRule.OPP_OR_EMPTY,
                                                  gi.AllowRule.RIGHT_HALF_1ST_OPE)
                            and ginfo.mlength > 1),
        msg='MLENGTH > 1 not supported with OPP_OR_EMPTY',
        excp=gi.GameInfoError)
        # UDIRECT: could be supported but it isn't implemented
        # TERRITORY: what does it mean if the hole is already opp?

    tester.test_rule('no_pres_opp_empty',
        rule=lambda ginfo: (ginfo.prescribed != gi.SowPrescribed.NONE
                            and ginfo.allow_rule == gi.AllowRule.OPP_OR_EMPTY),
        msg='Prescribed moves not supported with OPP_OR_EMPTY',
        excp=gi.GameInfoError)
        # don't know how to get the single_sower from a prescribed sow,
        # the don't have to follow a prescribed (pun intended) sow structure
        # RIGHT_HALF_1ST_OPE can use prescribed sow because it doesn't
        # overlap with use of OPP_OR_EMPTY

    tester.test_rule('sow_own_needs_stores',
        rule=lambda ginfo: ginfo.sow_stores and not ginfo.stores,
        msg='SOW_STORES requires STORES',
        excp=gi.GameInfoError)

    tester.test_rule('plocs_stores',
        rule=lambda ginfo: ginfo.play_locs and not ginfo.stores,
        msg='No stores available for PLAY_LOC',
        excp=gi.GameInfoError)

    tester.test_rule('plocs_direct',
        rule=lambda ginfo: (ginfo.play_locs
                            and ginfo.sow_direct not in (gi.Direct.CCW,
                                                         gi.Direct.CW)),
        msg="Selected PLAY_LOC requires sow direction be CW or CCW",
        excp=gi.GameInfoError)
        # probably could support, but then would need grids and it
        # would be more turns for the AI player's to search

    tester.test_rule('mlap_cont_store',
        rule=lambda ginfo: (ginfo.mlap_cont == gi.SowLapCont.STOP_STORE
                            and not ginfo.sow_stores),
        msg="""MLAP_CONT STOP_STORE requires sowing stores""",
        excp=gi.GameInfoError)

    tester.test_rule('sow_own_nocapt',
        rule=lambda ginfo: ginfo.sow_stores and ginfo.nocaptmoves,
        msg='SOW_STORES cannot be used with NOCAPTMOVES',
        excp=gi.GameInfoError)

    tester.test_rule('no_opp_n_sparam',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.NO_SOW_OPP_NS
                            and not ginfo.sow_param),
        msg='NO_SOW_OPP_NS requires sow_param',
        excp=gi.GameInfoError)

    tester.test_rule('max_sow_param',
        rule=lambda ginfo: (not ginfo.sow_param
                            and ginfo.sow_rule == gi.SowRule.MAX_SOW),
        msg='Sow rule MAX_SOW requires that sow_param be greater than 0',
        excp=gi.GameInfoError)

    tester.test_rule('lcapt_no_lnext',
        rule=lambda ginfo: (ginfo.sow_rule in (gi.SowRule.LAP_CAPT,
                                               gi.SowRule.LAP_CAPT_OPP_GETS,
                                               gi.SowRule.LAP_CAPT_SEEDS)
                            and ginfo.mlaps == gi.LapSower.LAPPER_NEXT),
        msg="""SOW_RULE LAP_CAPT and variants are not supported
            with LAPPER_NEXT""",
        excp=NotImplementedError)
        # would need to carefully decide how it would work

    tester.test_rule('sow_start_skip_incomp',
        rule=lambda ginfo: ginfo.sow_start and ginfo.skip_start,
        msg='SOW_START and SKIP_START do not make sense together',
        excp=gi.GameInfoError)

    tester.test_rule('blocks_wo_rounds',
        rule=lambda ginfo: (ginfo.blocks
                            and not sow_blkd_div(ginfo)
                            and not ginfo.rounds),
        msg='BLOCKS without ROUNDS or SOW_BLKD_DIV(_NR) does nothing',
        warn=True)

    tester.test_rule('rstarter_wo_rounds',
        rule=lambda ginfo: not ginfo.rounds
            and ginfo.round_starter != gi.RoundStarter.ALTERNATE,
        msg='ROUND_STARTER requires ROUNDS',
        excp=gi.GameInfoError)

    tester.test_rule('dupl_seeds_limits',
        rule=lambda ginfo: (ginfo.rounds in (gi.Rounds.END_S_SEEDS,
                                             gi.Rounds.END_2S_SEEDS)
                            and ginfo.end_cond == gi.EndGameCond.SEEDS_LIMIT),
        msg="""ROUNDS of END_S_SEEDS or END_2S_SEEDS
            cannot be used with END_COND SEEDS_LIMIT""",
        excp=gi.GameInfoError)

    tester.test_rule('mx_round_limit',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.rounds
                                   and ginfo.goal == gi.Goal.MAX_SEEDS
                                   and ginfo.goal_param > holes),
        msg="""Minimum holes needed to play another round must be
            less the holes per side""",
        excp=gi.GameInfoError)

    tester.test_rule('rnd_goals_rounds',
        rule=lambda ginfo: (ginfo.goal in round_tally.RoundTally.GOALS
                            and not ginfo.rounds),
        msg='RND_* goal requires game be played in rounds',
        excp=gi.GameInfoError)

    tester.test_rule('rnd_goals_gp1',
        rule=lambda ginfo: (ginfo.goal in round_tally.RoundTally.GOALS
                            and ginfo.goal_param <= 0),
        msg="""RND_* goal requires GOAL_PARAM be greater than 0 to
            define win condition""",
        excp=gi.GameInfoError)

    tester.test_rule('rnd_goals_no_fill',
        rule=lambda ginfo: (ginfo.goal in round_tally.RoundTally.GOALS
                            and ginfo.round_fill),
        msg='RND_* goal does not use round_fill',
        excp=gi.GameInfoError)

    tester.test_rule('move_one_start',
        rule=lambda ginfo: ginfo.move_one and not ginfo.sow_start,
        msg='MOVE_ONE requires SOW_START',
        excp=gi.GameInfoError)

    tester.test_rule('xc_draw1_sowstart',
        rule=lambda ginfo: (ginfo.presowcapt == gi.PreSowCapt.DRAW_1_XCAPT
                            and ginfo.sow_start),
        msg="""DRAW_1_XCAPT with SOW_START will capture when start hole
            has 2 seeds (1 is drawn)""",
        warn=True)

    tester.test_rule('presowcap_stores',
        rule=lambda ginfo: (ginfo.presowcapt
                            and not ginfo.stores and ginfo.child_type),
        msg="""PRESOWCAPT to children is not supported
            (not STORES and CHILD_TYPE)""",
        excp=NotImplementedError)
        # logic to prevent captures before children and moving seeds
        # out of stores back onto the board while not moving seeds
        # that are out of play for the round is not implemented

    tester.test_rule('presowcapt_locks',
        rule=lambda ginfo: ginfo.presowcapt and ginfo.moveunlock,
        msg='PRESOWCAPTs are not supported with MOVEUNLOCK',
        excp=gi.GameInfoError)
        # locks have two purposes: don't capt from locks and moveall first
        # see no need to make these compatible with presowcapt

    tester.test_rule('needs_moves',
        rule=lambda ginfo: (ginfo.min_move == 1
                            and ginfo.sow_start
                            and not ginfo.move_one),
        msg='MIN_MOVE of 1 with SOW_START play is confusing (unless MOVE_ONE)',
        excp=gi.GameInfoError)
        # pick-up a seed, sow it back into the same hole -> no change of state

    tester.test_rule('mmg1_mustshare',
        rule=lambda ginfo: ginfo.min_move > 1 and ginfo.mustshare,
        msg='Shared seeds from MUSTSHARE might not be playable with min_move > 1',
        warn=rule_tester.PRINT_MSG)

    tester.test_rule('rnd_score_setup',
        rule=lambda ginfo: (ginfo.rounds
                            and ginfo.goal not in round_tally.RoundTally.GOALS
                            and gi.EndGameSeeds.DONT_SCORE in (ginfo.unclaimed,
                                                               ginfo.quitter)),
        msg="""Games which use scored seeds to set up the next round
             cannot use DONT_SCORE""",
        excp=gi.GameInfoError)

    tester.test_rule('unfed_mustshare',
        rule=lambda ginfo: (ginfo.unclaimed == gi.EndGameSeeds.UNFED_PLAYER
                            and not ginfo.mustshare),
        msg='EndGameSeeds UNFED_PLAYER cannot be used without MUSTSHARE',
        excp=gi.GameInfoError)

    tester.test_rule('unfed_quitter',
        rule=lambda ginfo: ginfo.quitter == gi.EndGameSeeds.UNFED_PLAYER,
        msg="""EndGameSeeds UNFED_PLAYER should not be used as a QUITTER
            (DIVVIED will be used)""",
        warn=True)

    tester.test_rule('p1m1_conflict',
        rule=lambda ginfo: (ginfo.prescribed == gi.SowPrescribed.PLUS1MINUS1
                            and (ginfo.sow_start or ginfo.move_one)),
        msg='PLUS1MINUS1 is incompatible with SOW_START and/or MOVE_ONE',
        excp=gi.GameInfoError)

    tester.test_rule('too_many_udir',
        both_objs=True,
        rule=lambda ginfo, holes: len(ginfo.udir_holes) > holes,
        msg='Too many udir_holes specified',
        excp=gi.GameInfoError)

    tester.test_rule('udir_oo_range',
        both_objs=True,
        rule=lambda ginfo, holes: any(udir < 0 or udir >= holes
                                      for udir in ginfo.udir_holes),
        msg='Udir_holes value out of range 0..nbr_holes-1',
        excp=gi.GameInfoError)

    tester.test_rule('udir_gs_not',
        rule=lambda ginfo: (ginfo.udirect and
                            ginfo.grandslam == gi.GrandSlam.NOT_LEGAL),
        msg='UDIR_HOLES and GRANDLAM=Not Legal are incompatible',
        excp=NotImplementedError)
        # no games use these two features together,
        # implement when there's a use

    tester.test_rule('udir_bad_allowrule',
        rule=lambda ginfo: (ginfo.allow_rule not in  {
                                  gi.AllowRule.NONE,
                                  gi.AllowRule.SINGLE_ONLY_ALL,
                                  gi.AllowRule.TWO_ONLY_ALL,
                                  gi.AllowRule.TWO_ONLY_ALL_RIGHT,
                                  gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                  gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO,
                                  gi.AllowRule.MOVE_ALL_HOLES_FIRST,
                                  gi.AllowRule.NOT_XFROM_1S,
                                  gi.AllowRule.RIGHT_HALF_FIRSTS}
                             and ginfo.udirect),
        msg='UDIR_HOLES and ALLOW_RULE are incompatible',
        excp=NotImplementedError)
        # allow rules which do not depend on sow direction are fine
        # listing those so new allow rules are excluded with code changes

    tester.test_rule('odd_split_udir',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.sow_direct in (gi.Direct.SPLIT,
                                                        gi.Direct.TOCENTER)
                                   and holes % 2
                                   and holes // 2 not in ginfo.udir_holes),
        msg="""SPLIT or TOCENTER with odd number of holes,
            but center hole not listed in udir_holes""",
        excp=gi.GameInfoError)

    tester.test_rule('sdir_split',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.udirect
                                   and len(ginfo.udir_holes) != holes
                                   and ginfo.sow_direct
                                           not in (gi.Direct.SPLIT,
                                                   gi.Direct.TOCENTER)),
        msg= 'Odd choice of sow direction when udir_holes != nbr_holes',
        warn=True)

    tester.test_rule('gs_not_legal_no_tuple',
        rule=lambda ginfo: (ginfo.mlength > 1 and
                            ginfo.grandslam == gi.GrandSlam.NOT_LEGAL),
        msg='MLENGTH > 1 and GRANDLAM = Not Legal is not supported',
        excp=gi.GameInfoError)
        # GS allowables doesn't support tuples
        # UDIRECT: partials hole activation not supported
        # TERRITORY: partial side ownership is not implemented

    tester.test_rule('need_end_param',
        rule=lambda ginfo: (ginfo.end_cond in (gi.EndGameCond.SEEDS_LIMIT,
                                               gi.EndGameCond.HOLE_SEED_LIMIT)
                            and not ginfo.end_param),
        msg="""Selected END_COND requires positive END_PARAM""",
        excp=gi.GameInfoError)

    tester.test_rule('clear_no_pass',
        rule=lambda ginfo: (ginfo.mustpass
                            and ginfo.end_cond in (gi.EndGameCond.CLEARED_OPP,
                                                   gi.EndGameCond.CLEARED_OWN)),
        msg="""MUSTPASS incompatible with END_COND CLEARED OPP or OWN""",
        excp=gi.GameInfoError)


def test_round_fill(tester):
    """Test rules related to round fill."""

    tester.test_rule('short_no_blocks',
        rule=lambda ginfo: (ginfo.round_fill in (gi.RoundFill.SHORTEN,
                                                 gi.RoundFill.SHORTEN_ALL)
                            and not ginfo.blocks),
        msg='RoundFill SHORTEN without BLOCKS, yields an odd game dynamic',
        warn=True)

    def round_loser_and(flag_name):
        """Return a function that tests round_loser and the specified
        flag, based only on a ginfo parameter."""

        def _round_loser_and(ginfo):
            return (ginfo.round_fill == gi.RoundFill.LOSER_ONLY
                    and getattr(ginfo, flag_name))

        return _round_loser_and

    bad_loser_only = ['child_type', 'no_sides', 'moveunlock']
    for opt in bad_loser_only:
        tester.test_rule(f'rfl_bad_{opt}',
                         rule=round_loser_and(opt),
                         msg=f"""RoundFill LOSER_ONLY is incompatible with
                         {opt}""",
                         excp=gi.GameInfoError)
        # new_game.NewRoundLoserOnly does not change any of these
        # for the winner or loser

    tester.test_rule('rfl_owner',
        rule=lambda ginfo: (ginfo.round_fill == gi.RoundFill.LOSER_ONLY
                            and (ginfo.unclaimed or ginfo.quitter)),
        msg="""RoundFill LOSER_ONLY requires both UNCLAIMED and QUITTER
             be HOLE_OWNER""",
        excp=gi.GameInfoError)
        # nothing else makes sense if we are not going to change the
        # winner's side of the board

    tester.test_rule('pick_rend_agree',
        rule=lambda ginfo: (
            ginfo.rounds in (gi.Rounds.END_S_SEEDS,
                             gi.Rounds.END_2S_SEEDS)
            and ginfo.pickextra in (gi.CaptExtraPick.PICKLASTSEEDS,
                                    gi.CaptExtraPick.PICK2XLASTSEEDS)
            and ginfo.rounds != ginfo.pickextra),
        msg="""Pick extra and round end condition must agree
            on number of seeds (seeds or 2x seeds)""",
        excp=gi.GameInfoError)
        # if the picker is included, the round ender is not; so they must agree


# %% the base ruleset

def test_rules(ginfo, holes, skip=None):
    """Test the default Mancala rules.
    These can be deleted or modified by derived classes."""

    tester = rule_tester.RuleTester(ginfo, holes, skip)

    test_creation_rules(tester)
    test_pattern_rules(tester)
    test_eliminate_goal_rules(tester)
    test_territory_rules(tester)
    test_block_and_divert_rules(tester)
    test_child_rules(tester)
    test_no_sides_rules(tester)
    test_round_fill(tester)
    test_sower_rules(tester)
    test_capture_rules(tester)
    test_basic_rules(tester)
