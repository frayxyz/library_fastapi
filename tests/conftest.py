import os
from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app 
from app.database import Base, get_db  

load_dotenv()
# Debugging: Print the loaded variables to confirm
print("Loaded SECRET_KEY:", os.getenv("SECRET_KEY"))
print("Loaded ALGORITHM:", os.getenv("ALGORITHM"))
print("Loaded ACCESS_TOKEN_EXPIRE_MINUTES:", os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Crear la base de datos SQLite en memoria o archivo para pruebas
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db") 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture de base de datos
@pytest.fixture(scope="function")
def db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("Dropping tables...")
        Base.metadata.drop_all(bind=engine)

# Sobrescribir la dependencia de la base de datos para pruebas
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture de cliente de prueba
@pytest.fixture(scope="module")
def client():
    return TestClient(app)
