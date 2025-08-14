# ListenBack API Documentation

This document outlines all available endpoints in the ListenBack backend API.

## Base URL

For local development:
```
http://localhost:8000
```

## Authentication

Most endpoints require a user ID (`uid`) which is obtained from Firebase Authentication.

## Endpoints

### Classroom Endpoints

#### 1. Get User's Classrooms ids

Retrieves all classrooms ids associated with a user.

- **URL**: `/classrooms/list`
- **Method**: `GET`
- **Parameters**:
  - `uid` (query, required): The user ID of the student or teacher
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
      "classrooms": [
          "8esgWZKsvtsSFnr5stMX",
          "rNVQ3UjKjU0g6kHVRs8b",
          "Wt3OUwZ4drcpzN7u4jb3"
      ]
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "User not found" }`

#### 2. Get all User's Classrooms with details

Retrieves all classrooms ids associated with a user.

- **URL**: `/classrooms`
- **Method**: `GET`
- **Parameters**:
  - `uid` (query, required): The user ID of the student or teacher
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
    "classrooms": [
        {
            "classroom_id": "Wt3OUwZ4drcpzN7u4jb3",
            "description": "very bad",
            "subject": "maths",
            "members": [
                "Lv2BbNg70YOykAqJtHGqe5RkRoq1"
            ],
            "code": "DRM5ND",
            "created_time": "2025-08-13T13:22:35.347312",
            "is_active": true,
            "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32"
        },
        {
            "classroom_id": "lRlto9TMiWfES8jT9Ai4",
            "description": "some desc",
            "subject": "fnew class",
            "members": [],
            "code": "FMZACQ",
            "created_time": "2025-08-14T08:43:02.130379",
            "is_active": true,
            "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32"
        }
      ]
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "User not found" }`

#### 3. Create a Classroom

Creates a new classroom with the user as the teacher.

- **URL**: `/classrooms`
- **Method**: `POST`
- **Request Type**: `form-data`
- **Parameters**:
  - `uid` (form, required): The user ID of the teacher
  - `subject` (form, required): The subject or title of the classroom
  - `description` (form, required): A description of the classroom
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
    "classroom_id": "lRlto9TMiWfES8jT9Ai4",
    "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32",
    "subject": "fnew class",
    "description": "some desc",
    "code": "FMZACQ",
    "members": [],
    "created_time": "2025-08-14T08:43:02.130379",
    "is_active": true
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Only teachers can create classrooms" }`

#### 4. Join a Classroom

Allows a student to join an existing classroom using a code.

- **URL**: `/classrooms/join`
- **Method**: `POST`
- **Request Type**: `form-data`
- **Parameters**:
  - `uid` (form, required): The user ID of the student
  - `code` (form, required): The join code for the classroom
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
    "classroom_id": "zXVIqWiI7QYOpTxPusI8",
    "description": "some desc",
    "subject": "fnew class",
    "members": [],
    "code": "M8G51L",
    "created_time": "2025-08-14T08:47:02.535072",
    "is_active": true,
    "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32"
  }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Only students can join classrooms" }` or `{ "detail": "Classroom not found" }`

#### 4. Get one Classroom Details

Gets detailed information about a specific classroom.

- **URL**: `/classrooms/details`
- **Method**: `GET`
- **Parameters**:
  - `classroom_id` (query, required): The ID of the classroom
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
    "classroom_id": "zXVIqWiI7QYOpTxPusI8",
    "description": "some desc",
    "subject": "fnew class",
    "members": [
        "Lv2BbNg70YOykAqJtHGqe5RkRoq1"
    ],
    "code": "M8G51L",
    "created_time": "2025-08-14T08:47:02.535072",
    "is_active": true,
    "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32"
  }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Classroom not found" }`

#### 5. Get All Lectures for a Classroom

Retrieves all lectures associated with a specific classroom.

- **URL**: `/classrooms/lectures`
- **Method**: `GET`
- **Parameters**:
  - `classroom_id` (query, required): The ID of the classroom
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
    "classroom_id": "Wt3OUwZ4drcpzN7u4jb3",
    "lectures": [
        {
            "classroom_id": "Wt3OUwZ4drcpzN7u4jb3",
            "duration": 4.35,
            "transcription": " Hello, this is Joe.",
            "media_url": "https://storage.googleapis.com/listen-back-e8414.firebasestorage.app/lectures/JiBze4XySIbUgRXS2K5D/LB_test.mp4",
            "lecture_id": "JiBze4XySIbUgRXS2K5D",
            "title": "maths first lecture",
            "status": "ready",
            "upload_time": "2025-08-13T13:32:24.616442",
            "rag_file_id": "projects/listenback/locations/us-central1/ragCorpora/5685794529555251200/ragFiles/5499240336392864860"
        }
      ]
  }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Classroom not found" }`

### Lecture Endpoints

#### 1. Upload a Lecture

Uploads a lecture video file to the system.

- **URL**: `/lectures/upload`
- **Method**: `POST`
- **Request Type**: `form-data`
- **Parameters**:
  - `classroom_id` (form, required): The ID of the classroom
  - `title` (form, required): The title of the lecture
  - `file` (form, required): The lecture media file (video)
- **Processing**:
  - The API processes the video in the background:
    1. Uploads the video to Firebase Storage
    2. Extracts audio from the video
    3. Transcribes the audio
    4. Preprocesses the transcript
    5. Uploads the transcript to the RAG (Retrieval-Augmented Generation) system
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
      "success": true,
      "lecture_id": "udsOO7Wj6u026imA0mvU"
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Error processing upload" }`

#### 2. Get Lecture Status

Checks the processing status of a lecture.

- **URL**: `/lectures/status`
- **Method**: `GET`
- **Parameters**:
  - `classroom_id` (query, required): The ID of the classroom
  - `lecture_id` (query, required): The ID of the lecture
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
      "lecture_id": "udsOO7Wj6u026imA0mvU",
      "status": "ready"  // Possible values: "uploading", "transcribing", "ready", "error"
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Lecture not found" }`

#### 3. Get Lecture Data

Retrieves complete data for a specific lecture.

- **URL**: `/lectures`
- **Method**: `GET`
- **Parameters**:
  - `classroom_id` (query, required): The ID of the classroom
  - `lecture_id` (query, required): The ID of the lecture
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
    "lecture_id": "3TkIwtMgJqYavBqUWwuD",
    "lecture": {
        "classroom_id": "zXVIqWiI7QYOpTxPusI8",
        "duration": 4.35,
        "transcription": " Hello, this is Joe Ed.",
        "media_url": "https://storage.googleapis.com/listen-back-e8414.firebasestorage.app/lectures/3TkIwtMgJqYavBqUWwuD/LB_test.mp4",
        "lecture_id": "3TkIwtMgJqYavBqUWwuD",
        "title": "testing background tasks",
        "status": "ready",
        "upload_time": "2025-08-14T08:51:06.442222",
        "rag_file_id": "projects/listenback/locations/us-central1/ragCorpora/5685794529555251200/ragFiles/5499823577164574639"
    }
  }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Lecture not found" }`


### Questions Endpoints

#### 1. Ask question

Ask a question for a particular lecture

- **URL**: `/ask`
- **Method**: `GET`
- **Parameters**:
  - `uid` (query, required): User ID
  - `lecture_id` (query, required): The ID of the lecture
  - `rag_file_id` (query, required): The ID of the RAG file
  - `question` (query, required): The user's query
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
      "answer": "This is Joe Ed.\n"
    }
    ```
- **Error Response**:

#### 1. chat history for a user

gets a user's chat hisotry for a particular lecture

- **URL**: `/ask/history`
- **Method**: `GET`
- **Parameters**:
  - `uid` (query, required): User ID
  - `lecture_id` (query, required): The ID of the lecture
- **Success Response**:
  - **Code**: 200 OK
  - **Content Example**:
    ```json
    {
    "history": [
        {
            "parts": [
                "who is this"
            ],
            "role": "user"
        },
        {
            "parts": [
                "This is Joe Ed.\n"
            ],
            "role": "model"
        }
      ]
    }
    ```
- **Error Response**:


## Status Codes and Workflow

### Lecture Processing Status Codes

- **uploading**: Initial state when a lecture is being uploaded
- **transcribing**: Video has been uploaded, audio extraction and transcription in progress
- **ready**: Processing complete, lecture ready for viewing/interaction
- **error**: An error occurred during processing

### Lecture Processing Workflow

1. User uploads a video file via `/lectures/upload` endpoint
2. System creates a lecture document with status "uploading"
3. System processes the file in the background:
   - Uploads video to Firebase Storage
   - Updates status to "transcribing"
   - Extracts audio from video
   - Transcribes audio to text
   - Preprocesses transcript
   - Uploads to RAG engine
   - Updates status to "ready" when complete
4. If any error occurs, status is updated to "error" with an error message
5. Client can check status via `/lectures/status` endpoint


