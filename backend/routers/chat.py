from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.ai.chains import chat_with_rag

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str

@router.post("/")
async def chat(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    answer = chat_with_rag(request.query)
    
    return {"answer": answer}
