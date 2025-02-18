from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.schemas import User, UserCreate
from ..database import  get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Received user data: {user}")
    
    # Verificar si el usuario ya existe
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    print(f"Existing user: {db_user}")  # Imprime si se encontró un usuario existente

    if db_user:
        print("User already registered")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear un nuevo usuario
    new_user = UserModel(name=user.name, email=user.email, password=user.password)
    print(f"New user to add: {new_user}")  # Imprime los datos del usuario antes de agregarlo

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"User successfully created: {new_user}")  # Imprime el usuario después de haber sido guardado
    return new_user

    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserModel(name=user.name, email=user.email, password =user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

from ..auth import create_access_token

@router.post("/token")
def login_for_access_token(user_credentials: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para autenticar al usuario y generar un token JWT.
    """
    print(f"Received login data: {user_credentials}")
    
    # Buscar usuario en la base de datos
    user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    if not user:
        print(f"No user found with email: {user_credentials.email}")
    else:
        print(f"User found: {user.email}, checking password...")

    # Verificar contraseña
    if not user or user.password != user_credentials.password:
        print(f"Invalid credentials for email: {user_credentials.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    print(f"Login successful for user: {user.email}")

    # Generar token JWT
    access_token = create_access_token(data={"sub": str(user.id)})
    print(f"Generated access token for user ID: {user.id}")
    
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
