# backend/ai/chains.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

def get_rag_chain(retriever):
    """
    Creates a Retrieval-Augmented Generation (RAG) chain for answering questions
    based on a given context.

    Args:
        retriever: A retriever object that provides the context for the RAG chain.

    Returns:
        A RAG chain that can be used to answer questions.
    """
    # Import llm here to avoid circular imports
    from backend.ai.llm import llm

    # Define the prompt template for the RAG chain
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

    # Create the RAG chain by combining the retriever, prompt, and language model
    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    return chain