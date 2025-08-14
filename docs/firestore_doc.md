## Firestore Reference Paths

### Classrooms
```
classrooms (collection)
  └── classroom_id (document)
	  └── classroom data (fields)
```

### Lectures
```
lectures (collection)
  └── classroom_id (document)
	  └── lectures (collection)
		  └── lecture_id (document)
			  └── lecture data (fields)
```

### Chat History
```
chat_history (collection)
  └── lecture_id (document)
	  └── uid (collection)
		  └── history (document)
			  └── chat history data (fields)
```
