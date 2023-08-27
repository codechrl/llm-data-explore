from moviepy.editor import VideoFileClip


def extract_audio_from_video(title, output_path="./data/audio"):
    output_filepath = f"{output_path}/{title}.wav"
    video_path = f"data/video/{title}.mp4"

    video_clip = VideoFileClip(video_path)

    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_filepath)

    video_clip.close()

    return output_filepath
