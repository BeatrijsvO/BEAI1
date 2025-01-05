# from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vectorstore.store import SimpleVectorStore
from nlpgen.generation import generate_answer

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



@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload een document en voeg de inhoud toe aan de vectorstore.
    """
    try:
        # Sla het bestand tijdelijk op
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.file.read())
            temp_path = temp_file.name

        # Lees en verwerk het document (hier zou je een parser toevoegen)
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Voeg inhoud toe aan vectorstore
        vectorstore.add_texts([content])

        return {"filename": file.filename, "message": "Document succesvol geupload."}
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

