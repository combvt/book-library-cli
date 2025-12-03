from storage_base import LibraryStorage
from db import get_connection

class SqlLibraryStorage(LibraryStorage):
    def __init__(self, db_path="books.db"):
        self.path = db_path

    def load_all(self):
        ...

    def add(self, book):
        ...

    def remove(self, book_id):
        ...