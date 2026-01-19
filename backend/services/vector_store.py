from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.core.config import FAISS_PATH

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_text(text)
    
    db = FAISS.from_texts(docs, embeddings)
    
    return db.as_retriever()

def get_vector_store():
    if FAISS_PATH.exists():
        return FAISS.load_local(str(FAISS_PATH), embeddings, allow_dangerous_deserialization=True)
    return FAISS.from_texts([], embeddings)

def save_store(store):
    store.save_local(str(FAISS_PATH))
