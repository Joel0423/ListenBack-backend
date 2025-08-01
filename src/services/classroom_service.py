import random
import string
from datetime import datetime
from firebase_admin import firestore

db = firestore.client()

def list_user_classrooms(uid):
    """List classrooms for a given user."""
    user_ref = db.collection('users').document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise ValueError('User not found')

    user_data = user_doc.to_dict()
    return user_data.get('classrooms', [])

def create_classroom(uid, subject, description):
    """Create a new classroom for a teacher."""
    user_ref = db.collection('users').document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise ValueError('User not found')

    user_data = user_doc.to_dict()

    if user_data['role'] != 'Teacher':
        raise ValueError('Only teachers can create classrooms')

    # Generate random 6-digit alphanumeric code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    classroom_id = db.collection('classrooms').document().id
    classroom_data = {
        "classroom_id": classroom_id,
        "subject": subject,
        "description": description,
        "code": code,
        "teacher_id": uid,
        "members": [],
        "createdAt": datetime.utcnow().isoformat(),
        "isActive": True
    }

    # Save classroom directly under the classrooms collection
    classroom_ref = db.collection('classrooms').document(classroom_id)
    classroom_ref.set(classroom_data)

    # Update user's classrooms field
    user_ref.update({"classrooms": firestore.ArrayUnion([classroom_id])})

    return classroom_data

def join_classroom(uid, code):
    """Join a classroom using its code."""
    user_ref = db.collection('users').document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise ValueError('User not found')

    user_data = user_doc.to_dict()

    if user_data['role'] != 'Student':
        raise ValueError('Only students can join classrooms')

    # Find classroom by code
    classrooms_ref = db.collection('classrooms').where('code', '==', code)
    classrooms = classrooms_ref.get()

    if not classrooms:
        raise ValueError('Classroom not found')

    classroom = classrooms[0]
    classroom_data = classroom.to_dict()

    # Update classroom members
    classroom.reference.update({"members": firestore.ArrayUnion([uid])})

    # Update user's classrooms field
    user_ref.update({"classrooms": firestore.ArrayUnion([classroom_data['class_id']])})

    return classroom_data

def get_classroom_details(classroom_id):
    """Get details of a specific classroom."""
    classroom_ref = db.collection('classrooms').document(classroom_id)
    classroom_doc = classroom_ref.get()

    if not classroom_doc.exists:
        raise ValueError('Classroom not found')

    return classroom_doc.to_dict()