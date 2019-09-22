import json
import os
import webbrowser
import CreateVideo
import subprocess
from shutil import copyfile
from msvcrt import getch
import sys


def can_continue(message):
    print(message)
    while True:
        key = ord(getch())
        if key == 121:  # Y
            return True
        if key == 110:  # N
            return False
        if key == 3:  # C
            sys.exit()


def main(nutshell_directory, week_num, sections_selected):
    # Open output JSON
    with open(os.path.join(nutshell_directory, "TaskSheetContent", "GeneratedContent", "Week "+week_num, 'output.json'), 'r') as f:
        output_json = json.load(f)

    if "learn" in sections_selected:
        [print(topic["learn"]) for topic in output_json["topics"]]

    inputs = []

    if "homework" in sections_selected:

        total_tasks = 0

        for topic in output_json["topics"]:
            for task_number, task in enumerate(topic["n5w"]["homework"]):

                # Ensure directory created to store answer materials
                relative_path = os.path.join(nutshell_directory, "VideoContent", "GeneratedContent",
                                             "N5WQuestion", topic["title"].replace(" ", ""), "Task" + str(task_number + 1))
                if not os.path.exists(relative_path):
                    os.makedirs(relative_path)

                # Open Powerpoint
                powerpoint_path = os.path.join("C:\\", "Program Files (x86)", "Microsoft Office", "root", "Office16", "POWERPNT.EXE")
                resource_template_path = os.path.join(nutshell_directory, "Slides", "Resources", "Video Resources.pptx")
                resource_output_path = os.path.join(relative_path, "Video Resources.pptx")
                copyfile(resource_template_path, resource_output_path)
                subprocess.Popen([powerpoint_path, resource_output_path])

                # Open url to questions
                webbrowser.open_new_tab(task["link"])

                print(task["description"])

                # Screen Grab and save image
                while True:
                    if can_continue("Press y to screen grab, n to skip"):
                        subprocess.Popen(
                            [os.path.join("C:\\", "Program Files", "ShareX", "ShareX.exe"), "-RectangleRegion"]
                        )
                    else:
                        break

                inputs.append({
                    "type": "n5w",
                    "skill": topic["title"],
                    "task_number": task_number,
                    "relative_path": relative_path
                })

                # Record Screen
                while True:
                    if can_continue("Press y to record screen, n to skip"):
                        CreateVideo.main("prepare", inputs[total_tasks])
                    else:
                        break

                total_tasks += 1

    if can_continue("All questions prepared, would you like to create videos"):
        for task in inputs:
            CreateVideo.main("create", task)