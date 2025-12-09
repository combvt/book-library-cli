from fastapi import FastAPI, Depends, status, HTTPException
from library import Library
from storage.sql_storage import SqlLibraryStorage
from config import DB_PATH
from schemas import BookOut
from pydantic import BaseModel


app = FastAPI()

library_storage = SqlLibraryStorage(DB_PATH)
library = Library(library_storage)

def sql_library():
    return library

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
            
   
       