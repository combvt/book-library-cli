from models import Book


class LibraryStorage:
    def load_all(self) -> list[Book]:
        raise NotImplementedError

    def add(self, book: Book) -> None:
        raise NotImplementedError

    def remove(self, index: int) -> None:
        raise NotImplementedError

    def get_book_details(self, book: Book) -> dict:
        raise NotImplementedError

    def exists_by_google_id(self, google_id: str) -> bool:
        raise NotImplementedError

    def remove_by_sql_index(self, sql_index: int) -> bool:
        raise NotImplementedError
