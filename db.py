import sqlite3
from datetime import datetime


DB_PATH = "books.db"
now = datetime.now()
date_time = now.strftime(r"%m/%d/%Y %H:%M:%S")

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        description TEXT,
        categories TEXT,
        page_count INTEGER,
        date_published TEXT,
        google_id TEXT,
        isbn TEXT,
        created_at TEXT
        );
        """
        )
    conn.commit()


def add_book(
    title: str,
    author: str,
    description: str,
    categories: str,
    page_count: int,
    date_published: str,
    google_id: str,
    isbn: str,
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO books 
            (title, author, description, categories, page_count,
            date_published, google_id, isbn, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, author, description, categories, page_count, date_published,
            google_id, isbn, date_time)
        )
        conn.commit()















