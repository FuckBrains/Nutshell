from WeeklyContentGeneratorModules.SchemeOfWorkFunctions import getweekrow, get_file_path, openfile, getmatchedrow, \
    gettext, gettexts,getlink
from WeeklyContentGeneratorModules.TaskSheetFunctions import replace_in_output, add_to_output, code_to_information, \
    generate_resource_html
import pdfkit

__author__ = "Jack Walker"
import os
from dominate.tags import div, h5, p, strong
import json

# Guide
# schemeOfWork: The tables consisting of the content for each week
# template_task_sheet: A template of the document given to students every week
# outputTaskSheet: The completed task sheet filled with content for week provided by user


def main(nutshell_directory, week_num):

    # 1. Open all files and store values
    output_json = {}
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
    app_of_the_week["image"] = apps_week_row[3].get_text()

    # Iterate over each topic storing data for each
    topics = [{}, {}, {}]
    for topic_num in reversed(range(1, 4)):
        topic = topics[topic_num - 1]
        index = topic_num + 6
        topic["title"] = sow_week_row[index].get_text()

        nuts = openfile(get_file_path(nutshell_directory, "NUTS"))
        nuts_topic_row = getmatchedrow(nuts, 1, topics[topic_num-1]["title"])

        learn = [{}, {}, {}]
        # External links
        external_link_codes = ["bbc", "y", "ka"]
        external_link_rows = [2, 3, 9]
        for index, code in enumerate(external_link_codes):
            learn_dict = learn[index]
            title = gettext(nuts_topic_row, external_link_rows[index])
            learn_dict.update({
                "code": code,
                "title": gettext(nuts_topic_row, external_link_rows[index]),
                "link": getlink(nutshell_directory, code, title)
            })
        topic.update({"learn": learn})

        # National 5 Maths website
        exercises = {"exercises": []}
        topic["n5w"] = exercises
        for index, title in enumerate(gettexts(nuts_topic_row, 11, 16)):
            topic["n5w"]["exercises"].append({
                "title": title,
                "link": getlink(nutshell_directory, "n5w", title)
            })

        past_paper_questions = {"past_paper_questions": []}
        topic["n5w"].update(past_paper_questions)
        for index, title in enumerate(gettexts(nuts_topic_row, 16, 30)):
            topic["n5w"]["past_paper_questions"].append({
                "title": title,
                "link": getlink(nutshell_directory, "n5w", title)
            })

        homework = {"homework": []}
        topic["n5w"].update(homework)
        homework_num = -1
        for index, text in enumerate(gettexts(nuts_topic_row, 30, 36)):
            if index % 2 == 0:
                homework_num = homework_num + 1
                if text == "":
                    break
                else:
                    topic["n5w"]["homework"].append({
                        "link": getlink(nutshell_directory, "n5w", text),
                    })
            else:
                topic["n5w"]["homework"][homework_num].update({
                    "description": text
                })

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

    # 3. Create JSON file
    week_path = os.path.join(nutshell_directory, "TaskSheetContent", "GeneratedContent", "Week " + week_num)

    output_json.update({"week_number": week_num})
    output_json.update({"app_of_the_week": app_of_the_week})
    output_json.update({"topics": topics})

    if not os.path.exists(week_path):
        os.makedirs(week_path)
    with open(os.path.join(week_path, "output.json"), "w+") as output_json_file:
        output_json_file.write(json.dumps(output_json))

    # 4. Replace and add values to template file
    # Front page linear values
    replace_in_output(template_task_sheet, "span", "weekNum", "Week " + week_num + " of 18")
    replace_in_output(template_task_sheet, "span", "unitName", unit_name)
    replace_in_output(template_task_sheet, "h5", "appName", app_of_the_week["name"])
    replace_in_output(template_task_sheet, "p", "appDescription", app_of_the_week["description"])

    app_image_html = div(_class="app-icon", id="appIcon", style="background-image: url(" + app_of_the_week["image"] + ");")
    add_to_output(template_task_sheet, "app-container", str(app_image_html))

    # Topics
    for topic_num in reversed(range(1, 4)):
        topic = topics[topic_num - 1]

        # Front page topic circles
        topic_name_circle_html = div(_class='topic')
        with topic_name_circle_html:
            h5(topics[topic_num - 1]["title"], id="topicName-summary")
        add_to_output(template_task_sheet, "topicsContainer", str(topic_name_circle_html))

        # Pages for topic
        template_topic_page = openfile(
            os.path.join(nutshell_directory, "TaskSheetContent", "PremadeContent", "Weekly Task Sheet Templates",
                         "TopicPageTemplate.html"))
        add_to_output(template_task_sheet, "topicPages", str(template_topic_page))
        replace_in_output(template_task_sheet, "h1", "topicName-detailed", topics[topic_num - 1]["title"])

        # Learn section for topic
        if not topic["learn"]:
            error_html = p("")
            with error_html:
                strong("Sorry, no learning resources available yet.")

            add_to_output(
                template_task_sheet,
                "learn-resources-container",
                str(error_html)
            )
        else:
            for resource in reversed(topic["learn"]):
                resource_info = code_to_information(resource["code"])
                available_material_html = div(
                    p("Videos") if resource_info["videos"] else p(),
                    p("Notes") if resource_info["notes"] else p(),
                    p("Exercises") if resource_info["exercises"] else p()
                )

                generate_resource_html(
                    template_task_sheet,
                    topics[topic_num - 1]["title"],
                    resource_info["image"],
                    resource_info["name"],
                    available_material_html,
                    resource["link"],
                    "learning"
                )

        # Homework section for topic
        homeworks_remaining = 3
        if not topic["n5w"]["homework"]:
            replace_in_output(template_task_sheet, "p", "test-paragraph-container", "")
            error_html = p("")
            with error_html:
                strong("No homework for this topic, you're welcome!")

            add_to_output(
                template_task_sheet,
                "test-resources-container",
                str(error_html)
            )
        else:
            for index, resource in enumerate((topic["n5w"]["homework"])):
                resource_info = code_to_information("n5w")
                generate_resource_html(
                    template_task_sheet,
                    topics[topic_num - 1]["title"],
                    resource_info["image"],
                    "Task " + str(homeworks_remaining),
                    p(resource["description"]),
                    resource["link"],
                    "test"
                )

                homeworks_remaining = homeworks_remaining - 1
                if homeworks_remaining == 0:
                    break


        # Exercise section for topic
        # Add national 5 resources first
        row = 1
        resources = 0
        exercises_remaining = 3
        if topic["n5w"]["exercises"]:
            for index, resource in enumerate(topic["n5w"]["exercises"]):
                resources = resources + 1
                resource_info = code_to_information("n5w")
                generate_resource_html(
                    template_task_sheet,
                    topics[topic_num - 1]["title"],
                    resource_info["image"],
                    "Task " + str(exercises_remaining),
                    p(resource["title"]),
                    resource["link"],
                    "exercise",
                    row
                )

                exercises_remaining = exercises_remaining - 1
                if resources % 3 == 0:
                    row = row + 1
                    exercises_remaining = resources + 3
                elif resources == 9:
                    break

        # Add Past paper questions
        if topic["n5w"]["past_paper_questions"] and resources == 0:
            error_html = p("")
            with error_html:
                strong("No extra exercises available")

            add_to_output(
                template_task_sheet,
                "exercise-1-resources-container margin-top",
                str(error_html)
            )
        else:
            for index, resource in enumerate(topic["n5w"]["past_paper_questions"]):
                resources = resources + 1
                resource_info = code_to_information("n5w")
                generate_resource_html(
                    template_task_sheet,
                    topics[topic_num - 1]["title"],
                    resource_info["image"],
                    "Task " + str(exercises_remaining),
                    p(resource["title"]),
                    resource["link"],
                    "exercise",
                    row
                )

                exercises_remaining = exercises_remaining - 1
                if resources == 9:
                    break
                elif resources % 3 == 0:
                    exercises_remaining = resources + 3
                    row = row + 1


    # Close the Template file and output new HTML file
    if not os.path.exists(week_path):
        os.makedirs(week_path)
    with open(os.path.join(week_path, "task_sheet.html"), "wb") as output_task_sheet:
        output_task_sheet.write(template_task_sheet.prettify("utf-8"))

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
