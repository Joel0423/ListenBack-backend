from pathlib import Path

def preprocess_transcript(lecture_id, transcript_text):
    """
    Preprocess the transcript text by splitting into sentences with newlines,
    save to static/uploads with lecture_id prefix, and return the file path.
    """
    upload_folder = Path("static/uploads")
    upload_folder.mkdir(exist_ok=True, parents=True)
    out_path = upload_folder / f"{lecture_id}_transcript_newline.txt"
    sentences = [s.strip() for s in transcript_text.split('.') if s.strip()]
    with open(out_path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + ".\n")
    print(f"Preprocessed transcript saved to {out_path}")
    return str(out_path)