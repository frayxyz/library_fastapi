from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserAuth(BaseModel):    
    email: EmailStr
    password: str   
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None    

class User(UserBase):
    id: int
    registration_date: datetime

    class Config:
        from_attributes = True