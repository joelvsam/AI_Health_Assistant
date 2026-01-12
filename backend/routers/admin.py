from fastapi import APIRouter
from backend.services.vector_store import get_vector_store, save_store

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/documents")
def upload_doc(text: str):
    store = get_vector_store()
    store.add_texts([text])
    save_store(store)
    return {"status": "indexed"}
