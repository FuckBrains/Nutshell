from WeeklyContentGeneratorModules.SchemeOfWorkFunctions import openfile, get_file_path, getweekrow, getmatchedrow, \
    gettext, getlink, gettexts


def read_sow(nutshell_directory, week_num):

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
        nuts_topic_row = getmatchedrow(nuts, 1, topics[topic_num - 1]["title"])

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

    return {
        "unit_name": unit_name,
        "app_of_the_week": app_of_the_week,
        "topics": topics
    }