from models import Book


class LibraryStorage:
    def load_all(self) -> list[Book]:
        raise NotImplementedError


    def add(self, book: Book) -> None:
        pass


    def remove (self, index: int) -> None:
        pass