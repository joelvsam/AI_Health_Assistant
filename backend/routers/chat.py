# backend/routers/chat.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from backend.services.vector_store import get_vector_store
from backend.ai.llm import llm
from langchain.prompts import ChatPromptTemplate
from backend.core.security import get_current_user_id  # Assuming you have this

router = APIRouter()

retriever = get_vector_store()

# Store session-based memories
chat_histories = {}

def get_session_history(session_id: str):
    if session_id not in chat_histories:
        chat_histories[session_id] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
    return chat_histories[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI health assistant."),
    ("human", "{input}")
])

runnable = prompt | llm

runnable_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

@router.post("/chat/")
async def chat(request: Request, user_id: int = Depends(get_current_user_id)):
    try:
        data = await request.json()
        user_input = data.get("query")
        session_id = f"user_{user_id}"

        if not user_input:
            raise HTTPException(status_code=400, detail="No query provided")

        config = {"configurable": {"session_id": session_id}}

        # Use retrieval QA if documents are available
        if retriever and getattr(retriever, "index", None) and retriever.index.ntotal > 0:
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=False
            )
            # Must use invoke for RetrievalQA, not ainvoke with history
            result = await qa_chain.ainvoke({"query": user_input})
            answer = result.get("result", "No answer found.")

            # Manually save history for non-runnable chains
            history = get_session_history(session_id)
            history.chat_memory.add_user_message(user_input)
            history.chat_memory.add_ai_message(answer)
            
            return {"answer": answer}

        # Use the runnable with history
        result = await runnable_with_history.ainvoke({"input": user_input}, config=config)
        
        return {"answer": result.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

