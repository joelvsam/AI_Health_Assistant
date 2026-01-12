from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.core.config import FAISS_PATH

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vector_store():
    if FAISS_PATH.exists():
        return FAISS.load_local(str(FAISS_PATH), embeddings)
    return FAISS.from_texts([], embeddings)

def save_store(store):
    store.save_local(str(FAISS_PATH))
