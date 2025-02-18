from datetime import datetime
import pytest
from app.schemas.user import UserCreate
from app.models import User as UserModel
from app.main import app  # Ajusta este import según tu estructura

@pytest.fixture
def sample_user_data() -> UserCreate:
    """Datos de usuario de ejemplo para pruebas"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }

def test_create_user(client, db, sample_user_data):
    """Prueba la creación de un nuevo usuario"""
    response = client.post("/users/", json=sample_user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == sample_user_data["name"]
    assert response_data["email"] == sample_user_data["email"]

def test_create_user_with_existing_email(client, db, sample_user_data):
    """Prueba crear un usuario con un correo electrónico ya registrado"""
    # Crear el primer usuario
    client.post("/users/", json=sample_user_data)

    # Intentar crear otro usuario con el mismo correo
    response = client.post("/users/", json=sample_user_data)
    assert response.status_code == 400  # Se espera un error de conflicto
    assert response.json()["detail"] == "Email already registered"

def test_login_with_valid_credentials(client, db, sample_user_data):
    """Prueba el inicio de sesión con credenciales válidas"""
    # Crear un usuario para probar el inicio de sesión

    user = UserModel(name=sample_user_data["name"], email=sample_user_data["email"], password=sample_user_data["password"] )
    db.add(user)
    db.commit()
    db.refresh(user) 

    # Intentar iniciar sesión con las mismas credenciales
    response = client.post("/users/token", json=sample_user_data)

    assert response.status_code == 200  # Se espera autenticación exitosa
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

def test_login_with_invalid_credentials(client, db, sample_user_data):
    """Prueba el inicio de sesión con credenciales incorrectas"""
    # Crear un usuario para probar el inicio de sesión
    client.post("/users/", json=sample_user_data)

    # Intentar iniciar sesión con una contraseña incorrecta
    response = client.post("/users/token", json={
         "name": sample_user_data["name"],
        "email": sample_user_data["email"],
        "password": "wrongpassword"
    })

    assert response.status_code == 401  # Se espera un error de autenticación
    assert response.json()["detail"] == "Invalid credentials"


def test_get_user_by_id(client, db, sample_user_data):
    """Prueba la obtención de un usuario por su ID."""
    create_response = client.post("/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == sample_user_data["email"]

@pytest.fixture
def updated_user_data() -> dict:
    """Datos actualizados para pruebas de actualización."""
    return {
        "name": "Updated User",
        "email": "updated@example.com",
        "password": "newpassword123"
    }

def test_update_user(client, db, sample_user_data, updated_user_data):
    """Prueba la actualización de un usuario."""
    create_response = client.post("/users/", json=sample_user_data)
    user_id = create_response.json()["id"]

    update_response = client.put(f"/users/{user_id}", json=updated_user_data)
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == updated_user_data["name"]
    assert updated_data["email"] == updated_user_data["email"]

def test_delete_user(client, db, sample_user_data):
    """Prueba la eliminación de un usuario."""
    create_response = client.post("/users/", json=sample_user_data)
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
