# -*- coding: utf-8 -*-
"""This file defines the basic (non-round) ender decorator classes.

Return win/end-game-condition, winner from ender.game_ended.
self.game.turn is the player that just finished moving.

NOTE:  The ender results can be confusing so the logger is left
active when get_allowable_holes is called.

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

import abc

import animator
import claimer
import deco_chain_if
import format_msg as fmt
import game_info as gi

from game_logger import game_log


# %%  end turn interface

class EndTurnIf(deco_chain_if.DecoChainIf):
    """Interface for determining if the game is over."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator)
        self.sclaimer = sclaimer
        self.win_seeds = self.compute_win_seeds()

        # for games with rounds but not an even fill,
        # compute the win holes based on an equalized seeds per hole
        self.equalized = (self.game.info.start_pattern
                          != gi.StartPattern.ALL_EQUAL)


    def __str__(self):
        """A recursive func to print the whole decorator chain."""

        if self.sclaimer:
            return self.str_deco_detail(repr(self.sclaimer))
        return super().__str__()


    @abc.abstractmethod
    def game_ended(self, mdata):
        """Determine the end condition and winner;
        store in mdata.

        End condition will be one of None, WIN, TIE,
        ROUND_WIN and ROUND_TIE. The other values of
        WinCond are not generated here.

        if mdata.ended is truthy but not True and the game
        is played in rounds, end the round but not the
        game; unless ending the round also ends the game.

        There is no return value!"""


    def compute_win_holes(self):
        """Compute the number of holes that winner should own
        based on number of seeds. Seeds have already been collected
        from non-children.

        Return: fill start side for greater_holes (winner or True, for tie)
        and number of winner holes.

        This is used by the new_game deco."""

        game = self.game
        seeds = game.store.copy()
        for loc in range(game.cts.dbl_holes):
            if game.child[loc] is True:
                seeds[True] += game.board[loc]
            elif game.child[loc] is False:
                seeds[False] += game.board[loc]

        if seeds[True] == seeds[False]:
            # doesn't matter where fill starts for tie
            return True, game.cts.holes

        greater = seeds[True] > seeds[False]
        if self.equalized:
            alloc_count = game.cts.total_seeds / game.cts.dbl_holes
            greater_holes = round(seeds[greater] / alloc_count)
        else:
            nbr_start = game.cts.nbr_start
            greater_holes = (seeds[greater] + nbr_start // 2) // nbr_start

        game_log.add(f"{greater} holes = {greater_holes}", game_log.IMPORT)
        return greater, greater_holes


    @staticmethod
    def round_seeds_for_win(req_holes, nbr_start):
        """Seeds required for round win in territory games."""

        return req_holes * nbr_start - nbr_start + nbr_start // 2 + 1


    def compute_win_seeds(self):
        """Compute the number of seeds a player needs for an
        outright win (or round win). A player collecting more
        that win_seeds wins.

        Eliminate games (round tally or not) do not use this
        value, so -1."""

        game_goal = self.game.info.goal
        win_seeds = -1

        if self.game.info.goal.eliminate():
            return win_seeds

        if (self.game.info.rounds == gi.Rounds.NO_MOVES
                and game_goal == gi.Goal.MAX_SEEDS
                and not self.game.info.start_pattern
                and self.game.info.round_fill != gi.RoundFill.UMOVE):
            # force max seeds/rounds/no moves round to end
            # as soon as one player can outright win the game
            # as in one hole cannot be filled with nbr_start seeds
            min_needed = self.game.cts.nbr_start
            if self.game.info.goal_param:
                min_needed *= self.game.info.goal_param
            win_seeds = self.game.cts.total_seeds - min_needed

        # this test must be before the territory test
        elif self.game.info.rounds == gi.Rounds.NO_MOVES:
            win_seeds = self.game.cts.total_seeds - 1

        elif game_goal == gi.Goal.TERRITORY:
            win_seeds = EndTurnIf.round_seeds_for_win(self.game.info.goal_param,
                                                      self.game.cts.nbr_start)

        # this test must be after the territory test
        elif self.game.info.rounds in (gi.Rounds.END_S_SEEDS,
                                       gi.Rounds.END_2S_SEEDS):
            win_seeds = self.game.cts.total_seeds - 1

        elif (game_goal == gi.Goal.MAX_SEEDS
              or self.game.info.rounds == gi.Rounds.HALF_SEEDS):
            # do this math in case a start_pattern leaves an odd total seeds
            half, rem = divmod(self.game.cts.total_seeds, 2)
            win_seeds = half + rem

        else:
            raise gi.GameInfoError("Don't know how to compute seeds for win.")

        return win_seeds


    def has_seeds_for_win(self, seeds):
        """Determine if seed counts result in an
        end game condition."""

        if seeds[True] > self.win_seeds:
            return gi.WinCond.WIN, True

        if seeds[False] > self.win_seeds:
            return gi.WinCond.WIN, False

        if (seeds[False] == self.win_seeds
                and seeds[False] == seeds[True]):
            return gi.WinCond.TIE, None

        return None, self.game.turn


class ConcedeMixin:
    """A mixin for decorators that have different behavior for
    a normal end_move and a user directed conceded game.

    The parent class must set the conceder."""

    conceder = None

    def __str__(self):

        return self.str_deco_detail('conceder:  ' + str(self.conceder))



# %%

class ClearWinner(EndTurnIf):
    """Determine if the seed counts result in a clear winner.
    There must be decorators in the chain below this."""

    def __str__(self):
        return self.str_deco_detail(repr(self.sclaimer) + '\n   '
                                    + f'win_seeds: {self.win_seeds}')


    def game_ended(self, mdata):

        if mdata.ended:
            self.decorator.game_ended(mdata)

        else:
            cond, winner = self.has_seeds_for_win(self.sclaimer.claim_seeds())
            if cond:
                mdata.win_cond = cond
                mdata.winner = winner

            else:
                self.decorator.game_ended(mdata)


class EndTurnNoMoves(EndTurnIf):
    """No Pass, end game if there are no moves for the next player
    OR on repeat turn, the current player has no moves."""

    def game_ended(self, mdata):

        if mdata.ended:
            if self.decorator:
                self.decorator.game_ended(mdata)
            return

        if mdata.repeat_turn:
            mdata.ended = not any(self.game.get_allowable_holes())
            player = gi.PLAYER_NAMES[self.game.turn]
            msg = f"No moves for {player}'s repeat turn; _thing_ ended."
        else:
            with self.game.opp_turn():
                mdata.ended = not any(self.game.get_allowable_holes())
            player = gi.PLAYER_NAMES[not self.game.turn]
            msg = f"{player} had no moves; _thing_ ended."

        if mdata.ended:
            mdata.end_msg = msg
            game_log.add(msg, game_log.INFO)

        if self.decorator:
            self.decorator.game_ended(mdata)


class EndTurnPassPass(EndTurnIf):
    """End game if both players must pass.

    Pass move processing doesn't use the deco chains,
    so we need to catch it as soon as both players
    do not have moves.

    This can happen in split sow games, with a min move of 1,
    where a move pushed one seed across the side of the board;
    and possibly other situations. See allowables.DontUndoMoveOne"""

    def game_ended(self, mdata):

        if mdata.ended:
            return self.decorator.game_ended(mdata)

        if any(self.game.get_allowable_holes()):
            return self.decorator.game_ended(mdata)

        with self.game.opp_turn():
            no_next_moves = not any(self.game.get_allowable_holes())

        if no_next_moves:
            mdata.end_msg = "No moves for either player; game ended."
            game_log.add(mdata.end_msg, game_log.INFO)
            mdata.ended = True
            return self.decorator.game_ended(mdata)

        return self.decorator.game_ended(mdata)


class EndTurnMustShare(EndTurnIf):
    """With MUSTSHARE, the game is over if the next player to
    move needs to make seeds available to an opponent and cannot.
    If the game has ended, delegate to the deco chain and return
    the results.

    Do a scan for seeds and if required do the simulation
    to determine if the game is over.

    On repeat turn: if the opponent does not have have seeds
    and the current player does but can't make any available.

    On a first turn: if the current player does not have seeds
    and the opponent cannot make any seeds available to
    the current player.

    If seeds cannot be shared by the required player,
    call the claimer which may be configure as a taker.
    game.turn must be set to the player that should get
    the seeds."""

    def game_ended(self, mdata):

        if mdata.ended:
            return self.decorator.game_ended(mdata)

        opponent = not self.game.turn
        player_seeds = opp_seeds = False
        for loc in range(self.game.cts.dbl_holes):

            if (self.game.board[loc] >= self.game.info.min_move
                    and self.game.child[loc] is None):

                if self.game.owner[loc] == opponent:
                    opp_seeds = True
                else:
                    player_seeds = True

        if mdata.repeat_turn and player_seeds and not opp_seeds:
            mdata.ended = not any(self.game.get_allowable_holes())

        elif not mdata.repeat_turn and not player_seeds and opp_seeds:
            with self.game.opp_turn():
                mdata.ended = not any(self.game.get_allowable_holes())

        else:
            return self.decorator.game_ended(mdata)

        if mdata.ended:
            if mdata.repeat_turn:
                with self.game.opp_turn():
                    self.sclaimer.claim_seeds()
                    player = gi.PLAYER_NAMES[self.game.turn]
                msg = f"{player} can't share on repeat turn; _thing_ ended."
            else:
                self.sclaimer.claim_seeds()
                player = gi.PLAYER_NAMES[not self.game.turn]
                msg = f"{player} can't share; _thing_ ended."

            game_log.add(msg, game_log.INFO)
            mdata.end_msg = msg

        return self.decorator.game_ended(mdata)


class EndTurnNotPlayable(EndTurnIf):
    """If the game is no longer playable in any circustances,
    end it. Specifically, if none of the holes on the board
    have the minimum seeds required for a move, it's over.

    This is faster than simulating allowable moves and is
    needed for games w/o either mustshare or mustpass.

    This ends most territory games and rounds."""

    def game_ended(self, mdata):

        if mdata.ended:
            return self.decorator.game_ended(mdata)

        mdata.ended = not any(self.game.board[loc] >= self.game.info.min_move
                              and self.game.child[loc] is None
                              for loc in range(self.game.cts.dbl_holes))

        if mdata.ended:
            msg =  "No moves available for either player; _thing_ ended."
            game_log.add(msg, game_log.IMPORT)

            if not mdata.end_msg:
                mdata.end_msg = msg

        return self.decorator.game_ended(mdata)


class ChildNoStoresEnder(EndTurnIf):
    """The rest of the deco chain may collect seeds into
    the stores (if the game has ended). Move any seeds
    from the stores into available children.  If there
    were seeds out of play, leave them out of play."""

    def game_ended(self, mdata):
        """Children but no stores end move wrapper."""

        ostore = self.game.store.copy()

        self.decorator.game_ended(mdata)

        if not any(self.game.store) or ostore == self.game.store:
            return

        child_locs = self.game.find_child_stores()

        if all(loc is not None for loc in child_locs):
            self.game.board[child_locs[0]] += self.game.store[0] - ostore[0]
            self.game.board[child_locs[1]] += self.game.store[1] - ostore[1]

        elif child_locs[0] is not None:
            self.game.board[child_locs[0]] += sum(self.game.store) - ostore[0]
            game_log.add('Only False has child, gets all store seeds.',
                         game_log.INFO)

        elif child_locs[1] is not None:
            self.game.board[child_locs[1]] += sum(self.game.store) - sum(ostore)
            game_log.add('Only True has child, gets all store seeds.',
                         game_log.INFO)

        else:
            # game ended w/o child, move seeds from stores onto board
            self.game.board[0] += self.game.store[0] - ostore[0]
            self.game.board[-1] += self.game.store[1] - ostore[1]
            game_log.add('No children, but put seeds on board.',
                         game_log.INFO)

        self.game.store = ostore
        game_log.step('Moved store seeds to children', self.game)


class ConcedeDepImm(EndTurnIf):
    """Award the win to the player with more seeds."""

    def game_ended(self, mdata):

        seeds = self.sclaimer.claim_seeds()
        print("concdeDemImm", seeds)

        if seeds[0] > seeds[1]:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = False

        elif seeds[0] < seeds[1]:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = True

        else:
            mdata.win_cond = gi.WinCond.TIE


class DepriveEndGame(ConcedeMixin, EndTurnIf):
    """Determine if a deprive game is over based on who has seeds.

    Both player's had seeds at the start of the turn.
    If ended is true on entry call the conceder.

    If the opponent does not have seeds, then the current player
    won (even if they do not have seeds or it's a repeat turn).
    Otherwise, if the current player does not have seeds, then the
    opponent won.

    Otherwise, call the deco chain (allow rules are supported),
    to see who wins based on having/not having moves.

    This is not to be used with children, because the presence
    of children is not checked."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)
        self.conceder = ConcedeDepImm(game, None,
                                      claimer.ClaimBoardSeeds(game))

    def game_ended(self, mdata):
        """Check for end game."""

        if mdata.ended:
            self.conceder.game_ended(mdata)
            return

        test_range = self.game.cts.get_opp_range(self.game.turn)
        mdata.ended = not any(self.game.board[loc] for loc in test_range)
        if mdata.ended:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = self.game.turn
            mdata.end_msg = """_Winner_ won _thing_ by eliminating
                            _loser_'s seeds."""
            mdata.fmsg = True
            return

        test_range = self.game.cts.get_my_range(self.game.turn)
        mdata.ended = not any(self.game.board[loc] for loc in test_range)
        if mdata.ended:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = not self.game.turn
            if mdata.captured:
                mdata.end_msg = """_Loser_'s capture eliminated their own
                                seeds, but left _winner_ with seeds.
                                \n_Winner_ won the _thing_."""
            else:
                mdata.end_msg = """_Winner_ won _thing_ because _loser_
                                gave away all their seeds."""
            mdata.fmsg = True
            return

        self.decorator.game_ended(mdata)
        if mdata.ended:
            mdata.win_cond = gi.WinCond.WIN
            turn = self.game.turn
            mdata.winner = not turn if mdata.repeat_turn else turn
            mdata.end_msg += fmt.LINE_SEP if mdata.end_msg else ''
            mdata.end_msg += "_Winner_ won _thing_ because _loser_ cannot move."
            mdata.fmsg = True


class ImmobilizeEndGame(ConcedeMixin, EndTurnIf):
    """Determine if a immobilize game is over based on who moved last.

    Both player's had seeds at the start of the turn.
    If ended is true on entry call the conceder.

    If the opponent does not have a move, then the current player
    has won."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)
        self.conceder = ConcedeDepImm(game, None,
                                      claimer.ClaimBoardSeeds(game))


    def game_ended(self, mdata):
        """Check for end game."""

        if mdata.ended:
            self.conceder.game_ended(mdata)
            return

        with self.game.opp_turn():
            mdata.ended = not any(self.game.get_allowable_holes())

        if mdata.ended:

            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = self.game.turn
            mdata.end_msg = """_Loser_ had no valid moves.
                             \n\n_Winner_ won _thing_ by immobilizing _loser_."""
            mdata.fmsg = True
            game_log.add(fmt.fmsg(mdata.end_msg), game_log.INFO)


class ConcedeClear(EndTurnIf):
    """Award the win to the player with fewer seeds."""

    def game_ended(self, mdata):

        seeds = self.sclaimer.claim_seeds()

        if seeds[0] < seeds[1]:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = False

        elif seeds[0] > seeds[1]:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = True

        else:
            mdata.win_cond = gi.WinCond.TIE


class ClearSeedsEndGame(ConcedeMixin, EndTurnIf):
    """Win by giving away all your seeds.

    If both players end up without seeds, the win is awarded to
    the current player.

    Both player's had seeds at the start of the turn.
    If ended is true on entry call the conceder."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)
        self.conceder = ConcedeClear(game, None,
                                     claimer.ClaimBoardSeeds(game))


    def game_ended(self, mdata):
        """Check for end game."""

        if mdata.ended:
            self.conceder.game_ended(mdata)
            return

        my_range, opp_range = self.game.cts.get_ranges(self.game.turn)

        my_seeds = sum(self.game.board[loc] for loc in my_range)
        if not my_seeds:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = self.game.turn
            return

        opp_seeds = sum(self.game.board[loc] for loc in opp_range)
        if not opp_seeds:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = not self.game.turn
            mdata.end_msg = """_Winner_ won _thing_ because _loser_
                            removed their seeds."""
            mdata.fmsg = True


class NoOutcomeChange(EndTurnIf):
    """Call the deco chain to decide if the game ends by normal
    means. If the game hasn't ended by normal means, determine
    if there can be any change in outcome based on seeds still
    in play.

    Games that use this class must either employ Waldas or have
    stores. In the case of Waldas, WaldaEndMove will cleanup."""

    def __init__(self, game, min_needed, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)
        self.min_needed = min_needed


    def __str__(self):
        return self.str_deco_detail(f'min_needed: {self.min_needed}')


    @staticmethod
    def min_for_change(game):
        """Select a minimum number of seeds that must be on the
        board for a capture or to claim territory.

        Called by deco creator to decide if this class should
        be included."""
        # pylint: disable=too-many-branches

        if game.info.child_type:
            # presence of children checked at play-time
            min_needed = game.info.child_cvt
        else:
            min_needed = game.cts.total_seeds  # max possible and flag

        if (game.info.evens
                or game.info.capt_type == gi.CaptType.NEXT
                or game.info.crosscapt):
            min_needed = min(2, min_needed)

        if game.info.capt_type == gi.CaptType.TWO_OUT:
            if game.info.mlaps:
                min_needed = min(2, min_needed)
            else:
                min_needed = min(3, min_needed)

        if game.info.capt_on:
            if game.info.evens:
                min_needed = min(cval for cval in game.info.capt_on
                                    if not cval % 1)
            else:
                min_needed = min(*game.info.capt_on, min_needed)

        # a capt_min value overrides any other
        if game.info.capt_min:
            if min_needed == game.cts.total_seeds:
                min_needed = game.info.capt_min
            else:
                min_needed = max(game.info.capt_min, min_needed)

        return min_needed


    def _too_few_for_change(self):
        """Determine if the game outcome can change.
        If there are any children, return False (can sow into children).
        If there are not any seeds, return False (but this isn't called
        when there are no seeds).
        If there are too few seeds left to change the outcome,
        return True."""

        remaining = 0
        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is None:
                remaining += self.game.board[loc]
            else:
                return False

        if 0 < remaining < self.min_needed:
            return True

        return False


    def game_ended(self, mdata):
        """Determine if the game ended."""

        self.decorator.game_ended(mdata)

        if (not mdata.ended
                and not mdata.win_cond
                and self._too_few_for_change()):
            mdata.end_msg = f"""Too few seeds for outcome change
                            (< {self.min_needed}), _thing_ ended."""
            game_log.add(fmt.fmsg(mdata.end_msg))
            mdata.ended = True
            self.decorator.game_ended(mdata)


class EndGameWinner(EndTurnIf):
    """This is intended to be at the bottom of the deco chain.
    If any deco has determined that the game should end,
    this will end the game and pick a winner.

    The sclaimer should be a taker.
    The seeds for win is checked again (after running sclaimer/taker).

    Any child deco is ignored."""

    def game_ended(self, mdata):

        if not mdata.ended:
            return

        # check for clear win condition
        seeds = self.sclaimer.claim_seeds()
        cond, winner = self.has_seeds_for_win(seeds)

        if cond:
            mdata.win_cond = cond
            mdata.winner = winner

        # no clear win condition, pick player with most seeds
        elif seeds[0] > seeds[1]:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = False

        elif seeds[0] < seeds[1]:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = True

        else:
            mdata.win_cond = gi.WinCond.TIE


class QuitToTie(EndTurnIf):
    """Force the game to end in a tie; don't change the board.
    Used for DEPRIVE games."""

    def game_ended(self, mdata):
        """Determine if the game ended."""
        mdata.win_cond = gi.WinCond.TIE


class AnimateEndMove(EndTurnIf):
    """Animate end move as a single animation step.
    The taker and divvier look odd picking seeds up one
    hole at a time."""

    def game_ended(self, mdata):

        with animator.one_step():
            self.decorator.game_ended(mdata)
