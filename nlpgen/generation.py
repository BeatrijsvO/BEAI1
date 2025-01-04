from transformers import pipeline

# Initialiseer de NLP-pipeline
nlp_pipeline = pipeline("text-generation", model="distilgpt2")

def generate_answer(question: str, context: str):
    """
    Genereer een antwoord op basis van een vraag en context.
    """
    # Combineer context en vraag in één prompt
    prompt = (
        f"Gebruik de volgende context om de vraag te beantwoorden:\n"
        f"{context}\n\n"
        f"Vraag: {question}\n"
        f"Antwoord:"
    )

    # Genereer antwoord zonder `truncation` in de generate-aanroep
    result = nlp_pipeline(prompt, max_length=150, num_return_sequences=1)
    return result[0]["generated_text"]