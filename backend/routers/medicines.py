from fastapi import APIRouter, HTTPException, Depends
from backend.services.nlp_parser import parse_medicine_text
from backend.database import get_connection
from backend.routers.auth import get_current_user
from backend.models.user import UserOut
from backend.models.medicine import Medicine

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.post("/nlp")
def add_medicine_nl(text: str, current_user: UserOut = Depends(get_current_user)):
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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, dosage, time as timing FROM medicines WHERE user_id = ?", (current_user.id,))
    medicines = cur.fetchall()
    conn.close()
    return [dict(row) for row in medicines]

@router.post("/")
def add_medicine(medicine: Medicine, current_user: UserOut = Depends(get_current_user)):
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
