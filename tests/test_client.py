import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.google_api_client import GoogleBooksClient
from src.config import API_KEY


def test_search_for_no_results():
    client = GoogleBooksClient(API_KEY)

    assert client.search_books("dsaijdnaskj435kjnds") == []