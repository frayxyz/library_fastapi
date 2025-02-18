from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Author as AuthorModel
from app.schemas import Author, AuthorCreate
from ..database import get_db

router = APIRouter(prefix="/authors", tags=["authors"])


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
    return authors

# Obtener un autor por ID
@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
    return author

# Editar un autor
@router.put("/{author_id}", response_model=Author)
def update_author(author_id: int, author_update: AuthorCreate, db: Session = Depends(get_db)):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")

    # Actualizar los campos del autor
    for key, value in author_update.model_dump().items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author

# Eliminar un autor
@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")

    db.delete(author)
    db.commit()
    return {"detail": f"Author with ID {author_id} deleted successfully"}