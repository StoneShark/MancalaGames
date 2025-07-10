# -*- coding: utf-8 -*-
"""Build the sower deco chain to preform the seed sowing
step, that is, increment around the game board, dropping
one seed into each hole.

Any 'soft' direction (e.g. split, user choice) has already been
translated to clockwise or counter-clockwise (i.e. CW or CCW).
The sow_starter deco chain has already adjusted the start hole
contents and determined the number of seeds to sow.

Created on Fri Apr  7 15:57:47 2023
@author: Ann"""

import animator
import game_info as gi
import sower_decos as sowd
import sower_mlap_decos as msowd


def _add_blkd_divert_sower(game):
    """Implement the sow_blkd_div sower.
    When sowing seeds, blocked holes on own side of the board are
    skipped and seeds for blocked opponent holes are diverted out
    of play (actually store 0)."""

    sower = sowd.DivertSkipBlckdSower(game)
    if game.info.mlaps == gi.LapSower.OFF:
        sower = sowd.SowClosed(game,
                               game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV_NR,
                               sower)
    return sower


def _add_base_sower(game):
    """Choose the base sower."""
    # pylint: disable=too-complex
    # pylint: disable=too-many-branches

    sower = None
    if game.info.sow_rule:
        if game.info.sow_rule in (gi.SowRule.SOW_BLKD_DIV,
                                  gi.SowRule.SOW_BLKD_DIV_NR):
            sower = _add_blkd_divert_sower(game)

        elif game.info.sow_rule in (gi.SowRule.OWN_SOW_CAPT_ALL,
                                    gi.SowRule.SOW_CAPT_ALL):
            sower = sowd.SowCaptOwned(game)

        elif game.info.sow_rule == gi.SowRule.NO_SOW_OPP_NS:
            sower = sowd.SowSkipOppN(game, {game.info.sow_param})

        elif game.info.sow_rule == gi.SowRule.MAX_SOW:
            sower = sowd.SowMaxN(game, game.info.sow_param)

        elif game.info.sow_rule == gi.SowRule.NO_OPP_CHILD:
            sower = sowd.SowSkipOppChild(game)

        elif game.info.sow_rule == gi.SowRule.OPP_CHILD_ONLY1:
            sower = sowd.SowSkipOppChildUnlessFinal(game)

        elif game.info.sow_rule == gi.SowRule.LAP_CAPT_OPP_GETS:
            sower = sowd.SowSeeds(game)
            sower = sowd.SowOppCaptsLast(game, sower)

        elif game.info.sow_rule in (gi.SowRule.CHANGE_DIR_LAP,
                                    gi.SowRule.LAP_CAPT,
                                    gi.SowRule.LAP_CAPT_SEEDS):
            pass    # pick a base sower below

        else:
            raise NotImplementedError(
                    f"SowRule {game.info.sow_rule} not implemented.")

    if not sower:
        if game.info.sow_own_store:
            sower = sowd.SowSeedsNStore(game)
        else:
            sower = sowd.SowSeeds(game)

    return sower


def _add_pre_sow_capt(game, sower):
    """Add a presow capturer."""

    if game.info.presowcapt == gi.PreSowCapt.CAPT_ONE:
        sower = sowd.SCaptOne(game, sower)

    elif game.info.presowcapt == gi.PreSowCapt.ALL_SINGLE_XCAPT:
        sower = sowd.SCaptCrossSingles(game, sower)

    elif game.info.presowcapt == gi.PreSowCapt.DRAW_1_XCAPT:
        sower = sowd.SCaptCrossOnOne(game, sower)

    else:
        raise NotImplementedError(
                f"PreSowCapt {game.info.presowcapt} not implemented.")

    return sower


def _add_capt_stop_lap_cont(game, lap_cont):
    """Add the stop on 1 and then, one of the lap capture
    lap-continuer or a stop on capture decos.

    LAP_CONT rules without stores always include a
    StopNoOppSeeds to prevent an endless sow preventing a
    win condition."""

    lap_cont = msowd.StopSingleSeed(game, lap_cont)

    if game.info.sow_rule in (gi.SowRule.LAP_CAPT,
                              gi.SowRule.LAP_CAPT_OPP_GETS):

        if game.info.crosscapt:
            lap_cont = msowd.ContIfXCapt(game, lap_cont)

        elif game.info.capt_type in (gi.CaptType.NEXT,
                                     gi.CaptType.TWO_OUT):
            lap_cont = msowd.GapNextCapt(game, lap_cont)

        else:   # if basic_capt:
            lap_cont = msowd.ContIfBasicCapt(game, lap_cont)

    elif game.info.sow_rule == gi.SowRule.LAP_CAPT_SEEDS:
        lap_cont = msowd.ContWithCaptSeeds(game, lap_cont)

    elif game.info.capt_type == gi.CaptType.MATCH_OPP:
        lap_cont = msowd.StopCaptureSimul(game, lap_cont)

    elif game.info.basic_capt and not game.info.crosscapt:
        lap_cont = msowd.StopCaptureSeeds(game, lap_cont)

    if (not game.info.stores
            and game.info.sow_rule in (gi.SowRule.LAP_CAPT,
                                       gi.SowRule.LAP_CAPT_OPP_GETS,
                                       gi.SowRule.LAP_CAPT_SEEDS)):
        lap_cont = msowd.StopNoOppSeeds(game, lap_cont)

    return lap_cont


def _add_lap_decos(game, lap_cont):
    """Add any lap continuer wrapper decorators."""

    if game.info.mlap_cont == gi.SowLapCont.VISIT_OPP:
        lap_cont = msowd.MustVisitOpp(game, lap_cont)

    elif game.info.mlap_cont == gi.SowLapCont.ON_PARAM:
        lap_cont = msowd.StopNotN(game, lap_cont)

    elif game.info.mlap_cont == gi.SowLapCont.GREQ_PARAM:
        lap_cont = msowd.StopLessN(game, lap_cont)

    elif game.info.mlap_cont in (gi.SowLapCont.OWN_SIDE,
                                 gi.SowLapCont.OPP_SIDE):
        lap_cont = msowd.StopNotSide(game, lap_cont)

    if game.info.sow_own_store:
        lap_cont = msowd.StopRepeatTurn(game, lap_cont)

    if animator.ENABLED:
        lap_cont = msowd.AnimateLapStart(game, lap_cont)

    return lap_cont


def _build_lap_cont(game):
    """Choose a base lap continuer, then add any wrappers."""

    if game.info.mlaps == gi.LapSower.LAPPER:

        if game.info.child_type:
            lap_cont = msowd.ChildLapCont(game)

        elif game.info.sow_rule in (gi.SowRule.SOW_BLKD_DIV,
                                    gi.SowRule.SOW_BLKD_DIV_NR):
            lap_cont = msowd.DivertBlckdLapper(game)
        else:
            lap_cont = msowd.LapContinue(game)

        lap_cont = _add_capt_stop_lap_cont(game, lap_cont)

        if game.info.child_type:
            lap_cont = msowd.StopOnChild(game, lap_cont)

    elif game.info.mlaps == gi.LapSower.LAPPER_NEXT:
        lap_cont = msowd.NextLapCont(game)

    else:
        raise NotImplementedError(
                    f"LapSower {game.info.mlaps} not implemented.")

    lap_cont = _add_lap_decos(game, lap_cont)

    return lap_cont


def _add_mlap_sower(game, sower):
    """Build the deco chain elements for multiple lap sowing.
    Choose:
        1. an op to perform between laps
        2. a lap continue tester
    then build the mlap sower. Wrap if needed, with Visited."""

    if game.info.sow_rule == gi.SowRule.CHANGE_DIR_LAP:
        end_op = msowd.DirChange(game)
    elif game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV:
        end_op = msowd.CloseOp(game)
    elif game.info.sow_rule == gi.SowRule.SOW_BLKD_DIV_NR:
        end_op = msowd.CloseOp(game, True)
    else:
        end_op = msowd.NoOp(game)

    lap_cont = _build_lap_cont(game)
    sower = msowd.SowMlapSeeds(game, sower, lap_cont, end_op)

    return sower


def _add_prescribed_sower(game, sower):
    """Add the prescribed sowers to the deco chain."""

    if game.info.prescribed == gi.SowPrescribed.SOW1OPP:
        sower = sowd.SowOneOpp(game, 2, sower)

    elif game.info.prescribed == gi.SowPrescribed.PLUS1MINUS1:
        sower = sowd.SowPlus1Minus1Capt(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.BASIC_SOWER:
        sower = sowd.SowBasicFirst(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.MLAPS_SOWER:
        sower = msowd.SowMlapsFirst(game, 1, sower)

    elif game.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT:
        pass    # sower deco not needed

    else:
        raise NotImplementedError(
                f"SowPrescribed {game.info.prescribed} not implemented.")

    return sower


def deco_sower(game):
    """Build the sower chain."""

    sower = _add_base_sower(game)

    if game.info.presowcapt != gi.PreSowCapt.NONE:
        sower = _add_pre_sow_capt(game, sower)

    if game.info.mlaps != gi.LapSower.OFF:
        sower = _add_mlap_sower(game, sower)

    if game.info.prescribed != gi.SowPrescribed.NONE:
        sower = _add_prescribed_sower(game, sower)

    return sower
