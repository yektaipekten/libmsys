from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base, get_db
from .main import app
from .models import Book


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:ipekten@localhost/test_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Test Author",
            "ISBN": "1234567890",
            "publication_year": 2021,
            "is_available": True,
            "library_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["ISBN"] == "1234567890"


def test_read_book():
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Test Author",
            "ISBN": "1234567890",
            "publication_year": 2021,
            "is_available": True,
            "library_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    book_id = data["book_id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["ISBN"] == "1234567890"
