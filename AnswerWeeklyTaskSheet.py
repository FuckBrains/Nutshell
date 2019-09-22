__author__ = "Jack Walker"

from AnswerGeneratorModules import AnswerQuestions

import os
from pick import pick

nutshell_directory = os.path.abspath(os.path.dirname(__file__))

# Get task number from user
while True:
    try:
        task_num = input('Please enter the task you would like to create answers for:\n')
        if 0 < int(task_num) < 19:
            break
        else:
            raise TypeError
    except TypeError:
        print("Enter week task number between 1 and 14")
        continue

# Get sections from user
title = '\nWhich sections would you like to create answers for'
options = ["learn", "homework", "exercises", "past_paper_questions"]
sections_selected = pick(options, title, multi_select=True, min_selection_count=1)

AnswerQuestions.main(nutshell_directory, task_num, [section for (section, index) in sections_selected])
