from pydantic import BaseModel
from datetime import datetime

class Document(BaseModel):
    """
    Represents a document in the system.
    """
    id: int
    filename: str
    filepath: str
    user_id: int
    created_at: datetime

class DocumentCreate(BaseModel):
    """
    Represents a document to be created.
    """
    filename: str
    filepath: str