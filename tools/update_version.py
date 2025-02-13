# -*- coding: utf-8 -*-
"""Update the version info in the version.py file.

Created on Thu Feb 13 07:41:39 2025
@author: Ann"""

import datetime
import os

import git


date = datetime.datetime.now().ctime()

repo = git.repo(os.getcwd())
branch = repo.active_branch.name
version = sorted(repo.tags, key=lambda t: t.tag.tagged_date)[-1].name


with open('src/version.py', 'r', encoding='utf-8') as file:
    lines = file.readlines()

for idx, line in enumerate(lines[:]):

    if 'DATETIME =' in line:
        lines[idx] = f"DATETIME = '{date}'\n"

    elif 'VERSION =' in line:
        lines[idx] = f"VERSION = '{version}'\n"

    elif 'BRANCH =' in line:
        lines[idx] = f"BRANCH = '{branch}'\n"

with open('src/version.py', 'w', encoding='utf-8') as file:
    file.writelines(lines)
