from fastapi import APIRouter, HTTPException, UploadFile, Form
from fastapi import Query
from services.lecture_service import get_lecture_status, list_classroom_lectures
from services.lecture_service import create_lecture, update_lecture_status, update_lecture_data
from services.media_upload_cloud import upload_media_to_firebase
import services.audio_extract as audio_extract
import services.transcribe as transcribe
import services.RAG_cloud as RAG_cloud
import services.preprocess as preprocess
import os
import shutil
from pathlib import Path

lecture_router = APIRouter()

@lecture_router.post('/lectures/upload')
async def upload_lecture(
    classroom_id: str = Form(...),
    title: str = Form(...),
    file: UploadFile = Form(...)
):
    audio_path = None
    file_path = None
    preprocessed_transcript_path = None
    try:
        # Create Firestore lecture doc with status 'uploading' first
        lecture_data, lecture_id = create_lecture(
            classroom_id=classroom_id,
            title=title,
            media_url="",  # will update after upload
            transcription="",
            rag_file_id="",
            duration=0,
            status="uploading"
        )

        # Save file locally with lecture_id as prefix
        upload_folder = Path("static/uploads")
        upload_folder.mkdir(exist_ok=True, parents=True)
        file_path = upload_folder / f"{lecture_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Upload media to Firebase Storage
        media_url = upload_media_to_firebase(str(file_path), f"lectures/{lecture_id}/{file.filename}")
        update_lecture_data(classroom_id, lecture_id, {"media_url": media_url})

        # Update status to 'transcribing'
        update_lecture_status(classroom_id, lecture_id, "transcribing")

        # Extract audio and get path
        audio_path = audio_extract.extract_audio_from_video(lecture_id, str(file_path))

        # Transcribe audio
        transcribe_result = transcribe.transcribe_audio(str(audio_path))
        transcription = transcribe_result["text"]
        duration = transcribe_result.get("duration", 0)

        # Preprocess transcript
        preprocessed_transcript_path = preprocess.preprocess_transcript(lecture_id, transcription)

        # Upload to RAG engine with preprocessed transcript text
        rag_file = RAG_cloud.upload_transcript_file_to_corpus(
            project_id=os.getenv("GCP_PROJECT_ID"),
            corpus_name=os.getenv("RAG_CORPUS_NAME"),
            transcript_text_path=preprocessed_transcript_path,
            display_name=title
        )
        rag_file_id = rag_file.name

        # Update Firestore with transcription, rag_file_id, duration, status 'ready'
        update_lecture_data(classroom_id, lecture_id, {
            "transcription": transcription,
            "rag_file_id": rag_file_id,
            "duration": duration,
            "status": "ready"
        })

        return {"success": True, "lecture_id": lecture_id, "media_url": media_url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        # Clean up local files
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        if preprocessed_transcript_path and os.path.exists(preprocessed_transcript_path):
            os.remove(preprocessed_transcript_path)

@lecture_router.get('/lectures/status')
async def lecture_status(classroom_id: str = Query(...), lecture_id: str = Query(...)):
    try:
        status = get_lecture_status(classroom_id, lecture_id)
        return {"lecture_id": lecture_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@lecture_router.get('/classrooms/lectures')
async def classroom_lectures(classroom_id: str = Query(...)):
    try:
        lectures = list_classroom_lectures(classroom_id)
        return {"classroom_id": classroom_id, "lectures": lectures}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))