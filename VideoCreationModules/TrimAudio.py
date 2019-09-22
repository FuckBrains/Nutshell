import os


def main(details_of_video):
    raw_square_directory = os.path.join(details_of_video["relative_path"], "raw_square.mp4")
    trimmed_square_directory = os.path.join(details_of_video["relative_path"], "trimmed_square.mp4")

    # TODO: Is there anyway to record in 1080 x 1080
    jumpcutter_path = os.path.join("jumpcutter", "jumpcutter.py")
    mycmd = "python " + jumpcutter_path + " --input_file " + raw_square_directory + " --output_file " + trimmed_square_directory + " --sounded_speed 1 --silent_speed 999999 --frame_margin 2 --frame_rate 60"
    os.system(mycmd)
