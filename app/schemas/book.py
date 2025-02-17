from pydantic import BaseModel
from typing import Optional

from app.schemas.user import User  # Importación absoluta
from app.schemas.author import Author  # Importación absoluta


class BookBase(BaseModel):
    title: str
    publication_year: Optional[int] = None
    author_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author: Author
    borrowed_by: Optional[User] = None

    class Config:
        from_attributes = True