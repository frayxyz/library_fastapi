from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  #pswd property added

class User(UserBase):
    id: int
    registration_date: datetime

    class Config:
        from_attributes = True