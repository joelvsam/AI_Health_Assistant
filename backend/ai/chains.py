# backend/ai/chains.py
"""
This module defines the Chains for the AI Health Assistant.
A chain is a sequence of calls to components, which can include other chains.
In this case, we are using a Retrieval-Augmented Generation (RAG) chain.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

def get_rag_chain(retriever):
    """
    Creates a Retrieval-Augmented Generation (RAG) chain for answering questions
    based on a given context.

    The RAG chain is composed of three main components:
    1. Retriever: This component retrieves relevant information from a given source (e.g., a vector store).
    2. Prompt: This component formats the retrieved information into a prompt for the language model.
    3. Language Model: This component generates an answer to the question based on the prompt.

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