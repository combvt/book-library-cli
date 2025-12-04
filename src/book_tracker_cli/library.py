from book_tracker_cli.models import Book
from book_tracker_cli.storage.storage_base import LibraryStorage

class Library:
    def __init__(self, storage: LibraryStorage) -> None:
        self.storage = storage
        self.books: list[Book] = self.storage.load_all()
       
  
    def add(self, item: Book) -> None:
        self.storage.add(item)
        self.books = self.storage.load_all()
        
        print(f"Added {item.title}, by {item.author} to your library.\n")


    def remove(self, index: int) -> None:
        try:
            removed_book = self.books[index]
        except IndexError:
            print("Index out of range.")
            return

        self.storage.remove(index)
        self.books = self.storage.load_all()

        print(f"Removed {removed_book.title}, by {removed_book.author}.")


    def is_empty(self) -> bool:
        return len(self.books) == 0
