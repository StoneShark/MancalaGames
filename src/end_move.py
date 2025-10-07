# -*- coding: utf-8 -*-
"""Define the end_move decorators and build the end_move
and quitter decorator chains. The end_move deco chain is
called after each move to determine if the game has ended.
The quitter deco chain is used when a player conceeds
the game.

Enders might use a claimer to move seeds off the board into stores.

The decorators might update the mdata fields
    end_msg - reason for ending the game
    ended - set true when the game is ended
    win_cond - describes win condition (win, tie, * round, or repeat turn)
    winner - actual game winner

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
import warnings

import animator
import claimer
import deco_chain_if
import format_msg as fmt
import game_info as gi
import round_tally

from game_logger import game_log


# %%  end turn interface and concede mixin

class EndTurnIf(deco_chain_if.DecoChainIf):
    """Interface for determining if the game is over."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator)
        self.sclaimer = sclaimer
        self.win_seeds = self.compute_win_seeds()


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


    def terr_win_seeds(self):
        """Seeds required for round win in territory games.

        For TERR_EX_EMPTY fill, the winner must be able to
        completely fill & control goal_param holes.

        For all others, the winner must be able to fill/control
        goal_param holes by having enough seeds to fill the final
        hole with more than half the number of start seeds."""

        req_holes = self.game.info.goal_param
        seeds = self.game.cts.seed_equiv

        if self.game.info.round_fill == gi.RoundFill.TERR_EX_EMPTY:
            return req_holes * seeds

        return (req_holes - 1) * seeds + seeds // 2 + 1


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
            win_seeds = self.terr_win_seeds()

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



# %%  ender decos

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
            mdata.add_end_msg(msg)
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
            msg = "No moves for either player; game ended."
            mdata.add_end_msg(msg)
            game_log.add(msg, game_log.INFO)
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
            mdata.add_end_msg(msg)

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
            mdata.add_end_msg(msg)
            game_log.add(msg, game_log.IMPORT)

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
            mdata.add_end_msg("""_Winner_ won _thing_ by eliminating
                              _loser_'s seeds.""", True)
            return

        test_range = self.game.cts.get_my_range(self.game.turn)
        mdata.ended = not any(self.game.board[loc] for loc in test_range)
        if mdata.ended:
            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = not self.game.turn
            if mdata.captured:
                mdata.add_end_msg("""_Loser_'s capture eliminated their own
                                  seeds, but left _winner_ with seeds.
                                  \n_Winner_ won the _thing_.""")
            else:
                mdata.add_end_msg("""_Winner_ won _thing_ because _loser_
                                  gave away all their seeds.""", True)
            return

        self.decorator.game_ended(mdata)
        if mdata.ended:
            mdata.win_cond = gi.WinCond.WIN
            turn = self.game.turn
            mdata.winner = not turn if mdata.repeat_turn else turn
            mdata.add_end_msg("""_Winner_ won _thing_ because
                              _loser_ cannot move.""", True)


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

        if game.info.play_locs:
            self.moves_test = game.get_moves
        else:
            self.moves_test = game.get_allowable_holes


    def game_ended(self, mdata):
        """Check for end game."""

        if mdata.ended:
            self.conceder.game_ended(mdata)
            return

        with self.game.opp_turn():
            mdata.ended = not any(self.moves_test())

        if mdata.ended:

            mdata.win_cond = gi.WinCond.WIN
            mdata.winner = self.game.turn
            msg = """_Loser_ had no valid moves.
                     \n\n_Winner_ won _thing_ by immobilizing _loser_."""
            mdata.add_end_msg(msg, True)
            game_log.add(fmt.fmsg(msg), game_log.INFO)


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
            mdata.add_end_msg("""_Winner_ won _thing_ because _loser_
                              removed their seeds.""", True)


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

        if game.info.child_type.child_but_not_ram():
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
            msg = f"""Too few seeds for outcome change
                   (< {self.min_needed}), _thing_ ended."""
            mdata.add_end_msg(msg)
            game_log.add(fmt.fmsg(msg))
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


class EndSeedsLimit(EndTurnIf):
    """End the game when there are fewer than stop_at
    seeds.

    If there are fewer (<=) than the specified number of seeds
    on the board in play, call down the decorator chain
    with ended as True."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)

        if game.info.rounds == gi.Rounds.END_S_SEEDS:
            self.stop_at = game.cts.nbr_start

        elif game.info.rounds == gi.Rounds.END_2S_SEEDS:
            self.stop_at = 2 * game.cts.nbr_start

        elif game.info.end_cond == gi.EndGameCond.SEEDS_LIMIT:
            self.stop_at = self.game.info.end_param

        else:
            raise gi.GameInfoError(
                "Don't know what stop_at should be for EndSeedsLimit.")

    def __str__(self):
        clstr = (repr(self.sclaimer) + '\n   ') if self.sclaimer else ''
        return self.str_deco_detail(clstr + f'stop_at: {self.stop_at}')


    def game_ended(self, mdata):

        remaining = sum(self.game.board[loc]
                        for loc in range(self.game.cts.dbl_holes)
                        if self.game.child[loc] is None)

        if remaining <= self.stop_at:
            msg = f"""Seeds limit ({self.stop_at}) or fewer seeds
                            remaining, _thing_ ended."""
            mdata.add_end_msg(msg)
            game_log.add(fmt.fmsg(msg), game_log.IMPORT)
            mdata.ended = True

        self.decorator.game_ended(mdata)


class ClearedSideEnder(EndTurnIf):
    """Call down the deco chain with game ended if the
    specified player's holes are empty."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)

        if game.info.end_cond == gi.EndGameCond.CLEARED_OWN:
            self.side_op = lambda turn: turn
            self.side = "own"
        else:
            self.side_op = lambda turn: not turn
            self.side = "opponent"


    def __str__(self):
        clstr = (repr(self.sclaimer) + '\n   ') if self.sclaimer else ''
        return self.str_deco_detail(clstr + f'cleared side: {self.side}')


    def game_ended(self, mdata):

        side = self.side_op(self.game.turn)
        if all(not self.game.board[idx]
               for idx in self.game.cts.get_my_range(side)
               if self.game.child[idx] is None):

            player = self.game.turn_name()
            msg = f"{player} cleared {self.side} holes, _thing_ ended."
            mdata.add_end_msg(msg)
            game_log.add(fmt.fmsg(msg), game_log.IMPORT)
            mdata.ended = True

        self.decorator.game_ended(mdata)


class HoleSeedsLimit(EndTurnIf):
    """Call down the deco chain with game ended if all holes
    have end_param or fewer seeds."""

    def game_ended(self, mdata):

        if all(self.game.board[idx] <= self.game.info.end_param
               for idx in range(self.game.cts.dbl_holes)
               if self.game.child[idx] is None):

            msg = f"""All holes have have fewer than
                      {self.game.info.end_param}, _thing_ ended."""
            mdata.add_end_msg(msg)
            game_log.add(fmt.fmsg(msg), game_log.IMPORT)
            mdata.ended = True

        self.decorator.game_ended(mdata)


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


# %%  round enders

class RoundWinner(EndTurnIf):
    """"If the game is played in rounds where seeds collected
    are used to setup the board for a new round, let the rest
    of the chain decide the outcome, then adjust for end of
    game or end of round.

    Additionally, the game is over if either player does not have
    the minimum seeds to continue the game.  The claimer is used
    after the game is known to be over to determine if the
    round or game is over."""

    def __init__(self, game, decorator=None, sclaimer=None):
        """Init the parent deco's; then fill:

        req_seeds: the number of seeds required to keep playing
        the game.

        msg: message to log if either player has fewer
        than req_seeds"""

        super().__init__(game, decorator, sclaimer)

        nbr_start = game.cts.nbr_start
        goal_param = game.info.goal_param
        intro = "Game, not round, ended (too few seeds to "

        if game.info.goal == gi.Goal.TERRITORY:
            req_holes = game.cts.dbl_holes - goal_param + 1
            self.req_seeds = game.cts.total_seeds - self.terr_win_seeds()
            if game.info.round_fill == gi.RoundFill.TERR_EX_EMPTY:
                self.req_seeds += 1
            else:
                self.req_seeds += game.cts.seed_equiv // 2
            self.msg = intro + f"claim at least {req_holes} holes)."

        elif game.info.round_fill == gi.RoundFill.UMOVE:
            # uses even_fill so must be before it (to require more seeds)
            self.req_seeds = game.cts.holes + game.info.min_move - 1
            self.msg = intro + "fill a playable side)."

        elif game.info.round_fill == gi.RoundFill.EVEN_FILL:
            self.req_seeds = game.info.min_move
            self.msg = intro + "fill a playable side)."

        elif game.info.goal_param > 0:
            # max seeds games do not round seed counts (like territory games)
            self.req_seeds = game.info.goal_param * nbr_start
            self.msg = intro + f"fill at least {goal_param} holes)."

        else:
            self.req_seeds = nbr_start
            self.msg = intro + "fill a hole)."


    def __str__(self):
        return self.str_deco_detail(repr(self.sclaimer) + '\n   '
                                    + f'req_seeds: {self.req_seeds}')


    def game_ended(self, mdata):

        ended_in = mdata.ended
        self.decorator.game_ended(mdata)
        if ended_in is True or not mdata.win_cond:
            return

        seeds = self.sclaimer.claim_seeds()
        if seeds[True] < self.req_seeds or seeds[False] < self.req_seeds:
            mdata.add_end_msg(self.msg)
            game_log.add(self.msg, game_log.IMPORT)

        elif mdata.win_cond == gi.WinCond.WIN:
            mdata.win_cond = gi.WinCond.ROUND_WIN

        else:   # if mdata.win_cond == gi.WinCond.TIE:
            mdata.win_cond = gi.WinCond.ROUND_TIE


class RoundLoserFillWinner(EndTurnIf):
    """End the game if the loser cannot fill the required
    number of holes or the winner's side of the board is
    not playable."""

    def __init__(self, game, decorator=None, sclaimer=None):

        super().__init__(game, decorator, sclaimer)

        nbr_start = game.cts.nbr_start

        intro = "Game, not round, ended (_loser_ has too few seeds to fill "
        goal_param = game.info.goal_param

        if goal_param > 0:
            self.req_seeds = game.info.goal_param * nbr_start
            self.msg = intro + f"at least {goal_param} holes)."

        else:
            self.req_seeds = nbr_start
            self.msg = intro + "a hole)."


    def __str__(self):
        return self.str_deco_detail(repr(self.sclaimer) + '\n   '
                                    + f'req_seeds: {self.req_seeds}')


    def _winner_playable(self, mdata):
        """Return true if the winner's side is playable."""

        with self.game.save_restore_state():

            self.game.turn = mdata.winner
            return any(self.game.get_allowable_holes())


    def game_ended(self, mdata):

        ended_in = mdata.ended
        self.decorator.game_ended(mdata)
        if (ended_in is True
            or not mdata.win_cond
            or mdata.win_cond == gi.WinCond.TIE):
            return

        # loser must have sufficient seeds to fill a hole
        seeds = self.sclaimer.claim_seeds()
        if seeds[not mdata.winner] < self.req_seeds:
            mdata.add_end_msg(self.msg)
            game_log.add(self.msg, game_log.IMPORT)
            return

        # winner side must be playable
        if not self._winner_playable(mdata):
            msg = 'Winner side is unplayable; game, not round, ended.'
            mdata.add_end_msg(msg)
            game_log.add(msg, game_log.IMPORT)
            return

        mdata.win_cond = gi.WinCond.ROUND_WIN


class RoundTallyWinner(EndTurnIf):
    """"If the game is played in rounds, let the rest of the
    chain decide the outcome, then adjust for end of game or
    end of round based on the tallier."""


    def tally_prog_msg(self, mdata, win):
        """Add progress toward win to the end message"""

        rtally = self.game.rtally

        msg = ''
        earned = rtally.parameter(mdata.winner)
        needed = rtally.required_win
        plr = '' if earned == 1 else 's'

        match [self.game.info.goal, win]:

            case ([gi.Goal.RND_WIN_COUNT_MAX, False] |
                  [gi.Goal.RND_WIN_COUNT_CLR, False] |
                  [gi.Goal.RND_WIN_COUNT_DEP, False] |
                  [gi.Goal.RND_WIN_COUNT_IMB, False]):
                msg += f"""_Winner_ has {earned} round win{plr}"""

            case [gi.Goal.RND_SEED_COUNT, False]:
                msg += f"""_Winner_ has {earned} seed{plr}"""

            case [gi.Goal.RND_EXTRA_SEEDS, _]:

                msg += f"_Winner_ collected {rtally.extra} extra seeds"
                if not win and rtally.extra < earned:
                    msg += f" and has accumulated {earned}"

            case [gi.Goal.RND_POINTS, _]:

                if rtally.points == 1:
                    msg += fmt.LINE_SEP if mdata.end_msg else ''
                    msg += f"_Winner_ earned {rtally.points} point"
                else:
                    msg += f"""_Winner_ earned {rtally.points} points
                            due to skunk (>= {rtally.skunk_seeds})"""
                if not win and rtally.points < earned:
                    msg += f" and has {earned}"

        if msg:
            if win:
                msg += '.'
            else:
                msg += f" towards {needed} needed."
            mdata.add_end_msg(msg, 'force')


    def game_ended(self, mdata):
        """ended can be truthy, but only actually end the game
        if it exactly True; otherwise we are going to end the
        round."""

        ended_in = mdata.ended
        self.decorator.game_ended(mdata)
        if not mdata.win_cond:
            return

        seeds = self.sclaimer.claim_seeds()
        self.game.rtally.tally(mdata, seeds)

        if ended_in is True:
            rcond, rplayer = self.game.rtally.end_it()
        else:
            rcond, rplayer = self.game.rtally.win_test()

        if rcond and rcond.is_game_over():
            mdata.win_cond = rcond
            mdata.winner = rplayer

            if rcond == gi.WinCond.WIN:
                self.tally_prog_msg(mdata, win=True)

        elif mdata.win_cond == gi.WinCond.WIN:
            mdata.win_cond = gi.WinCond.ROUND_WIN
            self.tally_prog_msg(mdata, win=False)

        else:  #  if mdata.win_cond == gi.WinCond.TIE:
            mdata.win_cond = gi.WinCond.ROUND_TIE


# %% build ender


def _build_eliminate_ended(game):
    """Build the ender for eliminate games."""

    if game.info.goal in (gi.Goal.CLEAR,
                          gi.Goal.RND_WIN_COUNT_CLR):
        ender = ClearSeedsEndGame(game)

    elif game.info.goal in (gi.Goal.DEPRIVE,
                            gi.Goal.RND_WIN_COUNT_DEP):
        ender = EndTurnNoMoves(game)
        ender = DepriveEndGame(game, ender)

    elif game.info.goal in (gi.Goal.IMMOBILIZE,
                            gi.Goal.RND_WIN_COUNT_IMB):
        ender = ImmobilizeEndGame(game)

    else:
        raise NotImplementedError(f"Unknown eliminate goal: {game.info.goal}")

    if game.info.goal in (gi.Goal.RND_WIN_COUNT_CLR,
                          gi.Goal.RND_WIN_COUNT_DEP,
                          gi.Goal.RND_WIN_COUNT_IMB):
        sclaimer = claimer.ClaimBoardSeeds(game)
        ender = _add_round_ender(game, ender, sclaimer)

    return ender


def _add_end_game_winner(game):
    """Start the deco chain by adding the EndGameWinner.
    Select a claimer based on how the unclaimed seeds
    should be scored.  Some of the claimers create
    lambda's to look the actual player later.

    EndGameMustShare does the taker if seeds can't be shared,
    so this uses the default taker.
    If the ender is UNFED_PLAYER, use the configuration
    for the quitter."""

    condition = game.info.unclaimed
    if  game.info.unclaimed == gi.EndGameSeeds.UNFED_PLAYER:
        condition = game.info.quitter

    if game.info.round_fill == gi.RoundFill.LOSER_ONLY:
        sclaimer = claimer.ClaimOwnSeeds(game)

    elif game.info.no_sides or condition == gi.EndGameSeeds.DONT_SCORE:
        sclaimer = claimer.TakeOnlyChildNStores(game)

    elif condition == gi.EndGameSeeds.HOLE_OWNER:
        sclaimer = claimer.TakeOwnSeeds(game)

    elif condition == gi.EndGameSeeds.LAST_MOVER:
        sclaimer = claimer.TakeAllUnclaimed(game)

    elif condition == gi.EndGameSeeds.DIVVIED:
        sclaimer = claimer.DivvySeedsStores(game)

    else:
        raise NotImplementedError(
                f"Unclaimed {game.info.unclaimed} not implemented.")

    return EndGameWinner(game, sclaimer=sclaimer)


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
            ginfo.sow_stores,

            # game ends when a player has no seeds and opp can't share
            ginfo.mustshare and not ginfo.mustpass,

            # end_cond and picks take care of ending game
            ginfo.end_cond,
            ginfo.pickextra == gi.CaptExtraPick.PICKLASTSEEDS,
            ginfo.pickextra == gi.CaptExtraPick.PICK2XLASTSEEDS,

            # seeds only moved to children, no stores
            (game.info.child_type.child_but_not_ram()
             and not game.info.stores),

            # if can only capture from children
            (ginfo.child_type == gi.ChildType.WEG
             and not any([ginfo.capt_max,
                          ginfo.capt_min,
                          ginfo.capt_on,
                          ginfo.capt_type,
                          ginfo.crosscapt,
                          ginfo.evens,
                          ginfo.sow_stores]))]):
        return ender

    min_seeds = NoOutcomeChange.min_for_change(game)

    if game.info.min_move < min_seeds < game.cts.total_seeds:
        ender = NoOutcomeChange(game, min_seeds, ender)

    return ender


def _add_must_share_ender(game, ender):
    """Add the must share ender. If the scoring of unclaimed
    seeds is UNFED_PLAYER, provide a seed taker to
    do that. Otherwise, provide a claimer that does nothing."""

    if game.info.unclaimed == gi.EndGameSeeds.UNFED_PLAYER:
        sclaimer = claimer.TakeAllUnclaimed(game)

    else:
        sclaimer = claimer.ClaimSeeds(game)

    return EndTurnMustShare(game, ender, sclaimer)


def _add_round_ender(game, ender, sclaimer):
    """Add the round ender."""

    if (game.info.rounds in (gi.Rounds.END_S_SEEDS,
                             gi.Rounds.END_2S_SEEDS)
            and game.info.pickextra not in (gi.CaptExtraPick.PICKLASTSEEDS,
                                            gi.CaptExtraPick.PICK2XLASTSEEDS)):
        # only need RoundEndLimit when a picker is not doing the same work
        ender = EndSeedsLimit(game, ender)

    # the claimer here decides if game or round ends; after we know it ended
    if game.info.goal in round_tally.RoundTally.GOALS:
        # use the same claimer as for clear winner
        ender = RoundTallyWinner(game, ender, sclaimer)

    elif game.info.round_fill == gi.RoundFill.LOSER_ONLY:
        ender = RoundLoserFillWinner(game, ender, claimer.ClaimOwnSeeds(game))

    else:
        # use claim all seeds in owned holes (might be side or owner)
        ender = RoundWinner(game, ender, claimer.ClaimOwnSeeds(game))

    return ender


def _add_game_ender(game, ender):
    """Add an additional ender condition."""

    if (game.info.end_cond == gi.EndGameCond.SEEDS_LIMIT
            and game.info.rounds not in (gi.Rounds.END_S_SEEDS,
                                         gi.Rounds.END_2S_SEEDS)):
        # don't add if we have a limit based on round end
        ender = EndSeedsLimit(game, ender)

    elif game.info.end_cond in (gi.EndGameCond.CLEARED_OWN,
                                gi.EndGameCond.CLEARED_OPP):
        ender = ClearedSideEnder(game, ender)

    elif game.info.end_cond == gi.EndGameCond.HOLE_SEED_LIMIT:
        ender = HoleSeedsLimit(game, ender)

    else:
        raise NotImplementedError(
                f"END_COND {game.info.end_cond} not implemented.")

    return ender


def _build_ender(game):
    """Build the ender for non eliminate games."""

    ender = _add_end_game_winner(game)

    if game.info.mustpass:
        ender = EndTurnPassPass(game, ender)
    else:
        ender = EndTurnNoMoves(game, ender)

    if game.info.mustshare and not game.info.mustpass:
        ender = _add_must_share_ender(game, ender)

    ender = EndTurnNotPlayable(game, ender)
    ender = _add_no_change(game, ender)

    if game.info.child_type.child_but_not_ram():
        sclaimer = claimer.ChildClaimSeeds(game)
    else:
        sclaimer = claimer.ClaimSeeds(game)
    ender = ClearWinner(game, ender, sclaimer)

    if game.info.end_cond:
        ender = _add_game_ender(game, ender)

    if game.info.rounds:
        ender = _add_round_ender(game, ender, sclaimer)

    if (game.info.child_type.child_but_not_ram()
            and not game.info.stores):
        ender = ChildNoStoresEnder(game, ender)

    return ender


def deco_end_move(game):
    """Return a chain of move enders."""

    if game.info.goal.eliminate():
        ender = _build_eliminate_ended(game)

    else:
        ender = _build_ender(game)

    if animator.ENABLED:
        ender = AnimateEndMove(game, ender)

    return ender


# %%  build quitter


def pick_base_quitter(game):
    """Pick the base quitter."""

    sclaimer = None
    quitter = None

    if game.info.goal.eliminate():
        quitter = QuitToTie(game)

    elif game.info.quitter == gi.EndGameSeeds.HOLE_OWNER:
        sclaimer = claimer.TakeOwnSeeds(game)

    elif game.info.quitter == gi.EndGameSeeds.DONT_SCORE:
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
            quitter = QuitToTie(game)

    else:
        raise NotImplementedError(
                f"Quitter {game.info.unclaimed} not implemented.")

    if not quitter:
        quitter = EndGameWinner(game, sclaimer=sclaimer)

    return quitter


def deco_quitter(game):
    """Return a quitter. Used when either the user quit game or
    the game reached an ENDLESS condition. Base the quitter behavior
    on the goal type and quitter parameter in game info."""

    quitter = pick_base_quitter(game)

    if game.info.goal in round_tally.RoundTally.GOALS:
        # ChildClaimSeeds will work for both children games and not
        # the divvier on EndGameWinner did the divvying work
        quitter = RoundTallyWinner(game,
                                       quitter,
                                       sclaimer=claimer.ChildClaimSeeds(game))
    elif game.info.rounds:
        quitter = RoundWinner(game,
                                  quitter,
                                  sclaimer=claimer.ChildClaimSeeds(game))

    if animator.ENABLED:
        quitter = AnimateEndMove(game, quitter)

    return quitter
