from app.models import Author as AuthorModel
from app.schemas import AuthorCreate
from datetime import datetime

def test_create_author(client,db):
    # Arrange
    author_data : AuthorCreate= {
        "name": "J.K. Rowling",
        "birth_date": "17/02/1970"
    }
    
    # Act
    response = client.post("/authors/", json=author_data)

    # Assert
    assert response.status_code == 201
    created_author = response.json()
    
    # Validate the response structure
    assert created_author["name"] == "J.K. Rowling"
    assert created_author["birth_date"] == "1970-02-17T00:00:00"
    assert "id" in created_author

    # Verify the author is saved in the database
    db_author = db.query(AuthorModel).filter(AuthorModel.name == "J.K. Rowling").first()
    assert db_author is not None
    assert db_author.name == "J.K. Rowling"
    assert db_author.birth_date == datetime(1970, 2, 17)


def test_list_authors_empty(client, db):
    # Act
    response = client.get("/authors/")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "No authors found"

def test_list_authors_with_data(client, db):
    # Arrange: Agregar un autor de prueba
    author = AuthorModel(name="Gabriel García Márquez", birth_date=datetime(year=1927, month=3, day= 6))
    db.add(author)
    db.commit()

    # Act
    response = client.get("/authors/")

    # Assert
    assert response.status_code == 200
    authors = response.json()
    assert len(authors) == 1  # Verificar que se devuelve un autor
    assert authors[0]["name"] == "Gabriel García Márquez"
    assert authors[0]["birth_date"] == "1927-03-06T00:00:00"


def test_get_author(client, db):
    # Arrange: Agregar un autor de prueba
    author = AuthorModel(name="Isabel Allende", birth_date=datetime(year=1942, month=8, day=2))
    db.add(author)
    db.commit()

    # Act
    response = client.get(f"/authors/{author.id}")

    # Assert
    assert response.status_code == 200
    author_data = response.json()
    assert author_data["name"] == "Isabel Allende"
    assert author_data["birth_date"] == "1942-08-02T00:00:00"

def test_get_author_not_found(client,db):
    # Act
    response = client.get("/authors/999")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Author with ID 999 not found"

def test_update_author(client, db):
    # Arrange: Crear un autor de prueba
    author = AuthorModel(name="Mario Vargas Llosa", birth_date=datetime(year=1936, month=3, day=28))
    db.add(author)
    db.commit()

    updated_data = {
        "name": "M. Vargas Llosa",
        "birth_date": "28/03/1936"
    }

    # Act
    response = client.put(f"/authors/{author.id}", json=updated_data)

    # Assert
    assert response.status_code == 200
    updated_author = response.json()
    assert updated_author["name"] == "M. Vargas Llosa"
    assert updated_author["birth_date"] == "1936-03-28T00:00:00"

    # Verificar en la base de datos
    db.refresh(author)
    assert author.name == "M. Vargas Llosa"

def test_update_author_with_invalid_date_format_fails(client, db):
    # Arrange: Crear un autor de prueba
    author = AuthorModel(name="Mario Vargas Llosa", birth_date=datetime(year=1936, month=3, day=28))
    db.add(author)
    db.commit()

    updated_data = {
        "name": "M. Vargas Llosa",
        "birth_date": "1936-03-28"
    }

    # Act
    response = client.put(f"/authors/{author.id}", json=updated_data)

    # Assert
    assert response.status_code != 200
    assert response.status_code == 422
    assert "Invalid date format" in response.text

    # Verificar en la base de datos
    db.refresh(author)
    assert author.name != "M. Vargas Llosa"

def test_update_author_not_found(client, db):
    updated_data = {
        "name": "Author Not Found",
        "birth_date": "01/01/2000"
    }

    # Act
    response = client.put("/authors/999", json=updated_data)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Author with ID 999 not found"

def test_delete_author(client, db):
    # Arrange: Crear un autor de prueba
    author = AuthorModel(name="Julio Cortázar", birth_date=datetime(year=1914, month=8, day=26))
    db.add(author)
    db.commit()

    # Act
    response = client.delete(f"/authors/{author.id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["detail"] == f"Author with ID {author.id} deleted successfully"

    # Verificar que el autor se haya eliminado de la base de datos
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author.id).first()
    assert db_author is None

def test_delete_author_not_found(client, db):
    # Act
    response = client.delete("/authors/999")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Author with ID 999 not found"
