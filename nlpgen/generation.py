from transformers import pipeline

# Initialiseer de NLP-pipeline
nlp_pipeline = pipeline("text-generation", model="distilgpt2")

def generate_answer(question, context):
    """
    Genereer een antwoord op basis van een vraag en context.
    """
    prompt = (
        f"Gebruik de volgende context om de vraag te beantwoorden:\n"
        f"{context}\n\n"
        f"Vraag: {question}\n"
        f"Antwoord:"
    )
    result = nlp_pipeline(prompt, max_length=150, truncation=True, num_return_sequences=1)
    return result[0]["generated_text"]