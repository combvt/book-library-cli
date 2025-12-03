from models import Book


class LibraryStorage:
    def load_all(self) -> list[Book]:
        raise NotImplementedError


    def add(self, book: Book) -> None:
        raise NotImplementedError


    def remove (self, index: int) -> None:
        raise NotImplementedError