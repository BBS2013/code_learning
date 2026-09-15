"""End-to-end style tests for the Flask starter app."""
import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_index_page_renders(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"code_learning" in res.data


def test_notes_start_empty(client):
    res = client.get("/api/notes")
    assert res.status_code == 200
    assert res.get_json() == {"notes": []}


def test_create_and_list_note(client):
    res = client.post("/api/notes", json={"text": "learn flask"})
    assert res.status_code == 201
    note = res.get_json()["note"]
    assert note["id"] == 1
    assert note["text"] == "learn flask"
    assert "created_at" in note

    res = client.get("/api/notes")
    notes = res.get_json()["notes"]
    assert len(notes) == 1
    assert notes[0]["text"] == "learn flask"


def test_create_note_requires_text(client):
    res = client.post("/api/notes", json={"text": "   "})
    assert res.status_code == 400
    assert "error" in res.get_json()
