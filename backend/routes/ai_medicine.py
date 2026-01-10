from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from backend.database import get_connection

router = APIRouter(prefix="/ai_medicine", tags=["AI Medicine"])

class MedicineNLRequest(BaseModel):
    text: str

# Free model to parse simple instructions
nlp_parser = pipeline("text2text-generation", model="google/flan-t5-base")

@router.post("/add")
def add_medicine_nl(req: MedicineNLRequest):
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="No input text provided")

    try:
        # The model will try to extract: name, dosage, time, frequency
        prompt = f"Extract medicine details in format 'name;dosage;time;frequency' from: {req.text}"
        output = nlp_parser(prompt, max_length=100)[0]['generated_text']

        # Split output into fields
        parts = output.split(";")
        if len(parts) != 4:
            raise ValueError(f"Could not parse all fields. Got: {output}")

        name, dosage, time_str, frequency = [p.strip() for p in parts]

        # Save to database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO medicines (name, dosage, time, frequency) VALUES (?, ?, ?, ?)",
            (name, dosage, time_str, frequency)
        )
        conn.commit()
        conn.close()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse input: {str(e)}")

    return {"message": f"Medicine '{name}' added successfully", "details": {"name": name, "dosage": dosage, "time": time_str, "frequency": frequency}}
