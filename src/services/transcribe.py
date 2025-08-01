from transformers import pipeline

# Load the Whisper model from Hugging Face
# You can use "openai/whisper-base" for faster, or "openai/whisper-small"/"openai/whisper-medium"/"openai/whisper-large" for better accuracy
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=0)


audio_path = None  # Will be set externally

def transcribe_audio(path=None):
    """
    Transcribe the given audio file and return the result.
    """
    target_path = path if path else audio_path
    if not target_path:
        raise ValueError("audio_path must be set before transcription.")
    result = asr(target_path, return_timestamps=True, generate_kwargs={"language": "en"})
    return result

def save_transcription(result, file_name="transcript.txt"):
    """
    Save the transcription result to a text file.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"Transcription complete! Saved to {file_name}.")