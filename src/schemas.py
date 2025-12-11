from pydantic import BaseModel
from models import BookWithMetadata


class BookOut(BaseModel):
    sql_index: int
    title: str
    author: str | None
    description: str | None
    categories: str | None
    page_count: int | str
    date_published: str | None
    book_id: str
    isbn: str | None
    created_at: str

    @classmethod
    def from_metadata(cls, book: BookWithMetadata) -> BookOut:
        return cls(
            sql_index=book.sql_index,
            title=book.raw_book.title,
            author=book.raw_book.author,
            description=book.raw_book.description,
            categories=book.raw_book.categories,
            page_count=book.raw_book.page_count,
            date_published=book.raw_book.date_published,
            book_id=book.raw_book.book_id,
            isbn=book.raw_book.isbn,
            created_at=book.created_at,
        )


class BookSearchResult(BaseModel):
    title: str
    authors: str | None
    date_published: str | None
    book_id: str
    isbn: str | None
