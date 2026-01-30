from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
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

def run_rag_chain(text: str):
    """
    Run the RAG chain in the background.
    """
    retriever = create_vector_store(text)
    rag_chain = get_rag_chain(retriever)
    rag_chain.invoke("Explain this document in simple terms")

@router.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
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
    
    # Run the RAG chain in the background
    background_tasks.add_task(run_rag_chain, extracted_text)

    return {
        "filename": file.filename,
        "text": extracted_text.strip()[:2000],  # limit for display
        "explanation": "Your document is being processed. You will be notified when it is ready.",
        "indexed_for_rag": True
    }