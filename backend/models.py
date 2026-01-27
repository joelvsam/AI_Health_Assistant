# backend/models.py

from pydantic import BaseModel

class Medicine(BaseModel):
    """Pydantic model for creating a new medicine."""
    name: str
    dosage: str
    time: str  # HH:MM format
    frequency: str

class MedicineUpdate(BaseModel):
    """Pydantic model for updating an existing medicine. All fields are optional."""
    name: str | None = None
    dosage: str | None = None
    time: str | None = None
    frequency: str | None = None

class MedicineNLInput(BaseModel):
    """Pydantic model for processing natural language input for medicine."""
    text: str