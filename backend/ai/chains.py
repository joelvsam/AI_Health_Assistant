from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from backend.ai.llm import llm
from backend.services.vector_store import get_vector_store


def explain_text(text: str):
    store = get_vector_store()
    retriever = store.as_retriever()

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful medical assistant.
Use the following context to explain the text clearly and simply.

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

    return chain.invoke(text).content


def explain_document(text: str):
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful medical assistant.
Explain the following medical document in simple, easy-to-understand terms.
Avoid jargon and focus on what it means for the patient.

Document:
{document}

Explanation:"""
    )

    chain = prompt | llm
    return chain.invoke({"document": text}).content


def chat_with_rag(query: str):
    # Placeholder for real retrieval
    context = "No verified medical sources available."

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

    chain = prompt | llm
    return chain.invoke({
        "context": context,
        "question": query
    }).content
