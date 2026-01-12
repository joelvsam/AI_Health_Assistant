from langchain.llms import HuggingFacePipeline
from transformers import pipeline

hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=256
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)
