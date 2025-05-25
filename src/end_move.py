# -*- coding: utf-8 -*-
"""There are two  deco chains defined here:
    1. ender:  at the end of each turn determine if the game is over.
    2. quitter:  user ended the game or a sow resulted in ENDLESS,
    do something fair.

Decos return win/end-game-condition, if the game has ended.
These are called before the game.turn is changed at the end of
a move.

Decos will use claimers to determine what seeds to count.
game.info.unclaimed describes how to score seeds when
the game has ended.

Created on Fri Apr  7 07:43:19 2023
@author: Ann"""

# %% imports

import warnings

import animator
import claimer
import end_move_decos as emd
import end_move_rounds as emr
import game_interface as gi
import round_tally


# %% build decorator chains

def _build_deprive_ender(game):
    """Create a deprive game ender."""

    if game.info.min_move == 1:
        # player wo seeds loses, game ends when either player has 0 seeds
        ender = emd.EndTurnNoMoves(game)
        ender = emd.DepriveNoSeedsEndGame(game, ender)
    else:
        # last mover wins
        ender = emd.DepriveLastMoveEndGame(game)

    if game.info.goal == gi.Goal.RND_WIN_COUNT_DEP:
        sclaimer = claimer.ClaimSeeds(game)
        ender = _add_round_ender(game, ender, sclaimer)

    return ender


def _build_clear_ender(game):
    """Create a clear game ender."""

    ender = emd.ClearSeedsEndGame(game)

    if game.info.goal == gi.Goal.RND_WIN_COUNT_CLR:
        sclaimer = claimer.ClaimSeeds(game)
        ender = _add_round_ender(game, ender, sclaimer)

    return ender


def _add_end_game_winner(game):
    """Start the deco chain by adding the EndGameWinner.
    Select a claimer based on how the unclaimed seeds
    should be scored.  Some of the claimers create
    lambda's to look the actual player later.

    EndGameMustShare does the taker if can't share,
    so this uses the default taker here."""

    if (game.info.no_sides
            or game.info.unclaimed == gi.EndGameSeeds.DONT_SCORE
            or game.info.unclaimed == gi.EndGameSeeds.UNFED_PLAYER):
        sclaimer = claimer.TakeOnlyChildNStores(game)

    elif game.info.unclaimed == gi.EndGameSeeds.HOLE_OWNER:
        sclaimer = claimer.TakeOwnSeeds(game)

    elif game.info.unclaimed == gi.EndGameSeeds.LAST_MOVER:
        sclaimer = claimer.TakeAllUnclaimed(game)

    elif game.info.unclaimed == gi.EndGameSeeds.DIVVIED:
        sclaimer = claimer.DivvySeedsStores(game)

    else:
        raise NotImplementedError(
                f"Unclaimed {game.info.unclaimed} not implemented.")

    return emd.EndGameWinner(game, sclaimer=sclaimer)


def _add_no_change(game, ender):
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

            # seeds only moved to children, no stores
            game.info.child_type and not game.info.stores,

            # if can only capture from children
            (ginfo.child_type == gi.ChildType.WEG
             and not any([ginfo.capt_max,
                          ginfo.capt_min,
                          ginfo.capt_on,
                          ginfo.capt_type,
                          ginfo.crosscapt,
                          ginfo.evens,
                          ginfo.sow_own_store]))]):
        return ender

    min_seeds = emd.NoOutcomeChange.min_for_change(game)

    if game.info.min_move < min_seeds < game.cts.total_seeds:
        ender = emd.NoOutcomeChange(game, min_seeds, ender)

    return ender


def _add_must_share_ender(game, ender):
    """Add the must share ender. If the scoring of unclaimed
    seeds is UNFED_PLAYER, provide a seed taker to
    do that. Otherwise, provide a claimer that does nothing."""

    if game.info.unclaimed == gi.EndGameSeeds.UNFED_PLAYER:
        sclaimer = claimer.TakeAllUnclaimed(game)

    else:
        sclaimer = claimer.ClaimSeeds(game)

    return emd.EndTurnMustShare(game, ender, sclaimer)


def _add_round_ender(game, ender, sclaimer):
    """Add the round ender."""

    if (game.info.rounds in (gi.Rounds.END_S_SEEDS,
                             gi.Rounds.END_2S_SEEDS)
            and game.info.pickextra not in (gi.CaptExtraPick.PICKLASTSEEDS,
                                            gi.CaptExtraPick.PICK2XLASTSEEDS)):
        # only need RoundEndLimit when a picker is not doing the same work
        ender = emr.RoundEndLimit(game, ender)

    # the claimer here decides if game or round ends; after we know it ended
    if game.info.goal in round_tally.RoundTally.GOALS:
        # use the same claimer as for clear winner
        ender = emr.RoundTallyWinner(game, ender, sclaimer)

    else:
        # use claim all seeds in owned holes (might be side or owner)
        ender = emr.RoundWinner(game, ender, claimer.ClaimOwnSeeds(game))

    return ender


def _build_ender(game):
    """Build the ender for non clear and deprive
    games."""

    ender = _add_end_game_winner(game)

    if game.info.mustpass:
        ender = emd.EndTurnPassPass(game, ender)
    else:
        ender = emd.EndTurnNoMoves(game, ender)

    if game.info.mustshare:
        ender = _add_must_share_ender(game, ender)

    ender = emd.EndTurnNotPlayable(game, ender)
    ender = _add_no_change(game, ender)

    if game.info.child_type:
        sclaimer = claimer.ChildClaimSeeds(game)
    else:
        sclaimer = claimer.ClaimSeeds(game)
    ender = emd.ClearWinner(game, ender, sclaimer)

    if game.info.rounds:
        ender = _add_round_ender(game, ender, sclaimer)

    if game.info.child_type and not game.info.stores:
        ender = emd.ChildNoStoresEnder(game, ender)

    return ender


def deco_end_move(game):
    """Return a chain of move enders."""

    if game.info.goal in (gi.Goal.DEPRIVE,
                          gi.Goal.RND_WIN_COUNT_DEP):
        ender = _build_deprive_ender(game)

    elif game.info.goal in (gi.Goal.CLEAR,
                            gi.Goal.RND_WIN_COUNT_CLR):
        ender = _build_clear_ender(game)

    else:
        ender = _build_ender(game)

    if animator.ENABLED:
        ender = emd.AnimateEndMove(game, ender)

    return ender


def deco_quitter(game):
    """Return a quitter. Used when either the user qiot game or
    the game reached an ENDLESS condition.

    Do something that seems fair. Assume that seeds in play could
    belong to either player."""
    # pylint: disable=too-complex

    sclaimer = None
    quitter = None

    if game.info.goal in (gi.Goal.CLEAR,
                          gi.Goal.DEPRIVE,
                          gi.Goal.RND_WIN_COUNT_DEP,
                          gi.Goal.RND_WIN_COUNT_CLR):
        quitter = emd.QuitToTie(game)

    elif game.info.quitter == gi.EndGameSeeds.HOLE_OWNER:
        sclaimer = claimer.TakeOwnSeeds(game)

    elif game.info.quitter in (gi.EndGameSeeds.DONT_SCORE,
                               gi.EndGameSeeds.UNFED_PLAYER):
        sclaimer = claimer.TakeOnlyChildNStores(game)

    elif game.info.quitter == gi.EndGameSeeds.LAST_MOVER:
        sclaimer = claimer.TakeAllUnclaimed(game)

    elif game.info.quitter == gi.EndGameSeeds.DIVVIED:
        if game.info.stores:
            sclaimer = claimer.DivvySeedsStores(game)

        elif game.info.child_type:
            sclaimer = claimer.DivvySeedsChildOnly(game)

        else:
            warnings.warn("Quitter configuration defaulting to QuitToTie")
            quitter = emd.QuitToTie(game)

    else:
        raise NotImplementedError(
                f"Quitter {game.info.unclaimed} not implemented.")

    if not quitter:
        quitter = emd.EndGameWinner(game, sclaimer=sclaimer)

    if game.info.goal in round_tally.RoundTally.GOALS:
        # ChildClaimSeeds will work for both children games and not
        # the divvier on EndGameWinner did the divvying work
        quitter = emr.QuitRoundTally(game,
                                     quitter,
                                     sclaimer=claimer.ChildClaimSeeds(game))

    if animator.ENABLED:
        quitter = emd.AnimateEndMove(game, quitter)

    return quitter
