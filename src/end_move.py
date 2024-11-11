# -*- coding: utf-8 -*-
"""There are two  deco chains defined here:
    1. ender:  at the end of each turn determine if the game is over.
    2. quitter:  user ended the game or a sow resulted in ENDLESS,
    do something fair.

Return win/end-game-condition, winner from ender.game_ended.
self.game.turn is the player that just finished moving.

Process is as follows:
    0. RoundWinner defers to the rest of the chain
       (on returns it adjusts the outcome).
    1. Determine outright game winner or game tie
       via ClearWinner.
    2. Check for end condition: no outcome change, not playable,
       mustshare, or cannot pass (not mustpass).
    3. If the game has ended, collect seeds and determine if
       round/game winner or round/game tie.

Log a step if anything is changed on the board, e.g. TakeOwnSeeds.

Created on Fri Apr  7 07:43:19 2023
@author: Ann"""

# %% imports

import warnings

import claimer
import end_move_decos as emd
import end_move_rounds as emr
import game_interface as gi
import round_tally


# %% build decorator chains

def deco_add_bottom_winner(game):
    """Start the deco chain by adding the bottom Winner
    and MoreSeedsWinner (if needed)."""

    if game.info.no_sides:
        ender = emd.EndGameWinner(
            game, sclaimer=claimer.TakeOnlyChildNStores(game))

    else:
        ender = emd.EndGameWinner(game, sclaimer=claimer.TakeOwnSeeds(game))

    return ender


def deco_add_no_change(game, ender):
    """Consider adding the NoOutcomeChange deco.
    Don't include it if it won't do anything:
        if easy cases based on game props (see code)
        if min_for_change returns sentinel value
        if EndTurnNotPlayable covers what NoOutcomeChange would do"""

    ginfo = game.info
    if any([
            # single seeds may be moved into store,
            # all seeds will be moved out of play
            ginfo.sow_own_store,

            # game ends when a player has no seeds and opp can't share
            ginfo.mustshare,

            # picks take care of ending game
            ginfo.pickextra == gi.CaptExtraPick.PICKLASTSEEDS,
            ginfo.pickextra == gi.CaptExtraPick.PICK2XLASTSEEDS,

            # seeds only moved to waldas, no stores
            ginfo.child_type == gi.ChildType.WALDA,

            # if can only capture from children
            (ginfo.child_type == gi.ChildType.WEG
             and not any([ginfo.capt_max,
                          ginfo.capt_min,
                          ginfo.capt_next,
                          ginfo.capt_on,
                          ginfo.capttwoout,
                          ginfo.crosscapt,
                          ginfo.evens,
                          ginfo.sow_own_store]))]):
        return ender

    min_seeds = emd.NoOutcomeChange.min_for_change(game)

    if game.info.min_move < min_seeds < game.cts.total_seeds:
        ender = emd.NoOutcomeChange(game, min_seeds, ender)

    return ender



def deco_end_move(game):
    """Return a chain of move enders."""

    if game.info.goal == gi.Goal.DEPRIVE:
        return emd.DepriveSeedsEndGame(game)

    if game.info.goal == gi.Goal.CLEAR:
        return emd.ClearSeedsEndGame(game)

    ender = deco_add_bottom_winner(game)

    if not game.info.mustpass:
        ender = emd.EndTurnNoMoves(game, ender)

    if game.info.mustshare:
        ender = emd.EndTurnMustShare(game, ender)

    ender = emd.EndTurnNotPlayable(game, ender)
    ender = deco_add_no_change(game, ender)

    if game.info.child_cvt:
        sclaimer = claimer.ChildClaimSeeds(game)
    else:
        sclaimer = claimer.ClaimSeeds(game)
    ender = emd.ClearWinner(game, ender, sclaimer)

    if game.info.rounds:
        if game.info.goal in round_tally.RoundTally.GOALS:
            ender = emr.RoundTallyWinner(game, ender,
                                         claimer.ClaimOwnSeeds(game))
        else:
            ender = emr.RoundWinner(game, ender, claimer.ClaimOwnSeeds(game))

    if game.info.child_type and not game.info.stores:
        ender = emd.WaldaEndMove(game, ender)

    return ender


def deco_quitter(game):
    """Return a quitter. Used when either the user ended game or
    the game reached an ENDLESS condition.

    Do something that seems fair. Assume that seeds in play could
    belong to either player."""

    if game.info.goal in (gi.Goal.CLEAR, gi.Goal.DEPRIVE):
        quitter = emd.QuitToTie(game)

    elif game.info.stores or game.info.child_cvt:

        if game.info.stores:
            sclaimer = claimer.DivvySeedsStores(game)
        else:  # if game.info.child_cvt:
            sclaimer = claimer.DivvySeedsChildOnly(game)

        if game.info.goal in round_tally.RoundTally.GOALS:
            quitter = emr.QuitRoundTally(game, sclaimer=sclaimer)

        else:
            quitter = emd.EndGameWinner(game, sclaimer=sclaimer)

    else:
        warnings.warn("Quitter configuration defaulting to QuitToTie")
        quitter = emd.QuitToTie(game)

    return quitter
