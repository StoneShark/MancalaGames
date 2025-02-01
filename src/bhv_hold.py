# -*- coding: utf-8 -*-
"""Button and store behavior classes that use
Hold global data.

Created on Sun Aug 13 10:06:37 2023
@author: Ann"""

# pylint: disable=duplicate-code

import tkinter as tk
import textwrap

import behaviors as bhv
import man_config
from game_logger import game_log


# %%  global data for movers

class Hold:
    """Global data to store and manage the seed holding data.

    This is not intended to be instatiated or used outside this file."""

    active = False
    nbr = 0
    owner = None

    _game_ui = None
    _label = None


    @staticmethod
    def set_hold(nbr, owner):
        """Set the hold data and update the UI label"""
        Hold.nbr = nbr
        Hold.owner = owner
        Hold._label.config(text=f'Seeds: {Hold.nbr}\nRow: {Hold.owner}')


    @staticmethod
    def empty():
        """Remove seeds and owner."""
        Hold.nbr = 0
        Hold.owner = None
        if Hold._label:
            Hold._label.config(text=f'Seeds: {Hold.nbr}\nRow: na')


    @staticmethod
    def query_nbr_seeds(owner, max_seeds):
        """Get the number of seeds from the user.
        Store them in the hold, but the board is not updated."""

        if max_seeds == 1:
            Hold.set_hold(Hold.nbr + 1, owner)
            return 1

        nbr = tk.simpledialog.askinteger(
            'Pickup Seeds',
            f'How many seeds to pick up (1 .. {max_seeds})?')
        if not nbr or nbr <= 0 or nbr > max_seeds:
            Hold._game_ui.bell()
            return 0

        Hold.set_hold(Hold.nbr + nbr, owner)
        return nbr


    @staticmethod
    def hold_menu(game_ui, message=None):
        """Fill the right status frame with controls."""

        Hold.active = True
        Hold._game_ui = game_ui
        frame = game_ui.rframe

        text = 'Right click to pick seeds up.\n' + \
               'Left click to drop seeds from the hold.\n'
        if message:
            text = message + '\n' + text

        tk.Label(frame, anchor='nw', justify='left', text=text
                 ).pack(side='top', expand=True, fill='both')

        text = f'Seeds: {Hold.nbr}\nRow: {Hold.owner}'
        Hold._label = tk.Label(frame, anchor='nw', justify='left', text=text)
        Hold._label.pack(side='top', expand=True, fill='both')
        tk.Button(frame, text='Done', command=Hold.done
                  ).pack(side='bottom')


    @staticmethod
    def destroy_ui():
        """Remove the children we created in rframe.
        Clear local access to them."""

        for child in Hold._game_ui.rframe.winfo_children():
            child.destroy()
        Hold._label = None


    @staticmethod
    def done():
        """Go back to game play mode."""

        if Hold.active and Hold._game_ui.set_gameplay_mode():
            Hold.destroy_ui()


    @staticmethod
    def cleanup():
        """Abandoning the game mode, cleanup."""

        if Hold.active:
            Hold.active = False
            Hold.empty()
            Hold.destroy_ui()


    @staticmethod
    def warn_not_empty(game_ui):
        """If the hold is not empty warn the user and return True,
        otherwise return False."""

        if Hold.nbr:
            tk.messagebox.showerror(
                title='Game Mode',
                message='Hold is not empty; '
                'place seeds before returning to game mode.',
                parent=game_ui)
            return True

        return False


# %% button behaviors

class RndChooseButtonBehavior(bhv.BehaviorIf):
    """Round setup behavior. Choose which holes are blocked.

    Moving seeds is enabled on the side with blocked holes."""

    @classmethod
    def ask_mode_change(cls, game_ui):

        if not any(game_ui.game.blocked):
            return False

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message=textwrap.fill(textwrap.dedent("""\
                A new round is begining, so you may
                change the blocked holes on the loser's of the
                board. Do you wish to
                rearrange the blocks?"""), width=bhv.FILL_POPUP),
                    parent=game_ui)

        if ans != bhv.YES_STR:
            return False

        Hold.hold_menu(game_ui,
                       textwrap.fill(textwrap.dedent("""\
                           Move seeds out of holes you wish to block
                           and into other holes."""), width=bhv.FILL_HINTS))

        cls.starter = game_ui.game.turn
        loser = any(game_ui.game.blocked[l]
                    for l in range(game_ui.game.cts.holes,
                                   game_ui.game.cts.dbl_holes))
        game_ui.game.turn = loser
        return True


    @classmethod
    def leave_mode(cls, game_ui):

        if Hold.warn_not_empty(game_ui):
            return False

        # revert to the round starter that was saved
        game_ui.game.turn = cls.starter
        return True


    def set_props(self, props, bstate):
        """Set props and state of the hole."""
        self.btn.props = props
        self._refresh(bstate)


    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't drop seeds if:
            1. there are no seeds in the hold
            2. there are already seeds in the hole
            3. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if not Hold.nbr or self.btn.props.seeds or Hold.owner != self.btn.row:
            self.btn.bell()
            return

        game = self.btn.game_ui.game
        game.board[self.btn.loc] = Hold.nbr
        game.blocked[self.btn.loc] = False

        self.btn.props.blocked = False
        self.btn.props.seeds = Hold.nbr
        self._refresh()

        Hold.empty()
        self.btn.frame.config(cursor='')


    def right_click(self):
        """Pick up all of the seeds in the hole,
        unless we are already holding seeds
        or there are not any seeds to pick up."""

        if self.btn['state'] == tk.DISABLED:
            return
        if Hold.nbr or not self.btn.props.seeds:
            self.btn.bell()
            return

        Hold.set_hold(self.btn.props.seeds, self.btn.row)

        game = self.btn.game_ui.game
        game.board[self.btn.loc] = 0
        game.blocked[self.btn.loc] = True

        self.btn.props.blocked = True
        self.btn.props.seeds = 0
        self._refresh()

        self.btn.frame.config(cursor='circle')


    def _refresh(self, bstate=bhv.BtnState.ACTIVE):
        """Make the UI match the behavior and game data."""
        self.refresh_nonplay(bstate, man_config.CONFIG['choose_color'])



class RndMoveSeedsButtonBehavior(bhv.BehaviorIf):
    """Any number of seeds my placed on the board (by the loser)
    each hole must contain at least one seed. Extra seeds may be
    left in the store. Seeds cannot be moved from one side to
    the other.
    Winner's seeds will be arranged the same."""

    starter = None
    loser = None

    @classmethod
    def ask_mode_change(cls, game_ui):
        """If the user wants to enter move mode, need to collect
        some data; need to save it in the class.

        Save turn as the starter and set the turn to the loser.
        We know that new_game left the board sides equal,
        so we can compare the stores to determine the loser.

        Note that we never go into this move mode without going
        through this function and the leave_mode function can
        undo the local changes."""

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message=textwrap.fill(textwrap.dedent("""\
                  The loser may
                  arrange the playable seeds with the restrictions that each
                  hole contain at least one seed and one hole is playable.
                  Seeds maybe added or removed from the store.
                  The winner's seeds will be arranged the same way.
                  Do you wish to rearrange the seeds?"""),
                  width=bhv.FILL_POPUP),
            parent=game_ui)

        if ans != bhv.YES_STR:
            return False

        Hold.hold_menu(game_ui,
                       textwrap.fill(textwrap.dedent("""\
                           Each hole must contain at least one seed and
                           at least one hole must be playable."""),
                           width=bhv.FILL_HINTS))

        cls.starter = game_ui.game.turn
        cls.loser = game_ui.game.store[0] > game_ui.game.store[1]
        game_ui.game.turn = cls.loser

        return True


    @classmethod
    def leave_mode(cls, game_ui):

        game = game_ui.game
        holes = game.cts.holes
        dbl_holes = game.cts.dbl_holes

        if Hold.warn_not_empty(game_ui):
            return False

        if cls.loser:
            loser_slice = slice(holes, dbl_holes)
            winner_slice = slice(0, holes)
        else:
            loser_slice = slice(0, holes)
            winner_slice = slice(holes, dbl_holes)

        if not any(seeds >= game.info.min_move
                   for seeds in game.board[loser_slice]):
            tk.messagebox.showerror(
                title='Game Mode',
                message=textwrap.fill(textwrap.dedent(f"""\
                    None of the holes have min_moves seeds
                    ({game.info.min_move}); thus the game is not playable.
                    Move more seeds back from store."""), width=40),
                parent=game_ui)
            return False

        start_seeds = sum(game.board[winner_slice])
        game.board[winner_slice] = game.board[loser_slice]
        game.store[not cls.loser] += (start_seeds -
                                      sum(game.board[winner_slice]))

        # revert to the round starter that was saved
        game_ui.game.turn = cls.starter

        return True


    def set_props(self, props, bstate):
        """Set text, props and states of the hole.
        Because we set turn to the loser, disable will be set
        True for the loser."""
        self.btn.props = props
        self._refresh(bstate)


    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't drop seeds if:
            1. there are no seeds in the hold
            2. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if not Hold.nbr or Hold.owner != self.btn.row:
            self.btn.bell()
            return

        game = self.btn.game_ui.game
        seeds = game.board[self.btn.loc] + Hold.nbr
        self.btn.props.seeds = seeds
        game.board[self.btn.loc] = seeds
        self._refresh()

        Hold.empty()
        self.btn.game_ui.config(cursor='')


    def right_click(self):
        """Pick up some or all of the seeds, but
            1. only on loser side (game.turn is winner, row is not turn;
                                   so loser row it game.turn)
            2. if there are seeds to pick up (must leave 1)
            3. another condition that doesn't make sense at the moment !?!?!?

            Always leave at least one seed in each hole."""
        if self.btn['state'] == tk.DISABLED:
            return

        game = self.btn.game_ui.game
        if (game.turn == self.btn.row
                or self.btn.props.seeds <= 1
                or Hold.owner not in (None, self.btn.row)):
            self.btn.bell()
            return

        max_seeds = self.btn.props.seeds - 1
        seeds = Hold.query_nbr_seeds(self.btn.row, max_seeds)

        if seeds:
            seeds = game.board[self.btn.loc] - seeds
            self.btn.props.seeds = seeds
            game.board[self.btn.loc] = seeds
            self._refresh()

            self.btn.game_ui.config(cursor='circle')


    def _refresh(self, bstate=bhv.BtnState.ACTIVE):
        """Make the UI match the behavior and game data."""
        self.refresh_nonplay(bstate, man_config.CONFIG['seed_color'])


class MoveSeedsButtonBehavior(bhv.BehaviorIf):
    """Move Seeds behavior. The seeds may be rearranged as
    desired by the first player though all seeds must be
    left in play. This movement counts as the player's turn.

    If the player doesn't change anything, they are disallowed
    from capturing or making children until the opponent does
    one of those.
    The decos are not in the GameInterface--deal with it!

    This is used for SowPrescribed.ARNGE_LIMIT (Bao)."""

    @classmethod
    def ask_mode_change(cls, game_ui):

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message=textwrap.fill(textwrap.dedent("""\
                  At the start of this game you may rearrange seeds on
                  your side of the board. Your opponents seeds will be
                  arranged the same. Rearranging seeds counts as your
                  first move. Do you wish to move any
                  seeds?"""), width=bhv.FILL_POPUP),
            parent=game_ui)

        if ans != bhv.YES_STR:
            game_ui.game.inhibitor.set_on(game_ui.game.turn)
            return False

        cls.saved_state = game_ui.game.state
        Hold.hold_menu(game_ui,
                       textwrap.fill(textwrap.dedent("""\
                           Rearrange the seeds on your side of the board;
                           no seeds may be put into the store.
                           Your opponents seeds will reflect your position."""),
                           width=bhv.FILL_HINTS))
        return True


    @classmethod
    def leave_mode(cls, game_ui):

        if Hold.warn_not_empty(game_ui):
            return False

        game = game_ui.game
        if game.state == cls.saved_state:
            game_log.add('No changes in arrangement mode.')
            game_ui.game.inhibitor.set_on(game_ui.game.turn)
            return True

        game_ui.game.inhibitor.set_off()
        holes = game.cts.holes
        dbl_holes = game.cts.dbl_holes

        if game.turn:
            moved_slice = slice(holes, dbl_holes)
            other_slice = slice(0, holes)
        else:
            moved_slice = slice(0, holes)
            other_slice = slice(holes, dbl_holes)
        game.board[other_slice] = game.board[moved_slice]

        # movement was the player's turn
        game.turn = not game.turn
        return True


    def set_props(self, props, bstate):
        """Set text, props and states of the hole."""
        self.btn.props = props
        self._refresh(bstate)


    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't drop seeds if:
            1. there are no seeds in the hold
            2. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if not Hold.nbr or Hold.owner != self.btn.row:
            self.btn.bell()
            return

        game = self.btn.game_ui.game
        seeds = game.board[self.btn.loc] + Hold.nbr

        game.board[self.btn.loc] = seeds
        self.btn.props.seeds = seeds
        self._refresh()

        Hold.empty()
        self.btn.frame.config(cursor='')


    def right_click(self):
        """Pick up some or all of the seeds."""
        if self.btn['state'] == tk.DISABLED:
            return

        if (not self.btn.props.seeds
                or Hold.owner not in (None, self.btn.row)):
            self.btn.bell()
            return

        max_seeds = self.btn.props.seeds
        seeds = Hold.query_nbr_seeds(self.btn.row, max_seeds)

        if seeds:
            game = self.btn.game_ui.game
            seeds = game.board[self.btn.loc] - seeds

            game.board[self.btn.loc] = seeds
            self.btn.props.seeds = seeds
            self._refresh()

            self.btn.frame.config(cursor='circle')


    def _refresh(self, bstate=bhv.BtnState.ACTIVE):
        """Make the UI match the behavior and game data."""
        self.refresh_nonplay(bstate, man_config.CONFIG['move_color'])


# %% store behavior

class RndMoveStoreBehavior(bhv.StoreBehaviorIf):
    """Seeds may be moved in and out of the loser's store.
    Cursor is changed on the whole game_ui, when holding seeds.

    Remember game.set(get)_store take a row not a turn or owner"""

    def set_store(self, seeds, highlight):
        """Set the properties of the store button."""

        self.str['state'] = tk.NORMAL if highlight else tk.DISABLED
        self.str['text'] = str(seeds) if seeds else ''

        if highlight:
            self.str['background'] = man_config.CONFIG['seed_color']
        else:
            self.str['background'] = man_config.CONFIG['system_color']


    def left_click(self):
        """Drop all picked up seeds."""

        if not Hold.nbr and Hold.owner == self.str.owner:
            self.str.bell()
            return

        game = self.str.game_ui.game
        seeds = game.store[self.str.owner] + Hold.nbr
        self.set_store(seeds, True)
        game.store[self.str.owner] = seeds

        self.str.game_ui.config(cursor='')
        Hold.empty()


    def right_click(self):
        """Pop up the nbr seeds query, and pickup seeds if
        the user entered a valid number."""

        game = self.str.game_ui.game
        seeds = game.store[self.str.owner]

        if (game.turn == self.str.owner
                and Hold.query_nbr_seeds(not self.str.owner, seeds)):

            game = self.str.game_ui.game
            seeds -= Hold.nbr
            self.set_store(seeds, True)
            game.store[self.str.owner] = seeds

            self.str.game_ui.config(cursor='circle')
