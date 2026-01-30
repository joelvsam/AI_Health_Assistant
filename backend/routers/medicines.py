from fastapi import APIRouter, HTTPException, Depends
from backend.services.nlp_parser import parse_medicine_text
from backend.database import get_connection
from backend.routers.auth import get_current_user
from backend.models.user import UserOut
from backend.models.medicine import Medicine

# Create a new router for medicine endpoints
router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.post("/nlp")
def add_medicine_nl(text: str, current_user: UserOut = Depends(get_current_user)):
    """
    Add a new medicine using natural language processing.
    """
    try:
        data = parse_medicine_text(text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO medicines (user_id, name, dosage, time, frequency) VALUES (?, ?, ?, ?, ?)",
        (current_user.id, data["name"], data["dosage"], data["time"], data["frequency"])
    )
    conn.commit()
    conn.close()
    return data

@router.get("/")
def get_medicines(current_user: UserOut = Depends(get_current_user)):
    """
    Get all medicines for the current user.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, dosage, time, frequency FROM medicines WHERE user_id = ?", (current_user.id,))
    medicines = cur.fetchall()
    conn.close()
    # a little bug fix here from time to timing
    return [{"id": row[0], "name": row[1], "dosage": row[2], "time": row[3], "frequency": row[4]} for row in medicines]

@router.post("/")
def add_medicine(medicine: Medicine, current_user: UserOut = Depends(get_current_user)):
    """
    Add a new medicine.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO medicines (user_id, name, dosage, time, frequency) VALUES (?, ?, ?, ?, ?)",
        (current_user.id, medicine.name, medicine.dosage, medicine.time, medicine.frequency)
    )
    conn.commit()
    new_medicine_id = cur.lastrowid
    conn.close()
    return {"id": new_medicine_id, **medicine.dict()}

@router.put("/{medicine_id}")
def update_medicine(medicine_id: int, medicine: Medicine, current_user: UserOut = Depends(get_current_user)):
    """
    Update a medicine.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE medicines SET name = ?, dosage = ?, time = ?, frequency = ? WHERE id = ? AND user_id = ?",
        (medicine.name, medicine.dosage, medicine.time, medicine.frequency, medicine_id, current_user.id)
    )
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Medicine not found or not owned by user")
    conn.close()
    return {"id": medicine_id, **medicine.dict()}

@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: int, current_user: UserOut = Depends(get_current_user)):
    """
    Delete a medicine.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM medicines WHERE id = ? AND user_id = ?", (medicine_id, current_user.id))
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Medicine not found or not owned by user")
    conn.close()
    return {"detail": "Medicine deleted successfully"}