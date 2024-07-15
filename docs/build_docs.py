# -*- coding: utf-8 -*-
"""Create the html help files from the source data:
    Individual game property files (GameProps)
    game_params.txt (output from game_params.xlsm)
    param_consts source file
    game_classes source file
    ai_player source file

The game & properties cross reference table is
generated in both html and csv (props_used.csv).

Created on Wed Nov 22 18:38:01 2023
@author: Ann"""

import csv
import dataclasses as dc
import enum
import os
import re

from context import ai_player
from context import cfg_keys as ckey
from context import game_classes
from context import game_interface as gi
from context import man_config
from context import mancala_games
from context import param_consts as pc


GPROP_PATH = '../GameProps/'
TXTPART = '.txt'
EXFILE = 'all_params.txt'



# %% fill global tables


PARAMS = mancala_games.MancalaGames.read_params_file()

def get_game_names():
    """Scan the files and get the game names."""

    game_names = []
    for file in os.listdir(GPROP_PATH):

        if file[-4:] != TXTPART or file == EXFILE:
            continue
        game_dict = man_config.read_game(GPROP_PATH + file)

        if ckey.GAME_INFO in game_dict:
            game_names += [game_dict[ckey.GAME_INFO][ckey.NAME]]

    return game_names

GAMES = get_game_names()
UPARAMS = {param.upper() for param in PARAMS.keys()}

PUNCT = '().,?!;:'
SEP_PUNCT_RE = re.compile('([' + PUNCT + ']*)([-a-zA-Z_0-9]+)([' + PUNCT + ']*)')


# %% html extras


HEADER = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{bclass}">
"""

FOOTER = """\
<footer>
<table>
    <tr>
    <td>GPL-3.0 license</td>
    <td></td>
    <td style="text-align:right">&copy; 2024, Ann Davies</td>
    </tr>
</table>
</footer>
"""

def write_html_header(file, title, nav_content='<div>', bclass='narrow'):
    """write the header: title, css, etc."""

    print(HEADER.format(title=title, bclass=bclass),
          file=file)
    print(nav_content, file=file)
    print(f'<h1>{title}</h1>', file=file)


def write_html_footer(file):
    """Write the footer and close the tags."""

    print('<p />', file=file)
    print(FOOTER, file=file)
    print('</div>', file=file)
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


def sub_links(para):
    """For parameter names and games substitute in links.

    The handling of multi word game names seems forced :("""


    word_list = para.split(' ')
    w_links = []
    skip_words = 0

    for idx, word in enumerate(word_list):

        if skip_words:
            skip_words -= 1
            continue

        if word[:4] == 'http':
            w_links += [f'<a href="{word}" target="_blank">{word}</a>']
            continue


        match = SEP_PUNCT_RE.match(word)
        if match:
            pre, tword, post = match.groups()
        else:
            pre = post = ''
            tword = word

        mwgames = [' '.join(word_list[idx:idx + 2]),
                  ' '.join(word_list[idx:idx + 3])]


        if tword in UPARAMS:
            w_links += [f'{pre}'
                         + f'<a href="game_params.html#{tword.lower()}">'
                         + f'{tword}</a>'
                         + f'{post}']

        elif tword in GAMES:

            w_links += [f'{pre}'
                         + f'<a href="about_games.html#{tword}">'
                         + f'{tword}</a>'
                         + f'{post}']

        elif mwgames[0] in GAMES:

            w_links += [f'{pre}'
                         + f'<a href="about_games.html#{mwgames[0]}">'
                         + f'{mwgames[0]}</a>'
                         + f'{post}']
            skip_words = 1

        elif mwgames[1] in GAMES:

            w_links += [f'{pre}'
                         + f'<a href="about_games.html#{mwgames[1]}">'
                         + f'{mwgames[1]}</a>'
                         + f'{post}']
            skip_words = 2

        else:
            w_links += [word]

    return ' '.join(w_links)


def write_para(text, ofile):
    """Write a paragraph with
        * posible bullet lists for lines that start with -
        * make lines that start with 'Note: ' be in italic
        """

    in_list = False
    for para in text.split('\n'):
        if para == '':
            continue

        if para[:6] == 'Note: ':
            print('<p><i>', sub_links(para), '</i>', file=ofile)

        elif not in_list and para[0] == '-':
            in_list = True
            print('<ul><li class="helptext">', sub_links(para[2:]),
                  sep='', file=ofile)

        elif in_list and para[0] == '-':
            print('<li class="helptext">', sub_links(para[2:]),
                  sep='', file=ofile)

        elif in_list and para[:3] == '  +':
            print('<p class="helptext">', sub_links(para[3:]),
                  sep='', file=ofile)

        elif in_list:
            in_list = False
            print('</ul>', file=ofile)
            print('<p>', sub_links(para), sep='', file=ofile)

        else:
            print('<p>', sub_links(para), sep='', file=ofile)

    if in_list:
        in_list = False
        print('</ul>', file=ofile)


# %%  write game help


GAME_NAV = """\
<div class="sidenav">
<h3>Game Configurations</h2>
  <a href="#top">Top</a>
  <a href="#index">Game Index</a>
<h3>Other Help Files</h3>
  <a href="mancala_help.html">Mancala Help</a>
  <a href="game_params.html">Parameters</a>
  <a href="param_types.html">Param Types</a>
  <a href="game_xref.html">Cross Reference</a>
</div>
<div class="content">
"""

GAME_INTRO = """\
<p>A sampling of Mancala games that can be configured with
the Manacala Game Engine are predefined.
Descriptions are provided in the sections below.

<p>If you are new to Mancala,
<a href="#Wari">Wari</a> and <a href="#Oware">Oware</a>
are good places to start.
<a href="#Kalah">Kalah</a> is a simple cross capture game.

<p><a href="#Bechi">Bechi</a>,
<a href="#Cow">Cow</a> and
<a href="#Qelat">Qelat</a>
add interesting complications to the basic rules.
<a href="#Bechi">Bechi</a> introduces the concept of playing in rounds.
<a href="#Cow">Cow</a> introduces varying the sow direction.
<a href="#Qelat">Qelat</a> adds the idea of hole ownership,
 in this case, called walda's.

<p>Good introductions to multilap sowing are provided by
<a href="#Endodoi">Endodoi</a> and
<a href="#Ayoayo">Ayoayo</a>.

<p>Not all games have the goal of capturing the most seeds.
<a href="#Deka">Deka</a> and others have a goal of depriving
your opponent of seeds.
<a href="#Weg">Weg</a> and others involve capturing territory.

<p>
<p>Three games isolate unique game parameters:
    <ul>
    <li><a href="#NoCapt">NoCapt</a>:
    Captures are only accomplished by sowing into your own store.
    <li><a href="#NoSides">NoSides</a>:
    Players are not limited to starting a move on their own side of the board,
    instead a player may start a move from any hole.
    <li><a href="#NoSidesChild">NoSidesChild</a>:
    Players do not own the holes on their own side of the board;
    instead ownership is claimed (i.e. making a child)
    by sowing a hole to four seeds.
    </ul>

<p><i>Personal Note</i>:
These configurations are my best understanding of the rules
from various sources.
I cannot be certain that I have faithfully reproduced any game.
You may know a particular set of rules by a different name.
You may have a particular "house rule" that varies from the specific
configuration provided.
I might simply have an implementation error.
Please consider these file a starting point for defining your
own favorite games.
<p>The <a href="game_xref.html">Game / Parameter Cross Reference table</a>
can be used to determine if a particular set of rules has a different
name than you expect.
"""

def game_prop_text(game_dict):
    """Collect text string for the key game properties in the
    config dict."""

    holes = game_dict[ckey.GAME_CONSTANTS][ckey.HOLES]
    start = game_dict[ckey.GAME_CONSTANTS][ckey.NBR_START]
    goal = game_dict[ckey.GAME_INFO].get(ckey.GOAL, gi.Goal.MAX_SEEDS)

    ptxt = [f'Holes per side:  {holes}',
            f'Start seeds:  {start}',
            f'<a href="game_params.html#goal">Goal</a>: {goal.name}']

    for param, value in game_dict[ckey.GAME_INFO].items():

        if param in (ckey.NAME, ckey.ABOUT, ckey.GOAL):
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

    games = []
    with open(filename, 'w', encoding='utf-8') as ofile:

        write_html_header(ofile, "Mancala Game Configurations", GAME_NAV)
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

                # delete the standard contents, extra is printed at the end
                del game_dict[ckey.GAME_CLASS]
                del game_dict[ckey.GAME_CONSTANTS]
                del game_dict[ckey.GAME_INFO]
                del game_dict[ckey.PLAYER]

            print(f'<h3 id="{gname}">', gname, '</h3>',
                  sep='', file=ofile)
            games += [gname]

            write_para(about_str, ofile)
            write_columns(ofile, prop_text, 2)
            for key, text in game_dict.items():
                print('<p>', key.title(), ': ', sub_links(text),
                      sep='', file=ofile)

        print('<br><br><br>', file=ofile)
        print('<h2 id="index">Game Index</h2>', file=ofile)
        gindex = [f'<a href="#{gname}">' + gname + '</a>'
                  for gname in sorted(games)]
        write_columns(ofile, gindex, 3)

        write_html_footer(ofile)



# %% output param help


PARAM_NAV = """\
<div class="sidenav">
<h3>Game Parameters</h2>
  <a href="#top">Top</a>
  <a href="#tab_Game">Game Tab</a>
  <a href="#tab_Dynamics">Dynamics Tab</a>
  <a href="#tab_Allow">Allow Tab</a>
  <a href="#tab_Sow">Sow Tab</a>
  <a href="#tab_Capture">Capture Tab</a>
  <a href="#tab_Player">Player Tab</a>
  <a href="#index">Parameter Index</a>
<h3>Other Help Files</h3>
  <a href="mancala_help.html">Mancala Help</a>
  <a href="about_games.html">Mancala Game Configurations</a>
  <a href="param_types.html">Param Types</a>
  <a href="game_xref.html">Cross Reference</a>
</div>
<div class="content">
"""

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
    <li>Type of the parameter with a link to the Parameter Types help.
    <li>The default value for the parameter.
    If the default value is to be used the key-value pair is not needed
    in the game description file.
    Note that Mancala Options UI has slightly different
    defaults to yield a playable game.
    <li>The Mancala Options UI tab on which the parameter can be set.
    </ul>
"""


def write_params_help(filename):
    """Create the game_params help file."""

    tab_set = set(r.tab for r in PARAMS.values())
    extra_tabs = tab_set - set(mancala_games.PARAM_TABS)
    tabs = mancala_games.PARAM_TABS + tuple(extra_tabs)

    with open(filename, 'w', encoding='utf-8') as ofile:
        write_html_header(ofile, "Mancala Game Parameters", PARAM_NAV)

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
                print(f'<p id="{param.vtype}" class="pdesc">Type:',
                      f'<a href="param_types.html#{param.vtype}">',
                      param.vtype,
                      '</a>',
                      file=ofile)
                dval = gi.GameInfo.get_default(param.option)
                print('<p class="pdesc">Default value:', dval,
                      file=ofile)
                print('<p class="pdesc">UI Tab:', param.tab,
                      file=ofile)
                print(file=ofile)

                write_para(param.description, ofile)

        print('<br><br><br>', file=ofile)
        print('<h2 id="index">Parameter Index</h2>', file=ofile)
        pindex = [f'<a href="#{param}">' + param + '</a>'
                  for param in sorted(PARAMS.keys())]
        write_columns(ofile, pindex, 3)

        write_html_footer(ofile)



# %% types help file


TYPES_NAV = """\
<div class="sidenav">
<h3>Game Parameters</h2>
  <a href="#top">Top</a>
  <a href="#basic">Basic Types</a>
  <a href="#descript">Description Types</a>
  <a href="#enum">Enumeration Types</a>
<h3>Other Help Files</h3>
  <a href="mancala_help.html">Mancala Help</a>
  <a href="about_games.html">Mancala Game Configurations</a>
  <a href="game_params.html">Parameters</a>
  <a href="game_xref.html">Cross Reference</a>
</div>
<div class="content">
"""


BASIC_TYPES = """\
<p>This file provides a cross reference between the types and
values accepted for them.
Detailed descriptions are found in the
<a href="mancala_help.html">main help</a> or
<a href="game_params.html">Game Parameteres help</a>.

<h3 id="basic">Basic Types</h3>
<h4 id="int">int</h4>
<p>The value must be an integer.
Some are limited to a specific range.
<h4 id="bool">bool</h4>
<p>The value must be either true or false.
Quotes on the value are not required.
<h4 id="str">str</h4>
<p>The value must be an string surrounded by quotes (").
<h4 id="multi_str">multi_str</h4>
<p>The value must be a string surrounded by quotes (").
It will be presented in such a way that new lines (\\n)
will be expanded to new lines.
<h4 id="list_bool">list[bool]</h4>
The value must be a list of hole indicies (0 origin) for which
the property is true.
<h4 id="list_int">list[int]</h4>
The value must be an array of 4 integers.
These are used for the four strength properties of the AI player.
Each corresponds to a game difficulty.
"""

DESC_TYPES = """\
<h3 id="descript">Description Types</h3>
Two types are description strings; allowed values are shown below.
"""

ALG_TYPES = """\
<p>The Algorithm selection describes the algorithm used by the
<a href="mancala_help.html#ai_player">AI Player</a>.
"""

ENUM_INTRO = """\
<h3 id="enum">Enumeration Types</h3>
<p>Enumeration types appear in the JSON configuration files
as integers (int type).
Enumerations provide a list of names for parameter values.
Only the integer is put in the configuration file.
<p>Each enumeration type is listed below.
For each type the values (integer), enumeration value name, and string
description are list.
Detailed descriptions of the behavior of each value are in the
<a href="game_params.html">Game Parameters</a> help file.
"""
NOT_ENUMS = {'bool',
    'int',
    'list[bool]',
    'list[int]',
    'multi_str',
    'str',
    'Algorithm',
    'GameClasses'}

def write_desc_types(ofile):
    """Write the sections for the description strings."""

    print(DESC_TYPES, file=ofile)
    print('<h4 id="Algorithm">Algorithm',
          '<a href="game_params.html#Algorithm">(usage)</a></h4>',
          file=ofile)
    print(ALG_TYPES, file=ofile)
    print('<ul>', file=ofile)
    for name in ai_player.ALGORITHM_DICT.keys():
        print(f'<li>{name}', file=ofile)
    print('</ul>', file=ofile)

    print('<h4 id="GameClasses">GameClasses</h4>', file=ofile)
    print('<ul>', file=ofile)
    for name in game_classes.GAME_CLASSES.keys():
        print(f'<li>{name}', file=ofile)
    print('</ul>', file=ofile)


def write_types_file(filename):
    """Write the types help file."""

    types = [(pname, ptuple.vtype) for pname, ptuple in PARAMS.items()]

    with open(filename, 'w', encoding='utf-8') as ofile:
        write_html_header(ofile, "Parameters Types", TYPES_NAV)
        print(BASIC_TYPES, file=ofile)
        write_desc_types(ofile)

        print(ENUM_INTRO, file=ofile)
        for pname, tname in sorted(types):
            if tname in NOT_ENUMS:
                continue

            print(f'<h4 id="{tname}">{tname}',
                  f'(<a href="game_params.html#{pname}">usage</a>)</h4>',
                  file=ofile)
            strings = pc.STRING_DICTS[tname].int_dict

            try:
                ename = getattr(gi, tname)
            except AttributeError:
                print('  ', tname, 'not in game_interface')
                continue

            print('<table>', file=ofile)
            print('<tr><th style="width:10%">Value</th>'
                  '<th style="width:40%">Id</th>'
                  '<th style="width:40%">UI string</th></tr>',
                  file=ofile)
            for e_val in ename:
                print('<tr><td>', e_val.value,
                      '</td><td>', e_val.name,
                      '<td>', strings[e_val], '</td></tr>',
                      sep='', file=ofile)

                if e_val.name not in PARAMS[pname].description:
                    print('  Doc Error:',
                          f'{e_val.name} is not in {pname} description.')

            print('</table>', file=ofile)

        write_html_footer(ofile)



# %%  output the game xref table & html


def get_dc_field_names(dc_cls):
    """Return the field names for a dataclass."""
    return [field.name for  field in dc.fields(dc_cls)]


def write_game_xref(filename):
    """Create the game / parameter cross reference table."""

    gconsts = ['holes', 'nbr_start']
    ginfos = sorted(get_dc_field_names(gi.GameInfo))
    for dontcare in ['name', 'help_file', 'about', 'udirect']:
        ginfos.remove(dontcare)
    xref_params = gconsts + ginfos

    with open(filename, 'w', encoding='utf-8') as ofile:

        print(',', end='', file=ofile)
        print(','.join(xref_params), file=ofile)

        for gfile in os.listdir(GPROP_PATH):
            if gfile[-4:] != TXTPART or gfile == EXFILE:
                continue
            game_dict = man_config.read_game_config(GPROP_PATH + gfile)
            _, consts, info, _ = game_dict

            print(f'{gfile[:-4]},', end='', file=ofile)

            pvals = []
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

                pvals += [vstr]

            print(','.join(pvals), file=ofile)



def write_xref_html(csv_filename, out_filename):
    """Write a handy html file with filtering capabilities
    for the cross reference table."""

    with open(csv_filename, 'r', newline='',  encoding='utf-8') as ifile:
        csvreader = csv.reader(ifile, delimiter=',')

        with open(out_filename, 'w', encoding='utf-8') as ofile:

            write_html_header(ofile, "Game Property Cross Reference",
                              bclass="wide")

            print('<table class="xref">', file=ofile)

            header = next(csvreader)
            print('<tr>', file=ofile)
            print ('<th class="xref">Game Name</th>', file=ofile)
            for title in header[1:]:
                print('<th class="xref"><div>',
                      f'<a href="game_params.html#{title}">{title}',
                      '</a></div></th>', file=ofile)
            print('</tr>', file=ofile)

            odd_row = True
            for row in csvreader:
                td_class = "odd" if odd_row else "even"
                odd_row = not odd_row

                print('<tr>', file=ofile)
                print(f'<td class={td_class}>',
                      f'<a href="about_games.html#{row[0]}">',
                      f'{row[0]}</a></td>',
                      sep='', file=ofile)

                for value in row[1:]:
                    print(f'<td class={td_class}>{value}</td>', file=ofile)
                print('</tr>', file=ofile)


            print('</table>', file=ofile)

            write_html_footer(ofile)


# %%  main


if __name__ == '__main__':

    print("Writing games help")
    write_games_help('about_games.html')

    print("Writing params help")
    write_params_help('game_params.html')

    print("Writing type help")
    write_types_file('param_types.html')

    print("Writning games/params xref")
    write_game_xref('props_used.csv')
    write_xref_html('props_used.csv', 'game_xref.html')
