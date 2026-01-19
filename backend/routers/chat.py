from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.ai.chains import get_rag_chain
from backend.services.vector_store import get_vector_store

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str

@router.post("/")
async def chat(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    store = get_vector_store()
    retriever = store.as_retriever()
    rag_chain = get_rag_chain(retriever)
    
    answer = rag_chain.invoke(request.query)
    
    return {"answer": answer}
