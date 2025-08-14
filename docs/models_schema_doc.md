## Data Models

### Classroom
```
{
  "classroom_id": string,
  "teacher_id": string,
  "subject": string,
  "description": string,
  "code": string,         // 6-character alphanumeric join code
  "members": string[],    // Array of user IDs
  "created_time": string,    // ISO datetime string
  "is_active": boolean
}
```

### Lecture
```
{
  "lecture_id": string,
  "classroom_id": string,
  "title": string,
  "media_url": string,     // Firebase Storage URL
  "transcription": string, // Full lecture transcript
  "rag_file_id": string,   // ID in RAG system
  "duration": number,      // Duration in seconds
  "status": string,        // "uploading", "transcribing", "ready", "error"
  "upload_time": string    // ISO datetime string
}
```

### ChatHistoryModel
```
{
  "role": string,         // 'user' or 'model'
  "parts": string[]       // Array of message parts (usually one string per message)
}
```