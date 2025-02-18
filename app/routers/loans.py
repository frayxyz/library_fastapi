from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.models import Book, User
from app.auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post(
    "/borrow/{book_id}",
    responses={
        200: {"description": "Book borrowed successfully"},
        404: {"description": "Book not found"},
        400: {"description": "Book is already borrowed"},
        401: {"description": "Invalid token or user not found"},
    },
)
def borrow_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    print(f"Attempting to borrow book with ID: {book_id}")
    
    # Query the book from the database
    book = db.query(Book).filter(Book.id == book_id).first()
    print(f"Query result for book with ID {book_id}: {book}")
    
    if not book:
        print(f"Book with ID {book_id} not found in the database.")
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.borrowed_by_id:
        print(f"Book with ID {book_id} is already borrowed by user ID {book.borrowed_by_id}.")
        raise HTTPException(status_code=400, detail="Book is already borrowed")
    
    # Assign the book to the current user
    print(f"Borrowing book with ID {book_id} for user ID {current_user.id}")
    book.borrowed_by_id = current_user.id
    
    # Commit the changes to the database
    db.commit()
    print(f"Book with ID {book_id} successfully borrowed by user ID {current_user.id}")
    
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