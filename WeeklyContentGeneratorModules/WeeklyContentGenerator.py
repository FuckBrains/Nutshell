from WeeklyContentGeneratorModules.JSONtoTaskSheet import create_task_sheet
from WeeklyContentGeneratorModules.SOWInterpreter import read_sow
from WeeklyContentGeneratorModules.SOWtoJSON import create_json

__author__ = "Jack Walker"
import os

# Guide
# schemeOfWork: The tables consisting of the content for each week
# template_task_sheet: A template of the document given to students every week
# outputTaskSheet: The completed task sheet filled with content for week provided by user


def main(nutshell_directory, week_num):
    week_path = os.path.join(nutshell_directory, "TaskSheetContent", "GeneratedContent", "Week " + week_num)

    # Open all files and store values
    sow = read_sow(nutshell_directory, week_num)

    unit_name = sow["unit_name"]
    app_of_the_week = sow["app_of_the_week"]
    topics = sow["topics"]

    output_json = create_json(week_path, unit_name, week_num, app_of_the_week, topics)
    output_task_sheet = create_task_sheet(nutshell_directory, unit_name, week_num, app_of_the_week, topics, week_path)

    # TODO: Fix display issues
    # Convert HTML to PDF
    # options = {
    #     'page-size': 'A4',
    #     'margin-top': '0in',
    #     'margin-right': '0in',
    #     'margin-bottom': '0in',
    #     'margin-left': '0in',
    #     'no-outline': None
    # }
    # pdfkit.from_file(os.path.join(week_path, 'task_sheet.html'), 'out.pdf',options)
    # return ""
