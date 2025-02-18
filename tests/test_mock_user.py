import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.main import app
from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from app.database import engine, Base

# Mockear la sesión de la base de datos
@pytest.fixture
def mock_db_session():
    # Crear un motor mockeado para la base de datos
    mock_engine = MagicMock()
    
    # Crear una sesión mockeada
    mock_session = MagicMock()
    
    # Configurar la sesión mockeada para que funcione con SQLAlchemy
    sessionmaker_factory = sessionmaker(bind=mock_engine)
    mock_session_instance = sessionmaker_factory()
    
    # Simular el comportamiento de commit y añadir objetos a la sesión
    mock_session_instance.add = MagicMock()
    mock_session_instance.commit = MagicMock()
    mock_session_instance.rollback = MagicMock()
    
    # Devolver la sesión mockeada
    return mock_session_instance

# Prueba usando la sesión mockeada
def test_create_user_with_mock(mock_db_session):
    # Crear la base de datos de prueba (aunque en este caso no será usada real)
    Base.metadata.create_all(bind=engine)  # Aunque el engine está mockeado
    
    # Crear un usuario de prueba
    user = User(name='Test User', email='test@example.com')
    
    # Añadir y guardar el usuario con la sesión mockeada
    mock_db_session.add(user)
    mock_db_session.commit()
    
    # Verificar que add y commit fueron llamados
    mock_db_session.add.assert_called_once_with(user)
    mock_db_session.commit.assert_called_once()
