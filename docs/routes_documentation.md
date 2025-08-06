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

#### 1. Get User's Classrooms

Retrieves all classrooms associated with a user.

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
          "classroom_id": "ghMjwXHMhPWkG6kCMIVc",
          "subject": "Physics 101",
          "description": "Introduction to Physics",
          "code": "ABC123",
          "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32",
          "members": ["userId1", "userId2"],
          "createdAt": "2023-08-01T12:34:56.789Z",
          "isActive": true
        }
      ]
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "User not found" }`

#### 2. Create a Classroom

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
      "classroom_id": "ghMjwXHMhPWkG6kCMIVc",
      "subject": "Physics 101",
      "description": "Introduction to Physics",
      "code": "ABC123",
      "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32",
      "members": [],
      "createdAt": "2023-08-01T12:34:56.789Z",
      "isActive": true
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Only teachers can create classrooms" }`

#### 3. Join a Classroom

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
      "classroom_id": "ghMjwXHMhPWkG6kCMIVc",
      "subject": "Physics 101",
      "description": "Introduction to Physics",
      "code": "ABC123",
      "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32",
      "members": ["userId1"],
      "createdAt": "2023-08-01T12:34:56.789Z",
      "isActive": true
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Only students can join classrooms" }` or `{ "detail": "Classroom not found" }`

#### 4. Get Classroom Details

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
      "classroom_id": "ghMjwXHMhPWkG6kCMIVc",
      "subject": "Physics 101",
      "description": "Introduction to Physics",
      "code": "ABC123",
      "teacher_id": "2S1z2UrNRweQtOHEgg4QNo0aEX32",
      "members": ["userId1", "userId2"],
      "createdAt": "2023-08-01T12:34:56.789Z",
      "isActive": true
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
      "classroom_id": "aaaaaa",
      "lectures": [
        {
          "lecture_id": "udsOO7Wj6u026imA0mvU",
          "title": "Introduction to Thermodynamics",
          "media_url": "https://storage.firebase.com/...",
          "transcription": "Today we will discuss thermodynamics...",
          "status": "ready",
          "upload_time": "2023-08-01T12:34:56.789Z",
          "duration": 1200,
          "rag_file_id": "projects/12345/..."
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
      "lecture_id": "udsOO7Wj6u026imA0mvU",
      "lecture": {
        "lecture_id": "udsOO7Wj6u026imA0mvU",
        "classroomId": "aaaaaa",
        "title": "Introduction to Thermodynamics",
        "media_url": "https://storage.firebase.com/...",
        "transcription": "Today we will discuss thermodynamics...",
        "rag_file_id": "projects/12345/...",
        "duration": 1200,
        "status": "ready",
        "upload_time": "2023-08-01T12:34:56.789Z"
      }
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{ "detail": "Lecture not found" }`

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


