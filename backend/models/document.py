from pydantic import BaseModel
from datetime import datetime

class Document(BaseModel):
    id: int
    filename: str
    filepath: str
    user_id: int
    created_at: datetime

class DocumentCreate(BaseModel):
    filename: str
    filepath: str
