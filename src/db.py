import sqlite3
from config import DB_PATH



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
