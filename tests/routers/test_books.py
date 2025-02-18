from datetime import datetime
from app.models import Book as BookModel, Author as AuthorModel

def test_create_book(client, db):
    # Añadir un autor de prueba
    author = AuthorModel(id=1, name="Author 1", birth_date= datetime(year= 1970, month=6, day= 15))
    db.add(author)
    db.commit()

    # Datos del libro a crear
    book_data = {
        "title": "New Book",
        "author_id": 1,
        "publication_year": 2023
    }

    # Llamada a la API
    response = client.post("/books/", json=book_data)

    # Verificar respuesta
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Book"
    assert data["author_id"] == 1
    assert data["publication_year"] == 2023

def test_create_book_author_not_found(client, db):
    book_data = {
        "title": "Book without Author",
        "author_id": 999,  # Autor no existente
        "publication_year": 2023
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}

def test_search_books_by_title(client, db):
    # Añadir un autor y un libro de prueba
    author = AuthorModel(id=2, name="Author 2")
    book = BookModel(title="Search Book", author_id=2, publication_year=2023)
    db.add(author)
    db.add(book)
    db.commit()

    # Buscar el libro por título parcial
    response = client.get("/books/search?title=Search")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 1
    assert books[0]["title"] == "Search Book"

def test_search_books_not_found(client, db):
    response = client.get("/books/search?title=Nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Books not found"}

def test_search_books_by_author(client, db):
    # Añadir un autor y un libro de prueba
    author = AuthorModel(id=3, name="Author 3")
    book = BookModel(title="Another Book", author_id=3, publication_year=2022)
    db.add(author)
    db.add(book)
    db.commit()

    # Buscar el libro por el nombre del autor
    response = client.get("/books/search?author=Author 3")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["author_id"] == 3


def test_get_book_by_id(client, db):
    # Añadir un autor y un libro de prueba
    author = AuthorModel(id=4, name="Author 4")
    book = BookModel(id=1, title="Book to Retrieve", author_id=4, publication_year=2021)
    db.add(author)
    db.add(book)
    db.commit()

    # Llamar a la API para obtener el libro por ID
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Book to Retrieve"
    assert data["author_id"] == 4

def test_get_book_not_found(client, db):
    # Intentar obtener un libro que no existe
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_update_book(client, db):
    # Añadir un autor y un libro de prueba
    author = AuthorModel(id=5, name="Author 5")
    book = BookModel(id=2, title="Book to Update", author_id=5, publication_year=2020)
    db.add(author)
    db.add(book)
    db.commit()

    # Datos para actualizar el libro
    updated_data = {
        "title": "Updated Book Title",
        "publication_year": 2022,
        "author_id": 5
    }

    # Llamar a la API para actualizar el libro
    response = client.put("/books/2", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Book Title"
    assert data["publication_year"] == 2022

def test_update_book_not_found(client, db):
    # Intentar actualizar un libro que no existe
    updated_data = {
        "title": "Nonexistent Book",
        "publication_year": 2023,
        "author_id": 20
    }
    response = client.put("/books/999", json=updated_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_delete_book(client, db):
    # Añadir un autor y un libro de prueba
    author = AuthorModel(id=6, name="Author 6")
    book = BookModel(id=3, title="Book to Delete", author_id=6, publication_year=2019)
    db.add(author)
    db.add(book)
    db.commit()

    # Llamar a la API para eliminar el libro
    response = client.delete("/books/3")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

    # Verificar que el libro ya no está en la base de datos
    response = client.get("/books/3")
    assert response.status_code == 404

def test_delete_book_not_found(client, db):
    # Intentar eliminar un libro que no existe
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
