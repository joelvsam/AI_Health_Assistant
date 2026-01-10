from fastapi import APIRouter, HTTPException
from backend.models import Medicine, MedicineUpdate
from backend.database import get_connection
import re

router = APIRouter(prefix="/medicines", tags=["Medicines"])

# Example list of common medicines (expandable)
COMMON_MEDICINES = [
    "Paracetamol", "Ibuprofen", "Aspirin", "Amoxicillin", "Cetirizine",
    "Metformin", "Atorvastatin"
]

def parse_medicine_text(text: str):
    text_lower = text.lower()

    # Extract dosage (e.g., 500mg)
    dosage_match = re.search(r"(\d+\s?(mg|g|ml|iu))", text_lower)
    dosage = dosage_match.group(0) if dosage_match else None

    # Extract time (e.g., 14:30)
    time_match = re.search(r"(\d{1,2}:\d{2})", text_lower)
    time = time_match.group(0) if time_match else None

    # Extract frequency
    frequency_mapping = {
        "every day": "daily",
        "daily": "daily",
        "every 2 days": "every 2 days",
        "twice a day": "2x daily",
        "once a day": "daily",
        "weekly": "weekly"
    }
    frequency = None
    for key in frequency_mapping:
        if key in text_lower:
            frequency = frequency_mapping[key]
            break

    # Extract medicine name by checking against common medicines
    name = None
    for med in COMMON_MEDICINES:
        if med.lower() in text_lower:
            name = med
            break

    # If any required field is missing, raise error
    missing = [k for k, v in zip(["name", "dosage", "time", "frequency"], [name, dosage, time, frequency]) if not v]
    if missing:
        raise ValueError(f"Failed to parse input: missing {', '.join(missing)}")

    return {"name": name, "dosage": dosage, "time": time, "frequency": frequency}


# POST - Add a new medicine (structured input)
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
    return {"message": f"Medicine '{medicine.name}' saved"}


# POST - Add a new medicine using natural language
@router.post("/nl")
def add_medicine_nl(payload: dict):
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=422, detail="No text provided")

    try:
        parsed = parse_medicine_text(text)
        medicine = Medicine(**parsed)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicines (name, dosage, time, frequency) VALUES (?, ?, ?, ?)",
        (medicine.name, medicine.dosage, medicine.time, medicine.frequency)
    )
    conn.commit()
    conn.close()
    return {"message": f"Medicine '{medicine.name}' saved from natural language input"}


# GET - List all medicines
@router.get("/")
def list_medicines():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, dosage, time, frequency FROM medicines")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# DELETE - Delete medicine by id
@router.delete("/id/{medicine_id}")
def delete_medicine(medicine_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE id = ?", (medicine_id,))
    medicine = cursor.fetchone()
    if not medicine:
        conn.close()
        raise HTTPException(status_code=404, detail="Medicine not found")

    cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
    conn.commit()
    conn.close()
    return {"message": f"Medicine '{medicine['name']}' deleted successfully"}


# PATCH - Update medicine by id
@router.patch("/id/{medicine_id}")
def update_medicine(medicine_id: int, update: MedicineUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE id = ?", (medicine_id,))
    medicine = cursor.fetchone()
    if not medicine:
        conn.close()
        raise HTTPException(status_code=404, detail="Medicine not found")

    # Update only fields that are provided
    new_name = update.name if update.name else medicine["name"]
    new_dosage = update.dosage if update.dosage else medicine["dosage"]
    new_time = update.time if update.time else medicine["time"]
    new_frequency = update.frequency if update.frequency else medicine["frequency"]

    cursor.execute(
        "UPDATE medicines SET name = ?, dosage = ?, time = ?, frequency = ? WHERE id = ?",
        (new_name, new_dosage, new_time, new_frequency, medicine_id)
    )
    conn.commit()
    conn.close()
    return {"message": f"Medicine '{new_name}' updated successfully"}
