from app.models import Author as AuthorModel
from app.schemas import AuthorCreate
from datetime import datetime

def test_create_author(client,db):
    # Arrange
    author_data : AuthorCreate= {
        "name": "J.K. Rowling",
        "birth_date": "17/02/1970"  # Example birth date in DD/MM/YYYY format
    }
    
    # Act
    response = client.post("/authors/", json=author_data)

    # Assert
    assert response.status_code == 200  # Ensure the request was successful
    created_author = response.json()
    
    # Validate the response structure
    assert created_author["name"] == "J.K. Rowling"
    assert created_author["birth_date"] == "1970-02-17T00:00:00"  # Expected ISO 8601 format
    assert "id" in created_author  # Ensure the ID is generated

    # Verify the author is saved in the database
    db_author = db.query(AuthorModel).filter(AuthorModel.name == "J.K. Rowling").first()
    assert db_author is not None
    assert db_author.name == "J.K. Rowling"
    assert db_author.birth_date == datetime(1970, 2, 17)  # Match the parsed date


def test_list_authors_empty(client, db):
    # Act
    response = client.get("/authors/")

    # Assert
    assert response.status_code == 404  # Debe devolver 404 si no hay autores
    assert response.json()["detail"] == "No authors found"

def test_list_authors_with_data(client, db):
    # Arrange: Agregar un autor de prueba
    author = AuthorModel(name="Gabriel García Márquez", birth_date=datetime(year=1927, month=3, day= 6))
    db.add(author)
    db.commit()

    # Act
    response = client.get("/authors/")

    # Assert
    assert response.status_code == 200  # La solicitud debe ser exitosa
    authors = response.json()
    assert len(authors) == 1  # Verificar que se devuelve un autor
    assert authors[0]["name"] == "Gabriel García Márquez"
    assert authors[0]["birth_date"] == "1927-03-06T00:00:00"