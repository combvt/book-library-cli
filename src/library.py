from models import Book, BookWithMetadata
from storage.storage_base import LibraryStorage
from exceptions import BookNotFoundError


class Library:
    def __init__(self, storage: LibraryStorage) -> None:
        self.storage = storage
        self.books: list[Book] = self.storage.load_all()

    def add(self, item: Book) -> None:
        self.storage.add(item)
        self.books = self.storage.load_all()


    def remove(self, index: int) -> Book | None:
        try:
            removed_book = self.storage.remove(index)
            self.books = self.storage.load_all()
        except IndexError:
            raise BookNotFoundError("Index out of range.")

        if removed_book:
            return removed_book

    def is_empty(self) -> bool:
        return len(self.books) == 0
    
    def check_book_exists(self, google_id: str):
        return self.storage.exists_by_google_id(google_id)
