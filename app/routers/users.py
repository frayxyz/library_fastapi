from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.schemas import User, UserCreate, UserUpdate, UserAuth
from ..database import get_db
from ..auth import create_access_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario. Si el correo electrónico ya está registrado, devuelve un error.
    """
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserModel(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token", responses={
    200: {
        "description": "Successful authentication",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.PZXVw3E6f4U8pjNHvVmGNRb8Un5kXz4kKOfM5FBYVDQ",
                    "token_type": "bearer"
                }
            }
        }
    },
    401: {
        "description": "Invalid credentials",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid credentials"
                }
            }
        }
    }
})
def login_for_access_token(user_credentials: UserAuth, db: Session = Depends(get_db)):
    """
    Autentica al usuario y genera un token JWT.
    """
    user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    if not user or user.password != user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un usuario por su ID.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información de un usuario.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_update.name or user.name
    user.email = user_update.email or user.email
    user.password = user_update.password or user.password

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    204: {
        "description": "User deleted successfully",
        "content": {
            "application/json": {
                "example": None
            }
        }
    },
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            }
        }
    }
})
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario por su ID.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return
