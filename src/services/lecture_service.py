from firebase_admin import firestore
from datetime import datetime
import os
from services.media_upload_cloud import upload_media_to_firebase
import services.audio_extract as audio_extract
import services.transcribe as transcribe
import services.preprocess as preprocess
import services.RAG_cloud as RAG_cloud

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

def get_lecture_data(classroom_id, lecture_id):
    """Get all data for a particular lecture."""
    lecture_ref = db.collection('lectures').document(classroom_id).collection('lectures').document(lecture_id)
    lecture_doc = lecture_ref.get()
    if not lecture_doc.exists:
        raise ValueError('Lecture not found')
    return lecture_doc.to_dict()


# handle lecture upload processing
def process_lecture_upload(classroom_id, lecture_id, file_path, file_name, title):

    media_url = None
    audio_path = None
    preprocessed_transcript_path = None
    try:
        # Upload media to Firebase Storage
        media_url = upload_media_to_firebase(file_path, f"lectures/{lecture_id}/{file_name}")
        update_lecture_data(classroom_id, lecture_id, {"media_url": media_url})
        print("DONEA")

        # Update status to 'transcribing'
        update_lecture_status(classroom_id, lecture_id, "transcribing")
        print("DONEB")

        # Extract audio and get path
        audio_path = audio_extract.extract_audio_from_video(lecture_id, file_path)
        print("DONEC")

        # Transcribe audio
        transcribe_result = transcribe.transcribe_audio(str(audio_path))
        transcription = transcribe_result["text"]
        duration = transcribe_result.get("duration", 0)
        print("DONED")

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
    except Exception as e:
        update_lecture_data(classroom_id, lecture_id, {"status": "error", "error_message": str(e)})
    finally:
        # Clean up local files
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        if audio_path and audio_path != file_path and os.path.exists(audio_path):
            os.remove(audio_path)
        if preprocessed_transcript_path and os.path.exists(preprocessed_transcript_path):
            os.remove(preprocessed_transcript_path)