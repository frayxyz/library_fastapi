from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.models import Book, User
from app.auth import get_current_user
from ..database import SessionLocal

router = APIRouter(prefix="/loans", tags=["loans"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/borrow/{book_id}",
              responses={
                    200: {
                        "description": "Book borrowed successfully",
                    },
                    404: {"description": "Book not found"},
                    400: {"description": "Book is already borrowed"},
                    401: {"description": "Invalid token or user not found"},
                },)
def borrow_book(book_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.borrowed_by_id:
        raise HTTPException(status_code=400, detail="Book is already borrowed")
    book.borrowed_by_id = current_user.id
    db.commit()
    return {"message": "Book borrowed successfully"}

@router.post("/return/{book_id}",
             responses={
                    200: {
                        "description": "Book returned successfully",
                    },
                    404: {"description": "Book not found"},
                    400: {"description": "Book not borrowed by you"},
                    401: {"description": "Invalid token or user not found"},
                },)
def return_book(book_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.borrowed_by_id or book.borrowed_by_id != current_user.id:
        raise HTTPException(status_code=400, detail="Book not borrowed by you")
    book.borrowed_by_id = None
    db.commit()
    return {"message": "Book returned successfully"}