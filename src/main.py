from dotenv import load_dotenv
from library import Library
from api_client import GoogleBooksClient
from models import Book
import utils

load_dotenv()

if not utils.API_KEY:
    raise ValueError("Missing API KEY. Make sure to create your .env file.")



def inner_flow(chosen_book: Book | None, library: Library, books: list[Book]) -> str | None:
     while True:
            if chosen_book is not None:
                add_or_view = utils.get_string_from_user(
                    "Type 'add', 'detailed' or 'again' to add, view detailed info or search again: "
                )
                print()

                if add_or_view == "add":
                    library.add(chosen_book)
                    return None
                elif add_or_view == "detailed":
                    print()
                    utils.show_detailed_info(chosen_book)

                    while True:
                        answer = utils.get_string_from_user("Type 'add' or 'back' to add or go back: ")
                        print()

                        if answer == "add":
                            library.add(chosen_book)

                            return None
                        elif answer == "back":
                            print()
                            utils.show_searched_books(books)

                            return "continue"
                        else:
                            print("Invalid option.")
                            continue

                elif add_or_view == "again":
                    return "again"            
            else:
                return 



def search_and_add_book(client : GoogleBooksClient, library: Library) -> str | None:
    while True:
       user_input = utils.get_string_from_user("What book are you looking for?: ")

       if not user_input:
           print("Please type something.")
           continue
       else:
           break
       
    books = client.search_books(user_input)

    if not books:
        utils.show_searched_books(books)
        return
    
    utils.show_searched_books(books)

    while True:
        user_choice = utils.get_string_from_user("\nWhich book do you want to add to your library?: ")
        chosen_book = utils.choose_book_from_list(books, user_choice)
        result = inner_flow(chosen_book, library, books)

        if result == "again":
            return "again"
        elif result == "continue":
            continue
        elif result is None:
            return None
      


def manage_library(library: Library) -> str | None:
    while True:
        utils.show_library(library)
        print()

        user_input = utils.get_string_from_user(
            "Type 'remove' to remove a book, 'search' to search again, " 
            "'detailed' to view detailed info, or 'quit' to quit: "
        )

        if user_input == "remove":
            while True:
                utils.show_library(library)
                print()

                book_index = utils.get_int_from_user("Which book do you want to remove?: ")
                print()

                if book_index:
                    library.remove(book_index - 1)
                    print()

                    continue_removing = utils.get_string_from_user(
                        "Type 'remove' to remove another book, "
                        "'search' to search again, "
                        "or 'quit' to quit: "
                    )
                    
                    if continue_removing == "remove" and not library.is_empty():
                        continue
                    elif continue_removing == "search":
                        return "search"
                    elif continue_removing == "quit":
                        return "quit"
                    else:
                        print("Your library is empty.")
                        return

        elif user_input == "search":
            return "search"
        elif user_input == "detailed":
            utils.show_library(library)
            print()

            book_index = utils.get_int_from_user("What book do you want to view detailed info for?: ")

            if book_index:
                try:
                    book = library.books[book_index - 1]
                except IndexError:
                    print("Index out of range.")
                    continue

                utils.show_detailed_info_library(library, book)
                utils.stand_by()
        elif user_input == "quit":
            return "quit"
        else:
            print("Invalid input.")
            continue
 

def view_library_inner_flow(library: Library) -> str | None:
    answer = manage_library(library)

    if answer == "search":
        return "search"
    elif answer == "quit":
        return "quit"
    else:
        while True:
            user_input = utils.get_string_from_user("Do you want to search again? 'yes' or 'no': ")

            if user_input == "no":
                return "quit"
            elif user_input == "yes":
                return "search" 
            else:
                print("Invalid input.")
                

       




def main():
    library = utils.choose_storage()
    client = GoogleBooksClient(utils.API_KEY)
    choice = input("Type 'search' or 'view' to search books or view your library: ")
    while True:

        if choice == "quit":
            return
        elif choice == "search":
            user_answer = search_and_add_book(client, library)

            if user_answer == "again":
                continue

            while True:
                action = utils.get_string_from_user(
                    "Do you want to search again? 'yes' or 'no', or 'view' your library: "
                )

                if action == "no":
                    return
                elif action == "yes":
                    choice = "search"
                    break
                elif action == "view":
                    choice = view_library_inner_flow(library)
                    break
                else:
                    print("Invalid input.")
                    continue
        elif choice == "view":
            choice = view_library_inner_flow(library)


if __name__ == "__main__":
    main()
            







    
