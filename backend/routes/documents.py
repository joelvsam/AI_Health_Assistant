from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

router = APIRouter(prefix="/documents", tags=["Documents"])

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

    return {
        "filename": file.filename,
        "text": extracted_text.strip()[:2000]
    }
