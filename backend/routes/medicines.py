from fastapi import APIRouter
from backend.models import Medicine

router = APIRouter(prefix="/medicines", tags=["Medicines"])

medicines_db = []

@router.post("/")
def add_medicine(medicine: Medicine):
    medicines_db.append(medicine)
    return {"message": "Medicine added", "data": medicine}

@router.get("/")
def list_medicines():
    return medicines_db
