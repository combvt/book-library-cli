from src.google_api_client import GoogleBooksClient
from src.models import Book
import pytest


def test_search_for_no_results(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"items": []}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("src.google_api_client.requests.get", mock_get)

    client = GoogleBooksClient(api_key="fake_key")
    items = client.search_books("dsakjdawdjkwabdwa")

    assert items == []


def test_search_one_book(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "items": [
                    {
                        "id": "testds21",
                        "volumeInfo": {
                            "title": "test123",
                            "pageCount": 25,
                        },
                    }
                ]
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("src.google_api_client.requests.get", mock_get)

    client = GoogleBooksClient(api_key="fake_key")
    items = client.search_books("harry")

    assert len(items) == 1
    assert isinstance(items[0], Book)
    assert items[0].title == "test123"
    assert items[0].page_count == 25
    assert items[0].book_id == "testds21"
