from langchain_huggingface import HuggingFaceEndpoint
from backend.core.config import HUGGINGFACEHUB_API_TOKEN


llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    temperature=0.5,
    model_kwargs={
        "max_length": 256
    }
)
