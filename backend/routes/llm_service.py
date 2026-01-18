import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# InitializeAI client
# Ensure OPENAI_API_KEY is set in your .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    """
    Summarizes the provided text using an LLM.
    """
    if not text:
        return "No text provided for summarization."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes health-related video transcripts concisely."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in summarization: {e}")
        return "An error occurred while generating the summary."

def chat_with_ai(query: str) -> str:
    """
    Answers a user query using the LLM.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable AI Health Assistant. Answer health-related queries accurately but advise users to consult professionals for medical advice."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in chat: {e}")
        return "An error occurred while processing your query."