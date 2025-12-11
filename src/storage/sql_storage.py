from .storage_base import LibraryStorage
from db import get_connection, init_db
from models import Book, BookWithMetadata
import random


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
                    book.isbn,
                ),
            )

    def remove(self, index: int) -> Book | None:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                    SELECT id, title, author, description, categories,
                    page_count, date_published, google_id, isbn, created_at FROM books
                """
            )
            rows = cursor.fetchall()

            if index < 0 or index >= len(rows):
                raise IndexError

            row = rows[index]
            book_id = row[0]

            removed_book = self.build_book_from_row(row)

            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))

            return removed_book

    def _row_to_book(self, row: tuple) -> Book:
        row_title = row[0]
        row_google_id = row[1]
        row_author = row[2]
        row_page_count = row[3]
        row_description = row[4]
        row_categories = row[5]
        row_date_published = row[6]
        row_isbn = row[7]

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

    def _fetch_row_by_book(self, book: Book) -> tuple:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, author, description, categories,
                page_count, date_published, google_id, isbn, created_at FROM books
                WHERE google_id = ?
                """,
                (book.book_id,),
            )
            row = cursor.fetchone()

            return row

    def get_book_details(self, book: Book) -> dict:
        row = self._fetch_row_by_book(book)

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

    def get_with_metadata(self, book: Book) -> BookWithMetadata:
        row = self._fetch_row_by_book(book)

        return BookWithMetadata.from_row(row, book)

    def build_book_from_row(self, row: tuple) -> Book:
        return Book(
            title=row[1],
            book_id=row[7],
            author=row[2],
            page_count=row[5],
            description=row[3],
            categories=row[4],
            date_published=row[6],
            isbn=row[8],
        )

    def exists_by_google_id(self, google_id: str) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id FROM books
                where google_id = ?
                """,
                (google_id,),
            )

            row = cursor.fetchone()

        return row is not None

    def get_by_sql_index(self, sql_index: int) -> BookWithMetadata | None:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, author, description, categories,
                page_count, date_published, google_id, isbn, created_at FROM books
                WHERE id = ?
                """,
                (sql_index,),
            )
            row = cursor.fetchone()

            if row:
                book = self.build_book_from_row(row)

                return BookWithMetadata.from_row(row, book)

            return None

    def remove_by_sql_index(self, sql_index: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                DELETE from books
                WHERE id = ?
                """,
                (sql_index,),
            )

            return cursor.rowcount > 0

    def search(self, q: str) -> list[BookWithMetadata]:
        with get_connection() as conn:
            like_q = f"%{q}%"
            cursor = conn.execute(
                """
                    SELECT id, title, author, description, categories,
                    page_count, date_published, google_id, isbn, created_at FROM books
                    WHERE title LIKE ?
                    OR author LIKE ?
                    OR description LIKE ?
                """,
                (like_q, like_q, like_q),
            )
            rows = cursor.fetchall()

            if rows:
                book_list: list[BookWithMetadata] = []
                for row in rows:
                    book = self.build_book_from_row(row)

                    meta_book = BookWithMetadata.from_row(row, book)

                    book_list.append(meta_book)

                return book_list

            return []

    def get_random_book(self) -> BookWithMetadata | None:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id FROM books
                """
            )

            rows = cursor.fetchall()
            id_list = [x[0] for x in rows]

            fetched_id = random.choice(id_list)

            return self.get_by_sql_index(fetched_id)
