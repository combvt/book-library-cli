from fastapi import FastAPI, Depends, status
from library import Library
from storage.sql_storage import SqlLibraryStorage
from config import DB_PATH
from schemas import BookOut


app = FastAPI()

library_storage = SqlLibraryStorage(DB_PATH)
library = Library(library_storage)

def sql_library():
    return library


@app.get("/books", response_model=list[BookOut], status_code=status.HTTP_200_OK)
def read_books(library: Library = Depends(sql_library)):
    bookout_list = []

    if isinstance(library.storage, SqlLibraryStorage):
        for item in library.books:
            full_item = library.storage.get_with_metadata(item)
            bookout_item = BookOut(
                sql_index = full_item.sql_index,
                title = full_item.raw_book.title,
                author = full_item.raw_book.author,
                description = full_item.raw_book.description,
                categories = full_item.raw_book.categories,
                page_count = full_item.raw_book.page_count,
                date_published = full_item.raw_book.date_published,
                book_id = full_item.raw_book.book_id,
                isbn = full_item.raw_book.isbn,
                created_at = full_item.created_at,
            )
            bookout_list.append(bookout_item)

    return bookout_list

