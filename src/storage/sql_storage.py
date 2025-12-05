from .storage_base import LibraryStorage
from db import get_connection, init_db
from models import Book

class SqlLibraryStorage(LibraryStorage):
    def __init__(self, db_path="books.db"):
        self.path = db_path
        init_db()


    def load_all(self) -> list[Book]:
        with get_connection() as conn:
            cursor = conn.execute(
                        """
                        SELECT title, google_id, author, page_count, description,
                        categories, date_published, isbn FROM books 
                        ORDER BY id ASC
                        """
                    )
            rows = cursor.fetchall()

        return [self._row_to_book(row) for row in rows]


    def add(self, book: Book) -> None:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO books (
                    title,
                    google_id,
                    author,
                    page_count,
                    description,
                    categories,
                    date_published,
                    isbn
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    book.title,
                    book.book_id,
                    book.author,
                    book.page_count,
                    book.description,
                    book.categories,
                    book.date_published,
                    book.isbn
                )
            )




    def remove(self, index: int) -> None:
        with get_connection() as conn:
            cursor = conn.execute(
                    """
                    SELECT id FROM books ORDER BY id ASC
                    """)
            rows = cursor.fetchall()

            if index < 0 or index >= len(rows):
                print("Index out of range")
                return
            
            row = rows[index]
            book_id = row[0]

            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))



    def _row_to_book(self, row: tuple) -> Book:
        row_title = row[0]
        row_google_id = row[1]
        row_author = row[2]
        row_page_count = row[3]
        row_description = row[4]
        row_categories = row[5]
        row_date_published = row[6]
        row_isbn = row [7]

        return Book(
            title=row_title,
            book_id=row_google_id,
            author=row_author,
            page_count=row_page_count,
            description=row_description,
            categories=row_categories,
            date_published=row_date_published,
            isbn=row_isbn,
        )
    

    def get_book_details(self, book: Book) -> dict:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, author, description, categories,
                page_count, date_published, google_id, isbn, created_at FROM books
                WHERE google_id = ?
                """,
                (book.book_id,)
            )
            row = cursor.fetchone()

        return {
            "sql_index": row[0],
            "Title": row[1],
            "Author": row[2],
            "Description": row[3],
            "Categories": row[4],
            "Page count": row[5],
            "Date Published": row[6],
            "ID": row[7],
            "isbn": row[8],
            "created_at": row[9],
        }


    