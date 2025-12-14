from src.storage.sql_storage import SqlLibraryStorage
from src.models import Book
import src.db
import sqlite3
import src.storage.sql_storage


def test_get_stats_empty_library(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test.db"

    def fake_get_connection():
        return sqlite3.connect(test_db_path)

    monkeypatch.setattr(src.db, "get_connection", fake_get_connection)
    monkeypatch.setattr(src.storage.sql_storage, "get_connection", fake_get_connection)

    src.db.init_db()

    library = SqlLibraryStorage(test_db_path)

    assert library.get_stats() == {
        "total_books": 0,
        "unique_authors": 0,
        "page_count": None,
        "earliest_added": None,
        "latest_added": None,
    }


def test_get_stats_after_adding_book(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test.db"

    def fake_get_connection():
        return sqlite3.connect(test_db_path)

    monkeypatch.setattr(src.db, "get_connection", fake_get_connection)
    monkeypatch.setattr(src.storage.sql_storage, "get_connection", fake_get_connection)

    src.db.init_db()

    book = Book(
        title="test",
        book_id="test123GHbffdf",
        author="Mickey",
        page_count=67,
        description="testTesTTTTEST",
        categories="space",
        date_published="2077-03-16",
        isbn="FdsBHGf45DSs",
    )
    library = SqlLibraryStorage(test_db_path)

    library.add(book)
    stats = library.get_stats()
    assert stats["total_books"] == 1
