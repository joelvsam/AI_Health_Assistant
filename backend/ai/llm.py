# backend/ai/llm.py
"""
This module initializes the language model (LLM) for the AI Health Assistant.
The LLM is a HuggingFace model that is used to generate text.
"""

from functools import lru_cache
from langchain_huggingface import HuggingFaceEndpoint
from backend.core.config import HUGGINGFACEHUB_API_TOKEN

@lru_cache
def get_llm():
    """
    Lazily create the HuggingFaceEndpoint model.
    This avoids failing imports in CI when tokens are not available.
    """
    if not HUGGINGFACEHUB_API_TOKEN:
        raise RuntimeError("HUGGINGFACEHUB_API_TOKEN is not set")

    return HuggingFaceEndpoint(
        repo_id="google/flan-t5-large",
        task="text2text-generation",
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        temperature=0.5,
        max_new_tokens=256,
    )
