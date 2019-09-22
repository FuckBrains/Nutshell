import json
import os
import re
import textwrap

from pick import pick


def get_sqa_input(nutshell_directory, output_directory):

    # Get past paper year from regex validated input
    while True:
        try:
            year = str(input("Year of paper:\n"))
            if re.match('^[1-2][0-9]{3}$', year):
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter year in format yyyy:\n")
            continue

    # Get past paper type from selection
    paper_type_question = 'Please choose paper type'
    paper_type_options = ['Calculator', 'Non-Calculator']
    paper_type, paper_typeindex = pick(paper_type_options, paper_type_question)

    # Get question number from regex validated input
    while True:
        try:
            question_number = str(input("Question Number:\n"))

            if re.match('^[1-9]$|^[1-3][0-9]$', question_number):
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter question number between 1 and 39:\n")
            continue

    display_text = ["SQA Past Paper", year + " " + paper_type, "Question " + str(question_number)]

    return {
        "type": "sqa",
        "year": year,
        "paper_type": paper_type,
        "question_number": question_number,
        "display_text": {
            "landscape": display_text,
            "portrait": display_text
        },
        "relative_path": os.path.join(output_directory, "SQAPastPaper", year, paper_type,
                                     str(question_number))
    }


def get_n5w_input(nutshell_directory, output_directory):

    # Get topic
    skill_question = 'Please pick a Nat 5 skill'
    with open(os.path.join(nutshell_directory, "VideoCreationModules", "n5_skills.json"), 'r') as f:
        skill_options = json.load(f)["skills"]

    skill, skill_index = pick(skill_options, skill_question)

    # Get task number from regex validated input
    while True:
        try:
            task_number = str(input("Task Number:\n"))

            if re.match('^[1-9]$', task_number):
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter question number between 1 and 9:\n")
            continue

    return {
        "type": "n5w",
        "skill": skill,
        "task_number": task_number,
        "relative_path": os.path.join(output_directory, "N5WQuestion", skill.replace(" ", ""), "Task"+task_number)
    }


def get_display_text(skill):
    return {
            "landscape": ["Nat 5 Maths"] + textwrap.TextWrapper(width=16).wrap(text=skill),
            "portrait": ["Nat 5 Maths"] + textwrap.TextWrapper(width=32).wrap(text=skill),
        }


def get_input(nutshell_directory):
    switcher = {
        "sqa": get_sqa_input,
        "n5w": get_n5w_input
    }

    # Get type of background from user and generate accordingly
    question_type_question = 'Please choose question type'
    question_type_options = ['sqa', 'n5w']
    code, code_index = pick(question_type_options, question_type_question)

    output_directory = os.path.join(nutshell_directory, "VideoContent", "GeneratedContent")

    inputs = switcher.get(code)
    inputs = inputs(nutshell_directory, output_directory)

    return inputs
