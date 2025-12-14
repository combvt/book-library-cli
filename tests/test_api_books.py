from fastapi.testclient import TestClient
import sqlite3
from src.api_app import app
from src.api_app import google_client
from src.models import Book
import src.db
import src.storage.sql_storage

client = TestClient(app)

class FakeGoogleClient:
    def get_book_by_id(self, book_id: str):
        return Book(
            "test123",
            book_id,
            "Merlin",
            67,
            "hellothisisthest",
            "entertainment",
            "2018-7-19",
            "dsajgfdlk324"
        )


def test_create_and_get_book(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test.db"

    def fake_get_connection():
        return sqlite3.connect(test_db_path)
    
    monkeypatch.setattr(src.db, "get_connection", fake_get_connection)
    monkeypatch.setattr(src.storage.sql_storage, "get_connection", fake_get_connection)
    src.db.init_db()
    
    def override_dependency():
        return FakeGoogleClient()
    
    app.dependency_overrides[google_client] = override_dependency
    
    try:
        response = client.post("/books/from-google/Google2345") 
        assert response.status_code == 201
        data = response.json()
        assert data["book_id"] == "Google2345"
        assert "sql_index" in data

        sql_index = data["sql_index"]
        response = client.get(f"/books/{sql_index}")

        assert response.status_code == 200
        data = response.json()
        assert data["book_id"] == "Google2345"
        assert data["sql_index"] == sql_index
    finally:
        app.dependency_overrides.clear()

def test_get_invalid_index():
    response = client.get("/books/not-an-int")

    assert response.status_code == 422

    
