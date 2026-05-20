import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
VALID_KEY = "dev-api-key-change-in-production"
HEADERS = {"X-API-Key": VALID_KEY}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Document Gateway" in response.json()["service"]

def test_doc_available():
    response = client.get("/docs")
    response.status_code = 200