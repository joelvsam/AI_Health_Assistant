# backend/ai/llm.py
"""
This module initializes the language model (LLM) for the AI Health Assistant.
The LLM is a HuggingFace model that is used to generate text.
"""

from langchain_huggingface import HuggingFaceEndpoint
from backend.core.config import HUGGINGFACEHUB_API_TOKEN

# Create a HuggingFaceEndpoint instance to interact with the language model.
# The HuggingFaceEndpoint class allows us to use a model from the Hugging Face Hub as a language model.
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    task="text2text-generation",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    temperature=0.5,
    max_new_tokens=256,
)