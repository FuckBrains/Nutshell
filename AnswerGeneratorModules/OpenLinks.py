import json
import os


def main(nutshell_directory, week_num, sections_selected):
    # Open output JSON
    with open(os.path.join(nutshell_directory, "TaskSheetContent", "GeneratedContent", "Week "+week_num, 'output.json'), 'r') as f:
        output_json = json.load(f)

    if "learn" in sections_selected:
        [print(topic["learn"]) for topic in output_json["topics"]]

    for section in ["homework", "exercises", "past_paper_questions"]:
        if section in sections_selected:
            [print(topic["n5w"][section]) for topic in output_json["topics"]]