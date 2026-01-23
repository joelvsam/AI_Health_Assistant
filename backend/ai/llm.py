from langchain_huggingface import HuggingFaceEndpoint
from backend.core.config import HUGGINGFACEHUB_API_TOKEN

llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    task="text2text-generation",  
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    temperature=0.5,
    max_new_tokens=256,
)
