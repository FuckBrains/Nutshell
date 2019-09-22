from moviepy.editor import VideoFileClip, CompositeVideoClip
import os


def overlay_clips(resized_raw_square_video, background_video, position):
    return CompositeVideoClip(
        [background_video.set_duration(resized_raw_square_video.duration),
         resized_raw_square_video.set_pos(position)]).set_duration(resized_raw_square_video.duration)


def main(details_of_video, orientation, background_video_path):

    background_video = VideoFileClip(background_video_path)
    trimmed_square_video = VideoFileClip(os.path.join(details_of_video["relative_path"], "trimmed_square.mp4"))

    # TODO: Check with recording screen at different scale
    # TODO: Check with changing screen size once
    # 30 mins with resizing
    # 15 mins without resizing
    # https://stackoverflow.com/questions/25122740/different-between-s-and-vf-scale-in-ffmpeg-especially-in-two-pass-transc
    resized_raw_square_video = trimmed_square_video.resize((1080, 1080))
    # resized_raw_square_video = raw_square_video

    # TODO: Tidy up
    if orientation == "landscape":
        final_clip = (overlay_clips(resized_raw_square_video, background_video, (420, 0)))

    elif orientation == "portrait":
        final_clip = (overlay_clips(resized_raw_square_video, background_video, (0, 420)))

    else:
        print("orientation not supported")

    final_clip_path = os.path.join(details_of_video["relative_path"], "raw_with_background_" + orientation + ".mp4")
    # final_clip.write_videofile(final_clip_path, fps=60, logger=None)
    final_clip.write_videofile(final_clip_path, threads=4)

    background_video.reader.close()
    trimmed_square_video.reader.close()

    return final_clip_path
