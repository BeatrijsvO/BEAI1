from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Laad het .env-bestand
load_dotenv()

# Haal DATABASE_URL op
DATABASE_URL = os.getenv("DATABASE_URL")

# Definieer de FastAPI-app
app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.get("/test-db")
def test_db():
    # Controleer of DATABASE_URL correct is geladen
    if not DATABASE_URL:
        return {"error": "DATABASE_URL niet gevonden"}
    return {"database_url": DATABASE_URL}


# Definieer Document Retrieval
from document_retrieval import fetch_documents_from_source

@app.get("/fetch-documents")
def fetch_documents():
    connection_details = {"directory": "/path/to/documents"}
    documents = fetch_documents_from_source("local", connection_details)
    return {"documents": documents}