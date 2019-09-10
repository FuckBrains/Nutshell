__author__ = "Jack Walker"

import os
from VideoCreationModules import BackgroundGenerator
from VideoCreationModules import RecordScreen
from VideoCreationModules import CropRecording
from VideoCreationModules import BackgroundToVideo
from VideoCreationModules import OverlayClips
from VideoCreationModules import ConcatenateClips

orientations = ["landscape", "portrait"]
nutshell_directory = os.path.abspath(os.path.dirname(__file__))

details_of_video = BackgroundGenerator.main(nutshell_directory, orientations)
raw_wide_video = RecordScreen.main(details_of_video)
# TODO: Consider using Jumpcutter to trim audio
raw_square_video = CropRecording.main(details_of_video)

background_video = {}
for orientation in orientations:
    background_video[orientation] = BackgroundToVideo.main(
        orientation,
        details_of_video["background_path"][orientation],
        raw_square_video
    )

    raw_with_background_path = OverlayClips.main(details_of_video, orientation, background_video[orientation], raw_square_video)

    ConcatenateClips.main(details_of_video, nutshell_directory, orientation, raw_with_background_path)
