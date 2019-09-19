import json
import os
import webbrowser
import CreateVideo
import subprocess
from shutil import copyfile


def main(nutshell_directory, week_num, sections_selected):
    # Open output JSON
    with open(os.path.join(nutshell_directory, "TaskSheetContent", "GeneratedContent", "Week "+week_num, 'output.json'), 'r') as f:
        output_json = json.load(f)

    if "learn" in sections_selected:
        [print(topic["learn"]) for topic in output_json["topics"]]

    for section in ["homework", "exercises", "past_paper_questions"]:
        if section in sections_selected:

            if section == "homework":
                for topic in output_json["topics"]:
                    for task_number, task in enumerate(topic["n5w"][section]):

                        # Ensure directory created to store answer
                        relative_path = os.path.join(nutshell_directory, "VideoContent", "GeneratedContent",
                                                     "N5WQuestion", topic["title"], "Task" + str(task_number + 1))
                        if not os.path.exists(relative_path):
                            os.makedirs(relative_path)

                        # Open Powerpoint
                        powerpoint_path = os.path.join("C:\\", "Program Files (x86)", "Microsoft Office", "root", "Office16", "POWERPNT.EXE")
                        resource_template_path = os.path.join(nutshell_directory, "Slides", "Resources", "Video Resources.pptx")
                        resource_output_path = os.path.join(relative_path, "Video Resources.pptx")
                        copyfile(resource_template_path, resource_output_path)

                        subprocess.Popen([powerpoint_path, " /O ", resource_output_path])
                        # subprocess.call([powerpoint_path])

                        # Open url to questions
                        webbrowser.open_new_tab(task["link"])

                        inputs = {
                                "type": "n5w",
                                "skill": topic["title"],
                                "task_number": task_number,
                                "relative_path": relative_path
                            }

                        CreateVideo.main("prepare", inputs)
