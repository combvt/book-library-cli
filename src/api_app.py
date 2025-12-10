from fastapi import FastAPI, Depends, status, HTTPException, Query
from library import Library
from storage.sql_storage import SqlLibraryStorage
from config import DB_PATH, API_KEY
from schemas import BookOut, BookSearchResult
from google_api_client import GoogleBooksClient

app = FastAPI()

library_storage = SqlLibraryStorage(DB_PATH)
library = Library(library_storage)

def sql_library():
    return library


def google_client():
    return GoogleBooksClient(API_KEY)


@app.get("/books", response_model=list[BookOut], status_code=status.HTTP_200_OK)
def read_books(q: str | None = None, library: Library = Depends(sql_library)):
    if isinstance(library.storage, SqlLibraryStorage):
        if q is None or q == "":
            bookout_list = []   
            for item in library.books:
                full_item = library.storage.get_with_metadata(item)
                bookout_item = BookOut.from_metadata(full_item)
                
                bookout_list.append(bookout_item)

            return bookout_list
        elif q:
            meta_books = library.storage.search(q=q)
            
            return [BookOut.from_metadata(item) for item in meta_books]


@app.get("/books/{sql_index}", response_model=BookOut)
def get_book(sql_index: int, library: Library = Depends(sql_library)):
    if isinstance(library.storage, SqlLibraryStorage):
        fetched_book = library.storage.get_by_sql_index(sql_index)

        if not fetched_book:
            raise HTTPException(404, detail="Book does not exist.")
        
        return BookOut.from_metadata(fetched_book)
            
   
@app.get("/search/google", response_model=list[BookSearchResult])
def show_results(q: str = Query(min_length=1), results: int = Query(default=10, le=40, ge=1), client: GoogleBooksClient = Depends(google_client)):
        book_list = client.search_books(q, results)

        if not book_list:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No books found")
        
        return [BookSearchResult(
                title=book.title,
                authors=book.author,
                date_published=book.date_published,
                book_id=book.book_id,
                isbn=book.isbn
            )
                for book in book_list
        ]
    
    
        


