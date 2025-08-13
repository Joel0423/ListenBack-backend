from fastapi import APIRouter, HTTPException, Query
from services.questions_service import chat_service, get_chat_history
import re

questions_router = APIRouter()

@questions_router.get("/ask")
def ask_question(uid: str = Query(...), lecture_id: str = Query(...), rag_file_id: str = Query(...), question: str = Query(...)):
    """
    GET /ask?uid=...&lecture_id=...&rag_file_id=...&question=...
    Passes parameters to the questions service and returns the RAG answer.
    """
    try:
        match = re.search(r'[^/]+$', rag_file_id)
        if match:
            rag_file_id = match.group(0)

        answer = chat_service(uid, lecture_id, rag_file_id, question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@questions_router.get("/ask/history")
def ask_history(uid: str = Query(...), lecture_id: str = Query(...)):
    """
    GET /ask/history?uid=...&lecture_id=...
    Returns chat history for the user and lecture.
    """
    try:
        history = get_chat_history(uid, lecture_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))