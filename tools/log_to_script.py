# -*- coding: utf-8 -*-
"""Convert a log file into a test file.

THIS DOES NOT ASSURE THAT THE TEST IS CORRECT!!
The log must be carefully reviewed to assure correctness.

Created on Wed Aug 16 13:25:51 2023
@author: Ann"""

import argparse
import enum
import contextlib
import re
import sys


class CondAction(enum.Enum):
    """What action to take based on the game condition."""
    DONE = enum.auto()
    CONTINUE = enum.auto()
    RESTART = enum.auto()


TURN = '*'
BLOCK = 'x'
LOCK = '_'
UP = '\u02c4'
DN = '\u02c5'
TOP = 'Top'

OWNT = '\u2191'
OWNF = '\u2193'


WIN = 'WIN'
TIE = 'TIE'
PASS = 'PASS'

GAMECONST_RE = re.compile(r'GameConsts.nbr_start=([0-9]+), holes=([0-9]+)')

MOVE_RE = re.compile(r'^([0-9]+):.*move (PASS|([0-9]+)|(\(.+\)))( )?([A-Z_]+)?')

COND_LINE_RE = re.compile(r'^(ROUND_WIN|WIN|ROUND_TIE|TIE)( by (Top|Bottom))?')

STORE_RE = re.compile(r'([0-9]*) ?([A-Z_]+)?$')
BOARD_RE = re.compile(r'([0-9x]+)([ _˄˅↑↓]*) ')


SHORT_VALS = {None: 'N', False: 'F', True: 'T'}



def get_board_params(line_iter):
    """Get the start seeds per hole and size of the board."""

    line = next(line_iter)
    while 'GameConsts' not in line:
        line = next(line_iter)

    match = GAMECONST_RE.search(line)
    groups = match.groups()
    start_seeds = int(groups[0])
    holes = int(groups[1])

    return start_seeds, holes


def find_first_move(line_iter):
    """skip to the begining of the game,
    Return True if we found the start, else False"""

    while True:
        line = next(line_iter)
        if '0: Start' in line:
            return True

    assert False, "Starting move not found in the log."


def child_val(spec):
    """Return any child ownership."""

    if UP in spec:
        return True
    if DN in spec:
        return False
    return None


def owner_val(spec):
    """Return any hole ownership."""

    if OWNT in spec:
        return True
    if OWNF in spec:
        return False
    return None


def get_short_str(in_list):
    """Use the short names"""
    return '[' + ', '.join(SHORT_VALS[v] for v in in_list) + ']'


def print_indent(lvl, *pargs):
    """indent the prints by lvl spaces"""

    print(' ' * (lvl * 4), end='')
    print(*pargs)


def process_board(holes, true_line, false_line):
    """convert two game lines to asserts."""
    # pylint: disable=too-many-locals

    # check the board settings
    board_t = list(reversed(BOARD_RE.findall(true_line)))[:holes]
    board_f = BOARD_RE.findall(false_line)[:holes]

    board = [int(seeds) if seeds != BLOCK else 0
             for seeds, _ in board_f] + \
            [int(seeds) if seeds != BLOCK else 0
             for seeds, _ in board_t]
    blocked = [seeds == BLOCK for seeds, _ in board_f] + \
              [seeds == BLOCK for seeds, _ in board_t]
    unlocked = [LOCK not in spec for _, spec in board_f] + \
               [LOCK not in spec for _, spec in board_t]
    child = [child_val(spec) for _, spec in board_f] + \
            [child_val(spec) for _, spec in board_t]
    owner = [owner_val(spec) for _, spec in board_f] + \
            [owner_val(spec) for _, spec in board_t]

    blocked = get_short_str(blocked)
    unlocked = get_short_str(unlocked)
    child = get_short_str(child)
    owner = get_short_str(owner)

    print_indent(2, f'assert game.board == {board}')
    print_indent(2, f'assert game.blocked == {blocked}')
    print_indent(2, f'assert game.unlocked == {unlocked}')
    print_indent(2, f'assert game.child == {child}')
    print_indent(2, f'assert game.owner == {owner}')

    # check the stores
    store_m_t = STORE_RE.search(true_line)
    store_m_f = STORE_RE.search(false_line)
    store_t_str, store_f_str = store_m_t.groups()[0], store_m_f.groups()[0]
    store_t = int(store_t_str) if store_t_str else 0
    store_f = int(store_f_str) if store_f_str else 0
    print_indent(2, f'assert game.store == [{store_f}, {store_t}]')


def set_start(holes, line_iter):
    """Parse the initial board and set the start conditions"""

    true_line = next(line_iter)
    false_line = next(line_iter)

    turn = TURN in true_line
    print_indent(1, 'def test_game_setup(self, gstate):')
    print_indent(2, 'game = gstate.game')
    print_indent(2, f'game.turn = {turn}')
    print_indent(2, f'game.starter = {turn}')

    process_board(holes, true_line, false_line)


def write_test_board(holes, true_line, false_line):
    """Parse the two lines and write the assert tests."""

    # check the turn
    turn = TURN in true_line
    print_indent(2, f'assert game.turn is {turn}')

    process_board(holes, true_line, false_line)


def find_move_start(line_iter):
    """Find the start of the next move and parse out
    the move number, move string and result."""

    while True:
        line = next(line_iter)
        if 'GRAND' in line:
            print_indent(2, '# ', line)
        match = MOVE_RE.search(line)
        if match:
            break

    groups = match.groups()
    return groups[0], groups[1], groups[-1]


def get_board_lines(line_iter):
    """We are the start of a board read the three possible lines."""

    cond_line = None
    true_line = next(line_iter)
    if WIN in true_line or TIE in true_line:
        cond_line = true_line
        true_line = next(line_iter)
    false_line = next(line_iter)

    return cond_line, true_line, false_line


def write_move_call(move_str):
    """Given the move string, output the call to game.move:

    PASS needs to be translated to PASS_TOKEN
    otherwise use move_str"""

    if move_str == PASS:
        print_indent(2, 'cond = game.move(gi.PASS_TOKEN)')
    else:
        print_indent(2, f'cond = game.move({move_str})')


def write_cond_assert(result, cond_line):
    """write the assert for the move call result.
    Return the action to perform based on the condition:
        continue
        new_round the move numbering
        done - the game is over."""

    action = CondAction.CONTINUE
    if result:
        print_indent(2, f'assert cond.name == "{result}"')

    elif cond_line:
        match = COND_LINE_RE.search(cond_line)
        assert match, "Unexpected game cond line: " + cond_line
        mgroups = match.groups()
        rname = mgroups[0]
        print_indent(2, f'assert cond.name == "{rname}"')

        if TIE in rname:
            print_indent(2, 'assert game.mdata.winner is None')

        if len(mgroups) == 3 and mgroups[2]:
            winner = mgroups[2] == TOP
            print_indent(2, f'assert game.mdata.winner is {winner}')

        action = CondAction.DONE if rname in (WIN, TIE) else CondAction.RESTART

    else:
        print_indent(2, 'assert cond is None')
    print_indent(2, 'gstate.cond = cond')

    return action


def gen_test_code(lines):
    """Load the file and write the move commands & asserts."""

    line_iter = iter(lines)
    _, holes = get_board_params(line_iter)
    find_first_move(line_iter)
    set_start(holes, line_iter)

    round_no = 1
    turn_no = 1
    while True:

        print()
        print_indent(1, f'def test_round_{round_no}_move_{turn_no}(self, gstate):')
        print_indent(2, 'game = gstate.game')
        mnbr_str, move_str, result = find_move_start(line_iter)
        assert int(mnbr_str) == turn_no, f'file error {mnbr_str} != {turn_no}'

        write_move_call(move_str)

        cond_line, true_line, false_line = get_board_lines(line_iter)
        write_test_board(holes, true_line, false_line)
        action = write_cond_assert(result, cond_line)

        if action == CondAction.CONTINUE:
            turn_no += 1
        elif action == CondAction.RESTART:
            round_no += 1
            print()
            print_indent(1, f'def test_round_{round_no}_setup(self, gstate):')
            print_indent(2, 'game = gstate.game')
            print_indent(2, 'game.new_game(gstate.cond, new_round_ok=True)')
            find_first_move(line_iter)
            cond_line, true_line, false_line = get_board_lines(line_iter)
            write_test_board(holes, true_line, false_line)
            turn_no = 1
        else:
            break


def start_generator(logfile, testfile):
    """Load the file and redirect stdout and call the generator."""

    with open(logfile, 'r', encoding='utf-8') as ifile:
        lines = ifile.readlines()

    with open(testfile, 'w', encoding='utf-8') as ofile:
        with contextlib.redirect_stdout(ofile):
            gen_test_code(lines)


def get_args():
    """Define the parser and use it to get input and output files."""

    parser = argparse.ArgumentParser()
    parser.add_argument('logfile')
    parser.add_argument('testfile')

    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    return cargs


if __name__ == '__main__':

    args = get_args()
    start_generator(args.logfile, args.testfile)
