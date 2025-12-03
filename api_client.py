from models import Book
import requests

BOOK_URL = "https://www.googleapis.com/books/v1/volumes"
MAX_RESULTS = 10

class GoogleBooksClient:
    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key
        self.headers = {"key" : self.api_key}


    def search_books(self, book_title: str) -> list[Book]:
        book_params = {
            "q": book_title,
            "filter": "partial",
            "maxResults": MAX_RESULTS,
            "printType": "books",
            "projection": "full"
        }

        response = requests.get(url=BOOK_URL, headers=self.headers, params=book_params)
        response.raise_for_status()

        book_data = response.json()
        items = book_data.get("items", [])
        
        return [Book.from_api(item) for item in items]