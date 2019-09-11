from WeeklyContentGeneratorModules.SchemeOfWorkFunctions import getweekrow, get_file_path, openfile, getmatchedrow, \
    gettext, gettexts,getlink,getlinks
from WeeklyContentGeneratorModules.TaskSheetFunctions import insert_into_output, add_to_output

__author__ = "Jack Walker"
import os
from dominate.tags import div, h5
import json

# Guide
# schemeOfWork: The tables consisting of the content for each week
# template_task_sheet: A template of the document given to students every week
# outputTaskSheet: The completed task sheet filled with content for week provided by user

# ********************************************************************************
# Helper Functions


def main(nutshell_directory):
    # ********************************************************************************
    # Get weekNumber from user
    while True:
        try:
            week_num = input("Week Number:\n")
            if 0 < int(week_num) < 53:
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter week number between 1 and 52:\n")
            continue

    # ********************************************************************************

    # 1. Open all files and store values
    app_of_the_week = {}

    # Open the Scheme of Work files and parse HTML
    # SOW file
    sow = openfile(get_file_path(nutshell_directory, "SOW"))
    sow_week_row = getweekrow(sow, int(week_num))
    unit_name = sow_week_row[4].get_text()
    app_of_the_week["name"] = sow_week_row[6].get_text()

    # APPS file
    apps = openfile(get_file_path(nutshell_directory, "APPS"))
    apps_week_row = getweekrow(apps, int(week_num))
    app_of_the_week["description"] = apps_week_row[1].get_text()

    # Iterate over each topic storing data for each
    topics = [{}, {}, {}]
    for topic_num in range(1, 4):
        topic = topics[topic_num - 1]
        index = topic_num + 6
        topic["title"] = sow_week_row[index].get_text()

        nuts = openfile(get_file_path(nutshell_directory, "NUTS"))
        nuts_topic_row = getmatchedrow(nuts, 1, topics[topic_num-1]["title"])

        # External links
        topic["bbc"] = {"title": gettext(nuts_topic_row, 2)}
        topic["y"] = {"title": gettext(nuts_topic_row, 3)}
        topic["ka"] = {"title": gettext(nuts_topic_row, 9)}

        external_link_codes = ["bbc", "y", "ka"]
        for code in external_link_codes:
            topic[code].update({"link": getlink(nutshell_directory, code, topic[code]["title"])})

        # National 5 Maths website
        exercises = {"exercises": []}
        topic["n5w"] = exercises

        for index, title in enumerate(gettexts(nuts_topic_row, 11, 16)):
            topic["n5w"]["exercises"].append({"title": title})

        past_paper_questions = {"past_paper_questions": []}
        topic["n5w"].update(past_paper_questions)
        for index, title in enumerate(gettexts(nuts_topic_row, 16, 30)):
            topic["n5w"]["past_paper_questions"].append({"title": title})

        for index, title in enumerate(gettexts(nuts_topic_row, 11, 16)):
            topic["n5w"]["exercises"].append({"title": title})

            # TODO: Iterate over links
            # n5w_exercisesheetslinks = getlinks("N5W", N5WExerciseSheetsTitles)
            # n5w_pastpaperquestionslinks = getlinks("N5W", N5WPastPaperQuestionsTitles)

        # n5w_homeworklinks= getlinks("N5W", N5WHomeworkTitles)
            
        # Write to JSON File
        f = open("topic.json", "w+")
        f.write(json.dumps(topic))

        n5w_homework_titles = []
        n5w_homework_descriptions = []
        for homeworks in range(0, 3):
            title = nuts_topic_row[30 + (homeworks * 2)].get_text()
            description = nuts_topic_row[31 + (homeworks * 2)].get_text()
            if title != "":
                n5w_homework_titles.extend([title])
                n5w_homework_descriptions.extend([description])


    # 2. Make a copy of template file
    template_task_sheet = openfile(
        os.path.join(nutshell_directory, "TaskSheetContent", "PremadeContent", "Weekly Task Sheet Templates",
                     "WeeklyTasksTemplateContainer.html"))

    # 3. Replace and add values to template file
    # Front page linear values
    insert_into_output(template_task_sheet, "span", "weekNum", "Week " + week_num + " of 18")
    insert_into_output(template_task_sheet, "span", "unitName", unit_name)
    insert_into_output(template_task_sheet, "h5", "appName", app_of_the_week["name"])
    insert_into_output(template_task_sheet, "p", "appDescription", app_of_the_week["description"])

    # Topics
    for topic_num in range(1, 4):
        # Front page topic circles
        topic_html = div(_class='topic')
        with topic_html:
            h5(topics[topic_num - 1]["title"], id="topicName-summary")

        add_to_output(template_task_sheet, "topic-container", str(topic_html))

        # Pages for topic
        template_topic_page = openfile(
            os.path.join(nutshell_directory, "TaskSheetContent", "PremadeContent", "Weekly Task Sheet Templates",
                         "TopicPageTemplate.html"))
        add_to_output(template_task_sheet, "topicPages", str(template_topic_page))

        # Learn section for topic
        insert_into_output(template_task_sheet, "span", "unitName", unit_name)

    # Close the Template file and output new HTML file
    week_path = os.path.join(nutshell_directory, "TaskSheetContent", "GeneratedContent", "Week " + week_num)

    if not os.path.exists(week_path):
        os.makedirs(week_path)
    with open(os.path.join(week_path, "task_sheet.html"), "wb") as output_task_sheet:
        output_task_sheet.write(template_task_sheet.prettify("utf-8"))
    return ""
