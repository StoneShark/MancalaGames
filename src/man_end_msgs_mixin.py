# -*- coding: utf-8 -*-
"""Generate messages from the game for the ui.

Created on Fri Jun  6 09:23:25 2025
@author: Ann"""

import end_move_decos as emd
import format_msg as fmt
import game_interface as gi
from game_logger import game_log


class ManMsgsMixin:
    """Generate the end game messages."""


    def end_message(self, rtext, quitter):
        """Choose a suitable warning message before ending a game.
        Tell the user in general terms what will happen."""

        if quitter:
            deco = self.deco.quitter
            while deco and not isinstance(deco, emd.QuitToTie):
                deco = deco.decorator
            if deco:
                return f'The {rtext} will end in a tie.'

        param = 'quitter' if quitter else 'unclaimed'
        method = getattr(self.info, param)

        deco_name = 'quitter' if quitter else 'ender'
        concede = isinstance(getattr(self.deco, deco_name), emd.ConcedeMixin)

        message = 'Unclaimed seeds will '
        if ((not quitter and concede)         # generalization but good now
                or method == gi.EndGameSeeds.HOLE_OWNER):
            message += 'go to the hole owners'

        elif method == gi.EndGameSeeds.DONT_SCORE:
            message += 'not score for either player'

        elif method == gi.EndGameSeeds.LAST_MOVER:
            message += f'go to {gi.PLAYER_NAMES[self.mdata.player]}'

        elif method == gi.EndGameSeeds.UNFED_PLAYER:
            message += f'go to {gi.PLAYER_NAMES[not self.mdata.player]}'

        elif method == gi.EndGameSeeds.DIVVIED:
            message += """be divvied between the players (an odd seed will
                      go to player with fewer seeds)"""

        return message + '.'


    def _win_msg_subs(self, rtext):
        """Substitute the standard words in to the message created
        by decos or tallier. We don't always know the value of these
        tags when those messages are accumulated."""

        win = self.mdata.winner
        winner, loser = reversed(gi.PLAYER_NAMES) if win else gi.PLAYER_NAMES

        message = self.mdata.end_msg
        message = message.replace('_Winner_', winner)
        message = message.replace('_Loser_', loser)
        message = message.replace('_Thing_', rtext.capitalize())
        message = message.replace('_winner_', winner)
        message = message.replace('_loser_', loser)
        message = message.replace('_thing_', rtext)

        return message


    def _win_reason_str(self, win_cond):
        """Create the win reason string based on win_cond, game goal,
        and user ended game."""

        reason = '.'
        win_param = self.info.goal_param
        win_req = f"({win_param} required)"
        win_value = 0
        if self.rtally:
            win_value = self.rtally.parameter(self.mdata.winner)

        match [win_cond, self.info.goal, self.mdata.user_end]:

            case [gi.WinCond.ROUND_WIN, gi.Goal.MAX_SEEDS, _]:
                reason = " by collecting more seeds."

            case [gi.WinCond.WIN, gi.Goal.MAX_SEEDS, _]:
                reason = " by collecting the most seeds!"

            case [gi.WinCond.WIN, gi.Goal.TERRITORY, _]:
                reason = " by claiming more holes."

            case [gi.WinCond.WIN, gi.Goal.CLEAR, False]:
                reason = " by clearing all their seeds."

            case ([gi.WinCond.ROUND_WIN, gi.Goal.CLEAR, True] |
                  [gi.WinCond.WIN, gi.Goal.CLEAR, True]):
                reason = " because they had fewer seeds."

            case [gi.WinCond.WIN, gi.Goal.DEPRIVE, False]:
                loser = gi.PLAYER_NAMES[int(not self.mdata.winner)]
                reason = f" by eliminating {loser}'s seeds."

            case [gi.WinCond.WIN, gi.Goal.IMMOBILIZE, False]:
                loser = gi.PLAYER_NAMES[int(not self.mdata.winner)]
                reason = f" by immobilizing {loser}."

            case ([gi.WinCond.WIN, gi.Goal.DEPRIVE, True] |
                  [gi.WinCond.ROUND_WIN, gi.Goal.DEPRIVE, True] |
                  [gi.WinCond.WIN, gi.Goal.IMMOBILIZE, True] |
                  [gi.WinCond.ROUND_WIN, gi.Goal.IMMOBILIZE, True]):
                reason = " because they had more seeds."

            case [gi.WinCond.WIN, gi.Goal.RND_SEED_COUNT, True]:
                reason = " by collecting more seeds."

            case [gi.WinCond.WIN, gi.Goal.RND_SEED_COUNT, False]:
                reason = f" by collecting {win_value} total seeds {win_req}."

            case [gi.WinCond.WIN, gi.Goal.RND_EXTRA_SEEDS, True]:
                reason = " by accumulating more extra seeds per game."

            case [gi.WinCond.WIN, gi.Goal.RND_EXTRA_SEEDS, False]:
                reason = f" by accumulating {win_value} " \
                        + f"extra seeds per game {win_req}."

            case [gi.WinCond.WIN, gi.Goal.RND_POINTS, True]:
                reason = " by scoring more points."

            case [gi.WinCond.WIN, gi.Goal.RND_POINTS, False]:
                reason = f" by earning {win_value} points {win_req}."

            case ([gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_MAX, True] |
                  [gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_CLR, True] |
                  [gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_DEP, True] |
                  [gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_IMB, True]):
                reason = " by winning more rounds."

            case ([gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_MAX, False] |
                  [gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_CLR, False] |
                  [gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_DEP, False] |
                  [gi.WinCond.WIN, gi.Goal.RND_WIN_COUNT_IMB, False]):
                reason = f" by winning {win_value} rounds."

        return reason


    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message string."""

        rtext = 'the game'
        title = 'Game Over'
        if win_cond.is_round_over():
            rtext = 'the round'
            title = 'Round Over'

        message = ''
        if self.mdata.end_msg:
            message = self._win_msg_subs(rtext)
            if self.mdata.fmsg:
                return title, message

        message += fmt.LINE_SEP if message else ''

        if win_cond.is_win():
            message += gi.PLAYER_NAMES[int(self.mdata.winner)]
            message += ' won ' + rtext + self._win_reason_str(win_cond)

        elif win_cond.is_tie():
            if self.info.goal.eliminate() and not self.mdata.user_end:
                message += 'Both players ended with seeds; consider it a tie.'
            elif self.info.goal == gi.Goal.TERRITORY:
                message += 'Each player controls half the holes (a tie).'
            else:
                message += f'{rtext.title()} ended in a tie.'

        else:
            message += f'Unexpected end condition {win_cond and win_cond.name}.'

        game_log.add(fmt.fmsg(message), game_log.IMPORT)
        return title, message
