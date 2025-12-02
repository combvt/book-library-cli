from models import Book
import json

class Library:
    def __init__(self, path: str) -> None:
        self.path = path
        self.books: list[Book] = []
        self._load()
    
    def _load(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if not isinstance(raw, list):
                raise ValueError("The library file must contain a list")
            
            self.books = [Book.from_dict(item) for item in raw]

        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            self.books = []

    
    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                [book.to_dict() for book in self.books],
                f,
                indent=4,
                ensure_ascii=False,
            )


    def add(self, item: Book) -> None:
        self.books.append(item)
        self._save()

        print(f"Added {item.title}, by {item.author} to your library.\n")


    def remove(self, index: int) -> None:
        if index < 0 or index >= len(self.books):
            print("Index out of range.")
            return
        
        removed = self.books.pop(index)
        self._save()

        print(f"Removed {removed.title}, by {removed.author}.")


    def is_empty(self) -> bool:
        return len(self.books) == 0
