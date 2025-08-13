from pydantic import BaseModel
from typing import List

class ChatHistoryModel(BaseModel):
    role: str
    parts: List[str]
