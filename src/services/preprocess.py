input_file = "transcript3.txt"
output_file = "transcript_newline.txt"

def preprocess_transcript(infile=None, outfile=None):
    """
    Preprocess the transcript file by splitting into sentences with newlines.
    """
    src = infile if infile else input_file
    dst = outfile if outfile else output_file
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    with open(dst, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + ".\n")
    print(f"Preprocessed transcript saved to {dst}")