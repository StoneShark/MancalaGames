# -*- coding: utf-8 -*-
"""A game class that implements a unique must share:
if at the start of your turn your opponent does not have
seeds you must take one from a hole with two or more seeds
and put it in their leftmost hole.

Created on Wed Jul  2 08:58:07 2025
@author: Ann"""

import animator
import game_info as gi
import mancala
import rule_tester
import sower

from game_logger import game_log


# %%   rules

def test_rules(ginfo, holes, skip):
    """Rules specific to ShareOne then call mancala rules.

    ShareOneAllow deco was not written to support triples
    and it is inserted before the allowables.Allowable deco;
    thus, no_sides and territory are imcompatible.

    Always put seeds in leftmost hole in ShareOneSow,
    without checking for blocks; thus no blocks.

    Odd to have mustshare and ShareOne, just don't allow it.
    """

    tester = rule_tester.RuleTester(ginfo, holes, skip)

    tester.test_rule(
        's1_no_sides',
        rule=lambda ginfo: ginfo.no_sides,
        msg='ShareOne is incompatible with NO_SIDES',
        excp=gi.GameInfoError)

    tester.test_rule('s1_noterr',
        rule=lambda ginfo: ginfo.goal == gi.Goal.TERRITORY,
        msg="ShareOne is incompatible with TERRITORY games",
        excp=gi.GameInfoError)

    tester.test_rule(
        's1_no_blocks',
        rule=lambda ginfo: ginfo.blocks,
        msg='ShareOne is incompatible with BLOCKS',
        excp=gi.GameInfoError)

    tester.test_rule(
        's1_no_ms',
        rule=lambda ginfo: ginfo.mustshare,
        msg='ShareOne is incompatible with MUSTSHARE',
        excp=gi.GameInfoError)

    tester.test_rule(
        's1_no_rturn',
        rule=lambda ginfo: ginfo.repeat_turn,
        msg="""ShareOne is incompatible with any repeat turn--it
            is used to perform a normal move after a share one move""",
        excp=gi.GameInfoError)

    mancala.Mancala.rules(ginfo, holes, skip=skip)


# %% new decos


class ShareOneSow(sower.SowMethodIf):
    """When the opponent does not have any seeds, the move
    is to share one seed into the opponent's left most hole.
    Then do a repeat turn to do a real move."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        opp_range = self.game.cts.get_opp_range(self.game.turn)

        if any(self.game.board[loc] for loc in opp_range):
            self.decorator.sow_seeds(mdata)

        else:
            loc = mdata.cont_sow_loc
            self.game.board[loc] = mdata.seeds - 1

            oloc = min(opp_range)
            self.game.board[oloc] += 1

            mdata.repeat_turn = True

            game_log.add(f"Sharing from {loc} to {oloc}", game_log.DETAIL)


# %%  game class

class ShareOne(mancala.Mancala):
    """A game class that supports sharing one seed from a hole
    with two or more seeds to an opponent without seeds.

    The user gets to choose which hole the seed comes from,
    and repeat turn is used to then allow a normal turn."""

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """Test the rules. This is run before the game class
        is created."""
        test_rules(ginfo, holes, skip)


    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        self.deco.sower = ShareOneSow(self, self.deco.sower)


    def move(self, move):
        """Popup an animation message if the next move is to
        share one seed."""

        rval = super().move(move)

        # turn has been changed to next player
        opp_range = self.cts.get_opp_range(self.turn)
        if (not rval
                and not any(self.board[loc] for loc in opp_range)
                and animator.active()):
            animator.do_message("Must Share a Seed")

        return rval


    def get_allowable_holes(self):
        """When the opponent does not have any seeds, filter
        allowable holes to only those with 2 or more seeds
        that are not children.

        Blocks are not allowed, so don't need to check."""

        opp_range = self.cts.get_opp_range(self.turn)

        if any(self.board[loc] for loc in opp_range):
            return super().get_allowable_holes()

        row = not self.turn
        allow = [False] * self.cts.holes
        for pos in range(self.cts.holes):

            loc = self.cts.xlate_pos_loc(row, pos)
            allow[pos] = self.board[loc] >= 2 and self.child[loc] is None

        return allow
