from pydantic import BaseModel

class Medicine(BaseModel):
    name: str
    dosage: str
    time: str  # HH:MM format
    frequency: str

class MedicineUpdate(BaseModel):
    name: str | None = None
    dosage: str | None = None
    time: str | None = None
    frequency: str | None = None
