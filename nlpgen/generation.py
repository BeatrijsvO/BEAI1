from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Initialiseer het model en de tokenizer
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def generate_answer(question: str, context: str) -> str:
    """
    Genereer een antwoord op basis van een vraag en context.
    """
    # Combineer de vraag en context in een prompt
    prompt = (
        f"Gebruik de volgende context om de vraag te beantwoorden:\n\n"
        f"Context: {context}\n\n"
        f"Vraag: {question}\n"
        f"Antwoord:"
    )

    # Tokeniseer de prompt
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Genereer tekst
    outputs = model.generate(inputs.input_ids, max_length=150, temperature=0.7, top_k=50)

    # Decodeer de gegenereerde tekst
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Splits de output om het antwoord te isoleren
    answer = generated_text.split("Antwoord:")[-1].strip()

    return answer
