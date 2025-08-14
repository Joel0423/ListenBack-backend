import os
from services.RAG_cloud import get_rag_lecture_chat_model
from vertexai.generative_models import Content, Part
from models.chat_history_model import ChatHistoryModel
from firebase_admin import firestore
from services.chat_session_manager import ChatSessionManager
from config import RAG_TOP_K, RAG_LOCATION, RAG_VECTOR_DISTANCE_THRESHOLD, RAG_MODEL_NAME

session_manager = ChatSessionManager(timeout_seconds=1800)

def serialize_history(history):
    # Convert Content objects to new ChatHistoryModel and dicts for Firestore
    serialized = []
    for item in history:
        model = ChatHistoryModel(
            role=item.role,
            parts=[part.text for part in item.parts]
        )
        serialized.append(model.model_dump())
    return serialized

def deserialize_history(data):
    # Convert dicts from Firestore to Content objects using new ChatHistoryModel
    history = []
    for item in data:
        model = ChatHistoryModel(**item)
        parts = [Part.from_text(text) for text in model.parts]
        history.append(Content(role=model.role, parts=parts))
    return history

def chat_service(uid: str, lecture_id: str, rag_file_id: str, question: str):
    """
    Uses Vertex AI RAG engine to answer a question for a given user and specific rag file, with chat history stored in Firestore and session manager.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    corpus_name  = os.environ.get("RAG_CORPUS_NAME")
    db = firestore.client()
    chat_ref = db.collection("chat_history").document(lecture_id).collection(uid).document("history")

    # Try to get session from memory
    chat_session, history = session_manager.get_session(uid, lecture_id)
    if chat_session is None:
        # Load history from Firestore if session expired or missing
        history_data = chat_ref.get().to_dict() if chat_ref.get().exists else None
        if history_data and "history" in history_data:
            history = deserialize_history(history_data["history"])
        else:
            history = []
            
        chat_model = get_rag_lecture_chat_model(project_id, corpus_name, rag_file_id, RAG_TOP_K, RAG_LOCATION, RAG_VECTOR_DISTANCE_THRESHOLD, RAG_MODEL_NAME)
        chat_session = chat_model.start_chat(history=history)
        session_manager.set_session(uid, lecture_id, chat_session, history)

    # Always append new question/answer, but avoid double appending if chat_session.send_message already appends internally
    prev_len = len(history)
    response = chat_session.send_message(question)
    answer = response.text

    # If chat_session.send_message did NOT append, do it here
    if len(history) == prev_len:
        history.append(Content(role="user", parts=[Part.from_text(question)]))
        history.append(Content(role="model", parts=[Part.from_text(answer)]))
    chat_ref.set({"history": serialize_history(history)})
    session_manager.set_session(uid, lecture_id, chat_session, history)
    session_manager.clear_expired_sessions()
    return answer

def get_chat_history(uid: str, lecture_id: str):
    """
    Returns chat history from Firestore for a given user and lecture.
    """
    db = firestore.client()
    chat_ref = db.collection("chat_history").document(lecture_id).collection(uid).document("history")
    history_data = chat_ref.get().to_dict() if chat_ref.get().exists else None
    return history_data["history"] if history_data else []