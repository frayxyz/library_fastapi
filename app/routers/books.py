from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.models import Book as BookModel, Author as AuthorModel
from app.schemas import Book, BookCreate
from ..database import SessionLocal

router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == book.author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = BookModel(**book.dict())
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


#prestamo y devolucion de libros  (actualizar borrowed_by_id?)