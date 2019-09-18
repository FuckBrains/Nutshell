import os
from moviepy.editor import VideoFileClip


def main(details_of_video):
    raw_full_directory = os.path.join(details_of_video["relative_path"], "raw_full.mp4")
    raw_square_directory = os.path.join(details_of_video["relative_path"], "raw_square.mp4")

    # TODO: Is there anyway to record in 1080 x 1080
    mycmd = 'ffmpeg -i "' + raw_full_directory + '" -filter:v \"crop=815:815:700:214\" -c:a copy "' + raw_square_directory + '"'
    os.system(mycmd)
