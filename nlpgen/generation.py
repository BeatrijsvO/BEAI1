from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialiseer de tokenizer en het model
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloomz-7b1")
model = AutoModelForCausalLM.from_pretrained("bigscience/bloomz-7b1")

def generate_answer(question: str, context: str) -> str:
    """
    Genereer een antwoord op basis van een vraag en context met BLOOMZ.
    """
    # Combineer context en vraag in een prompt
    prompt = (
        f"Gebruik de volgende context om de vraag te beantwoorden:\n\n"
        f"Context: {context}\n\n"
        f"Vraag: {question}\n"
        f"Antwoord:"
    )

    # Tokeniseer de prompt
    inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)

    # Genereer antwoord met het model
    outputs = model.generate(
        inputs.input_ids,
        max_length=200,  # Maximale lengte van het antwoord
        temperature=0.7,  # Controleert de creativiteit van het model
        top_k=50,  # Beperk tot de top 50 tokens
        eos_token_id=tokenizer.eos_token_id,
    )

    # Decodeer de output naar tekst
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Haal het antwoord na "Antwoord:" uit de tekst
    answer = generated_text.split("Antwoord:")[-1].strip()

    return answer