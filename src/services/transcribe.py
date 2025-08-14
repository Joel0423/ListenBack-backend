import os
from groq import Groq
from config import GROQ_MODEL, GROQ_TEMPERATURE, GROQ_LANGUAGE

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def transcribe_audio(file_path):
    """
    Transcribe audio using Groq Whisper API.
    Returns a dict with 'text' and optionally other metadata.
    """

    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            response_format="verbose_json",
            language=GROQ_LANGUAGE,
            timestamp_granularities=["segment"]
        )


    # transcription.duration is available in verbose_json response
    return {
        "text": transcription.text,
        "duration": getattr(transcription, "duration", None)
    }