# backend/models.py
"""
This module defines the Pydantic models used for data validation and
serialization in the API. These models are used in the API endpoints to
validate the incoming request body and to serialize the response body.
"""

from pydantic import BaseModel

class Medicine(BaseModel):
    """
    Pydantic model for creating a new medicine.
    This model is used in the request body for the create_medicine endpoint.
    """
    name: str
    dosage: str
    time: str  # HH:MM format
    frequency: str

class MedicineUpdate(BaseModel):
    """
    Pydantic model for updating an existing medicine.
    All fields are optional, so that the user can update only the fields they want.
    """
    name: str | None = None
    dosage: str | None = None
    time: str | None = None
    frequency: str | None = None

class MedicineNLInput(BaseModel):
    """
    Pydantic model for processing natural language input for medicine.
    This model is used in the request body for the ai_medicine_parser endpoint.
    """
    text: str