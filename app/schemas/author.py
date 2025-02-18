from pydantic import BaseModel, ConfigDict, Field, validator
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    birth_date: Optional[datetime] = Field(
        None, 
        example="18/02/2025"
    )


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
        model_config = ConfigDict(from_attributes=True)