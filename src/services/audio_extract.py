import ffmpeg
from pathlib import Path

def extract_audio_from_video(lecture_id: str, video_path: str):
    """
    Extracts audio from a video file and saves it as an MP3 file with lecture_id as prefix.
    Args:
        lecture_id (str): The lecture ID to prefix the audio file.
        video_path (str): Path to the input video file.
    Returns:
        str: Path to the extracted audio file.
    """
    upload_folder = Path("static/uploads")
    audio_path = upload_folder / f"{lecture_id}_audio.mp3"
    try:
        (
            ffmpeg
            .input(video_path)
            .output(str(audio_path), format='mp3', acodec='libmp3lame', ac=2, ar='44100')
            .overwrite_output()
            .run(quiet=True)
        )
        print("Audio extracted successfully and saved to:", audio_path)
        return str(audio_path)
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to extract audio: {e.stderr.decode() if hasattr(e.stderr, 'decode') else e.stderr}")
