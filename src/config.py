from dotenv import load_dotenv
import os





load_dotenv()

DB_PATH = os.getenv("DB_PATH", "books.db")
API_KEY = os.getenv("API_KEY")
LIBRARY_PATH = os.getenv("LIBRARY_PATH", "book_library.json")
