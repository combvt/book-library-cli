from models import Book, BookWithMetadata
from library import Library
from storage.sql_storage import SqlLibraryStorage
from storage.json_storage import JsonLibraryStorage
from db import DB_PATH
import os
import msvcrt

API_KEY = os.getenv("API_KEY")
LIBRARY_PATH = os.getenv("LIBRARY_PATH", "book_library.json")


def get_int_from_user(prompt: str) -> int | None:
    user_input = input(prompt).strip()

    if not user_input.isdigit():
        print("Invalid input. Please enter a number.")
        print()

        return None
    
    return int(user_input)


def get_string_from_user(prompt: str) -> str:
    user_input = input(prompt).strip().lower()

    return user_input


def show_library(library: Library):
    if library.is_empty():
        print("Your library is empty.")
        return
    
    for index, book in enumerate(library.books, start=1):
        print(f"{index}. {book.title} -- {book.author} ({book.date_published})")


def show_detailed_info(book: Book | None) -> None:
    if not book:
        print("Detailed info not found.")
        return None
    
    print(book.detailed_text())

#FIXME continue printing out bookwithmetadata info
# Maybe look into using book.detailed_text() + 2 more lines of metadata
def show_detailed_info_library(library: Library, book: Book) -> None:
    if book is None:
        print("Book not found.")
        return None
    
    if isinstance(library.storage, JsonLibraryStorage):
        fetched_book =  library.storage.get_book_details(book)
        if fetched_book is not None:
            for key, value in fetched_book.items():
                print(f"{key}: {value}")
        else:
            print("Book not found.")
            return
    elif isinstance(library.storage, SqlLibraryStorage):
        fetched_book = library.storage.get_with_metadata(book)

    print()


def choose_book_from_list(book_list: list[Book], choice: str) -> Book | None:
    try:
        idx = int(choice) - 1
    except (TypeError, ValueError):
        print("Invalid input, please enter a number.")
        return None
    
    if idx >= len(book_list) or idx < 0:
        print("Choice out of range.")
        return None
    
    return book_list[idx]


def show_searched_books(books: list[Book]) -> None:
    if not books:
        print("No results found")
        print()
        return None
    
    for index ,item in enumerate(books, start=1):
        print(f"{index}. {item.short_line()}")


def choose_storage() -> Library:
    while True:
        chosen_storage = get_string_from_user("Choose storage type: 'json' or 'sql': ")

        if chosen_storage == "json":
            library = JsonLibraryStorage(LIBRARY_PATH)
            return Library(library)
        elif chosen_storage == "sql":
            library = SqlLibraryStorage(DB_PATH)
            return Library(library)
        else:
            print("Invalid option. Please type either 'json' or 'sql'.")


def stand_by():
    print("Press any key to continue...")
    msvcrt.getch()


