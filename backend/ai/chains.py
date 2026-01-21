from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
def get_rag_chain(retriever):
    # Import llm here to avoid circular imports
    from backend.ai.llm import llm

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful medical assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{question}

Answer:"""
    )

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    return chain
