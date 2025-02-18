from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Author as AuthorModel
from app.schemas import Author, AuthorCreate
from ..database import get_db

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post(
    "/",
    response_model=Author,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Author created successfully", "content": {"application/json": {"example": {"id": 1, "name": "Author Name"}}}},
        400: {"description": "Bad Request"},
        422: {"description": "Invalid request or data format"},
    },
)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Crear un nuevo autor"""
    new_author = AuthorModel(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get(
    "/",
    response_model=list[Author],
    responses={
        200: {
            "description": "List of authors",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "name": "Author One"},
                        {"id": 2, "name": "Author Two"},
                    ]
                }
            },
        },
        404: {"description": "No authors found"},
    },
)
def list_authors(db: Session = Depends(get_db)):
    """Obtener la lista de todos los autores"""
    authors = db.query(AuthorModel).all()
    if not authors:
        raise HTTPException(status_code=404, detail="No authors found")
    return authors

@router.get(
    "/{author_id}",
    response_model=Author,
    responses={
        200: {
            "description": "Author found",
            "content": {
                "application/json": {"example": {"id": 1, "name": "Author Name"}}
            },
        },
        404: {"description": "Author not found"},
    },
)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un autor por su ID"""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
    return author

@router.put(
    "/{author_id}",
    response_model=Author,
    responses={
        200: {
            "description": "Author updated successfully",
            "content": {"application/json": {"example": {"id": 1, "name": "Updated Author Name"}}},
        },
        404: {"description": "Author not found"},
    },
)
def update_author(author_id: int, author_update: AuthorCreate, db: Session = Depends(get_db)):
    """Actualizar los detalles de un autor"""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")

    # Actualizar los campos del autor
    for key, value in author_update.model_dump().items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author

@router.delete(
    "/{author_id}",
    responses={
        200: {"description": "Author deleted successfully", "content": {"application/json": {"example": {"detail": "Author with ID 1 deleted successfully"}}}},
        404: {"description": "Author not found"},
    },
)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Eliminar un autor por su ID"""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")

    db.delete(author)
    db.commit()
    return {"detail": f"Author with ID {author_id} deleted successfully"}