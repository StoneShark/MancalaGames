# -*- coding: utf-8 -*-
"""Does the UI render as expected and do the mouse clicks
behave as expected.

These tests do not run well from with in pytest,
generally 1 in 8 fails to find Tk.


Created on Mon Feb  3 07:30:40 2025
@author: Ann"""

# %% imports

import dataclasses as dc
import functools as ft
import time

from context import game_constants as gconsts
from context import game_interface as gi
from context import mancala
from context import mancala_ui

from context import game_logger


# %% constants

N = None
F = False
T = True

LEFT_CLICK = '<Button-1>'
RIGHT_CLICK = '<Button-3>'

LEFT = 'left'
RIGHT = 'right'
HIDDEN = 'hidden'
NORMAL = 'normal'

HOLES = 4
START = 3

ALL_HOLES = list(range(HOLES))
NONES = [N, N, N, N, N, N, N, N]

# %% support functions

def get_button(game_ui, loc):
    """Return the button object associated with loc."""

    row = int(loc < game_ui.game.cts.holes)
    pos = game_ui.game.cts.xlate_pos_loc(row, loc)

    return game_ui.disp[row][pos]


# %% dataclasses and config functions

@dc.dataclass
class GameOpts:
    """Options for creation of Mancala.
    GameInfo is too big and checks rules."""

    sow_dir: int = gi.Direct.CCW
    no_sides: bool = False
    udir_holes: list = dc.field(default_factory=list)
    mustshare: bool = False
    # TODO children

def make_game(game_opt):

    game_consts = gconsts.GameConsts(nbr_start=START, holes=HOLES)
    game_info = gi.GameInfo(stores=True,
                            evens=True,
                            sow_direct=game_opt.sow_dir,
                            no_sides=game_opt.no_sides,
                            mustshare=game_opt.mustshare,
                            udir_holes=game_opt.udir_holes,
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    return mancala.Mancala(game_consts, game_info)


@dc.dataclass
class SetupOpts:
    """Options for board configuration for test case."""
    turn: bool
    board: list
    owner: list

def setup_game(game, setup):

    game.turn = setup.turn
    game.board = setup.board.copy()
    game.owner = setup.owner.copy()

    quot, rem = divmod(game.cts.total_seeds - sum(game.board), 2)
    game.store = [quot, quot + rem]


@dc.dataclass
class UIOpts:
    """Options for the user interface."""

    facing_players: bool = False
    touch_screen: bool = False
    ownership_arrows: bool = False

def make_ui(game, ui_opt):

    game_ui = mancala_ui.MancalaUI(game, {})

    game_ui.vars.facing_players.set(ui_opt.facing_players)
    game_ui.vars.touch_screen.set(ui_opt.touch_screen)

    return game_ui


@dc.dataclass
class Action:
    """Click action description."""

    loc: int
    click: str
    on_tgrid: bool = False

def gen_event_fnc(game_ui, action):

    btn = get_button(game_ui, action.loc)

    if action.on_tgrid:
        x, y, *_ = btn.coords(btn.rclick_id)
        return ft.partial(btn.event_generate,
                          action.click,
                          x=x + 5, y=y + 5)

    return ft.partial(btn.event_generate, action.click)


@dc.dataclass
class ERender:
    """How a hole is expected to be rendered.
    rc_grid, rblock and lblock test visibility of grid."""

    rc_grid: bool = False
    rc_grid_loc: str = RIGHT

    rblock: bool = False   # can sow to player's right (not spec ccw or cw)
    lblock: bool = False   # can sow to player's left (not spec ccw or cw)

    rotate: bool = False


# %% test prolog and epilog

def test_setup(game_opt, setup, ui_opt):
    """Build the game and game_ui, and update the game_ui."""

    game = make_game(game_opt)
    game_logger.game_log.active = False
    game_ui = make_ui(game, ui_opt)

    setup_game(game, setup)
    game_ui._refresh()
    game_ui.master.update()

    return game_ui, game


def test_cleanup(game_ui):
    """Add the destroy action and run the loop.
    Do final update because it seems to need it."""

    # time.sleep(3)
    game_ui.master.after(200, game_ui.master.destroy)
    game_ui.ui_loop()
    game_ui.master.update()


# %% global opts

GAME_OPTS = {

    'split_all': GameOpts(sow_dir=gi.Direct.SPLIT,
                          udir_holes=ALL_HOLES),

    'spl_mshare': GameOpts(sow_dir=gi.Direct.SPLIT,
                          mustshare=True,
                          udir_holes=ALL_HOLES),
}

SETUPS = {

    'twos_t': SetupOpts(turn=True,
                        board=[2, 2, 2, 2, 2, 2, 2, 2],
                        owner=NONES),
    'twos_f': SetupOpts(turn=False,
                        board=[2, 2, 2, 2, 2, 2, 2, 2],
                        owner=NONES),

    'ms_1_1_2_4_f': SetupOpts(turn=False,
                              board=[1, 1, 2, 4, 0, 0, 0, 0],
                              owner=NONES),
    'ms_1_1_2_4_t': SetupOpts(turn=True,
                              board=[0, 0, 0, 0, 1, 1, 2, 4],
                              owner=NONES),

}


# %% render tests


TGRID_CASES = {
    'split_all_f_f':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=False),
         {1: ERender(),
          5: ERender()}],

    'split_all_f_t':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=True),
         {1: ERender(rc_grid=True),
          5: ERender(rc_grid=True)}],

    'split_all_t_f':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=True, touch_screen=False),
         {1: ERender(),
          5: ERender(rotate=True)}],

    'split_all_t_t':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=True, touch_screen=True),
         {1: ERender(rc_grid=True),
          5: ERender(rc_grid=True, rc_grid_loc=LEFT, rotate=True)}],

    'spl_mshare_1124_f_f_f':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_f'],
         UIOpts(facing_players=False, touch_screen=False),
         {0: ERender(rblock=True),
          1: ERender(),     # hole not playable, lr grids not shown
          2: ERender(lblock=True),
          3: ERender(),     # hole playable both ways
          }],

    'spl_mshare_1124_f_f_t':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_t'],
         UIOpts(facing_players=False, touch_screen=False),
         {4: ERender(lblock=True),
          5: ERender(),     # hole not playable, lr grids not shown
          6: ERender(rblock=True),
          7: ERender(),     # hole playable both ways
          }],

    'spl_mshare_1124_t_f_t':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_t'],
         UIOpts(facing_players=True, touch_screen=False),
         {4: ERender(rotate=True, lblock=True),
          5: ERender(rotate=True),     # hole not playable, lr grids not shown
          6: ERender(rotate=True, rblock=True),
          7: ERender(rotate=True),     # hole playable both ways
          }],

    'spl_mshare_1124_t_t_t':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_t'],
         UIOpts(facing_players=True, touch_screen=True),
         {4: ERender(rotate=True, lblock=True),
          5: ERender(rotate=True, rc_grid=True, rc_grid_loc=LEFT),
          6: ERender(rotate=True, rblock=True, rc_grid=True, rc_grid_loc=LEFT),
          7: ERender(rotate=True, rc_grid=True, rc_grid_loc=LEFT),
          }],

    }


def test_render(prefix, casename):
    """Test if the button is drawn as expected with the
    right click present when requested and in the right spot,
    check for present/absence of sow direction blocks,
    check for rotated state of text.

    Checking bindings/actions is NOT done here."""

    print(f"{prefix} {casename}...")

    game_opt, setup, ui_opt, ecell_dict = TGRID_CASES[casename]

    game_ui, game = test_setup(game_opt, setup, ui_opt)
    success = True

    for loc, exp in ecell_dict.items():

        btn = get_button(game_ui, loc)

        rot_angle = btn.itemcget(btn.text_id, 'angle')
        if exp.rotate != bool(rot_angle != '0.0'):
            print(f"{loc}: text rotation not as expected, actual {rot_angle}")
            success = False
            continue

        # TODO test rotation of owners and children markers

        if not btn.rclick_id:
            print(f"{loc}: rclick_id not set, grids not tested")
            continue

        rclick_state = btn.itemcget(btn.rclick_id, 'state')

        # confirm expected presence of right click grid
        if exp.rc_grid != bool(rclick_state == NORMAL):
            print('touch:', game_ui.vars.touch_screen.get())
            print(f"{loc}: right click grid not as expected, actual {rclick_state}")
            success = False

        # confirm location of right click grid
        if exp.rc_grid:

            x1, y1, x2, y2 = btn.coords(btn.rclick_id)
            xhalf = btn.winfo_width() // 2

            if ((exp.rc_grid_loc == RIGHT and x1 < xhalf)
                    or (exp.rc_grid_loc == LEFT and x2 > xhalf)):
                print(f"{loc}: RClick grid in wrong location:",
                      f" expected: {exp.rc_grid_loc}",
                      f" actual:   {LEFT if x1 < xhalf else RIGHT}", sep='\n')
                success = False

        right_state = btn.itemcget(btn.right_id, 'state')
        if exp.rblock != bool(right_state == NORMAL):
            print(f"{loc}: right grid not as expected, actual {right_state}")
            success = False


        left_state = btn.itemcget(btn.left_id, 'state')
        if exp.lblock != bool(left_state == NORMAL):
            print(f"{loc}: left grid not as expected, actual {left_state}")
            success = False

    test_cleanup(game_ui)
    return success


def debug_render(cname):

    print(f"{cname}...")

    game_opt, setup, ui_opt, ecell_dict = TGRID_CASES[cname]
    game_ui, game = test_setup(game_opt, setup, ui_opt)
    game_ui.ui_loop()

    # user must close window


# %% click tests

CLICK_CASES = {
    # split sow -- left & clicks on both T and F side
    'split_f_lclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=False),
         Action(loc=1, on_tgrid=False, click=LEFT_CLICK),
         [3, 0, 2, 2, 2, 2, 2, 3]],

    'split_f_rclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=False),
         Action(loc=1, on_tgrid=False, click=RIGHT_CLICK),
         [2, 0, 3, 3, 2, 2, 2, 2]],

    'split_t_lclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=False, touch_screen=False),
         Action(loc=5, on_tgrid=False, click=LEFT_CLICK),
         [2, 2, 2, 2, 2, 0, 3, 3]],

    'split_t_rclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=False, touch_screen=False),
         Action(loc=5, on_tgrid=False, click=RIGHT_CLICK),
         [2, 2, 2, 3, 3, 0, 2, 2]],

    # split sow -- left & clicks on both T and F side; facing players
    'facing_f_lclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=True, touch_screen=False),
         Action(loc=1, on_tgrid=False, click=LEFT_CLICK),
         [3, 0, 2, 2, 2, 2, 2, 3]],   # save as prev setup

    'facing_f_rclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=True, touch_screen=False),
         Action(loc=1, on_tgrid=False, click=RIGHT_CLICK),
         [2, 0, 3, 3, 2, 2, 2, 2]],  # same as prev setup

    'facing_t_lclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=True, touch_screen=False),
         Action(loc=5, on_tgrid=False, click=LEFT_CLICK),
         [2, 2, 2, 3, 3, 0, 2, 2]],  # opp dir from prev setup

    'facing_t_rclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=True, touch_screen=False),
         Action(loc=5, on_tgrid=False, click=RIGHT_CLICK),
         [2, 2, 2, 2, 2, 0, 3, 3]],  # opp dir from prev setup


    # touch screen - simul right click with left
    'touch_f_lclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=1, on_tgrid=False, click=LEFT_CLICK),
         [3, 0, 2, 2, 2, 2, 2, 3]],

    'touch_f_rclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=1, on_tgrid=False, click=RIGHT_CLICK),
         [2, 0, 3, 3, 2, 2, 2, 2]],

    'touch_f_lclick_rgrid':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=1, on_tgrid=True, click=LEFT_CLICK),
         [2, 0, 3, 3, 2, 2, 2, 2]],

    'touch_f_rclick_rgrid':
        [GAME_OPTS['split_all'],
         SETUPS['twos_f'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=1, on_tgrid=True, click=RIGHT_CLICK),
         [2, 0, 3, 3, 2, 2, 2, 2]],

    'touch_t_lclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=5, on_tgrid=False, click=LEFT_CLICK),
         [2, 2, 2, 2, 2, 0, 3, 3,]],

    'touch_t_rclick':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=5, on_tgrid=False, click=RIGHT_CLICK),
         [2, 2, 2, 3, 3, 0, 2, 2]],

    'touch_t_lclick_rgrid':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=5, on_tgrid=True, click=LEFT_CLICK),
         [2, 2, 2, 3, 3, 0, 2, 2]],

    'touch_t_rclick_rgrid':
        [GAME_OPTS['split_all'],
         SETUPS['twos_t'],
         UIOpts(facing_players=False, touch_screen=True),
         Action(loc=5, on_tgrid=True, click=RIGHT_CLICK),
         [2, 2, 2, 3, 3, 0, 2, 2]],


    'spl_ms_1124_f_f_f_0':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_f'],
         UIOpts(facing_players=False, touch_screen=False),
         Action(loc=0, click=LEFT_CLICK),
         [0, 1, 2, 4, 0, 0, 0, 1]],

    'spl_ms_1124_f_f_t_4':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_t'],
         UIOpts(facing_players=False, touch_screen=False),
         Action(loc=4, click=RIGHT_CLICK),
         [0, 0, 0, 1, 0, 1, 2, 4]],

    'spl_mshare_1124_f_f_t_6':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_t'],
         UIOpts(facing_players=False, touch_screen=False),
         Action(loc=6, click=LEFT_CLICK),
         [1, 0, 0, 0, 1, 1, 0, 5]],

    'spl_ms_1124_t_f_t_4':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_t'],
         UIOpts(facing_players=True, touch_screen=False),
         Action(loc=4, click=LEFT_CLICK),
         [0, 0, 0, 1, 0, 1, 2, 4]],    # facing players: do same op as _f_f_t_4

    'spl_ms_1124_t_f_t_6':
        [GAME_OPTS['spl_mshare'],
         SETUPS['ms_1_1_2_4_t'],
         UIOpts(facing_players=True, touch_screen=False),
         Action(loc=6, click=RIGHT_CLICK),
         [1, 0, 0, 0, 1, 1, 0, 5]],    # facing players: do same op as _f_f_t_6

    }


def test_click(prefix, cname):

    print(f"{prefix} {cname}...")
    game_opt, setup, ui_opt, action, eboard = CLICK_CASES[cname]

    game_ui, game = test_setup(game_opt, setup, ui_opt)

    game_ui.master.after(100, gen_event_fnc(game_ui, action))
    test_cleanup(game_ui)

    if game.board != eboard:
        print("Board doesn't match:",
              f"expected {eboard}",
              f"actual   {game.board}", sep='\n')
        return False

    return True



def debug_click(cname):

    print(f"{cname}...")
    game_opt, setup, ui_opt, action, eboard = CLICK_CASES[cname]
    game_ui, game = test_setup(game_opt, setup, ui_opt)
    game_ui.ui_loop()

    # user must close the window


# %%  test runner and reporter


def run_tests(prefix, cases, test_func):

    for cname in cases.keys():
        summary[prefix + ' ' + cname] = test_func(prefix, cname)

def report_tests():
    print("\n\nTest Summary:")
    for cname, result in summary.items():
        print(f"{cname:.<35}", 'Passed' if result else 'Failed')


# %%  main

if __name__ == '__main__':

    summary = {}

    run_tests("Render", TGRID_CASES, test_render)
    run_tests("Click", CLICK_CASES, test_click)

    report_tests()
