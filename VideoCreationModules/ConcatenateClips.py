from moviepy.editor import VideoFileClip, concatenate_videoclips
import os


# Concatenate Clips
def main(details_of_video, nutshell_directory, orientation, raw_with_background_path):

    if orientation == "portrait":
        size = (1080, 1920)
    elif orientation == "landscape":
        size = (1920, 1080)

    # METHOD 1: Moviepy slow good quality
    pre_made_clips_directory = os.path.join(nutshell_directory, "VideoContent", "PremadeClips")

    intro = VideoFileClip(os.path.join(pre_made_clips_directory, orientation, "Intro-RollOnly.mp4"))
    main = VideoFileClip(raw_with_background_path)
    outro = VideoFileClip(os.path.join(pre_made_clips_directory, orientation, "Outro-Blank.mp4"))

    # TODO: Play about with padding
    final_clip = concatenate_videoclips([intro, main, outro], method="chain")
    # final_clip = concatenate_videoclips([intro, main, outro], method="chain")

    # TODO: Check each separately
    # final_clip.write_videofile(os.path.join(details_of_video["relative_path"], "final " + orientation + ".mp4"), fps=60, logger=None)
    final_clip.write_videofile(os.path.join(details_of_video["relative_path"], "final " + orientation + ".mp4"), threads=4)

    intro.close()
    main.close()
    outro.close()

    # METHOD 2: ffmpeg fast bad quality
    # intro_path= os.path.join(nutshell_directory, "VideoContent", "PremadeClips", orientation, "Intro-RollOnly.mp4")
    # main_path = raw_with_background_path
    # outro_path = os.path.join(nutshell_directory, "VideoContent", "PremadeClips", orientation, "Outro-Blank.mp4")
    #
    # mycmd = "(echo file '" + intro_path + "' & echo file '" + main_path + "' & echo file '" + outro_path + "' )>list.txt"
    # os.system(mycmd)
    # output_filename = os.path.join(details_of_video["relative_path"], "final" + orientation + ".mp4")
    # mycmd = "ffmpeg -safe 0 -f concat -i list.txt -c copy " + output_filename + ""
    # os.system(mycmd)


    # METHOD 3: ffmpeg
    # mycmd = 'ffmpeg -i ' + intro_path + ' -i ' + main_path + ' -i ' + outro_path + ' -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mp4'
    # os.system(mycmd)