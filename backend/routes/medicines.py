from fastapi import APIRouter, HTTPException
from backend.models import Medicine, MedicineUpdate
from backend.database import get_connection

router = APIRouter(prefix="/medicines", tags=["Medicines"])

# POST - Add a new medicine
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
