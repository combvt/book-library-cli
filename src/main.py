from dotenv import load_dotenv
from library import Library
from api_client import GoogleBooksClient
import utils
#TODO Add a BookWithMetaData class, storing book + sql info (date_added, 
# index in sql, etc.)
#TODO handle typeError when book not found when calling get_book_details()
# in SqlStorage
#TODO update changelog
#TODO check for indexErrors, ValueErrors, typeErrors
#TODO add get_string_from_user function
#TODO maybe add a delay after showing detailed info in library 
#so the info is not covered by show books
load_dotenv()

if not utils.API_KEY:
    raise ValueError("Missing API KEY. Make sure to create your .env file.")


def search_and_add_book(client : GoogleBooksClient, library: Library):
    user_input = input("What book are you looking for?: ")
    books = client.search_books(user_input)

    if not books:
        utils.show_searched_books(books)
        return
    
    utils.show_searched_books(books)

    while True:
        user_choice = input("\nWhich book do you want to add to your library?: ").strip()
        chosen_book = utils.choose_book_from_list(books, user_choice)

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
                utils.show_detailed_info(chosen_book)

                answer = input("Type 'add' or 'back' to add or go back: ").strip().lower()
                print()

                if answer == "add":
                    library.add(chosen_book)
                    break
                else:
                    print()
                    utils.show_searched_books(books)
                    continue
            elif add_or_view == "again":
                return "again"            
        else:
            return


def manage_library(library: Library) -> str | None:
    while True:
        utils.show_library(library)
        print()

        user_input = input(
            "Type 'remove' to remove a book, 'search' to search again, " 
            "'detailed' to view detailed info, or 'quit' to quit: "
        ).strip().lower()

        if user_input == "remove":
            while True:
                utils.show_library(library)
                print()

                book_index = utils.get_int_from_user("Which book do you want to remove?: ")
                print()

                if book_index:
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
        elif user_input == "detailed":
            utils.show_library(library)
            print()

            book_index = utils.get_int_from_user("What book do you want to view detailed info for?: ")

            if book_index:
                book = library.books[book_index - 1]

                utils.show_detailed_info_library(library, book)
        elif user_input == "quit":
            return "quit"
        else:
            print("Invalid input. ")
            continue
 

def main():
    library = utils.choose_storage()
    client = GoogleBooksClient(utils.API_KEY)
    
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
            







    
