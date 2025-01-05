from nlpgen.generation import generate_answer  # Importeer de aangepaste BLOOMZ-functie
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vectorstore.store import SimpleVectorStore

from fastapi import File, UploadFile
import tempfile

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

# Initialiseer de vectorstore
vectorstore = SimpleVectorStore()

# Probeer de opgeslagen vectorstore te laden
try:
    vectorstore.load_store("vectorstore.index")
    print("Vectorstore succesvol geladen van disk.")
except FileNotFoundError:
    print("Geen opgeslagen vectorstore gevonden. Nieuwe store wordt aangemaakt.")

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.get("/test-db")
def test_db():
    # Controleer of DATABASE_URL correct is geladen
    if not DATABASE_URL:
        return {"error": "DATABASE_URL niet gevonden"}
    return {"database_url": DATABASE_URL}

# Requestmodel
class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = (await file.read()).decode('utf-8')  # Verwerk tekst
        vectorstore.add_texts([content])  # Voeg toe aan de vectorstore
        vectorstore.save_store("vectorstore.index")  # Sla de bijgewerkte vectorstore op
        return {"filename": file.filename, "message": "Document succesvol geupload en opgeslagen."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fout bij uploaden: {str(e)}")

@app.post("/answer")
async def answer_question(request: QuestionRequest):
    try:
        # Zoek relevante context in de vectorstore
        relevant_context = vectorstore.search(request.question, top_k=3)
        context = "\n".join(relevant_context)

        if not context.strip():
            return {"question": request.question, "answer": "Geen relevante informatie gevonden in de data."}

        # Genereer antwoord
        answer = generate_answer(request.question, context)

        return {"question": request.question, "context": relevant_context, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fout bij beantwoording: {str(e)}")