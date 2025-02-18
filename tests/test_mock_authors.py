from unittest.mock import Mock
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db 

client = TestClient(app)

def test_list_authors():
    # Mock de la sesión de la base de datos
    mock_db_session = Mock()
    mock_db_session.query.return_value.all.return_value = [
        {"id": 1, "name": "J.K. Rowling", "birth_date": "1970-02-17T00:00:00"},
        {"id": 2, "name": "George R.R. Martin", "birth_date": "1948-09-20T00:00:00"},
    ]

    # Sobrescribir la dependencia `get_db` para usar el mock
    app.dependency_overrides[get_db] = lambda: mock_db_session

    # Ejecutar la solicitud GET
    response = client.get("/authors/")

    assert response.status_code == 200
    assert response.status_code != 400

    authors = response.json()
    assert isinstance(authors, list)
    assert len(authors) == 2
    assert authors[0]["id"] == 1
    assert authors[0]["name"] == "J.K. Rowling"
    assert authors[0]["birth_date"] == "1970-02-17T00:00:00"
    assert authors[1]["id"] == 2
    assert authors[1]["name"] == "George R.R. Martin"
    assert authors[1]["birth_date"] == "1948-09-20T00:00:00"
