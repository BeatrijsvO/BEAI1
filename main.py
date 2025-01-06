from nlpgen.generation import generate_answer  # Importeer de  Flant5 ipv BLOOMZ-functie
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile
# from fastapi import File
from pydantic import BaseModel
from vectorstore.store import SimpleVectorStore

# import tempfile

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


# Initialiseer vectorstore
vectorstore = SimpleVectorStore()
try:
    os.makedirs("vectorstore", exist_ok=True)  # Zorg dat de map bestaat
    vectorstore.load_store("vectorstore/vectorstore.index")
    print("FAISS-index geladen.")
except FileNotFoundError:
    print("Geen opgeslagen FAISS-index gevonden. Nieuwe store wordt aangemaakt.")
    vectorstore = SimpleVectorStore()  # Maak een lege vectorstore aan


@app.post("/upload")
async def upload_document(file: UploadFile):
    try:
        content = (await file.read()).decode("utf-8")
        vectorstore.add_texts([content])  # Voeg de inhoud toe aan de vectorstore
        vectorstore.save_store("vectorstore/vectorstore.index")  # Sla de index op
        return {"message": "Document succesvol geupload en toegevoegd aan de vectorstore."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fout bij uploaden: {str(e)}")


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