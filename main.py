# from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.docstore.document import Document
from transformers import pipeline

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from vectorstore.store import SimpleVectorStore
from nlpgen.generation import generate_answer

# Laad het .env-bestand
load_dotenv()

# Haal DATABASE_URL op
DATABASE_URL = os.getenv("DATABASE_URL")

# Definieer de FastAPI-app
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# 2. Definieer een Wrapper voor SentenceTransformer
class SentenceTransformerWrapper(Embeddings):
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        """Genereer embeddings voor een lijst met teksten."""
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, query):
        """Genereer een embedding voor een enkele vraag."""
        return self.model.encode([query], show_progress_bar=False)[0]

# Initialiseer het embeddingsmodel via de wrapper
embeddings_model = SentenceTransformerWrapper()

# 3. Initialiseer Flan-T5 model pipeline
#nlp_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")
# Gebruik BLOOMZ als krachtiger model
nlp_pipeline = pipeline("text-generation", model="bigscience/bloomz-1b7")


# 4. Nieuw voor CKBA en website
@app.post("/upload")
async def upload_documents(files: list[UploadFile]):
    """
    Upload en verwerk documenten.
    """
    documents = []
    for file in files:
        # Lees en decodeer de inhoud van elk bestand
        content = (await file.read()).decode('utf-8')  # Pas encoding aan als nodig
        texts = content.split('\n')
        file_documents = [Document(page_content=text.strip(), metadata={"source": file.filename}) for text in texts if text.strip()]
        documents.extend(file_documents)

    # Log het aantal geüploade documenten
    print(f"Aantal documenten: {len(documents)}")

    # Hier kun je documenten opslaan in een vectorstore of database
    return {"message": f"{len(documents)} documenten succesvol geüpload en verwerkt."}

# 5. Maak de FAISS-vectorstore
document_texts = [doc.page_content for doc in documents]
vectorstore = FAISS.from_texts(document_texts, embeddings_model)

# 6. Functie voor ophalen van relevante documenten
def retrieve_documents(vraag, k=3):
    """Haal de top k relevante documenten op uit de vectorstore."""
    # Controleer of vectorstore is aangemaakt
    if 'vectorstore' not in globals():
        raise NameError("Vectorstore is niet gedefinieerd. Zorg ervoor dat je FAISS-vectorstore hebt aangemaakt.")

    # Zoek naar relevante documenten
    results = vectorstore.similarity_search(vraag, k=k)
    return [doc.page_content for doc in results]

# 7. Functie voor antwoord genereren met BLOOMZ
def generate_answer(vraag, context):

    prompt = (
        f"Gebruik de onderstaande informatie om de vraag te beantwoorden:\n"
        f"{context}\n\n"
        f"Vraag: {vraag}\n"
        f"Antwoord (geef alleen het relevante deel van de context):"
    )


    #prompt = f"Gebruik de onderstaande informatie om de vraag te beantwoorden:{context}\n\nVraag: {vraag}\nAntwoord (geef alleen het relevante deel van de context):"

    #prompt = f"Context: {context}\n\nVraag: {vraag}\nAntwoord:"

    print(f"DEBUG Prompt:\n{prompt}")  # Debugging
    result = nlp_pipeline(prompt, max_length=200, truncation=True, num_return_sequences=1)
    print(f"DEBUG Result:\n{result}")  # Debugging
    print(f"DEBUG Result[0] Generated tekst:\n{result[0]['generated_text']}")  # Debugging
    return result[0]['generated_text']

# 8. Hoofdfunctie: Vraag en antwoord

def kba_antwoord(vraag):
    relevante_documenten = retrieve_documents(vraag)
    context = "\n".join(relevante_documenten)

    antwoord = generate_answer(vraag, context)

    print(f"DEBUG Gevonden documenten:\n{relevante_documenten}")
    print(f"DEBUG antwoord in kba_antwoord:\n{antwoord}")

    return antwoord

# Testvraag
#vraag = "Wat moet ik doen met bedrijfsapparatuur?"
vraag = "Hoe laat is het lunchpauze?"
antwoord = kba_antwoord(vraag)
print(f"EINDE DEBUG antwoord:\n{antwoord}")

#print(f"Vraag : {vraag}")
























@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.get("/test-db")
def test_db():
    # Controleer of DATABASE_URL correct is geladen
    if not DATABASE_URL:
        return {"error": "DATABASE_URL niet gevonden"}
    return {"database_url": DATABASE_URL}

TESTJE = True
@app.get("/shortcut1")
def shortcut_1():
    # Controleer of dit TESTje werkt
    if not TESTJE:
        return {"error": "TESTJE niet gevonden"}
    return {"shortcut1": TESTJE}


# Dummy dataset
texts = [
    "FastAPI is een modern webframework voor Python.",
    "Retrieval-Augmented Generation combineert zoekfunctionaliteit met tekstgeneratie.",
    "Vectorstores zoals FAISS worden vaak gebruikt om semantische zoekopdrachten te versnellen.",
    "Het ontwikkelen van een CKBA-product vereist een combinatie van backend, frontend en machine learning."
]

# Initialiseer vectorstore en voeg teksten toe
vectorstore = SimpleVectorStore()
vectorstore.add_texts(texts)

# Requestmodel
class QuestionRequest(BaseModel):
    question: str

@app.post("/answer")
async def answer_question(request: QuestionRequest):
    """
    Beantwoord een vraag op basis van de opgeslagen teksten.
    """
    try:
        # Zoek relevante context
        relevant_context = vectorstore.search(request.question, top_k=3)
        context = "\n".join(relevant_context[:3])  # Beperk de context tot 3 resultaten
        # Genereer antwoord
        answer = generate_answer(request.question, context)
        return {"question": request.question, "context": relevant_context, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fout bij beantwoording: {str(e)}")

