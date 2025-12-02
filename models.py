class Book:
    def __init__(self,
        title: str,
        book_id: str, 
        author: str,
        page_count: int | str,
        description: str,
        categories: str,
        date_published: str,
    ):
        self.title = title
        self.book_id = book_id
        self.author = author
        self.page_count = page_count
        self.description = description
        self.categories = categories
        self.date_published = date_published


    @classmethod
    def from_api(cls, item: dict) -> Book:
        volume_info = item.get("volumeInfo", {})

        book_title = volume_info.get("title", "Unknown")
        book_id = item.get("id", "")
        book_author = ", ".join(volume_info.get("authors", ["Unknown author"]))
        book_published_date = volume_info.get("publishedDate", "Unknown")
        book_page_count = volume_info.get("pageCount", "Unknown")
        book_description = volume_info.get("description", "No book description")
        book_category = ", ".join(volume_info.get("categories", ["Unknown category"]))

        return cls(
            title = book_title,
            author = book_author,
            date_published = book_published_date,
            page_count = book_page_count,
            description = book_description,
            categories = book_category,
            book_id = book_id,
        )


    @classmethod
    def from_dict(cls, data: dict) -> Book:
        book_title = data.get("Title", "Unknown")
        book_id = data.get("ID", "")
        book_author = data.get("Authors", ["Unknown author"])
        book_published_date = data.get("Date Published", "Unknown")
        book_page_count = data.get("Page Count", "Unknown")
        book_description = data.get("Description", "No book description")
        book_category = data.get("Categories", ["Unknown category"])

        return cls(
            title = book_title,
            author = book_author,
            date_published = book_published_date,
            page_count = book_page_count,
            description = book_description,
            categories = book_category,
            book_id = book_id,
        )


    def to_dict(self) -> dict:
        return {
            "Title": self.title,
            "ID": self.book_id,
            "Authors": self.author,
            "Date Published": self.date_published,
            "Page Count": self.page_count,
            "Description": self.description,
            "Categories": self.categories,
        }
    

    def short_line(self) -> str:
        return f"{self.title} -- {self.author} ({self.date_published})"
    

    def detailed_text(self) -> str:
        return (
        f"Title: {self.title}\n"
        f"Author: {self.author}\n"
        f"Description: {self.description}\n"
        f"Page count: {self.page_count}\n"
        f"Categories: {self.categories}\n"
    )
 
