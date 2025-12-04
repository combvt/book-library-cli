from .storage_base import LibraryStorage
from book_tracker_cli.db import get_connection, init_db
from book_tracker_cli.models import Book

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


    