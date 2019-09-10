import math
import os
from moviepy.editor import ImageClip, VideoFileClip


nutshell_directory = os.path.abspath(os.path.dirname(__file__))
# fps = (1/14)
# background_image.write_videofile(os.path.join(nutshell_directory, "background.mp4"), fps=fps)

background_image = ImageClip(os.path.join(nutshell_directory, "Portrait Lemon Lime Filled Background.png")).set_duration(1).resize((1920, 1080))
background_image.write_imagefile(os.path.join(nutshell_directory, "SMALL Portrait Lemon Lime Filled Background.png"), "PNG")