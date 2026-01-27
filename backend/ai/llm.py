# backend/ai/llm.py

from langchain_huggingface import HuggingFaceEndpoint
from backend.core.config import HUGGINGFACEHUB_API_TOKEN

# Create a HuggingFaceEndpoint instance to interact with the language model
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",  # The ID of the model repository on Hugging Face
    task="text2text-generation",  # The task the model is intended for
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,  # The API token for Hugging Face Hub
    temperature=0.5,  # The temperature for text generation (controls randomness)
    max_new_tokens=256,  # The maximum number of new tokens to generate
)