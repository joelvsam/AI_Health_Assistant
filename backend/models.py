from pydantic import BaseModel

class Medicine(BaseModel):
    name: str
    dosage: str
    time: str
    frequency: str
