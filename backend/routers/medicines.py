from fastapi import APIRouter, HTTPException
from backend.services.nlp_parser import parse_medicine_text
from backend.database import get_connection

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.post("/nlp")
def add_medicine_nl(text: str, user_id: int):
    try:
        data = parse_medicine_text(text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO medicines (user_id, name, dosage, time, frequency) VALUES (?, ?, ?, ?, ?)",
        (user_id, data["name"], data["dosage"], data["time"], data["frequency"])
    )
    conn.commit()
    conn.close()
    return data
