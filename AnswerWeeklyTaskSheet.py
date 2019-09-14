__author__ = "Jack Walker"

from AnswerGeneratorModules import OpenLinks

import os
from pick import pick

nutshell_directory = os.path.abspath(os.path.dirname(__file__))

# Get weekNumber from user
while True:
    try:
        week_num = input('Please enter the week you would like to create answers for:\n')
        if 0 < int(week_num) < 19:
            break
        else:
            raise TypeError
    except TypeError:
        print("Enter week number between 1 and 18")
        continue

# Get weekNumber from user
title = '\nWhich sections would you like to view'
options = ["learn", "homework", "exercises", "past_paper_questions"]
sections_selected = pick(options, title, multi_select=True, min_selection_count=1)

OpenLinks.main(nutshell_directory, week_num, [section for (section, index) in sections_selected])
