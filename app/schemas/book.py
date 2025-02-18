from pydantic import BaseModel
from typing import Optional
from app.schemas.user import User  # Absolute import
from app.schemas.author import Author  # Absolute import

class BookBase(BaseModel):
    title: str
    publication_year: Optional[int] = None
    author_id: int

    class Config:
        schema_extra = {
            "example": {
                "title": "Pride and Prejudice",
                "publication_year": 1813,
                "author_id": 1
            }
        }

class BookCreate(BookBase):
    pass  # Inherits the example from `BookBase`

class Book(BookBase):
    id: int
    author: Author
    borrowed_by: Optional[User] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Pride and Prejudice",
                "publication_year": 1813,
                "author_id": 1,
                "author": {
                    "id": 1,
                    "name": "Jane Austen",
                    "birth_date": "16/12/1775"
                },
                "borrowed_by": {
                    "id": 2,
                    "name": "John Doe",
                    "email": "johndoe@example.com"
                }
            }
        }
