from fastapi import FastAPI, Depends
from library import Library
from storage.sql_storage import SqlLibraryStorage
from utils import DB_PATH

app = FastAPI()

library_storage = SqlLibraryStorage(DB_PATH)
library = Library(library_storage)

def sql_library():
    return library