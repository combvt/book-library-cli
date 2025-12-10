from .storage_base import LibraryStorage
import json
from models import Book


class JsonLibraryStorage(LibraryStorage):
    def __init__(self, path: str):
        self.path = path

    def load_all(self) -> list[Book]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            if not isinstance(raw, list):
                raise ValueError("The library file must contain a list")

            return [Book.from_dict(item) for item in raw]

        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            return []

    def add(self, book: Book) -> None:
        book_list = self.load_all()

        book_list.append(book)
        self._save(book_list)

    def remove(self, index: int) -> Book | None:
        books_list = self.load_all()

        if index < 0 or index >= len(books_list):
            raise IndexError
            

        removed_book = books_list.pop(index)

        self._save(books_list)

        return removed_book

    def _save(self, book_list: list[Book]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                [book.to_dict() for book in book_list],
                f,
                indent=4,
                ensure_ascii=False,
            )

    def get_book_details(self, book: Book) -> str:
        return book.detailed_text()
