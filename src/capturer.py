# -*- coding: utf-8 -*-
"""Create the capturer deco chain.

Created on Fri Apr  7 08:52:03 2023
@author: Ann"""


import capt_decos
import game_info as gi


def _add_cross_capt_deco(game):
    """Choose base the cross capture decorator.
    crosscapt and multicapt is always captsamedir"""

    capturer = capt_decos.CaptCross(game)

    if game.info.xcpickown == gi.CrossCaptOwn.LEAVE:
        pass

    elif game.info.xcpickown == gi.CrossCaptOwn.PICK_ON_CAPT:
        capturer = capt_decos.CaptCrossPickOwnOnCapt(game, capturer)

    elif game.info.xcpickown == gi.CrossCaptOwn.ALWAYS_PICK:
        capturer = capt_decos.CaptCrossPickOwn(game, capturer)

    else:
        raise NotImplementedError(
                f"CrossCaptOwn {game.info.xcpickown} not implemented.")

    if game.info.xc_sown:
        capturer = capt_decos.CaptCrossVisited(game, capturer)

    return capturer


def _add_grand_slam_deco(game, capturer):
    """Add the grand slam decorators to the capturer deco."""

    if game.info.grandslam == gi.GrandSlam.NO_CAPT:
        capturer = capt_decos.GSNone(game, capturer)

    elif game.info.grandslam in (gi.GrandSlam.LEAVE_LEFT,
                                 gi.GrandSlam.LEAVE_RIGHT):
        capturer = capt_decos.GSKeep(game, game.info.grandslam, capturer)

    elif game.info.grandslam == gi.GrandSlam.OPP_GETS_REMAIN:
        capturer = capt_decos.GSOppGets(game, capturer)

    elif game.info.grandslam in (gi.GrandSlam.LEGAL,
                                 gi.GrandSlam.NOT_LEGAL):
        # grand slam rule does not need a capture deco
        pass

    else:
        raise NotImplementedError(
                f"GrandSlam {game.info.grandslam} not implemented.")

    return capturer


def _add_child_deco(game, capturer):
    """Add a child handling deco if needed.
    only one child handler: bull/weg/waldas/tuzdek/children"""

    if game.info.child_type == gi.ChildType.NOCHILD:
        return capturer

    if game.info.child_type in (gi.ChildType.NORMAL,
                                gi.ChildType.ONE_CHILD):
        capturer = capt_decos.MakeChild(game, capturer)

    elif game.info.child_type == gi.ChildType.WEG:
        capturer = capt_decos.MakeWegCapture(game, capturer)

    elif game.info.child_type == gi.ChildType.BULL:
        capturer = capt_decos.MakeBull(game, capturer)

    elif game.info.child_type == gi.ChildType.QUR:
        capturer = capt_decos.MakeQur(game, capturer)

    else:
        raise NotImplementedError(
                f"ChildType {game.info.child_type} not implemented.")

    return capturer


def _add_capt_type_deco(game):
    """Choose a base capture type decos."""

    if game.info.capt_type == gi.CaptType.TWO_OUT:
        capturer = capt_decos.CaptTwoOut(game)

    elif game.info.capt_type == gi.CaptType.NEXT:
        capturer = capt_decos.CaptNext(game)

    elif game.info.capt_type == gi.CaptType.MATCH_OPP:
        capturer = capt_decos.CaptMatchOpp(game)

    elif game.info.capt_type == gi.CaptType.SINGLETONS:
        capturer = capt_decos.CaptSingles(game)

    else:
        raise NotImplementedError(
            f"CaptType {game.info.capt_type} not implemented.")

    return capturer


def _add_capt_pick_deco(game, capturer):
    """Add any extra pickers."""

    if game.info.pickextra in (gi.CaptExtraPick.NONE,
                               gi.CaptExtraPick.PICKCROSSMULT):
        pass

    elif game.info.pickextra == gi.CaptExtraPick.PICKCROSS:
        capturer = capt_decos.PickCross(game, capturer)

    elif game.info.pickextra == gi.CaptExtraPick.PICKOPPBASIC:
        capturer = capt_decos.PickOppBasic(game, capturer)

    elif game.info.pickextra == gi.CaptExtraPick.PICKLASTSEEDS:
        capturer = capt_decos.PickLastSeeds(game, capturer, turn_takes=True)

    elif game.info.pickextra == gi.CaptExtraPick.PICK2XLASTSEEDS:
        capturer = capt_decos.PickLastSeeds(game, capturer, turn_takes=False)

    elif game.info.pickextra == gi.CaptExtraPick.PICKFINAL:
        capturer = capt_decos.PickFinal(game, capturer)

    else:
        raise NotImplementedError(
            f"CaptExtraPick {game.info.pickextra} not implemented.")

    return capturer


def _add_base_capturer(game):
    """Select the base capturer."""

    if game.info.crosscapt:
        capturer = _add_cross_capt_deco(game)

    elif game.info.capt_type:
        capturer = _add_capt_type_deco(game)

    elif (game.info.evens or game.info.capt_on
          or game.info.capt_max or game.info.capt_min):
        capturer = capt_decos.CaptBasic(game)

    else:
        capturer = capt_decos.CaptNone(game)

    return capturer


def deco_capturer(game):
    """Build capture chain and return it."""

    capturer = _add_base_capturer(game)

    # add decorators to the base capturer
    if game.info.multicapt:
        if game.info.pickextra == gi.CaptExtraPick.PICKCROSSMULT:
            capturer = capt_decos.PickCross(game, capturer)

        capturer = capt_decos.CaptMultiple(game, capturer)

    if (game.info.capt_dir == gi.CaptDir.OPP_SOW
            and (game.info.multicapt
                 or game.info.capt_type == gi.CaptType.NEXT)):
        # opp_sow is default, don't add CaptOppDir if not needed
        capturer = capt_decos.CaptOppDir(game, capturer)

    elif game.info.capt_dir == gi.CaptDir.BOTH:
        capturer = capt_decos.CaptBothDir(game, capturer)

    capturer = _add_child_deco(game, capturer)
    capturer = _add_capt_pick_deco(game, capturer)
    capturer = _add_grand_slam_deco(game, capturer)

    if (game.info.child_type
            and not game.info.stores
            and game.info.any_captures):
        # if there is no capture mechanism, never need to move to children
        capturer = capt_decos.CaptureToChild(game, capturer)

    if game.info.nosinglecapt:
        capturer = capt_decos.NoSingleSeedCapt(game, capturer)

    if (game.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT
            or game.info.round_fill == gi.RoundFill.SHORTEN
            or game.info.nocaptmoves):
        capturer = capt_decos.NotInhibited(game, capturer)

    if game.info.capt_rturn:
        capturer = capt_decos.RepeatTurn(game, capturer)

    return capturer
