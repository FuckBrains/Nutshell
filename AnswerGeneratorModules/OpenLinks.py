import json
import os
import webbrowser
import CreateVideo


def main(nutshell_directory, week_num, sections_selected):
    # Open output JSON
    with open(os.path.join(nutshell_directory, "TaskSheetContent", "GeneratedContent", "Week "+week_num, 'output.json'), 'r') as f:
        output_json = json.load(f)

    if "learn" in sections_selected:
        [print(topic["learn"]) for topic in output_json["topics"]]

    for section in ["homework", "exercises", "past_paper_questions"]:
        if section in sections_selected:
            for topic in output_json["topics"]:
                print(topic["title"])
                for task_number, task in enumerate(topic["n5w"][section]):
                    # Open url in a new page (“tab”) of the default browser, if possible
                    print(task["description"])
                    webbrowser.open_new_tab(task["link"])

                    relative_path = os.path.join(nutshell_directory, "VideoContent", "GeneratedContent", "N5WQuestion", topic["title"], "Task"+str(task_number+1))

                    if not os.path.exists(relative_path):
                        os.makedirs(relative_path)

                    inputs = {
                            "type": "n5w",
                            "skill": topic["title"],
                            "task_number": task_number,
                            "relative_path": relative_path
                        }

                    CreateVideo.main("prepare", inputs)
