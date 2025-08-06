from pydantic import BaseModel
from typing import Optional

class Lecture(BaseModel):
    lecture_id: str
    classroom_id: str
    title: str
    media_url: Optional[str] = None
    transcription: Optional[str] = None
    rag_file_id: Optional[str] = None
    duration: Optional[float] = None
    status: str
    upload_time: str
