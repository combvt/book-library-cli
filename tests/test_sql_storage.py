from src.storage.sql_storage import SqlLibraryStorage
from src.models import Book


def test_get_stats_empty_library():
    library = SqlLibraryStorage("test_sql.db")

    assert library.get_stats() == {
                                    "total_books": 0,
                                    "unique_authors": 0,
                                    "page_count": None,
                                    "earliest_added": None,
                                    "latest_added": None,
                                }
    
    
def test_get_stats_after_adding_book():
    book = Book(
                title="test",
                book_id="test123GHbffdf",
                author="Mickey",
                page_count=67,
                description="testTesTTTTEST",
                categories="space",
                date_published="2077-03-16",
                isbn="FdsBHGf45DSs"
           )
    library = SqlLibraryStorage("test_sql.db")

    library.add(book)
    stats = library.get_stats()
    assert stats["total_books"] == 1
