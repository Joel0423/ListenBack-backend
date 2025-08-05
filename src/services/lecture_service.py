from firebase_admin import firestore
from datetime import datetime

db = firestore.client()

def create_lecture(classroom_id, title, media_url, transcription, rag_file_id, duration, status):
    lecture_id = db.collection('lectures').document().id
    lecture_data = {
        "lecture_id": lecture_id,
        "classroomId": classroom_id,
        "title": title,
        "media_url": media_url,
        "transcription": transcription,
        "rag_file_id": rag_file_id,
        "duration": duration,
        "status": status,
        "upload_time": datetime.utcnow().isoformat()
    }
    # Save lecture under lectures>classroom_id>lecture_id
    lecture_ref = db.collection('lectures').document(classroom_id).collection('lectures').document(lecture_id)
    lecture_ref.set(lecture_data)
    return lecture_data, lecture_id

def update_lecture_status(classroom_id, lecture_id, status):
    lecture_ref = db.collection('lectures').document(classroom_id).collection('lectures').document(lecture_id)
    lecture_ref.update({"status": status})

def update_lecture_data(classroom_id, lecture_id, update_fields):
    lecture_ref = db.collection('lectures').document(classroom_id).collection('lectures').document(lecture_id)
    lecture_ref.update(update_fields)

def get_lecture_status(classroom_id, lecture_id):
    """Get the processing status of a lecture."""
    lecture_ref = db.collection('lectures').document(classroom_id).collection('lectures').document(lecture_id)
    lecture_doc = lecture_ref.get()
    if not lecture_doc.exists:
        raise ValueError('Lecture not found')
    return lecture_doc.to_dict().get('status', None)

def list_classroom_lectures(classroom_id):
    """List all lectures for a classroom."""
    lectures_ref = db.collection('lectures').document(classroom_id).collection('lectures')
    lectures = lectures_ref.stream()
    return [lecture.to_dict() for lecture in lectures]