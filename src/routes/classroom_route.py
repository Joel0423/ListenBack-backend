from fastapi import APIRouter, HTTPException, Form, Query
from services.classroom_service import get_user_classrooms, list_user_classroom_ids, create_classroom, join_classroom, get_classroom_details

classroom_router = APIRouter()

@classroom_router.get('/classrooms/list')
async def list_classroom_ids(uid: str = Query(...)):
    try:
        classrooms = list_user_classroom_ids(uid)
        return {"classrooms": classrooms}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@classroom_router.get('/classrooms')
async def get_classrooms(uid: str = Query(...)):
    try:
        classrooms = get_user_classrooms(uid)
        return {"classrooms": classrooms}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@classroom_router.post('/classrooms')
async def create_new_classroom(
    uid: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...)
):
    try:
        classroom = create_classroom(uid, subject, description)
        return classroom
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@classroom_router.post('/classrooms/join')
async def join_classroom_endpoint(uid: str = Form(...), code: str = Form(...)):
    try:
        classroom = join_classroom(uid, code)
        return classroom
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@classroom_router.get('/classrooms/details')
async def get_classroom(classroom_id: str = Query(...)):
    try:
        classroom = get_classroom_details(classroom_id)
        return classroom
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))