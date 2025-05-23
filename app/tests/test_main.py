import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


# ------------------- USER TESTS -------------------

def test_create_user():
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id():
    # Create user
    user_response = client.post("/users/", json={
        "username": "getuser",
        "email": "get@example.com",
        "password": "testpass"
    })
    user_id = user_response.json()["id"]

    # Fetch user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user():
    # Create user
    user_response = client.post("/users/", json={
        "username": "updateuser",
        "email": "update@example.com",
        "password": "testpass"
    })
    user_id = user_response.json()["id"]

    # Update
    update_response = client.put(f"/users/{user_id}", json={
        "username": "updateduser"
    })
    assert update_response.status_code == 200
    assert update_response.json()["username"] == "updateduser"


def test_delete_user():
    # Create user
    user_response = client.post("/users/", json={
        "username": "deleteuser",
        "email": "delete@example.com",
        "password": "testpass"
    })
    user_id = user_response.json()["id"]

    # Delete
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204


# ------------------- DOCUMENT TESTS -------------------

def test_upload_document():
    file_content = "Test document content"
    files = {"file": ("testdoc.txt", file_content, "text/plain")}
    response = client.post("/documents/", files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "testdoc.txt"


def test_read_documents():
    response = client.get("/documents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ------------------- INGESTION TESTS -------------------

def test_trigger_ingestion():
    # Upload document
    file_content = "Ingestion document"
    files = {"file": ("ingestdoc.txt", file_content, "text/plain")}
    doc_response = client.post("/documents/", files=files)
    doc_id = doc_response.json()["id"]

    # Trigger ingestion
    response = client.post(f"/ingestions/trigger/{doc_id}")
    assert response.status_code == 202
    assert response.json()["message"] == "Ingestion triggered"


def test_read_ingestions():
    response = client.get("/ingestions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
