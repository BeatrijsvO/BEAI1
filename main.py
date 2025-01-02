from fastapi import FastAPI
from dotenv import load_dotenv
import os
import logging

# Laad omgevingsvariabelen uit .env-bestand
load_dotenv()

# Maak een nieuwe FastAPI-applicatie
app = FastAPI()

# Haal de DATABASE_URL op uit omgevingsvariabelen
DATABASE_URL = os.getenv("DATABASE_URL")

# Logging instellen voor debugging
logging.basicConfig(level=logging.INFO)

@app.get("/")
def read_root():
    logging.info("Root endpoint accessed.")
    return {"message": "Hello from CKBA with Hypercorn!"}

@app.get("/test-db")
def test_db():
    if not DATABASE_URL:
        logging.error("DATABASE_URL is not set.")
        return {"error": "DATABASE_URL is not set in the environment variables."}
    try:
        # Simuleer een test met de databaseverbinding
        logging.info(f"