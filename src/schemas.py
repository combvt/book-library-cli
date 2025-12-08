from pydantic import BaseModel

class BookOut(BaseModel):
    sql_index: int
    title: str
    author: str | None = None
    description: str | None = None
    categories: str | None = None
    page_count: int | None = None
    date_published: str | None = None
    book_id: str
    isbn: str | None = None
    created_at: str