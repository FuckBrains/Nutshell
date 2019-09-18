__author__ = "Jack Walker"

import os
from WeeklyContentGeneratorModules import WeeklyContentGenerator
from pick import pick
nutshell_directory = os.path.abspath(os.path.dirname(__file__))

# Get weekNumber from user
title = 'Please choose which weeks you would like to generate scheme of work for '
options = range(1, 15)
selected = pick(options, title, multi_select=True, min_selection_count=1)

for (i, j) in selected:
    WeeklyContentGenerator.main(nutshell_directory, str(i))
