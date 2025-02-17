from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.schemas import User, UserCreate
from ..database import SessionLocal

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserModel(name=user.name, email=user.email, password =user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#protected endpoints
'''
from fastapi import Depends, HTTPException
from ..auth import verify_token

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    return user_id

@router.post("/protected")
def protected_route(current_user: int = Depends(get_current_user)):
    return {"user_id": current_user}
    '''

from ..auth import create_access_token

@router.post("/token")
def login_for_access_token(user_credentials: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para autenticar al usuario y generar un token JWT.
    """
    user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    if not user or user.password != user_credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generar token JWT
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
'''


@router.post("/auth")  #auth and generate token
def login(user_credentials: UserCreate, db: Session = Depends(SessionLocal)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or user.password != user_credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
'''