from fastapi import APIRouter, UploadFile, File
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF or image file and extract its text content.
    """
    contents = await file.read()
    text = ""

    # PDF processing
    if file.content_type == "application/pdf":
        pdf_doc = fitz.open(stream=contents, filetype="pdf")
        for page in pdf_doc:
            text += page.get_text()
        pdf_doc.close()

    # Image processing (OCR)
    elif file.content_type.startswith("image/"):
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)

    else:
        return {"error": "Unsupported file type. Upload PDF or image."}

    return {"filename": file.filename, "text": text[:1000]}  #
