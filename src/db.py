import sqlite3
from dotenv import load_dotenv
import os


load_dotenv()

DB_PATH = os.getenv("DB_PATH", "books.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT,
        description TEXT,
        categories TEXT,
        page_count INTEGER,
        date_published TEXT,
        google_id TEXT,
        isbn TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        )
        conn.commit()



def get_all_books_from_db():
    with get_connection() as conn:
        cursor = conn.execute(
        """
        SELECT id, title, author, description, categories, page_count,
        date_published, google_id, isbn, created_at FROM books
        """
    )    
        rows = cursor.fetchall()

    books = []

    for row in rows:
        book = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "description": row[3],
            "categories": row[4],
            "page_count": row[5],
            "date_published": row[6],
            "google_id": row[7],
            "isbn": row[8],
            "created_at": row[9],
        }
        books.append(book)

    return books


        













