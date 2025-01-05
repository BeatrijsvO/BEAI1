from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Vervang BLOOMZ door Flan-T5
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def generate_answer(question: str, context: str) -> str:
    prompt = f"Context: {context}\n\nVraag: {question}\nAntwoord:"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=200, temperature=0.7, top_k=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)




    # Haal het antwoord na "Antwoord:" uit de tekst
    answer = generated_text.split("Antwoord:")[-1].strip()

    return answer