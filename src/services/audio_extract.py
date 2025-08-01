import ffmpeg

def extract_audio_from_video(video_path: str, audio_path: str):
    """
    Extracts audio from a video file and saves it as an MP3 file.
    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to save the extracted audio file (should end with .mp3).
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format='mp3', acodec='libmp3lame', ac=2, ar='44100')
            .overwrite_output()
            .run(quiet=True)
        )
        print("Audio extracted successfully and saved to:", audio_path)
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to extract audio: {e.stderr.decode() if hasattr(e.stderr, 'decode') else e.stderr}")
