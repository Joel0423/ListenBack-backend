from pathlib import Path
from config import UPLOADS_TEMP_PATH

def preprocess_transcript(lecture_id, transcript_text):
    """
    Preprocess the transcript text by splitting into sentences with newlines,
    save to {UPLOADS_TEMP_PATH} with lecture_id prefix, and return the file path.
    """
    upload_folder = Path(UPLOADS_TEMP_PATH)
    upload_folder.mkdir(exist_ok=True, parents=True)
    out_path = upload_folder / f"{lecture_id}_transcript_newline.txt"
    sentences = [s.strip() for s in transcript_text.split('.') if s.strip()]
    with open(out_path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + ".\n")

    return str(out_path)