from datetime import datetime
from app.models import Book as BookModel, Author as AuthorModel

# Prueba para crear un libro exitosamente
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

# Prueba para crear un libro con un autor no existente
def test_create_book_author_not_found(client, db):
    book_data = {
        "title": "Book without Author",
        "author_id": 999,  # Autor no existente
        "publication_year": 2023
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}

# Prueba para buscar libros por título
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

# Prueba para buscar libros con filtros que no devuelven resultados
def test_search_books_not_found(client, db):
    response = client.get("/books/search?title=Nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Books not found"}

# Prueba para buscar libros por autor
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
