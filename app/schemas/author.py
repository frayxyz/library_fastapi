from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    birth_date: Optional[datetime] = None

class AuthorCreate(AuthorBase):
    @validator("birth_date", pre=True)
    def parse_birth_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Invalid date format. Use dd/mm/yyyy")
        return value

class Author(AuthorBase):
    id: int

    class Config:
        #orm_mode = True v1
        from_attributes = True #v2