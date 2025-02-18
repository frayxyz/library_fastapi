from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.models import Book as BookModel, Author as AuthorModel
from app.schemas import Book, BookCreate
from ..database import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == book.author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = BookModel(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/search", response_model=List[Book])
def search_books( title: str | None = None, author: str | None = None, year: int | None = None,  db: Session = Depends(get_db)):
    query = db.query(BookModel)

    if author:
        query = query.join(AuthorModel).filter(AuthorModel.name.ilike(f"%{author}%"))

    # Filtros dinámicos
    filters = []
    if title:
        filters.append(BookModel.title.ilike(f"%{title}%"))  # Búsqueda parcial insensible a mayúsculas/minúsculas
    if year:
        filters.append(BookModel.publication_year == year)

    # Combinar los filtros con AND si existen
    if filters:
        query = query.filter(and_(*filters))

    books = query.all()

    if not books:
        raise HTTPException(status_code=404, detail="Books not found")

    return books


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Actualizar los campos
    for field, value in book_update.model_dump().items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}