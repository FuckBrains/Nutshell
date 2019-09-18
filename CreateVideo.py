__author__ = "Jack Walker"

import os
import json
import sys

from VideoCreationModules import BackgroundGenerator
from VideoCreationModules import RecordScreen
from VideoCreationModules import CropRecording
from VideoCreationModules import BackgroundToVideo
from VideoCreationModules import OverlayClips
from VideoCreationModules import ConcatenateClips
from VideoCreationModules import UserInput

def write_video_details_to_json(details_of_video):
    with open(os.path.join(details_of_video["relative_path"], "details_of_video.json"), "w+") as output_json_file:
        output_json_file.write(json.dumps(details_of_video))


def prepare_video(nutshell_directory, orientations, inputs):
    print("Prepare video")
    if not inputs:
        inputs = UserInput.get_input(nutshell_directory)
    inputs["display_text"] = UserInput.get_display_text(inputs["skill"])
    details_of_video = BackgroundGenerator.main(nutshell_directory, orientations, inputs)
    RecordScreen.main(details_of_video)
    return details_of_video


def create_video(nutshell_directory, orientations, details_of_video):
    print("Create video")
    CropRecording.main(details_of_video)
    background_video_paths = {}
    for orientation in orientations:
        print(orientation)
        background_video_paths[orientation] = BackgroundToVideo.main(
            orientation,
            details_of_video["background_path"][orientation]
        )

        raw_with_background_path = OverlayClips.main(details_of_video, orientation, background_video_paths[orientation])
        ConcatenateClips.main(details_of_video, nutshell_directory, orientation, raw_with_background_path)


# Decide whether to prepare video, create it from pre preared content or do both
def main(operation, inputs):
    orientations = ["landscape", "portrait"]
    nutshell_directory = os.path.abspath(os.path.dirname(__file__))

    if operation == "prepare":
        details_of_video = prepare_video(nutshell_directory, orientations, inputs)
        write_video_details_to_json(details_of_video)

    elif operation == "create":
        if inputs:
            with open(os.path.join(inputs["relative_path"], "details_of_video.json"), 'r') as f:
                details_of_video = json.load(f)
            create_video(nutshell_directory, orientations, details_of_video)
        else:
            print("Must provide input JSON with details of pre prepared content")

    elif operation == "all":
        details_of_video = prepare_video(nutshell_directory, orientations)
        write_video_details_to_json(details_of_video)
        create_video(nutshell_directory, orientations, details_of_video)

    else:
        print("Please input arg as prepare, create or all")


if len(sys.argv) > 1:
    main(sys.argv[1], {})
else:
    print("Please input arg as prepare, create or all")
