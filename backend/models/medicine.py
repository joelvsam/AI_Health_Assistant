from pydantic import BaseModel

class Medicine(BaseModel):
    """
    Represents a medicine in the system.
    """
    name: str
    dosage: str
    time: str
    frequency: str