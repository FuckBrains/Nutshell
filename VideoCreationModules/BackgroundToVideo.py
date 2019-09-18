import math
import os
from moviepy.editor import ImageClip, VideoFileClip


def main(orientation, background_image_path):

    if orientation == "portrait":
        size = (1080, 1920)
    elif orientation == "landscape":
        size = (1920, 1080)

    background_image = ImageClip(os.path.join(background_image_path, "background.png")).set_duration(1).resize(size)
    # fps = (1/math.ceil(raw_square_video.duration))
    # fps = 30
    background_image.write_videofile(os.path.join(background_image_path, "background.mp4"), fps=60)
    background_image.close()

    return os.path.join(background_image_path, "background.mp4")
