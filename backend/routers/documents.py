from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
from backend.ai.chains import get_rag_chain
from backend.services.vector_store import create_vector_store

# Set Tesseract path if using Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Create a new router for document endpoints
router = APIRouter(prefix="/documents", tags=["Documents"])

def run_rag_chain(text: str) -> str:
    """
    Run the RAG chain and return an explanation.
    """
    store = create_vector_store(text)
    rag_chain = get_rag_chain(store.as_retriever())
    result = rag_chain.invoke("Explain this document in simple terms")
    return getattr(result, "content", result)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for processing.
    """
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
    
    try:
        explanation = run_rag_chain(extracted_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {exc}")

    return {
        "filename": file.filename,
        "text": extracted_text.strip()[:2000],  # limit for display
        "explanation": explanation,
        "indexed_for_rag": True
    }
