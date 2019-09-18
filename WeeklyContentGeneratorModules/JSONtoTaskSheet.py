import os

from dominate.tags import div, h5, p, strong

from WeeklyContentGeneratorModules.SchemeOfWorkFunctions import openfile
from WeeklyContentGeneratorModules.TaskSheetFunctions import replace_in_output, add_to_output, code_to_information, \
    generate_resource_html


def update_front_page(template_task_sheet, unit_name, week_num, app_of_the_week):
    # Front page linear values
    replace_in_output(template_task_sheet, "span", "weekNum", "Task sheet " + week_num + " of 14")
    replace_in_output(template_task_sheet, "span", "unitName", unit_name)
    replace_in_output(template_task_sheet, "h5", "appName", app_of_the_week["name"])
    replace_in_output(template_task_sheet, "p", "appDescription", app_of_the_week["description"])

    app_image_html = div(_class="app-icon", id="appIcon",
                         style="background-image: url(" + app_of_the_week["image"] + ");")
    add_to_output(template_task_sheet, "app-container", str(app_image_html))


def make_grid_list(num_resources):
    if num_resources == 0:
        return []
    elif num_resources == 1:
        return [1]
    elif num_resources < 4:
        return [num_resources] + make_grid_list(num_resources-1)
    elif 3 < num_resources < 7:
        return make_grid_list(3) + list(reversed(range(4, num_resources+1)))
    elif num_resources > 6:
        return make_grid_list(6) + list(reversed(range(7, num_resources+1)))


def add_section(template_task_sheet, topic, section_heading, error_message, materials_list):
    if not materials_list:
        error_html = p("")
        with error_html:
            strong(error_message)
        id_tag = section_heading + "-1-resources-container margin-top" if section_heading == "exercises" else section_heading + "-resources-container"

        if section_heading == "homework":
            replace_in_output(template_task_sheet, "p", "homework-paragraph-container", "")

        add_to_output(template_task_sheet, id_tag, str(error_html))
    else:
        resource_num = 0
        index_to_task = make_grid_list(len(materials_list))

        row = 1
        for resource in materials_list:

            if section_heading == "learn":
                resource_info = code_to_information(resource["code"])
                paragraph_html = div(
                    p("Videos") if resource_info["videos"] else p(),
                    p("Notes") if resource_info["notes"] else p(),
                    p("Exercises") if resource_info["exercises"] else p()
                )
            elif section_heading == "homework":
                paragraph_html = p(resource["description"])
                resource_info = code_to_information("n5w", index_to_task[resource_num])
            else:
                paragraph_html = p(resource["title"])
                resource_info = code_to_information("n5w", index_to_task[resource_num])

            generate_resource_html(
                template_task_sheet,
                topic["title"],
                resource_info["image"],
                resource_info["name"],
                paragraph_html,
                resource["link"],
                section_heading,
                row
            )

            if resource_num == 9:
                print("Too many resources")
                break
            else:
                resource_num = resource_num + 1
                if resource_num % 3 == 0:
                    row = row + 1


def add_topics(nutshell_directory, template_task_sheet, topics):
    for topic_num in reversed(range(1, 4)):
        topic = topics[topic_num - 1]

        # Front page topic circles
        topic_name_circle_html = div(_class='topic')
        with topic_name_circle_html:
            h5(topic["title"], id="topicName-summary")
        add_to_output(template_task_sheet, "topicsContainer", str(topic_name_circle_html))

        # Pages for topic
        template_topic_page = openfile(
            os.path.join(nutshell_directory, "TaskSheetContent", "PremadeContent", "Weekly Task Sheet Templates",
                         "TopicPageTemplate.html"))
        add_to_output(template_task_sheet, "topicPages", str(template_topic_page))
        replace_in_output(template_task_sheet, "h1", "topicName-detailed", topic["title"])

        add_section(
            template_task_sheet,
            topic,
            "learn",
            "Sorry, no learning resources available yet.",
            list(reversed(topic["learn"]))
        )

        add_section(
            template_task_sheet,
            topic,
            "homework",
            "No homework for this topic, you're welcome!",
            list(reversed(topic["n5w"]["homework"]))
        )

        add_section(
            template_task_sheet,
            topic,
            "exercises",
            "Sorry, no extra resources for this topic yet.",
            list(reversed(topic["n5w"]["exercises"]))
        )
        # add_homework_section(template_task_sheet, topic)
        # add_exercises_section(template_task_sheet, topic)


def create_task_sheet(nutshell_directory, unit_name, week_num, app_of_the_week, topics, week_path):
    # Replace and add values to template file
    
    #  Make a copy of template file
    template_task_sheet = openfile(
        os.path.join(nutshell_directory, "TaskSheetContent", "PremadeContent", "Weekly Task Sheet Templates",
                     "WeeklyTasksTemplateContainer.html"))

    update_front_page(template_task_sheet, unit_name, week_num, app_of_the_week)

    # Topics
    add_topics(nutshell_directory, template_task_sheet, topics)

    # Close the Template file and output new HTML file
    if not os.path.exists(week_path):
        os.makedirs(week_path)
    with open(os.path.join(week_path, "task_sheet.html"), "wb") as output_task_sheet:
        output_task_sheet.write(template_task_sheet.prettify("utf-8"))

    return output_task_sheet
