import sqlite3
from datetime import datetime

DB_PATH = "books.db"

con = sqlite3.connect(DB_PATH)
cursor = con.cursor()

cursor.execute(
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
cursor.execute("""
    DELETE FROM books 
"""
)
con.commit()
res = cursor.execute("SELECT author FROM books")
print(res.fetchone())