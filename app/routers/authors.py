from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Author as AuthorModel
from app.schemas import Author, AuthorCreate
from ..database import SessionLocal, get_db

router = APIRouter(prefix="/authors", tags=["authors"])
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        '''

@router.post("/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = AuthorModel(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get("/", response_model=list[Author])
def list_authors( db: Session = Depends(get_db)):
    authors = db.query(AuthorModel).all()
    if not authors:
        raise HTTPException(status_code=404, detail="No authors found")
    return authors # FastAPI convierte automáticamente el modelo SQLAlchemy a User (esquema Pydantic)