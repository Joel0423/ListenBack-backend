from fastapi import APIRouter, HTTPException, UploadFile, Form
from fastapi import Query, BackgroundTasks
from services.lecture_service import get_lecture_status, list_classroom_lectures, get_lecture_data
from services.lecture_service import create_lecture
from config import UPLOADS_TEMP_PATH
import shutil
from pathlib import Path
from services.lecture_service import process_lecture_upload

lecture_router = APIRouter()

@lecture_router.post('/lectures/upload')
async def upload_lecture(
    classroom_id: str = Form(...),
    title: str = Form(...),
    file: UploadFile = Form(...),
    background_tasks: BackgroundTasks = None
):
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
        upload_folder = Path(UPLOADS_TEMP_PATH)
        upload_folder.mkdir(exist_ok=True, parents=True)
        file_path = upload_folder / f"{lecture_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Start background processing
        if background_tasks is not None:
            background_tasks.add_task(
                process_lecture_upload,
                classroom_id=classroom_id,
                lecture_id=lecture_id,
                file_path=str(file_path),
                file_name=file.filename,
                title=title
            )

        return {"success": True, "lecture_id": lecture_id}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    
@lecture_router.get('/lectures')
async def get_lecture(classroom_id: str = Query(...), lecture_id: str = Query(...)):
    try:
        lecture = get_lecture_data(classroom_id, lecture_id)
        return {"lecture_id": lecture_id, "lecture": lecture}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))