from transformers import pipeline

def get_text_generation_pipeline(model_name="distilgpt2"):
    return pipeline("text-generation", model=model_name)