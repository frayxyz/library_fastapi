from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db

# Configuración JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    """
    Genera un token JWT con los datos proporcionados.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Configure logging
import logging
logger = logging.getLogger(__name__)

def verify_token(token: str):
    """
    Verifica la validez de un token JWT.
    """
    try:
        # Log: Intentando decodificar el token
        logger.warning("Iniciando verificación del token JWT.")
        
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.warning("Token decodificado exitosamente.")

        # Extraer el ID del usuario del payload
        user_id: int = payload.get("sub")
        if user_id is None:
            logger.warning("El token no contiene el campo 'sub' (user_id).")
            raise HTTPException(status_code=401, detail="Invalid token")

        # Log: Token válido y user_id extraído
        logger.warning(f"Token verificado correctamente. User ID: {user_id}")
        return user_id

    except JWTError as e:
        # Log: Error al decodificar el token
        logger.warning(f"Error al decodificar el token JWT: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtiene el usuario actual a partir del token JWT.
    """
  
    try:
        # Log the incoming token for debugging purposes
        logger.warning("Verifying token...")
        logger.warning(f"Received token: {token}")

        # Verify the token and extract the user ID
        user_id = verify_token(token)
        logger.warning(f"Token verified successfully. Extracted user_id: {user_id}")

        # Query the database for the user
        logger.warning("Querying database for user...")
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.error(f"User with id {user_id} not found in the database.")
            raise HTTPException(status_code=401, detail="User not found")

        logger.warning(f"User found: {user}")
        return user

    except Exception as e:
        # Log any exceptions that occur during the process
        logger.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token or user not found")