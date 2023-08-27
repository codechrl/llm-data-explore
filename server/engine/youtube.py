from pytube import YouTube


def download(url, output_path="./data/video"):
    """docstring"""
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream (you can customize this)
        video_stream = yt.streams.get_highest_resolution()

        # Set the output path for the downloaded video
        output_file = video_stream.default_filename
        output_filepath = f"{output_path}/{output_file}"

        # Download the video
        video_stream.download(output_path)

        print(f"Download complete: {output_filepath}")
        return output_file
    except Exception as exc:
        print(f"Error: {exc}")
