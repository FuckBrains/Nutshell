import os
from moviepy.editor import VideoFileClip
import subprocess
from msvcrt import getch


def main(details_of_video):

    output_filepath = os.path.join(details_of_video["relative_path"], "raw_full.mp4")
    # TODO: Make command more generic
    mycmd = 'ffmpeg -y -rtbufsize 150M -f dshow -framerate 60 -i video="screen-capture-recorder":audio="Microphone (4- Logitech USB Microphone)" -c:v libx264 -r 60 -preset ultrafast -tune zerolatency -crf 28 -pix_fmt yuv420p -movflags +faststart -c:a aac -strict -2 -ac 2 -b:a 192k "' + output_filepath + '"'
    # os.system(mycmd)
    subprocess.call(mycmd, shell=True)
    raw_wide_recording = VideoFileClip(output_filepath)
    raw_wide_recording.close()

    return raw_wide_recording
