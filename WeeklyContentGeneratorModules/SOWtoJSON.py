import json
import os


# Create JSON file
def create_json(week_path, unit_name, week_num, app_of_the_week, topics):
    output_json = {}

    output_json.update({"unit_name": unit_name})
    output_json.update({"week_number": week_num})
    output_json.update({"app_of_the_week": app_of_the_week})
    output_json.update({"topics": topics})

    if not os.path.exists(week_path):
        os.makedirs(week_path)
    with open(os.path.join(week_path, "output.json"), "w+") as output_json_file:
        output_json_file.write(json.dumps(output_json))

    return output_json
