import src.services.RAG_cloud as RAG_cloud
import os
PROJECT_ID = os.getenv("PROJECT_ID")
var = 0
import re
from dotenv import load_dotenv

load_dotenv()

corpus_name = os.environ["RAG_CORPUS_NAME"]  # Must be set in your environment
rag_file = RAG_cloud.upload_transcript_file_to_corpus(
    project_id=PROJECT_ID,
    corpus_name=corpus_name,
    transcript_file=str(r"testing.txt"),
    display_name= "Lecture_" + str(var)
)

print("rag_file:", rag_file)
print("proper name: ",rag_file.name)
print("rag_file.display_name:", rag_file.display_name)

match = re.search(r"([^/]+)/?$", rag_file.name)

result = match.group(1)

print("id i guess for our purpose:", result)
