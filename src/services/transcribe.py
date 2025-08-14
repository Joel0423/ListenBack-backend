import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def transcribe_audio(file_path):
    """
    Transcribe audio using Groq Whisper API.
    Returns a dict with 'text' and optionally other metadata.
    """

    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3",
            temperature=0.1,
            response_format="verbose_json",
            language="en",
            timestamp_granularities=["segment"]
        )

    print("\n\nTranscription--\n\n", transcription)
    # transcription.duration is available in verbose_json response
    return {
        "text": transcription.text,
        "duration": getattr(transcription, "duration", None)
    }