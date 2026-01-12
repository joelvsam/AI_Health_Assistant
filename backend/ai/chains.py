from langchain.chains import RetrievalQA
from backend.ai.llm import llm
from backend.services.vector_store import get_vector_store

def explain_text(text: str):
    store = get_vector_store()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=store.as_retriever()
    )
    return qa.run(text)
