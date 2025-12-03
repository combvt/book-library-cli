from storage_base import LibraryStorage
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
        list = self.load_all()

        list.append(book)
        self._save(list)

        print(f"Added {book.title}, by {book.author} to your library.\n")


    def remove(self, index: int) -> None:
        books_list = self.load_all()

        if index < 0 or index >= len(books_list):
            print("Index out of range.")
            return
        
        removed_book = books_list.pop(index)

        self._save(books_list)
        
        print(f"Removed {removed_book.title}, by {removed_book.author}.")


     
    def _save(self, book_list: list[Book]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                [book.to_dict() for book in book_list],
                f,
                indent=4,
                ensure_ascii=False,
            )
