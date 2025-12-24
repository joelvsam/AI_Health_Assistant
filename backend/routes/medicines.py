from fastapi import APIRouter
from backend.models import Medicine
from backend.database import get_connection

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.post("/")
def add_medicine(medicine: Medicine):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO medicines (name, dosage, time, frequency) VALUES (?, ?, ?, ?)",
        (medicine.name, medicine.dosage, medicine.time, medicine.frequency)
    )

    conn.commit()
    conn.close()

    return {"message": "Medicine saved"}

@router.get("/")
def list_medicines():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, dosage, time, frequency FROM medicines")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
