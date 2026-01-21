from pathlib import Path
import faiss

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from backend.core.config import FAISS_PATH

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_store(text: str) -> FAISS:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    docs = text_splitter.split_text(text)

    if not docs:
        raise ValueError("No text provided to create vector store")

    db = FAISS.from_texts(docs, embeddings)
    db.save_local(str(FAISS_PATH))
    return db


def get_vector_store() -> FAISS:
    if Path(FAISS_PATH).exists():
        return FAISS.load_local(
            str(FAISS_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )

    # ✅ Create EMPTY but valid FAISS store
    dim = len(embeddings.embed_query("init"))
    index = faiss.IndexFlatL2(dim)

    return FAISS(
        embedding_function=embeddings,
        index=index,
        docstore={},
        index_to_docstore_id={}
    )


def save_store(store: FAISS):
    store.save_local(str(FAISS_PATH))
