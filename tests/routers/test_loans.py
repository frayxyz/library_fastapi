from datetime import datetime
from dotenv import load_dotenv
import pytest
from app.models import Book as BookModel, User as UserModel, Author as AuthorModel

load_dotenv()
# Prueba para prestar un libro exitosamente
def test_borrow_book_success(client, db):
    # Crear un usuario y un libro de prueba
    user = UserModel(id=1, name="User 1", email= "user@gmail.com", password="12345")
    author= AuthorModel(id=1, name="Author 1", birth_date=datetime(year=1920, month=6, day=13))
    book = BookModel(id=1, title="Test Book", author_id=1, publication_year = datetime(year=1949, month=6, day=13),  borrowed_by_id=None)
    db.add(user)
    db.add(author)
    db.add(book)
    db.commit()
    db.refresh(book) 

    # Verificar que el libro se guardó correctamente
    saved_book = db.query(BookModel).filter(BookModel.id == 1).first()
    assert saved_book is not None

    sample_user_data={
        "name": "User 1",
        "email": "user@gmail.com",
        "password": "12345"
    }
    #generate token
    responseToken = client.post("/users/token", json=sample_user_data)

    assert responseToken.status_code == 200  
    response_data = responseToken.json()
    print("----------responsa data token es -> ",response_data['access_token'])
    
    # Simular autenticación de usuario
    headers = {"Authorization": "Bearer "+response_data['access_token']}

    # Llamar a la API de préstamo
    response = client.post("/loans/borrow/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Book borrowed successfully"}
    
    # Verificar que el libro fue marcado como prestado
    borrowed_book = db.query(BookModel).filter(BookModel.id == 1).first()
    db.refresh(borrowed_book)
    assert borrowed_book.borrowed_by_id == 1

def test_return_book_success(client, db):
    # Crear un usuario, autor y un libro prestado
    user = UserModel(id=2, name="User 2", email="user2@gmail.com", password="12345")
    author = AuthorModel(id=2, name="Author 2", birth_date=datetime(year=1980, month=1, day=1))
    book = BookModel(id=2, title="Borrowed Book", author_id=2, publication_year=datetime(year=2000, month=1, day=1), borrowed_by_id=2)
    db.add(user)
    db.add(author)
    db.add(book)
    db.commit()
    db.refresh(book)

    # Generar token para el usuario
    sample_user_data = {
        "name": "User 2",
        "email": "user2@gmail.com",
        "password": "12345"
    }
    responseToken = client.post("/users/token", json=sample_user_data)
    assert responseToken.status_code == 200
    response_data = responseToken.json()
    headers = {"Authorization": f"Bearer {response_data['access_token']}"}

    # Llamar a la API de devolución
    response = client.post("/loans/return/2", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Book returned successfully"}

    # Verificar que el libro fue marcado como no prestado
    returned_book = db.query(BookModel).filter(BookModel.id == 2).first()
    db.refresh(returned_book)
    assert returned_book.borrowed_by_id is None

def test_borrow_book_not_found(client, db):
    # Crear un usuario para generar un token válido
    user = UserModel(id=6, name="User 6", email="user6@gmail.com", password="12345")
    db.add(user)
    db.commit()

    # Generar token para el usuario
    sample_user_data = {
        "name": "User 6",
        "email": "user6@gmail.com",
        "password": "12345"
    }
    responseToken = client.post("/users/token", json=sample_user_data)
    assert responseToken.status_code == 200
    response_data = responseToken.json()
    headers = {"Authorization": f"Bearer {response_data['access_token']}"}

    # Intentar prestar un libro inexistente
    response = client.post("/loans/borrow/999", headers=headers)
    assert response.status_code == 404
    assert response.status_code != 200
    assert response.json() == {"detail": "Book not found"}

def test_return_book_not_found(client, db):
    # Crear un usuario para generar un token válido
    user = UserModel(id=7, name="User 7", email="user7@gmail.com", password="12345")
    db.add(user)
    db.commit()

    # Generar token para el usuario
    sample_user_data = {
        "name": "User 7",
        "email": "user7@gmail.com",
        "password": "12345"
    }
    responseToken = client.post("/users/token", json=sample_user_data)
    assert responseToken.status_code == 200
    response_data = responseToken.json()
    headers = {"Authorization": f"Bearer {response_data['access_token']}"}

    # Intentar devolver un libro inexistente
    response = client.post("/loans/return/999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}    

def test_borrow_book_already_borrowed(client, db):
    # Crear un usuario, autor y un libro ya prestado
    user = UserModel(id=8, name="User 8", email="user8@gmail.com", password="12345")
    author = AuthorModel(id=3, name="Author 3", birth_date=datetime(year=1990, month=1, day=1))
    book = BookModel(id=3, title="Already Borrowed Book", author_id=3, publication_year=datetime(year=2010, month=1, day=1), borrowed_by_id=8)
    db.add(user)
    db.add(author)
    db.add(book)
    db.commit()

    # Generar token para el usuario
    sample_user_data = {
        "name": "User 8",
        "email": "user8@gmail.com",
        "password": "12345"
    }
    responseToken = client.post("/users/token", json=sample_user_data)
    assert responseToken.status_code == 200
    response_data = responseToken.json()
    headers = {"Authorization": f"Bearer {response_data['access_token']}"}

    # Intentar prestar un libro ya prestado
    response = client.post("/loans/borrow/3", headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Book is already borrowed"}

def test_return_book_not_borrowed_by_user(client, db):
    # Crear dos usuarios, un autor y un libro prestado por el primer usuario
    user1 = UserModel(id=9, name="User 9", email="user9@gmail.com", password="12345")
    user2 = UserModel(id=10, name="User 10", email="user10@gmail.com", password="12345")
    author = AuthorModel(id=4, name="Author 4", birth_date=datetime(year=1970, month=1, day=1))
    book = BookModel(id=4, title="Borrowed by another user", author_id=4, publication_year=datetime(year=1995, month=1, day=1), borrowed_by_id=9)
    db.add(user1)
    db.add(user2)
    db.add(author)
    db.add(book)
    db.commit()

    # Generar token para el segundo usuario
    sample_user_data = {
        "name": "User 10",
        "email": "user10@gmail.com",
        "password": "12345"
    }
    responseToken = client.post("/users/token", json=sample_user_data)
    assert responseToken.status_code == 200
    response_data = responseToken.json()
    headers = {"Authorization": f"Bearer {response_data['access_token']}"}

    # Intentar devolver un libro prestado por otro usuario
    response = client.post("/loans/return/4", headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Book not borrowed by you"}

def test_borrow_book_without_valid_token(client):
    # Arrange: Intentar prestar un libro sin proporcionar un token válido
    headers = {}  # Sin encabezado de autorización

    # Act: Hacer una solicitud para prestar un libro
    response = client.post("/loans/borrow/1", headers=headers)

    # Assert: Verificar que la respuesta sea 401 Unauthorized
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_return_book_without_valid_token(client):
    # Arrange: Intentar devolver un libro sin proporcionar un token válido
    headers = {}  # Sin encabezado de autorización

    # Act: Hacer una solicitud para devolver un libro
    response = client.post("/loans/return/1", headers=headers)

    # Assert: Verificar que la respuesta sea 401 Unauthorized
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}    