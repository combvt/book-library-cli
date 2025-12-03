from models import Book
import json

class Library:
    def __init__(self, path: str) -> None:
        self.path = path
        self.books: list[Book] = []
    

    def is_empty(self) -> bool:
        return len(self.books) == 0
