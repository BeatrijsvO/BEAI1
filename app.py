from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

# Haal DATABASE_URL op vanuit de omgeving
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    return {"message": "Hello from CKBA!"}

@app.get("/test-db")
def test_db():
    try:
        # Maak verbinding met de database
        connection = psycopg2.connect(DATABASE_URL)
        connection.close()
        return {"status": "Databaseverbinding succesvol!"}
    except Exception as e:
        return {"status": "Fout bij databaseverbinding", "error": str(e)}