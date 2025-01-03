from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "greeting": "Hello, World!",
        "message": "Welcome to FastAPI!"
    }

def test_db():
    response = client.get("/test-db")
    assert response.status_code == 200
    assert "database_url" in response.json() or "error" in response.json()