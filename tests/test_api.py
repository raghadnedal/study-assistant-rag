from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_session():
    response = client.post("/sessions")

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data
    assert isinstance(data["session_id"], str)


def test_chat_document_not_found():
    session_response = client.post("/sessions")
    session_id = session_response.json()["session_id"]

    response = client.post(
        "/chat",
        json={
            "session_id": session_id,
            "document_id": 999999,
            "question": "Hello",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Document not found."
    }


def test_chat_session_not_found():
    response = client.post(
        "/chat",
        json={
            "session_id": "11111111-1111-1111-1111-111111111111",
            "document_id": 4,
            "question": "Hello",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Session not found."
    }


def test_chat_success():
    session_response = client.post("/sessions")
    session_id = session_response.json()["session_id"]

    fake_response = {
        "answer": "Test answer",
        "sources": [
            {
                "file_name": "test.pdf",
                "page_number": 1,
            }
        ],
    }

    with patch(
        "app.main.answer_question",
        return_value=fake_response,
    ):
        response = client.post(
            "/chat",
            json={
                "session_id": session_id,
                "document_id": 4,
                "question": "What is this document about?",
            },
        )

    assert response.status_code == 200
    assert response.json()["answer"] == "Test answer"
