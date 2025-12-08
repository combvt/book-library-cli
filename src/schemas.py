from pydantic import BaseModel

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

