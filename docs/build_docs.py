# -*- coding: utf-8 -*-
"""Create the html help files from the source data:
    about_games.html from the GameProps files
    game_params.html from the game_params.txt file

Created on Wed Nov 22 18:38:01 2023
@author: Ann"""

import dataclasses as dc
import enum
import os

from context import cfg_keys as ckey
from context import game_interface as gi
from context import man_config
from context import mancala_games


GPROP_PATH = '../GameProps/'
TXTPART = '.txt'
EXFILE = 'all_params.txt'

PARAMS = mancala_games.MancalaGames.read_params_file()



# %% html extras

def write_html_header(file, title):
    """write the header: title, css, etc."""

    print('<!DOCTYPE html>', file=file)
    print('<html lang="en">', file=file)
    print('<head>', file=file)
    print(f'<title>{title}</title>', file=file)
    print('<link rel="stylesheet" href="styles.css">', file=file)
    print('</head>', file=file)
    print('<body>', file=file)
    print(f'<h1>{title}</h1>', file=file)

    # TODO add nav button for Mancala game


def write_html_footer(file):
    """Close the tags."""

    # TODO add copyright and owner info

    print('</body>', file=file)
    print('</html>', file=file)


def write_columns(file, text, ncols):
    """Write out the lines of text in the number of specified columns
    using the float method."""

    per_col = len(text) // ncols + 1

    print('<div class="cols_row">', file=file)

    for col in range(ncols):
        print(f'  <div class="column{ncols}">', file=file)

        for line in text[col * per_col:(col + 1) * per_col]:
            print(f'    <p class="param">{line}</p>', file=file)

        print('  </div>', file=file)

    print('</div>', file=file)



# %%  write game help

GAME_INTRO = """\
A sampling of Mancala games that can be configured with
the Manacala Game Engine are predefined.
They are described below.
"""

# TODO add intro for game configurations (include a where to start)
# TODO add an index organized by high level property:
    # rounds, multilap, goal, capture type, demonstration

def game_prop_text(game_dict):
    """Collect text string for the key game properties in the
    config dict."""

    holes = game_dict[ckey.GAME_CONSTANTS][ckey.HOLES]
    start = game_dict[ckey.GAME_CONSTANTS][ckey.NBR_START]
    ptxt = [f'Holes per side:  {holes}',
            f'Start seeds:  {start}' ]

    for param, value in game_dict[ckey.GAME_INFO].items():

        if param in (ckey.NAME, ckey.ABOUT):
            continue

        if param in (ckey.CAPT_ON, ckey.UDIR_HOLES):
            vstr = ' '.join(str(val) for val in value)

        elif value is True:
            vstr = 'Yes'

        elif isinstance(value, enum.Enum):
            vstr = value.name

        else:
            vstr = str(value)

        pstr = f'<a href="game_params.html#{param}">' \
            + PARAMS[param].text + '</a>:'
        ptxt += [f'{pstr} {vstr}']

    return ptxt


def write_games_help(filename):
    """Collect the about texts from the game files and
    create the associated help file."""

    with open(filename, 'w', encoding='utf-8') as ofile:

        write_html_header(ofile, "Mancala Game Configurations")
        print(GAME_INTRO, file=ofile)

        for file in os.listdir(GPROP_PATH):

            if file[-4:] != TXTPART or file == EXFILE:
                continue
            game_dict = man_config.read_game(GPROP_PATH + file)

            about_str = ''
            if (ckey.GAME_INFO in game_dict
                    and ckey.ABOUT in game_dict[ckey.GAME_INFO]):

                gname = game_dict[ckey.GAME_INFO][ckey.NAME]
                about_str = game_dict[ckey.GAME_INFO][ckey.ABOUT]
                prop_text = game_prop_text(game_dict)

                del game_dict[ckey.GAME_CLASS]
                del game_dict[ckey.GAME_CONSTANTS]
                del game_dict[ckey.GAME_INFO]
                del game_dict[ckey.PLAYER]

            print(f'<h3 id="{gname}">', gname, '</h3>',
                  sep='', file=ofile)

            in_list = False
            for para in about_str.split('\n'):
                if para == '':
                    continue

                if not in_list and para[0] == '-':
                    in_list = True
                    print('<ul><li>', para[2:], sep='', file=ofile)

                elif in_list and para[0] == '-':
                    print('<li>', para[2:], sep='', file=ofile)

                elif in_list:
                    in_list = False
                    print('</ul>', file=ofile)
                    print('<p>', para, sep='', file=ofile)

                else:
                    print('<p>', para, sep='', file=ofile)

            if in_list:
                in_list = False
                print('</ul>', file=ofile)

            write_columns(ofile, prop_text, 2)

            for key, text in game_dict.items():
                print('<p>', key.title(), ': ', text, sep='', file=ofile)


        write_html_footer(ofile)



# %% output param help



PARAM_INTRO = """\
<p>Game options are provided in the following categories
(presented on corresponding tabs on the Mancala Options UI):
<ul>
<li><a href="#tab_Game"><b class="inhead">Game</b></a>:
Provide high level information about a game: name, description,
size, setup, etc.
<li><a href="#tab_Dynamics"><b class="inhead">Dynamics</b></a>:
Parameters that provide some high level of control over how
game play is conducted.
<li><a href="#tab_Allow"><b class="inhead">Allow</b></a>:
Parameters that control which holes moves may be started from.
<li><a href="#tab_Sow"><b class="inhead">Sow</b></a>:
Parameters that control how the seeds are sown (moved around)
in the sow phase of a turn.
<li><a href="#tab_Capture"><b class="inhead">Capture</b></a>:
Parameters that control where seeds are captured from and
any special mechanisms for multiple captures.
<li><a href="#tab_Player"><b class="inhead">Player</b></a>:
Parameters that control how the AI player evaluates the
board after each simulated move
(see <a href="mancala_help.html#aiplayer"><b class="inhead">AI Player</b></a>).
</ul>
<p>An alphabetical parameter <a href="#index">index</a>
is included after the parameter sections.

<p>Each parameter description includes:
    <ul>
    <li>Location in Config File to describe where
    the parameter is defined in the Game Description file.
    <li>Type of the parameter.
    <b class="todo">decribe the types someplace</b>
    <li>The default value for the parameter.
    If the default value is to be used the key-value pair is not needed
    in the game description file.
    Note that Mancala Options UI has slightly different
    defaults to yield a playable game.
    <li>The Mancala Options UI tab on which the parameter can be set.
    </ul>
"""

# TODO parameter file overview ^



def write_params_help(filename):
    """Create the game_params help file."""

    tab_set = set(r.tab for r in PARAMS.values())
    extra_tabs = tab_set - set(mancala_games.PARAM_TABS)
    tabs = mancala_games.PARAM_TABS + tuple(extra_tabs)

    with open(filename, 'w', encoding='utf-8') as ofile:
        write_html_header(ofile, "Mancala Game Parameters")

        print(PARAM_INTRO, file=ofile)

        for tab in tabs:
            print(f'<h2 id="tab_{tab}">{tab} Tab</h2>', file=ofile)

            for param in PARAMS.values():
                if param.tab != tab:
                    continue

                print(f'<h4 id="{param.option}">', param.text, '</h4>',
                      file=ofile)

                if param.cspec[-1] == '_':
                    ploc = param.cspec[:-2] + ' ' + param.option
                    ploc = ploc.replace(' ', ' : ')
                else:
                    ploc = param.cspec
                print('<p class="pdesc">Location in Config Files:',
                      ploc, file=ofile)
                print('<p class="pdesc">Type:', param.vtype,
                      file=ofile)
                dval = gi.GameInfo.get_default(param.option)
                # TODO lookup enumeration values
                print('<p class="pdesc">Default value:', dval,
                      file=ofile)
                print('<p class="pdesc">UI Tab:', param.tab,
                      file=ofile)
                print(file=ofile)

                for para in param.description.split('\n'):
                    if para == '':
                        continue

                    print('<p>', para, sep='', file=ofile)

        print('<br><br><br>', file=ofile)
        print('<h2 id="index">Parameter Index</h2>', file=ofile)
        pindex = [f'<a href="#{param}">' + param + '</a>'
                  for param in sorted(PARAMS.keys())]
        write_columns(ofile, pindex, 3)

        write_html_footer(ofile)


# %%  output the game xref table


# TODO figure out how to make a html table from the csv file
# interesting stuff here:  https://stackoverflow.com/questions/69357454/excel-like-filter-for-html-tables-with-javascript

def get_dc_field_names(dc_cls):
    """Return the field names for a dataclass."""
    return [field.name for  field in dc.fields(dc_cls)]


def write_game_xref(filename):
    """Create the game / parameter cross reference table."""

    gconsts = ['holes', 'nbr_start']
    ginfos = sorted(get_dc_field_names(gi.GameInfo))
    for dontcare in ['name', 'help_file', 'about']:
        ginfos.remove(dontcare)
    xref_params = gconsts + ginfos

    with open(filename, 'w', encoding='utf-8') as file:

        print(',', end='', file=file)
        for param in xref_params:
            print(f'{param},', end='', file=file)
        print(file=file)

        for gfile in os.listdir(GPROP_PATH):
            if gfile[-4:] != TXTPART or gfile == EXFILE:
                continue
            game_dict = man_config.read_game_config(GPROP_PATH + gfile)
            _, consts, info, _ = game_dict

            print(f'{gfile[:-4]},', end='', file=file)

            for param in xref_params:
                vstr = ''

                if param in gconsts:
                    vstr = str(getattr(consts, param))

                elif param in ('capt_on', 'udir_holes'):
                    vstr = ' '.join(str(val) for val in getattr(info, param))

                elif param in ginfos:
                    pval = getattr(info, param)
                    if pval is True:
                        vstr = 'x'
                    elif pval not in (0, False):
                        vstr = str(getattr(info, param))

                elif param == 'player':
                    pass

                else:
                    vstr = str(getattr(info, param))

                print(vstr, ',', sep='', end='', file=file)

            print(file=file)



# %%


if __name__ == '__main__':

    print("Writing games help")
    write_games_help('about_games.html')

    print("Writing params help")
    write_params_help('game_params.html')

    print("Writning games/params xref")
    write_game_xref('props_used.csv')
