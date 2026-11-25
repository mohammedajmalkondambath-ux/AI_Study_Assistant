
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Check whether the API health endpoint works."""

    response = client.get("/health")

    assert response.status_code == 200

def test_general_chat_endpoint():
    """Check whether the general chat API works."""

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What is Python?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "general_question"
    assert data["answer"]

def test_list_documents_endpoint():
    """Check whether the document listing API works."""

    response = client.get("/api/v1/documents")

    assert response.status_code == 200

    data = response.json()

    assert "total_documents" in data
    assert "documents" in data
    assert isinstance(data["documents"], list)
