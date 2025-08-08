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

def save_transcription(result, file_name="transcript.txt"):
    """
    Save the transcription result to a text file.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Transcription complete! Saved to {file_name}.")



if __name__ == "__main__":
    # Example usage
    
    audio_file_path = r"C:\Users\joela\Pictures\Camera Roll\LB_test.mp4"
    transcription_result = transcribe_audio(audio_file_path)

    print(transcription_result)