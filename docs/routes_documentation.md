# ListenBack API Documentation

## Endpoints

### 1. Upload Lecture
**Route:** `/lectures/upload`

**Method:** POST

**Input:**
- `classroom_id` (string, Form Data)
- `title` (string, Form Data)
- `file` (UploadFile, Form Data)

**Output:**
- JSON: `{ "success": true, "lecture_id": <id> }`

**Details:**
- Creates a new lecture record and starts background processing (media upload, transcription, RAG, etc).

---

### 2. Get Lecture Status
**Route:** `/lectures/status`

**Method:** GET

**Input:**
- `classroom_id` (string, Query)
- `lecture_id` (string, Query)

**Output:**
- JSON: `{ "lecture_id": <id>, "status": <status> }`

**Details:**
- Returns the current processing status of a lecture (e.g., uploading, transcribing, ready, error).

---

### 3. Get Lecture Data
**Route:** `/lectures`

**Method:** GET

**Input:**
- `classroom_id` (string, Query)
- `lecture_id` (string, Query)

**Output:**
- JSON: `{ "lecture_id": <id>, "lecture": { ...lecture fields... } }`

**Details:**
- Returns all stored data for a particular lecture.

---


### 4. List Lectures in Classroom
**Route:** `/classrooms/lectures`

**Method:** GET

**Input:**
- `classroom_id` (string, Query)

**Output:**
- JSON: `{ "classroom_id": <id>, "lectures": [ ...lecture objects... ] }`

**Details:**
- Lists all lectures for a given classroom.

---

### 5. Create Classroom
**Route:** `/classrooms/create`

**Method:** POST

**Input:**
- `name` (string, Form Data or JSON)
- `description` (string, Form Data or JSON, optional)

**Output:**
- JSON: `{ "success": true, "classroom_id": <id> }`

**Details:**
- Creates a new classroom record in Firestore.

---

### 6. Update Classroom
**Route:** `/classrooms/update`

**Method:** PUT

**Input:**
- `classroom_id` (string, Form Data or JSON)
- `name` (string, Form Data or JSON, optional)
- `description` (string, Form Data or JSON, optional)

**Output:**
- JSON: `{ "success": true }`

**Details:**
- Updates classroom details in Firestore.

---

### 7. List Classrooms
**Route:** `/classrooms`

**Method:** GET

**Input:**
- None

**Output:**
- JSON: `{ "classrooms": [ ...classroom objects... ] }`

**Details:**
- Lists all classrooms.

---

## Notes
- All endpoints return errors as `{ "detail": <error message> }` with appropriate HTTP status codes.
- File uploads use multipart/form-data.
- All lecture and classroom data is stored in Firestore under `lectures/<classroom_id>/lectures/<lecture_id>` and `classrooms/<classroom_id>`.
