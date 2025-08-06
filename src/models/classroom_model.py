from pydantic import BaseModel, Field
from typing import List

class Classroom(BaseModel):
    classroom_id: str
    teacher_id: str
    subject: str
    description: str
    code: str
    members: List[str] = Field(default_factory=list)
    created_time: str
    is_active: bool = True
