# backend/routes/documents.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.database import get_connection
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

# Set Tesseract path if using Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

router = APIRouter(prefix="/documents", tags=["Documents"])

# POST - Upload document (PDF or image) and save extracted text
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    extracted_text = ""

    # PDF handling
    if file.content_type == "application/pdf":
        try:
            pdf = fitz.open(stream=contents, filetype="pdf")
            for page in pdf:
                extracted_text += page.get_text()
            pdf.close()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid PDF file")

    # Image OCR handling
    elif file.content_type.startswith("image/"):
        try:
            image = Image.open(io.BytesIO(contents))
            extracted_text = pytesseract.image_to_string(image)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")

    else:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Upload PDF or image only."
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in document"
        )

    # Save to database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS documents ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "filename TEXT NOT NULL, "
        "text TEXT NOT NULL, "
        "uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    cursor.execute(
        "INSERT INTO documents (filename, text) VALUES (?, ?)",
        (file.filename, extracted_text.strip())
    )
    conn.commit()
    doc_id = cursor.lastrowid
    conn.close()

    return {
        "id": doc_id,
        "filename": file.filename,
        "text": extracted_text.strip()[:2000]
    }

# GET - Retrieve document by ID
@router.get("/{doc_id}")
def get_document(doc_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, text, uploaded_at FROM documents WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()
    conn.close()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return dict(doc)
