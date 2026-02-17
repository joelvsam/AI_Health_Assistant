from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.ai.llm import llm

# Create a new router for AI endpoints
router = APIRouter(prefix="/ai", tags=["AI"])

# Define the request model for the explain endpoint
class ExplainRequest(BaseModel):
    text: str

@router.post("/explain")
async def explain_document(req: ExplainRequest):
    """
    Explain a document in simple terms.
    """
    # Validate the input
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="No text provided")

    try:
        prompt = (
            "You are a helpful medical assistant. "
            "Explain the following text in simple, non-diagnostic terms. "
            "If the text is unclear or incomplete, say so.\n\n"
            f"Text:\n{req.text}\n\nExplanation:"
        )
        result = llm.invoke(prompt)
        explanation = getattr(result, "content", result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"explanation": explanation}
