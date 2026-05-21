import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
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

def test_unauthorized_with_bad_key():
    response = client.get("/api/v1/documents")
    response.status_code == 401

def test_unauthorized_with_bad_key():
    response = client.get("/api/v1/documents",headers={"X-API-Key": "wrong"})
    response.status_code == 403

@patch("app.routes.health.legacy_api.health_check", new_callable=AsyncMock)
def test_health_check(mock_health):
    mock_health.return_value = True
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["legacy_backend"] == "connected"

@patch("app.routes.documents.legacy_api.get_documents", new_callable=AsyncMock)
def test_list_documents(mock_get):
    mock_get.return_value = [
        {
            "id": 1,
            "title": "Test Document",
            "document_number": "TEST-001",
            "category_name": "Federal Register",
            "author_name": "GPO",
            "status": "draft",
            "page_count": 10,
            "submitted_date": "2026-05-13T10:00:00",
            "published_date": None,
        }
    ]
    response = client.get("/api/v1/documents/", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Document"


@patch("app.routes.documents.legacy_api.get_documents", new_callable=AsyncMock)
def test_filter_by_status(mock_get):
    mock_get.return_value = []
    response = client.get("/api/v1/documents/?status=published", headers=HEADERS)
    assert response.status_code == 200
    mock_get.assert_called_once_with(status="published", search=None, category=None, page=1)


@patch("app.routes.documents.legacy_api.get_document_stats", new_callable=AsyncMock)
def test_get_stats(mock_stats):
    mock_stats.return_value = {
        "total_documents": 10,
        "by_status": {"draft": 3, "published": 7},
        "categories": 5,
        "authors": 4,
    }
    response = client.get("/api/v1/documents/stats", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["total_documents"] == 10


@patch("app.routes.documents.legacy_api.create_document", new_callable=AsyncMock)
def test_create_document(mock_create):
    mock_create.return_value = {
        "id": 1,
        "title": "New Document",
        "document_number": "NEW-001",
        "category": {"id": 1, "name": "Federal Register", "code": "FR", "description": ""},
        "author": {"id": 1, "name": "GPO", "agency": "GPO", "email": "test@gpo.gov"},
        "status": "draft",
        "content_summary": "Test content",
        "page_count": 5,
        "submitted_date": "2026-05-13T10:00:00",
        "published_date": None,
        "updated_at": "2026-05-13T10:00:00",
        "status_history": [],
    }
    response = client.post("/api/v1/documents/", headers=HEADERS, json={
        "title": "New Document",
        "document_number": "NEW-001",
        "category_id": 1,
        "author_id": 1,
        "content_summary": "Test content",
        "page_count": 5,
    })
    assert response.status_code == 201


def test_invalid_transition_status():
    with patch("app.routes.documents.legacy_api.transition_document", new_callable=AsyncMock):
        response = client.post(
            "/api/v1/documents/1/transition",
            headers=HEADERS,
            json={"status": "invalid_status"}
        )
        assert response.status_code == 400