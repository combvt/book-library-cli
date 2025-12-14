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


def test_search_for_no_results():
    client = GoogleBooksClient(API_KEY)

    assert client.search_books("dsaijdnaskj435kjnds") == []