from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Create a new router for AI endpoints
router = APIRouter(prefix="/ai", tags=["AI"])

# Define the request model for the explain endpoint
class ExplainRequest(BaseModel):
    text: str

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="google/flan-t5-base")

@router.post("/explain")
async def explain_document(req: ExplainRequest):
    """
    Explain a document in simple terms.
    """
    # Validate the input
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="No text provided")

    try:
        # Summarize / explain in simple terms
        output = summarizer(req.text, max_length=200, min_length=50, do_sample=False)
        explanation = output[0]['summary_text']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"explanation": explanation}