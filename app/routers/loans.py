from fastapi import APIRouter, Depends, HTTPException
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models import Book, User
from app.auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

security_scheme = HTTPBearer() 

@router.post(
    "/borrow/{book_id}",
    responses={
        200: {
            "description": "Book borrowed successfully",
            "content": {
                "application/json": {
                    "example": {"message": "Book borrowed successfully"}
                }
            }
        },
        404: {
            "description": "Book not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Book not found"}
                }
            }
        },
        400: {
            "description": "Book is already borrowed",
            "content": {
                "application/json": {
                    "example": {"detail": "Book is already borrowed"}
                }
            }
        },
        401: {
            "description": "Invalid token or user not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid token or user not found"}
                }
            }
        },
    },
       openapi_extra={
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {
                    "type": "string",
                    "example": "Bearer YOUR_TOKEN_HERE",
                },
            }
        ]
    },
    dependencies=[Security(security_scheme)]
)
def borrow_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    # Query the book from the database
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.borrowed_by_id:
        raise HTTPException(status_code=400, detail="Book is already borrowed")
    
    # Assign the book to the current user
    book.borrowed_by_id = current_user.id
    
    # Commit the changes to the database
    db.commit()
    return {"message": "Book borrowed successfully"}

@router.post("/return/{book_id}",
             responses={
        200: {
            "description": "Book returned successfully",
            "content": {
                "application/json": {
                    "example": {"message": "Book returned successfully"}
                }
            }
        },
        404: {
            "description": "Book not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Book not found"}
                }
            }
        },
        400: {
            "description": "Book not borrowed by you",
            "content": {
                "application/json": {
                    "example": {"detail": "Book not borrowed by you"}
                }
            }
        },
        401: {
            "description": "Invalid token or user not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid token or user not found"}
                }
            }
        },
    },openapi_extra={
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {
                    "type": "string",
                    "example": "Bearer YOUR_TOKEN_HERE",
                },
            }
        ]
    })
def return_book(book_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.borrowed_by_id or book.borrowed_by_id != current_user.id:
        raise HTTPException(status_code=400, detail="Book not borrowed by you")
    book.borrowed_by_id = None
    db.commit()
    return {"message": "Book returned successfully"}