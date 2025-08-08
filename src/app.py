from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from config import UPLOADS_TEMP_PATH

load_dotenv()

import services.transcribe as transcribe
import services.preprocess as preprocess
import services.RAG_cloud as RAG_cloud
from services.audio_extract import extract_audio_from_video

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIREBASE_CRED_FILE"))
    firebase_admin.initialize_app(cred, {
    'storageBucket': f"{os.getenv('FIREBASE_STORAGE_DEFAULT_BUCKET')}"
})

from routes.classroom_route import classroom_router
from routes.lecture_route import lecture_router

app = FastAPI(title="ListenBack - RAG Chatbot for Lectures")

app.include_router(classroom_router)
app.include_router(lecture_router)

if not os.path.exists("static"):
    os.makedirs("static")
    os.makedirs(f"{UPLOADS_TEMP_PATH}", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global state
current_video_path = None
current_transcript = None
current_index = None
lecture_no = 1
API_KEY = os.getenv("GEMINI_API_KEY")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "video_path": current_video_path,
        "transcript": current_transcript
    })

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global current_video_path, current_transcript, current_index, lecture_no, project_id
    try:
        upload_folder = Path(UPLOADS_TEMP_PATH)
        upload_folder.mkdir(exist_ok=True, parents=True)
        file_extension = os.path.splitext(file.filename)[1].lower()
        file_path = upload_folder / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        audio_extensions = ['.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg']
        if file_extension not in audio_extensions:
            current_video_path = f"/{UPLOADS_TEMP_PATH}/{file.filename}"
            audio_path = upload_folder / "extracted_audio.mp3"
            extract_audio_from_video(str(file_path), str(audio_path))
        else:
            current_video_path = None
            audio_path = file_path
        transcribe.audio_path = str(audio_path)
        transcribe_result = transcribe.transcribe_audio(str(audio_path))
        transcript_file = upload_folder / "transcript.txt"
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcribe_result["text"])
        current_transcript = transcribe_result["text"]
        processed_file = upload_folder / "transcript_newline.txt"
        preprocess.preprocess_transcript(str(transcript_file), str(processed_file))
        # Upload processed transcript to Vertex RAG Corpus
        
        corpus_name = os.environ["RAG_CORPUS_NAME"]  # Must be set in your environment
        rag_file = RAG_cloud.upload_transcript_file_to_corpus(
            project_id=GCP_PROJECT_ID,
            corpus_name=corpus_name,
            transcript_file=str(processed_file),
            display_name= "Lecture_" + str(lecture_no)
        )
        lecture_no = lecture_no+1
        current_index = rag_file.name  # Store file resource name for later retrieval
        return {
            "success": True,
            "message": "File processed and uploaded to Vertex RAG Corpus successfully",
            "video_path": current_video_path,
            "transcript": current_transcript
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/query")
async def query(question: str = Form(...)):
    global current_index
    if not current_index:
        raise HTTPException(status_code=400, detail="Please upload a file first")
    try:

        corpus_name = os.environ["RAG_CORPUS_NAME"]
        # Use Gemini RAG answer
        answer = RAG_cloud.vertex_rag_generate_answer(
            project_id=GCP_PROJECT_ID,
            corpus_name=corpus_name,
            query=question
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host=host, port=port, reload=True)
