import os
from dotenv import load_dotenv
from models import Book
from library import Library
from api_client import GoogleBooksClient
from storage.json_storage import JsonLibraryStorage

load_dotenv()

API_KEY = os.getenv("API_KEY")
LIBRARY_PATH = os.getenv("LIBRARY_PATH", "book_library.json")

if not API_KEY:
    raise ValueError("Missing API KEY. Make sure to create your .env file.")

def show_searched_books(books: list[Book]) -> None:
    if not books:
        print("No results found\n")
        return None
    
    for index ,item in enumerate(books, start=1):
        print(f"{index}. {item.short_line()}")


def choose_book_from_list(book_list: list[Book], choice: str) -> Book | None:
    try:
        idx = int(choice) - 1
    except (TypeError, ValueError):
        print("Invalid input, please enter a number.")
        return None
    
    if idx >= len(book_list) or idx < 0:
        print("Choice out of range.")
        return 
    
    return book_list[idx]


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

def search_and_add_book(client : GoogleBooksClient, library: Library):
    user_input = input("What book are you looking for?: ")
    books = client.search_books(user_input)

    if not books:
        show_searched_books(books)
        return
    
    show_searched_books(books)

    while True:
        user_choice = input("\nWhich book do you want to add to your library?: ").strip()
        chosen_book = choose_book_from_list(books, user_choice)

        if chosen_book is not None:
            add_or_view = input(
                "Type 'add', 'detailed' or 'again' to add, view detailed info or search again: "
            ).strip().lower()
            print()

            if add_or_view == "add":
                library.add(chosen_book)
                break
            elif add_or_view == "detailed":
                print()
                show_detailed_info(chosen_book)

                answer = input("Type 'add' or 'back' to add or go back: ").strip().lower()
                print()

                if answer == "add":
                    library.add(chosen_book)
                    break
                else:
                    print()
                    show_searched_books(books)
                    continue
            elif add_or_view == "again":
                return "again"            
        else:
            return


def manage_library(library: Library):
    while True:
        show_library(library)
        print()

        user_input = input(
            "Type 'remove' to remove a book, 'search' to search again, " 
            "or 'quit' to quit: "
        ).strip().lower()

        if user_input == "remove":
            while True:
                show_library(library)
                print()

                book_index_str = input("Which book do you want to remove?: ").strip()
                print()

                if not book_index_str.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue

                book_index = int(book_index_str)

                library.remove(book_index - 1)
                print()

                continue_removing = input(
                    "Type 'remove' to remove another book, "
                    "'search' to search again, "
                    "or 'quit' to quit: "
                ).strip().lower()
                
                if continue_removing == "remove" and not library.is_empty():
                    continue
                elif continue_removing == "search":
                    return "again"
                elif continue_removing == "quit":
                    return "quit"
                else:
                    print("Your library is empty.")
                    return

        elif user_input == "search":
            return "again"
        else:
            return "quit"
 

def main():
    json_storage = JsonLibraryStorage(LIBRARY_PATH)
    library = Library(json_storage)
    client = GoogleBooksClient(API_KEY)
    while True:
        user_answer = search_and_add_book(client, library)

        if user_answer == "again":
            continue
    
        action = input(
            "Do you want to search again? 'yes' or 'no', or 'view' your library: "
        ).strip().lower()

        if action == "no":
            break
        elif action == "view":
            answer = manage_library(library)

            if answer == "again":
                continue
            elif answer == "quit":
                break
            else:
                user_input = input("Do you want to search again? 'yes' or 'no': ")

                if user_input == "no":
                    break
                else:
                    continue
        else:
            continue

if __name__ == "__main__":
    main()
            







    
